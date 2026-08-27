from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(String, primary_key=True, index=True) # e.g. "ban-na-san", "mueang-surat", "bangkok"
    name = Column(String, nullable=False) # e.g. "บ้านนาสาร"
    en_name = Column(String, nullable=True)
    province = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

class SubDistrict(Base):
    __tablename__ = "sub_districts"

    id = Column(String, primary_key=True, index=True) # e.g. "nasan", "phru-phi"
    name_th = Column(String, nullable=False)
    name_en = Column(String, nullable=True)
    postal_code = Column(String, default="84120")
    is_active = Column(Boolean, default=True)

    shops = relationship("Shop", back_populates="sub_district")
    orders = relationship("Order", back_populates="sub_district")
    node_locations = relationship("NodeLocation", back_populates="sub_district")

class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True, index=True) # e.g. "ban-na-san-node", "surat-thani-node"
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    locations = relationship("NodeLocation", back_populates="node", cascade="all, delete-orphan")
    manager_assignments = relationship("NodeManagerAssignment", back_populates="node", cascade="all, delete-orphan")

class NodeLocation(Base):
    __tablename__ = "node_locations"

    id = Column(String, primary_key=True, index=True) # e.g. "loc-nasan", "loc-phru-phi"
    node_id = Column(String, ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    sub_district_id = Column(String, ForeignKey("sub_districts.id"), nullable=True)
    name = Column(String, nullable=False)
    polygon_data = Column(JSON, nullable=True) # JSON list of {lat, lng}

    node = relationship("Node", back_populates="locations")
    sub_district = relationship("SubDistrict", back_populates="node_locations")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    line_user_id = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(String, default="customer") # primary role for legacy compatibility
    granted_roles = Column(JSON, default=list) # e.g. ["customer", "merchant", "rider"]
    active_role = Column(String, default="customer") # customer, merchant, rider, node_manager, admin
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    shops = relationship("Shop", back_populates="owner")
    merchant_bindings = relationship("MerchantUserBinding", back_populates="user", cascade="all, delete-orphan")
    node_assignments = relationship("NodeManagerAssignment", back_populates="user", cascade="all, delete-orphan")
    rider_profile = relationship("RiderProfile", back_populates="user", uselist=False)
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    orders = relationship("Order", foreign_keys="[Order.customer_id]", back_populates="customer")
    rewards = relationship("UserReward", back_populates="user")
    ride_bookings = relationship("RideBooking", foreign_keys="[RideBooking.customer_id]", back_populates="customer")

class MerchantUserBinding(Base):
    __tablename__ = "merchant_user_bindings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)
    merchant_role = Column(String, default="owner") # owner, manager, staff
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="merchant_bindings")
    shop = relationship("Shop", back_populates="staff_bindings")

class NodeManagerAssignment(Base):
    __tablename__ = "node_manager_assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    node_id = Column(String, ForeignKey("nodes.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="node_assignments")
    node = relationship("Node", back_populates="manager_assignments")

class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    tagline = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False, default="mart") # gi-otop, mart, food, fresh, retail
    sub_district_id = Column(String, ForeignKey("sub_districts.id"), nullable=False)
    province = Column(String, default="สุราษฎร์ธานี")
    origin_label = Column(String, default="บ้านนาสาร")
    courier_shipping = Column(Boolean, default=False)
    courier_from = Column(Float, default=50.0)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    status = Column(String, default="approved") # pending, approved, suspended
    gp_rate = Column(Float, default=15.0) # GP percentage
    rating = Column(Float, default=4.8)
    image_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="shops")
    sub_district = relationship("SubDistrict", back_populates="shops")
    products = relationship("Product", back_populates="shop")
    orders = relationship("Order", back_populates="shop")
    staff_bindings = relationship("MerchantUserBinding", back_populates="shop", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=True)
    unit = Column(String, default="ชิ้น")
    badge = Column(String, nullable=True) # GI, OTOP
    is_favorite = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)

    shop = relationship("Shop", back_populates="products")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True) # e.g. "ORD-2026-001"
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=True)
    rider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    sub_district_id = Column(String, ForeignKey("sub_districts.id"), nullable=False)

    total_amount = Column(Float, nullable=False)
    delivery_fee = Column(Float, default=25.0)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)

    status = Column(String, default="pending") # pending, accepted, preparing, delivering, completed, cancelled
    payment_method = Column(String, default="promptpay")
    payment_status = Column(String, default="pending") # pending, paid
    delivery_mode = Column(String, default="local") # local, nationwide
    delivery_address = Column(Text, nullable=False)
    eta = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="orders")
    shop = relationship("Shop", back_populates="orders")
    sub_district = relationship("SubDistrict", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    note = Column(String, nullable=True)

    order = relationship("Order", back_populates="items")

class RiderProfile(Base):
    __tablename__ = "rider_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    vehicle_type = Column(String, default="มอเตอร์ไซค์")
    vehicle = Column(String, nullable=True) # e.g. "มอเตอร์ไซค์ • ฮอนด้า เวฟ"
    plate_number = Column(String, nullable=False)
    is_online = Column(Boolean, default=False)
    kyc_status = Column(String, default="verified") # pending, verified, rejected
    inspection_status = Column(String, default="passed") # pending, passed, failed
    vehicle_details = Column(JSON, nullable=True)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    rating = Column(Float, default=4.9)
    trips = Column(Integer, default=0)

    user = relationship("User", back_populates="rider_profile")

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    wallet_type = Column(String, default="user_earning") # holding, operating, user_earning
    balance = Column(Float, default=0.0)
    pending_balance = Column(Float, default=0.0)
    account_number = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="wallet")
    transactions = relationship("WalletTransaction", back_populates="wallet")

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False) # earning, fee_deduction, withdrawal, topup, holding_transfer
    ref_id = Column(String, nullable=True)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="transactions")

class PointLog(Base):
    __tablename__ = "point_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points_change = Column(Integer, nullable=False) # positive for earn, negative for redeem
    type = Column(String, nullable=False) # earn, redeem
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(String, primary_key=True, index=True) # e.g. "d20", "ship", "d60", "d150"
    title = Column(String, nullable=False)
    detail = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    code = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

class UserReward(Base):
    __tablename__ = "user_rewards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_id = Column(String, ForeignKey("rewards.id"), nullable=False)
    code = Column(String, nullable=False)
    claimed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rewards")

class RideBooking(Base):
    __tablename__ = "ride_bookings"

    id = Column(String, primary_key=True, index=True) # e.g. "RIDE-2026-001"
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    service_type = Column(String, default="ride") # ride, parcel, shop, document
    mode = Column(String, default="passenger") # passenger, parcel
    vehicle_type = Column(String, default="motorcycle") # motorcycle, tuktuk, car, songthaew, truck
    origin_address = Column(String, nullable=False)
    origin_lat = Column(Float, nullable=True)
    origin_lng = Column(Float, nullable=True)
    destination_address = Column(String, nullable=False)
    destination_lat = Column(Float, nullable=True)
    destination_lng = Column(Float, nullable=True)
    distance_km = Column(Float, default=1.0)
    passenger_count = Column(Integer, default=1)
    is_fragile = Column(Boolean, default=False)
    parcel_type = Column(String, nullable=True)
    parcel_width_cm = Column(Float, nullable=True)
    parcel_length_cm = Column(Float, nullable=True)
    parcel_weight_kg = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    base_fare = Column(Float, default=20.0)
    surcharge_amount = Column(Float, default=0.0)
    estimated_fare = Column(Float, nullable=False)
    status = Column(String, default="requesting") # requesting, finding, matched, accepted, on_the_way, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", foreign_keys=[customer_id], back_populates="ride_bookings")
    rider = relationship("User", foreign_keys=[rider_id])


