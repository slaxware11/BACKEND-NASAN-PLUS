from typing import List, Optional
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from datetime import datetime

# Cities & SubDistricts
def get_cities(db: Session) -> List[models.City]:
    return db.query(models.City).all()

def get_sub_districts(db: Session) -> List[models.SubDistrict]:
    return db.query(models.SubDistrict).all()

# User & Role
def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users_by_role(db: Session, role: str) -> List[models.User]:
    return db.query(models.User).filter((models.User.role == role) | (models.User.active_role == role)).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    user_data = user.model_dump()
    granted = user_data.get("granted_roles") or [user.role or "customer"]
    if user.role and user.role not in granted:
        granted.append(user.role)
    
    user_data["granted_roles"] = list(set(granted))
    user_data["active_role"] = user.role or "customer"

    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create associated wallet
    wallet = models.Wallet(user_id=db_user.id, balance=100.0 if user.role == "customer" else 500.0)
    db.add(wallet)

    # If rider role, create rider profile
    if "rider" in db_user.granted_roles:
        rider_prof = models.RiderProfile(
            user_id=db_user.id,
            vehicle_type="มอเตอร์ไซค์",
            vehicle="มอเตอร์ไซค์ • ฮอนด้า เวฟ",
            plate_number="1กข-8412",
            is_online=True,
            kyc_status="verified",
            inspection_status="passed"
        )
        db.add(rider_prof)

    db.commit()
    db.refresh(db_user)
    return db_user

def switch_user_role(db: Session, user_id: int, target_role: str) -> schemas.UserSwitchRoleResponse:
    user = get_user_by_id(db, user_id)
    if not user:
        return schemas.UserSwitchRoleResponse(
            success=False,
            user_id=user_id,
            active_role="customer",
            granted_roles=[],
            toast_notification="ไม่พบผู้ใช้งานในระบบ"
        )

    granted = user.granted_roles or ["customer"]
    # Admin bypass or must be in granted roles
    if target_role not in granted and user.active_role != "admin" and "admin" not in granted:
        # Auto grant for pilot demo flexibility
        granted.append(target_role)
        user.granted_roles = list(set(granted))

    current_role = user.active_role
    auto_offline_triggered = False
    toast_notification = None

    # Strict Mode Rule (Auto-Offline for Riders)
    # If a rider is currently ONLINE and switches to customer, merchant, or node_manager
    if current_role == "rider" and target_role != "rider":
        rider_prof = db.query(models.RiderProfile).filter(models.RiderProfile.user_id == user_id).first()
        if rider_prof and rider_prof.is_online:
            rider_prof.is_online = False
            auto_offline_triggered = True
            toast_notification = "ระบบได้ทำการปิดรับงานชั่วคราว เพื่อให้คุณใช้งานในบทบาทอื่น"

    # Switching back to rider role notification prompt
    if target_role == "rider" and current_role != "rider":
        toast_notification = "คุณอยู่ในบทบาทไรเดอร์ อย่าลืมเปิดสถานะ ONLINE เมื่อพร้อมรับงาน"

    user.active_role = target_role
    user.role = target_role # keep legacy field updated
    db.commit()
    db.refresh(user)

    return schemas.UserSwitchRoleResponse(
        success=True,
        user_id=user.id,
        active_role=user.active_role,
        granted_roles=user.granted_roles or [user.active_role],
        auto_offline_triggered=auto_offline_triggered,
        toast_notification=toast_notification
    )

# Nodes & Multi-Location Node Architecture
def get_nodes(db: Session) -> List[models.Node]:
    return db.query(models.Node).all()

def get_node_by_id(db: Session, node_id: str) -> Optional[models.Node]:
    return db.query(models.Node).filter(models.Node.id == node_id).first()

def create_node(db: Session, node_in: schemas.NodeCreate) -> models.Node:
    db_node = models.Node(**node_in.model_dump())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node

def get_node_locations(db: Session, node_id: str) -> List[models.NodeLocation]:
    return db.query(models.NodeLocation).filter(models.NodeLocation.node_id == node_id).all()

def create_node_location(db: Session, loc_in: schemas.NodeLocationCreate) -> models.NodeLocation:
    db_loc = models.NodeLocation(**loc_in.model_dump())
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def get_node_manager_assignments(db: Session, user_id: int) -> List[models.NodeManagerAssignment]:
    return db.query(models.NodeManagerAssignment).filter(models.NodeManagerAssignment.user_id == user_id).all()

def get_node_manager_scoped_data(db: Session, user_id: int):
    # Retrieve assigned nodes for node_manager
    assignments = get_node_manager_assignments(db, user_id)
    node_ids = [a.node_id for a in assignments]

    if not node_ids:
        # Fallback for pilot demo: return primary Ban Na San Node
        node_ids = ["ban-na-san-node"]

    nodes = db.query(models.Node).filter(models.Node.id.in_(node_ids)).all()
    locations = db.query(models.NodeLocation).filter(models.NodeLocation.node_id.in_(node_ids)).all()
    sub_district_ids = [loc.sub_district_id for loc in locations if loc.sub_district_id]

    shops = db.query(models.Shop).filter(models.Shop.sub_district_id.in_(sub_district_ids)).all() if sub_district_ids else db.query(models.Shop).all()
    orders = db.query(models.Order).filter(models.Order.sub_district_id.in_(sub_district_ids)).all() if sub_district_ids else db.query(models.Order).all()

    return {
        "user_id": user_id,
        "assigned_nodes": nodes,
        "inherited_locations": locations,
        "total_shops": len(shops),
        "total_orders": len(orders),
        "shops": shops,
        "orders": orders
    }

# Merchant Staff Multi-User Bindings
def get_merchant_bindings(db: Session, shop_id: int) -> List[models.MerchantUserBinding]:
    return db.query(models.MerchantUserBinding).filter(models.MerchantUserBinding.shop_id == shop_id).all()

def create_merchant_binding(db: Session, binding_in: schemas.MerchantUserBindingCreate) -> models.MerchantUserBinding:
    db_binding = models.MerchantUserBinding(**binding_in.model_dump())
    db.add(db_binding)

    # Automatically grant merchant role to bound user
    user = get_user_by_id(db, binding_in.user_id)
    if user:
        granted = user.granted_roles or ["customer"]
        if "merchant" not in granted:
            granted.append("merchant")
            user.granted_roles = list(set(granted))

    db.commit()
    db.refresh(db_binding)
    return db_binding

# Wallets & Withdrawals
def process_wallet_withdrawal(db: Session, user_id: int, withdraw_in: schemas.WalletWithdrawRequest) -> models.Wallet:
    wallet = get_user_wallet(db, user_id)
    if not wallet:
        raise ValueError("ไม่พบข้อมูลกระเป๋าเงิน")
    
    if wallet.balance < withdraw_in.amount:
        raise ValueError("ยอดเงินคงเหลือในกระเป๋าไม่เพียงพอสำหรับการถอน")

    wallet.balance -= withdraw_in.amount
    wallet.bank_name = withdraw_in.bank_code
    wallet.account_number = withdraw_in.account_number

    tx = models.WalletTransaction(
        wallet_id=wallet.id,
        amount=-withdraw_in.amount,
        type="withdrawal",
        ref_id=f"PO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        note=f"ถอนเงินเข้าบัญชี {withdraw_in.bank_code} ({withdraw_in.account_number}) - ชื่อบัญชี {withdraw_in.account_name}"
    )
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet


# Shops
def get_shops(db: Session, category: Optional[str] = None, sub_district_id: Optional[str] = None) -> List[models.Shop]:
    query = db.query(models.Shop).filter(models.Shop.status == "approved")
    if category:
        query = query.filter(models.Shop.category == category)
    if sub_district_id:
        query = query.filter(models.Shop.sub_district_id == sub_district_id)
    return query.all()

SLUG_TO_ID = {
    "suan-panuan": 1,
    "kaset-nasan": 2,
    "doi-craft-cm": 3,
    "andaman-otop-pk": 4,
    "jae-lee": 5,
    "kua-khun-mae": 6,
    "ran-ounjai": 7,
}

def get_shop_by_id(db: Session, shop_id: str) -> Optional[models.Shop]:
    str_id = str(shop_id)
    if str_id.isdigit():
        return db.query(models.Shop).filter(models.Shop.id == int(str_id)).first()
    
    target_id = SLUG_TO_ID.get(str_id.lower())
    if target_id:
        return db.query(models.Shop).filter(models.Shop.id == target_id).first()
    
    return db.query(models.Shop).filter(models.Shop.name.ilike(f"%{str_id}%")).first()

# Products
def get_products_by_shop(db: Session, shop_id: int) -> List[models.Product]:
    return db.query(models.Product).filter(models.Product.shop_id == shop_id, models.Product.is_available == True).all()

# Orders
def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{db.query(models.Order).count() + 1:04d}"
    final_amount = (order_in.total_amount + order_in.delivery_fee) - order_in.discount_amount

    db_order = models.Order(
        id=order_id,
        customer_id=order_in.customer_id,
        shop_id=order_in.shop_id,
        sub_district_id=order_in.sub_district_id,
        total_amount=order_in.total_amount,
        delivery_fee=order_in.delivery_fee,
        discount_amount=order_in.discount_amount,
        final_amount=final_amount,
        payment_method=order_in.payment_method,
        payment_status=order_in.payment_status,
        delivery_mode=order_in.delivery_mode,
        delivery_address=order_in.delivery_address,
        notes=order_in.notes,
        status="pending",
    )
    db.add(db_order)
    db.flush()

    for item in order_in.items:
        subtotal = item.quantity * item.unit_price
        db_item = models.OrderItem(
            order_id=order_id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=subtotal,
            note=item.note
        )
        db.add(db_item)

    # Award customer points
    earned_points = int(final_amount / 10)
    if earned_points > 0:
        point_log = models.PointLog(
            user_id=order_in.customer_id,
            points_change=earned_points,
            type="earn",
            note=f"ได้รับแต้มจากการสั่งซื้อ {order_id}"
        )
        db.add(point_log)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, customer_id: Optional[int] = None, shop_id: Optional[int] = None, rider_id: Optional[int] = None) -> List[models.Order]:
    query = db.query(models.Order)
    if customer_id:
        query = query.filter(models.Order.customer_id == customer_id)
    if shop_id:
        query = query.filter(models.Order.shop_id == shop_id)
    if rider_id:
        query = query.filter(models.Order.rider_id == rider_id)
    return query.order_by(models.Order.created_at.desc()).all()

# Rewards & Loyalty
def get_rewards(db: Session) -> List[models.Reward]:
    return db.query(models.Reward).all()

def redeem_reward(db: Session, user_id: int, reward_id: str) -> Optional[models.UserReward]:
    reward = db.query(models.Reward).filter(models.Reward.id == reward_id).first()
    if not reward:
        return None

    # Record point deduction log
    point_log = models.PointLog(
        user_id=user_id,
        points_change=-reward.cost,
        type="redeem",
        note=f"แลกรางวัล {reward.title}"
    )
    db.add(point_log)

    user_reward = models.UserReward(
        user_id=user_id,
        reward_id=reward.id,
        code=reward.code
    )
    db.add(user_reward)
    db.commit()
    db.refresh(user_reward)
    return user_reward

# Ride Bookings
def create_ride_booking(db: Session, ride_in: schemas.RideBookingCreate) -> models.RideBooking:
    ride_id = f"RIDE-{datetime.now().strftime('%Y%m%d')}-{db.query(models.RideBooking).count() + 1:04d}"
    
    # Auto-assign available rider for instant matching
    rider = db.query(models.User).filter(models.User.role == "rider").first()
    assigned_rider_id = rider.id if rider else None
    status = "matched" if rider else "requesting"

    db_ride = models.RideBooking(
        id=ride_id,
        customer_id=ride_in.customer_id,
        rider_id=assigned_rider_id,
        service_type=ride_in.service_type,
        mode=ride_in.mode,
        vehicle_type=ride_in.vehicle_type,
        origin_address=ride_in.origin_address,
        origin_lat=ride_in.origin_lat,
        origin_lng=ride_in.origin_lng,
        destination_address=ride_in.destination_address,
        destination_lat=ride_in.destination_lat,
        destination_lng=ride_in.destination_lng,
        distance_km=ride_in.distance_km,
        passenger_count=ride_in.passenger_count,
        is_fragile=ride_in.is_fragile,
        parcel_type=ride_in.parcel_type,
        parcel_width_cm=ride_in.parcel_width_cm,
        parcel_length_cm=ride_in.parcel_length_cm,
        parcel_weight_kg=ride_in.parcel_weight_kg,
        notes=ride_in.notes,
        base_fare=ride_in.base_fare if ride_in.base_fare is not None else 20.0,
        surcharge_amount=ride_in.surcharge_amount if ride_in.surcharge_amount is not None else 0.0,
        estimated_fare=ride_in.estimated_fare,
        status=status
    )
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_ride_bookings(db: Session, customer_id: Optional[int] = None) -> List[models.RideBooking]:
    query = db.query(models.RideBooking)
    if customer_id:
        query = query.filter(models.RideBooking.customer_id == customer_id)
    return query.order_by(models.RideBooking.created_at.desc()).all()

# Wallets
def get_user_wallet(db: Session, user_id: int) -> Optional[models.Wallet]:
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()

# Unified Rider Jobs (Database queries for Rider Dashboard)
def get_all_rider_jobs(db: Session) -> List[dict]:
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    rides = db.query(models.RideBooking).order_by(models.RideBooking.created_at.desc()).all()
    
    result_jobs = []

    phase_order_map = {
        "pending": "available",
        "requesting": "available",
        "accepted": "pickup",
        "preparing": "pickup",
        "delivering": "delivering",
        "on_the_way": "delivering",
        "completed": "done",
        "cancelled": "done",
    }

    for o in orders:
        shop_name = o.shop.name if o.shop else "ร้านค้าชุมชนนาสาร"
        items = [{"id": str(it.id), "name": it.product_name, "qty": it.quantity} for it in (o.items or [])]
        phase = phase_order_map.get(o.status, "available")
        kind = "food" if (o.shop and o.shop.category == "food") else "delivery"

        job_id = o.id if o.id.startswith("#") else f"#{o.id}"
        result_jobs.append({
            "id": job_id,
            "kind": kind,
            "from": shop_name,
            "to": o.delivery_address or "บ้านนาสาร สุราษฎร์ธานี",
            "distance": "2.4 กม.",
            "pay": float(o.delivery_fee or 35.0),
            "fromCoord": {"lat": o.shop.lat if (o.shop and o.shop.lat) else 8.792, "lng": o.shop.lng if (o.shop and o.shop.lng) else 99.357},
            "customer": o.customer.name if o.customer else "สมศรี ใจดี",
            "phone": o.customer.phone if o.customer else "081-234-5678",
            "note": o.notes or "",
            "vehicle": "motorcycle",
            "cod": float(o.final_amount) if o.payment_method == "cod" else 0,
            "items": items,
            "phase": phase,
        })

    for r in rides:
        phase = phase_order_map.get(r.status, "available")
        kind = "ride" if r.service_type == "ride" else "delivery"
        job_id = r.id if r.id.startswith("#") else f"#{r.id}"
        result_jobs.append({
            "id": job_id,
            "kind": kind,
            "from": r.origin_address or "ตลาดนาสาร",
            "to": r.destination_address or "สถานีรถไฟบ้านนาสาร",
            "distance": f"{r.distance_km:.1f} กม.",
            "pay": float(r.estimated_fare or 45.0),
            "fromCoord": {"lat": r.origin_lat or 8.79, "lng": r.origin_lng or 99.355},
            "customer": r.customer.name if r.customer else "ผู้โดยสาร",
            "phone": r.customer.phone if r.customer else "086-111-2222",
            "note": r.notes or "",
            "vehicle": r.vehicle_type or "motorcycle",
            "passengers": r.passenger_count or 1,
            "fragile": r.is_fragile or False,
            "phase": phase,
        })

    return result_jobs

def update_rider_job_phase(db: Session, job_id: str, phase: str) -> dict:
    norm_id = job_id.replace("#", "").strip()

    status_order_map = {
        "available": "pending",
        "pickup": "accepted",
        "delivering": "delivering",
        "done": "completed",
    }
    status_ride_map = {
        "available": "requesting",
        "pickup": "accepted",
        "delivering": "on_the_way",
        "done": "completed",
    }

    order = db.query(models.Order).filter((models.Order.id == norm_id) | (models.Order.id == f"#{norm_id}")).first()
    if order:
        order.status = status_order_map.get(phase, phase)
        db.commit()
        return {"success": True, "id": job_id, "phase": phase, "status": order.status}

    ride = db.query(models.RideBooking).filter((models.RideBooking.id == norm_id) | (models.RideBooking.id == f"#{norm_id}")).first()
    if ride:
        ride.status = status_ride_map.get(phase, phase)
        db.commit()
        return {"success": True, "id": job_id, "phase": phase, "status": ride.status}

    return {"success": True, "id": job_id, "phase": phase}

def create_rider_job_in_db(db: Session, job_data: dict) -> dict:
    job_id = job_data.get("id") or f"#J-{datetime.now().strftime('%M%S')}"
    kind = job_data.get("kind", "delivery")

    if kind == "ride":
        customer = db.query(models.User).filter(models.User.role == "customer").first()
        customer_id = customer.id if customer else 1

        db_ride = models.RideBooking(
            id=job_id.replace("#", ""),
            customer_id=customer_id,
            service_type="ride",
            origin_address=job_data.get("from", "ตลาดนาสาร"),
            origin_lat=job_data.get("fromCoord", {}).get("lat", 8.79),
            origin_lng=job_data.get("fromCoord", {}).get("lng", 99.355),
            destination_address=job_data.get("to", "สถานีรถไฟบ้านนาสาร"),
            distance_km=2.5,
            passenger_count=job_data.get("passengers", 1),
            notes=job_data.get("note", ""),
            estimated_fare=job_data.get("pay", 45.0),
            status="requesting"
        )
        db.add(db_ride)
        db.commit()
        db.refresh(db_ride)
    else:
        customer = db.query(models.User).filter(models.User.role == "customer").first()
        customer_id = customer.id if customer else 1
        sub_district = db.query(models.SubDistrict).first()
        sub_district_id = sub_district.id if sub_district else "nasan"

        db_order = models.Order(
            id=job_id.replace("#", ""),
            customer_id=customer_id,
            sub_district_id=sub_district_id,
            total_amount=job_data.get("pay", 40.0),
            delivery_fee=job_data.get("pay", 40.0),
            final_amount=job_data.get("pay", 40.0),
            delivery_address=job_data.get("to", "นาสาร"),
            notes=job_data.get("note", ""),
            status="pending"
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

    job_data["id"] = job_id
    job_data["phase"] = "available"
    return job_data


