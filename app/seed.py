from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
import app.models as models

def ensure_retail_shop(db: Session):
    owner_ounjai = db.query(models.User).filter(models.User.phone == "082-111-2222").first()
    if not owner_ounjai:
        owner_ounjai = models.User(name="พี่อุ่นใจ มินิมาร์ท", phone="082-111-2222", role="merchant")
        db.add(owner_ounjai)
        db.flush()
        db.add(models.Wallet(user_id=owner_ounjai.id, balance=3500.0))
        db.flush()

    shop_ounjai = db.query(models.Shop).filter(models.Shop.category == "retail").first()
    if not shop_ounjai:
        shop_ounjai = models.Shop(
            owner_id=owner_ounjai.id,
            name="ร้านอุ่นใจ มินิมาร์ท",
            tagline="ของใช้ประจำวัน ดื่ม-กิน ครบจบส่งไวถึงบ้าน",
            description="ร้านค้าอุ่นใจประจำชุมชน สินค้าอุปโภคบริโภค น้ำดื่ม ทิชชู่ ขนม ของใช้ในบ้านครบครัน",
            category="retail",
            sub_district_id="nasan",
            province="สุราษฎร์ธานี",
            origin_label="บ้านนาสาร",
            courier_shipping=False,
            status="approved",
            gp_rate=10.0,
            rating=4.9,
            lat=8.7905,
            lng=99.3555,
            phone="082-111-2222",
            is_open=True,
            image_url="/products/rice.png"
        )
        db.add(shop_ounjai)
        db.flush()

        products = [
            models.Product(shop_id=shop_ounjai.id, name="น้ำดื่มตราอุ่นใจ (แพ็ค 12 ขวด)", description="น้ำดื่มสะอาด 600ml แพ็ค 12 ขวด", price=55.0, unit="แพ็ค", category="เครื่องดื่ม", badge="ยอดนิยม", is_favorite=True, is_available=True, image_url="/products/rice.png"),
            models.Product(shop_id=shop_ounjai.id, name="ทิชชู่ม้วนเปียกหนาพิเศษ", description="กระดาษทิชชู่เช็ดสะอาด แพ็ค 4 ม้วน", price=45.0, unit="แพ็ค 4 ม้วน", category="ของใช้", badge="ขายดี", is_favorite=True, is_available=True, image_url="/products/vegetables.png"),
            models.Product(shop_id=shop_ounjai.id, name="เลย์ รสมันฝรั่งแท้", description="ขนมมันฝรั่งทอดกรอบ", price=30.0, unit="ซอง", category="ขนม", is_favorite=True, is_available=True, image_url="/products/otop-snack.png"),
            models.Product(shop_id=shop_ounjai.id, name="นมสดพาสเจอร์ไรส์ 830ml", description="นมสดพาสเจอร์ไรส์ รสจืด", price=48.0, unit="ขวด", category="เครื่องดื่ม", is_favorite=True, is_available=True, image_url="/products/eggs.png"),
            models.Product(shop_id=shop_ounjai.id, name="สบู่เหลวอาบน้ำถนอมผิว", description="สบู่เหลวถนอมผิว ขวด 400ml", price=89.0, unit="ขวด 400ml", category="ของใช้", is_available=True, image_url="/products/otop-snack.png"),
            models.Product(shop_id=shop_ounjai.id, name="บะหมี่ต้มยำกุ้ง (แพ็ค 5 ซอง)", description="บะหมี่กึ่งสำเร็จรูป รสต้มยำกุ้ง แพ็ค 5", price=35.0, unit="แพ็ค", category="อาหารแห้ง", badge="อุ่นใจ", is_available=True, image_url="/products/noodles.png"),
        ]
        db.add_all(products)
        db.commit()

def seed_database(db: Session):
    # Check if sub-districts already populated
    if db.query(models.SubDistrict).first():
        print("Database contains base data. Ensuring retail shop is seeded...")
        ensure_retail_shop(db)
        return

    print("Seeding complete mockup data matching screen design...")

    # 1. Cities
    cities = [
        models.City(id="ban-na-san", name="บ้านนาสาร", en_name="Ban Na San", province="สุราษฎร์ธานี", lat=8.7896, lng=99.3547),
        models.City(id="mueang-surat", name="เมืองสุราษฎร์ธานี", en_name="Mueang Surat Thani", province="สุราษฎร์ธานี", lat=9.1382, lng=99.3215),
        models.City(id="bangkok", name="กรุงเทพมหานคร", en_name="Bangkok", province="กรุงเทพมหานคร", lat=13.7563, lng=100.5018),
        models.City(id="chiang-mai", name="เชียงใหม่", en_name="Chiang Mai", province="เชียงใหม่", lat=18.7883, lng=98.9853),
        models.City(id="phuket", name="ภูเก็ต", en_name="Phuket", province="ภูเก็ต", lat=7.8804, lng=98.3923),
    ]
    db.add_all(cities)
    db.flush()

    # 2. SubDistricts
    sub_districts = [
        models.SubDistrict(id="nasan", name_th="นาสาร", name_en="Na San", postal_code="84120"),
        models.SubDistrict(id="phru-phi", name_th="พรุพี", name_en="Phru Phi", postal_code="84120"),
        models.SubDistrict(id="lamphun", name_th="ลำพูน", name_en="Lamphun", postal_code="84120"),
        models.SubDistrict(id="phoem-phun-sap", name_th="เพิ่มพูนทรัพย์", name_en="Phoem Phun Sap", postal_code="84120"),
        models.SubDistrict(id="khlong-prab", name_th="คลองปราบ", name_en="Khlong Prab", postal_code="84120"),
    ]
    db.add_all(sub_districts)
    db.flush()

    # 2.1 Multi-Location Nodes & Polygons
    node_nasan = models.Node(id="ban-na-san-node", name="ศูนย์บริหารจัดการโซนอำเภอบ้านนาสาร", code="NS-NODE-01", is_active=True)
    node_surat = models.Node(id="surat-thani-node", name="ศูนย์บริหารจัดการส่วนกลางสุราษฎร์ธานี", code="SR-NODE-01", is_active=True)
    db.add_all([node_nasan, node_surat])
    db.flush()

    loc_nasan = models.NodeLocation(
        id="loc-nasan",
        node_id="ban-na-san-node",
        sub_district_id="nasan",
        name="โซนเทศบาลเมืองนาสาร",
        polygon_data=[
            {"lat": 8.795, "lng": 99.350},
            {"lat": 8.795, "lng": 99.365},
            {"lat": 8.780, "lng": 99.365},
            {"lat": 8.780, "lng": 99.350}
        ]
    )
    loc_phru_phi = models.NodeLocation(
        id="loc-phru-phi",
        node_id="ban-na-san-node",
        sub_district_id="phru-phi",
        name="โซนพรุพี-เหมืองทวด",
        polygon_data=[
            {"lat": 8.770, "lng": 99.340},
            {"lat": 8.770, "lng": 99.360},
            {"lat": 8.750, "lng": 99.360},
            {"lat": 8.750, "lng": 99.340}
        ]
    )
    loc_lamphun = models.NodeLocation(
        id="loc-lamphun",
        node_id="ban-na-san-node",
        sub_district_id="lamphun",
        name="โซนลำพูนเกษตรกรรม",
        polygon_data=[
            {"lat": 8.810, "lng": 99.370},
            {"lat": 8.810, "lng": 99.390},
            {"lat": 8.790, "lng": 99.390},
            {"lat": 8.790, "lng": 99.370}
        ]
    )
    db.add_all([loc_nasan, loc_phru_phi, loc_lamphun])
    db.flush()

    # 3. Rewards Catalog
    rewards = [
        models.Reward(id="d20", title="ส่วนลด ฿20", detail="ใช้กับออเดอร์ถัดไป ไม่มีขั้นต่ำ", cost=100, code="PT20", image_url="/products/vegetables.png"),
        models.Reward(id="ship", title="ส่งฟรีในตำบล", detail="ยกเว้นค่าจัดส่งในเขตนาสาร 1 ครั้ง", cost=250, code="PTSHIP", image_url="/products/noodles.png"),
        models.Reward(id="d60", title="ส่วนลด ฿60", detail="เมื่อสั่งซื้อครบ 200 บาทขึ้นไป", cost=400, code="PT60", image_url="/products/otop-snack.png"),
        models.Reward(id="d150", title="ส่วนลด ฿150", detail="เมื่อสั่งซื้อครบ 500 บาทขึ้นไป", cost=600, code="PT150", image_url="/products/mangosteen.png"),
    ]
    db.add_all(rewards)
    db.flush()

    # 4. Users with Granted Roles (Customer, Merchant owners/staff, Riders, Node Manager, Admin)
    customer = models.User(name="คุณสมศรี ชุมชนนาสาร", phone="081-234-5678", role="customer", active_role="customer", granted_roles=["customer"])
    owner_panuan = models.User(name="ป้านวล สวนผักสด", phone="089-876-5432", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])
    owner_kaset = models.User(name="พี่ปรีชา เกษตรกรนาสาร", phone="086-555-4321", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])
    owner_cm = models.User(name="พ่อเลี้ยงล้านนา เชียงใหม่", phone="053-111-222", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])
    owner_pk = models.User(name="พี่บังอันดามัน ภูเก็ต", phone="076-333-444", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])
    owner_jaelee = models.User(name="เจ๊ลี่ ตลาดนาสาร", phone="081-999-8888", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])
    owner_kua = models.User(name="คุณแม่ ครัวคุณแม่", phone="088-777-6666", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])
    owner_ounjai = models.User(name="พี่อุ่นใจ มินิมาร์ท", phone="082-111-2222", role="merchant", active_role="merchant", granted_roles=["merchant", "customer"])

    rider_user = models.User(name="สมชาย เร็วทันใจ", phone="0812345678", role="rider", active_role="rider", granted_roles=["rider", "customer"])
    node_mgr_user = models.User(name="ผู้จัดการศูนย์บ้านนาสาร", phone="077-888-999", role="node_manager", active_role="node_manager", granted_roles=["node_manager", "customer"])
    admin_user = models.User(name="ผู้ดูแลระบบบ้านนาสาร", phone="077-341-111", role="admin", active_role="admin", granted_roles=["admin", "node_manager", "merchant", "rider", "customer"])

    db.add_all([customer, owner_panuan, owner_kaset, owner_cm, owner_pk, owner_jaelee, owner_kua, owner_ounjai, rider_user, node_mgr_user, admin_user])
    db.flush()

    # Node Manager Assignment
    db.add(models.NodeManagerAssignment(user_id=node_mgr_user.id, node_id="ban-na-san-node"))
    db.flush()

    # Rider Profile
    rider_profile = models.RiderProfile(
        user_id=rider_user.id,
        vehicle_type="มอเตอร์ไซค์",
        vehicle="มอเตอร์ไซค์ • ฮอนด้า เวฟ",
        plate_number="กข 1234",
        is_online=True,
        kyc_status="verified",
        inspection_status="passed",
        current_lat=8.7890,
        current_lng=99.3550,
        rating=4.9,
        trips=1240
    )
    db.add(rider_profile)

    # Wallets
    db.add(models.Wallet(user_id=customer.id, balance=650.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=owner_panuan.id, balance=4250.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=owner_kaset.id, balance=3890.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=owner_cm.id, balance=5600.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=owner_pk.id, balance=4100.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=owner_jaelee.id, balance=2950.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=rider_user.id, balance=1280.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=node_mgr_user.id, balance=3200.0, wallet_type="user_earning"))
    db.add(models.Wallet(user_id=admin_user.id, balance=24500.0, wallet_type="operating"))
    db.flush()

    # 5. Shops matching UI (shops.ts)
    shop1 = models.Shop(
        owner_id=owner_panuan.id,
        name="สวนป้านวล",
        tagline="ผักสด เก็บเช้าทุกวัน",
        description="ผักสด ปลอดสารพิษ สดจากแปลงทุกเช้า บ้านนาสาร",
        category="fresh",
        sub_district_id="nasan",
        province="สุราษฎร์ธานี",
        origin_label="บ้านนาสาร",
        courier_shipping=False,
        status="approved",
        gp_rate=10.0,
        rating=4.9,
        lat=8.7915,
        lng=99.3562,
        phone="089-876-5432",
        is_open=True,
        image_url="/products/vegetables.png"
    )

    shop2 = models.Shop(
        owner_id=owner_kaset.id,
        name="กลุ่มเกษตรกรนาสาร",
        tagline="มังคุด GI และของฝากขึ้นชื่อ",
        description="มังคุด GI และของฝากนาสารเกรดพรีเมียม ส่งทั่วไทย",
        category="gi-otop",
        sub_district_id="nasan",
        province="สุราษฎร์ธานี",
        origin_label="บ้านนาสาร",
        courier_shipping=True,
        courier_from=50.0,
        status="approved",
        gp_rate=12.0,
        rating=5.0,
        lat=8.7802,
        lng=99.3488,
        phone="086-555-4321",
        is_open=True,
        image_url="/products/mangosteen.png"
    )

    shop3 = models.Shop(
        owner_id=owner_cm.id,
        name="ดอยคราฟต์ เชียงใหม่",
        tagline="กาแฟดอยและผ้าทอมือล้านนา",
        description="เมล็ดกาแฟดริปดอยช้าง GI และผ้าทอมือล้านนาพิถีพิถัน",
        category="gi-otop",
        sub_district_id="nasan",
        province="เชียงใหม่",
        origin_label="เชียงใหม่",
        courier_shipping=True,
        courier_from=60.0,
        status="approved",
        gp_rate=12.0,
        rating=4.9,
        lat=18.7883,
        lng=98.9853,
        phone="053-111-222",
        is_open=True,
        image_url="/products/cm-coffee.png"
    )

    shop4 = models.Shop(
        owner_id=owner_pk.id,
        name="อันดามัน OTOP ภูเก็ต",
        tagline="เม็ดมะม่วงหิมพานต์และผ้าบาติก",
        description="ของฝากขึ้นชื่อภูเก็ต เม็ดมะม่วงหิมพานต์เคลือบน้ำผึ้งและผ้าบาติก",
        category="gi-otop",
        sub_district_id="nasan",
        province="ภูเก็ต",
        origin_label="ภูเก็ต",
        courier_shipping=True,
        courier_from=60.0,
        status="approved",
        gp_rate=12.0,
        rating=4.8,
        lat=7.8804,
        lng=98.3923,
        phone="076-333-444",
        is_open=True,
        image_url="/products/pk-cashew.png"
    )

    shop5 = models.Shop(
        owner_id=owner_jaelee.id,
        name="ร้านเจ๊ลี่",
        tagline="อาหารใต้ ปรุงร้อนทุกจาน",
        description="ก๋วยเตี๋ยวและอาหารใต้รสเด็ด ตลาดนาสาร",
        category="food",
        sub_district_id="nasan",
        province="สุราษฎร์ธานี",
        origin_label="บ้านนาสาร",
        courier_shipping=False,
        status="approved",
        gp_rate=15.0,
        rating=4.8,
        lat=8.7889,
        lng=99.3601,
        phone="081-999-8888",
        is_open=True,
        image_url="/products/noodles.png"
    )

    shop_kua = models.Shop(
        owner_id=owner_kua.id,
        name="ครัวคุณแม่",
        tagline="ข้าวแกงใต้ รสจัดจ้าน",
        description="ข้าวแกงใต้แท้ ปรุงสดใหม่ทุกวัน",
        category="food",
        sub_district_id="nasan",
        province="สุราษฎร์ธานี",
        origin_label="บ้านนาสาร",
        courier_shipping=False,
        status="approved",
        gp_rate=15.0,
        rating=4.7,
        lat=8.7900,
        lng=99.3580,
        phone="088-777-6666",
        is_open=True,
        image_url="/products/noodles.png"
    )

    shop_ounjai = models.Shop(
        owner_id=owner_ounjai.id,
        name="ร้านอุ่นใจ มินิมาร์ท",
        tagline="ของใช้ประจำวัน ดื่ม-กิน ครบจบส่งไวถึงบ้าน",
        description="ร้านค้าอุ่นใจประจำชุมชน สินค้าอุปโภคบริโภค น้ำดื่ม ทิชชู่ ขนม ของใช้ในบ้านครบครัน",
        category="retail",
        sub_district_id="nasan",
        province="สุราษฎร์ธานี",
        origin_label="บ้านนาสาร",
        courier_shipping=False,
        status="approved",
        gp_rate=10.0,
        rating=4.9,
        lat=8.7905,
        lng=99.3555,
        phone="082-111-2222",
        is_open=True,
        image_url="/products/rice.png"
    )

    db.add_all([shop1, shop2, shop3, shop4, shop5, shop_kua, shop_ounjai])
    db.flush()

    # 6. Products matching UI (shops.ts)
    products = [
        # Shop 1: สวนป้านวล
        models.Product(shop_id=shop1.id, name="ผักสดรวมตะกร้า", description="ผักสดรวมตะกร้า ปลอดสารพิษ", price=60.0, original_price=75.0, unit="ตะกร้า", category="ของสด", is_favorite=True, is_available=True, image_url="/products/vegetables.png"),
        models.Product(shop_id=shop1.id, name="ไข่ไก่สดฟาร์ม", description="ไข่ไก่สด แผง 30 ฟอง", price=95.0, original_price=110.0, unit="แผง 30 ฟอง", category="ของสด", is_favorite=True, is_available=True, image_url="/products/eggs.png"),
        models.Product(shop_id=shop1.id, name="ข้าวหอมมะลิ", description="ข้าวหอมมะลิแท้ ถุง 5 กก.", price=180.0, unit="ถุง 5 กก.", category="ของใช้", is_favorite=True, is_available=True, image_url="/products/rice.png"),
        models.Product(shop_id=shop1.id, name="ผักบุ้งไทย", description="ผักบุ้งไทยสด", price=20.0, unit="กำ", category="ของสด", is_available=True, image_url="/products/vegetables.png"),
        models.Product(shop_id=shop1.id, name="ไข่ไก่ แผงเล็ก", description="ไข่ไก่ แผง 10 ฟอง", price=38.0, unit="แผง 10 ฟอง", category="ของสด", is_available=True, image_url="/products/eggs.png"),
        models.Product(shop_id=shop1.id, name="ข้าวสารถุงเล็ก", description="ข้าวสารถุงเล็ก 1 กก.", price=45.0, unit="ถุง 1 กก.", category="ของใช้", is_available=True, image_url="/products/rice.png"),

        # Shop 2: กลุ่มเกษตรกรนาสาร
        models.Product(shop_id=shop2.id, name="มังคุดนาสาร GI", description="มังคุด GI บ้านนาสาร", price=120.0, original_price=150.0, unit="กิโลกรัม", category="ผลไม้ GI", badge="GI", is_favorite=True, is_available=True, image_url="/products/mangosteen.png"),
        models.Product(shop_id=shop2.id, name="กล้วยฉาบ OTOP", description="กล้วยฉาบ OTOP 5 ดาว", price=45.0, unit="ถุง", category="ของฝาก", badge="OTOP", is_favorite=True, is_available=True, image_url="/products/otop-snack.png"),
        models.Product(shop_id=shop2.id, name="มังคุดกล่องของฝาก", description="มังคุดกล่อง 3 กก.", price=350.0, unit="กล่อง 3 กก.", category="ของฝาก", badge="GI", is_favorite=True, is_available=True, image_url="/products/mangosteen.png"),
        models.Product(shop_id=shop2.id, name="ขนมพื้นบ้านรวม", description="ขนมพื้นบ้านรวมถุง", price=60.0, unit="ถุง", category="ของฝาก", is_available=True, image_url="/products/otop-snack.png"),
        models.Product(shop_id=shop2.id, name="มังคุดครึ่งกิโล", description="มังคุด 0.5 กก.", price=65.0, unit="0.5 กก.", category="ผลไม้ GI", badge="GI", is_available=True, image_url="/products/mangosteen.png"),

        # Shop 3: ดอยคราฟต์ เชียงใหม่
        models.Product(shop_id=shop3.id, name="กาแฟดริปดอยช้าง GI", description="กาแฟดริปดอยช้าง GI 250g", price=220.0, unit="ถุง 250 ก.", category="กาแฟ", badge="GI", is_favorite=True, is_available=True, image_url="/products/cm-coffee.png"),
        models.Product(shop_id=shop3.id, name="ผ้าพันคอทอมือ", description="ผ้าพันคอทอมือล้านนา", price=350.0, unit="ผืน", category="หัตถกรรม", badge="OTOP", is_favorite=True, is_available=True, image_url="/products/cm-textile.png"),
        models.Product(shop_id=shop3.id, name="เมล็ดกาแฟคั่วอ่อน", description="เมล็ดกาแฟคั่วอ่อน 250g", price=260.0, unit="ถุง 250 ก.", category="กาแฟ", badge="GI", is_favorite=True, is_available=True, image_url="/products/cm-coffee.png"),
        models.Product(shop_id=shop3.id, name="กระเป๋าผ้าทอมือ", description="กระเป๋าผ้าทอมือ", price=180.0, unit="ใบ", category="หัตถกรรม", is_available=True, image_url="/products/cm-textile.png"),

        # Shop 4: อันดามัน OTOP ภูเก็ต
        models.Product(shop_id=shop4.id, name="เม็ดมะม่วงหิมพานต์อบ", description="เม็ดมะม่วงหิมพานต์อบ 500g", price=190.0, unit="ถุง 500 ก.", category="ของฝาก", badge="OTOP", is_favorite=True, is_available=True, image_url="/products/pk-cashew.png"),
        models.Product(shop_id=shop4.id, name="ผ้าบาติกลายอันดามัน", description="ผ้าบาติกลายอันดามัน", price=420.0, unit="ผืน", category="หัตถกรรม", badge="OTOP", is_favorite=True, is_available=True, image_url="/products/pk-batik.png"),
        models.Product(shop_id=shop4.id, name="มะม่วงหิมพานต์เคลือบน้ำผึ้ง", description="มะม่วงหิมพานต์เคลือบน้ำผึ้ง", price=210.0, unit="ถุง", category="ของฝาก", is_favorite=True, is_available=True, image_url="/products/pk-cashew.png"),
        models.Product(shop_id=shop4.id, name="เสื้อบาติกพื้นเมือง", description="เสื้อบาติกพื้นเมือง", price=550.0, unit="ตัว", category="เครื่องแต่งกาย", is_available=True, image_url="/products/pk-batik.png"),

        # Shop 5: ร้านเจ๊ลี่
        models.Product(shop_id=shop5.id, name="ก๋วยเตี๋ยวหมูใต้", description="ก๋วยเตี๋ยวหมูใต้รสเด็ด", price=50.0, unit="ชาม", category="อาหาร", is_favorite=True, is_available=True, image_url="/products/noodles.png"),
        models.Product(shop_id=shop5.id, name="ก๋วยเตี๋ยวแห้งพิเศษ", description="ก๋วยเตี๋ยวแห้งพิเศษ", price=55.0, unit="ชาม", category="อาหาร", is_favorite=True, is_available=True, image_url="/products/noodles.png"),
        models.Product(shop_id=shop5.id, name="ก๋วยเตี๋ยวชามใหญ่", description="ก๋วยเตี๋ยวชามใหญ่", price=65.0, unit="ชาม", category="อาหาร", is_favorite=True, is_available=True, image_url="/products/noodles.png"),
        models.Product(shop_id=shop5.id, name="ก๋วยเตี๋ยวน้ำธรรมดา", description="ก๋วยเตี๋ยวน้ำธรรมดา", price=45.0, unit="ชาม", category="อาหาร", is_available=True, image_url="/products/noodles.png"),

        # Shop Kitchen: ครัวคุณแม่
        models.Product(shop_id=shop_kua.id, name="ข้าวแกงใต้", description="ข้าวแกงใต้ราดข้าว", price=60.0, unit="จาน", category="อาหาร", is_available=True, image_url="/products/noodles.png"),
        models.Product(shop_id=shop_kua.id, name="น้ำสมุนไพร", description="น้ำเก๊กฮวย/กระเจี๊ยบ/อัญชัน", price=25.0, unit="ขวด", category="เครื่องดื่ม", is_available=True, image_url="/products/noodles.png"),

        # Shop 7: ร้านอุ่นใจ มินิมาร์ท
        models.Product(shop_id=shop_ounjai.id, name="น้ำดื่มตราอุ่นใจ (แพ็ค 12 ขวด)", description="น้ำดื่มสะอาด 600ml แพ็ค 12 ขวด", price=55.0, unit="แพ็ค", category="เครื่องดื่ม", badge="ยอดนิยม", is_favorite=True, is_available=True, image_url="/products/rice.png"),
        models.Product(shop_id=shop_ounjai.id, name="ทิชชู่ม้วนเปียกหนาพิเศษ", description="กระดาษทิชชู่เช็ดสะอาด แพ็ค 4 ม้วน", price=45.0, unit="แพ็ค 4 ม้วน", category="ของใช้", badge="ขายดี", is_favorite=True, is_available=True, image_url="/products/vegetables.png"),
        models.Product(shop_id=shop_ounjai.id, name="เลย์ รสมันฝรั่งแท้", description="ขนมมันฝรั่งทอดกรอบ", price=30.0, unit="ซอง", category="ขนม", is_favorite=True, is_available=True, image_url="/products/otop-snack.png"),
        models.Product(shop_id=shop_ounjai.id, name="นมสดพาสเจอร์ไรส์ 830ml", description="นมสดพาสเจอร์ไรส์ รสจืด", price=48.0, unit="ขวด", category="เครื่องดื่ม", is_favorite=True, is_available=True, image_url="/products/eggs.png"),
        models.Product(shop_id=shop_ounjai.id, name="สบู่เหลวอาบน้ำถนอมผิว", description="สบู่เหลวถนอมผิว ขวด 400ml", price=89.0, unit="ขวด 400ml", category="ของใช้", is_available=True, image_url="/products/otop-snack.png"),
        models.Product(shop_id=shop_ounjai.id, name="บะหมี่ต้มยำกุ้ง (แพ็ค 5 ซอง)", description="บะหมี่กึ่งสำเร็จรูป รสต้มยำกุ้ง แพ็ค 5", price=35.0, unit="แพ็ค", category="อาหารแห้ง", badge="อุ่นใจ", is_available=True, image_url="/products/noodles.png"),
    ]
    db.add_all(products)
    db.flush()

    # 7. Orders & Items matching UI (orders.ts)
    # Order 1: NS-1043
    o1 = models.Order(
        id="NS-1043",
        customer_id=customer.id,
        shop_id=shop_kua.id,
        sub_district_id="nasan",
        total_amount=145.0,
        delivery_fee=20.0,
        discount_amount=0.0,
        final_amount=165.0,
        status="pending",
        payment_method="promptpay",
        payment_status="pending",
        delivery_mode="local",
        delivery_address="123 ม.4 ต.นาสาร อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120",
        eta="ร้านกำลังยืนยันออเดอร์"
    )

    # Order 2: NS-1042
    o2 = models.Order(
        id="NS-1042",
        customer_id=customer.id,
        shop_id=shop5.id,
        rider_id=rider_user.id,
        sub_district_id="nasan",
        total_amount=100.0,
        delivery_fee=15.0,
        discount_amount=0.0,
        final_amount=115.0,
        status="delivering",
        payment_method="promptpay",
        payment_status="paid",
        delivery_mode="local",
        delivery_address="88/2 ถ.เหมืองทวด ต.นาสาร อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120",
        eta="ถึงใน 10 นาที"
    )

    # Order 3: NS-1039
    o3 = models.Order(
        id="NS-1039",
        customer_id=customer.id,
        shop_id=shop1.id,
        sub_district_id="nasan",
        total_amount=150.0,
        delivery_fee=20.0,
        discount_amount=0.0,
        final_amount=170.0,
        status="preparing",
        payment_method="promptpay",
        payment_status="paid",
        delivery_mode="local",
        delivery_address="45 ม.1 ต.ท่าชี อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120",
        eta="กำลังจัดของ"
    )

    # Order 4: NS-1021
    o4 = models.Order(
        id="NS-1021",
        customer_id=customer.id,
        shop_id=shop2.id,
        sub_district_id="nasan",
        total_amount=240.0,
        delivery_fee=0.0,
        discount_amount=0.0,
        final_amount=240.0,
        status="completed",
        payment_method="promptpay",
        payment_status="paid",
        delivery_mode="nationwide",
        delivery_address="123 ม.4 ต.นาสาร อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120"
    )

    db.add_all([o1, o2, o3, o4])
    db.flush()

    # Order Items
    db.add_all([
        models.OrderItem(order_id=o1.id, product_id=products[19].id, product_name="ข้าวแกงใต้", quantity=2, unit_price=60.0, subtotal=120.0),
        models.OrderItem(order_id=o1.id, product_id=products[20].id, product_name="น้ำสมุนไพร", quantity=1, unit_price=25.0, subtotal=25.0),
        models.OrderItem(order_id=o2.id, product_id=products[15].id, product_name="ก๋วยเตี๋ยวหมูใต้", quantity=2, unit_price=50.0, subtotal=100.0),
        models.OrderItem(order_id=o3.id, product_id=products[0].id, product_name="ผักสดรวมตะกร้า", quantity=1, unit_price=120.0, subtotal=120.0),
        models.OrderItem(order_id=o3.id, product_id=products[1].id, product_name="ไข่ไก่ (แผง)", quantity=1, unit_price=30.0, subtotal=30.0),
        models.OrderItem(order_id=o4.id, product_id=products[6].id, product_name="มังคุดนาสาร GI (กก.)", quantity=2, unit_price=120.0, subtotal=240.0),
    ])

    # Points Logs
    db.add_all([
        models.PointLog(user_id=customer.id, points_change=16, type="earn", note="ได้รับแต้มจากการสั่งซื้อ NS-1043"),
        models.PointLog(user_id=customer.id, points_change=11, type="earn", note="ได้รับแต้มจากการสั่งซื้อ NS-1042"),
        models.PointLog(user_id=customer.id, points_change=17, type="earn", note="ได้รับแต้มจากการสั่งซื้อ NS-1039"),
        models.PointLog(user_id=customer.id, points_change=24, type="earn", note="ได้รับแต้มจากการสั่งซื้อ NS-1021"),
    ])

    # Sample User Reward Claimed
    db.add(models.UserReward(user_id=customer.id, reward_id="d20", code="PT20"))

    # Sample Ride Bookings matching Customer Rider UI
    ride_matched = models.RideBooking(
        id="RIDE-20260816-0008",
        customer_id=customer.id,
        rider_id=rider_user.id,
        service_type="ride",
        mode="passenger",
        origin_address="บ้านเลขที่ 88 หมู่ 3 ต.นาสาร",
        origin_lat=8.7896,
        origin_lng=99.3547,
        destination_address="ที่ทำการ องค์การบริหารส่วนตำบลทุ่งเตา",
        destination_lat=8.7750,
        destination_lng=99.3120,
        vehicle_type="motorcycle",
        passenger_count=1,
        is_fragile=False,
        notes="รอที่หน้าบ้าน โทรก่อนถึง",
        base_fare=20.0,
        surcharge_amount=0.0,
        estimated_fare=27.0,
        distance_km=1.5,
        status="matched"
    )

    ride_completed = models.RideBooking(
        id="R-311",
        customer_id=customer.id,
        rider_id=rider_user.id,
        service_type="ride",
        mode="passenger",
        origin_address="ตลาดนาสาร (หน้าธนาคาร)",
        origin_lat=8.7900,
        origin_lng=99.3550,
        destination_address="โรงพยาบาลบ้านนาสาร",
        destination_lat=8.7950,
        destination_lng=99.3580,
        vehicle_type="motorcycle",
        passenger_count=1,
        is_fragile=False,
        notes="รอที่หน้าธนาคาร",
        base_fare=20.0,
        surcharge_amount=0.0,
        estimated_fare=38.0,
        distance_km=3.0,
        status="completed"
    )

    parcel_fragile = models.RideBooking(
        id="RIDE-20260816-0009",
        customer_id=customer.id,
        rider_id=rider_user.id,
        service_type="parcel",
        mode="parcel",
        origin_address="บ้านเลขที่ 88 หมู่ 3 ต.นาสาร",
        origin_lat=8.7896,
        origin_lng=99.3547,
        destination_address="ที่ทำการ องค์การบริหารส่วนตำบลทุ่งเตา",
        destination_lat=8.7750,
        destination_lng=99.3120,
        vehicle_type="motorcycle",
        passenger_count=0,
        is_fragile=False,
        parcel_type="กล่องพัสดุ",
        parcel_width_cm=20.0,
        parcel_length_cm=30.0,
        parcel_weight_kg=2.5,
        notes="ผู้ส่ง: คุณสมศรี ชุมชนนาสาร (081-234-5678) | ผู้รับ: คุณสมชาย สุขใจ (089-876-5432)",
        base_fare=20.0,
        surcharge_amount=0.0,
        estimated_fare=45.0,
        distance_km=4.5,
        status="delivering"
    )

    shop_errand = models.RideBooking(
        id="R-314",
        customer_id=customer.id,
        rider_id=rider_user.id,
        service_type="shop",
        mode="passenger",
        origin_address="ร้านอุ่นใจ มินิมาร์ท",
        origin_lat=8.7905,
        origin_lng=99.3555,
        destination_address="บ้านเลขที่ 88 หมู่ 3 ต.นาสาร",
        destination_lat=8.7896,
        destination_lng=99.3547,
        vehicle_type="motorcycle",
        passenger_count=0,
        is_fragile=False,
        notes="ฝากซื้อไข่ไก่ 1 แผง น้ำดื่ม 1 แพ็ค โทรก่อนถึง",
        base_fare=40.0,
        surcharge_amount=0.0,
        estimated_fare=51.0,
        distance_km=1.8,
        status="completed"
    )

    doc_requesting = models.RideBooking(
        id="R-315",
        customer_id=customer.id,
        rider_id=None,
        service_type="document",
        mode="parcel",
        origin_address="สำนักงานเทศบาลเมืองบ้านนาสาร",
        origin_lat=8.7920,
        origin_lng=99.3570,
        destination_address="ที่ทำการผู้ใหญ่บ้าน หมู่ 3 ต.นาสาร",
        destination_lat=8.7850,
        destination_lng=99.3450,
        vehicle_type="motorcycle",
        passenger_count=0,
        is_fragile=False,
        parcel_type="เอกสาร",
        parcel_width_cm=21.0,
        parcel_length_cm=30.0,
        parcel_weight_kg=0.5,
        notes="เอกสารสำคัญ กรุณาใส่ซองกันน้ำ",
        base_fare=25.0,
        surcharge_amount=0.0,
        estimated_fare=50.0,
        distance_km=4.1,
        status="requesting"
    )

    db.add_all([ride_matched, ride_completed, parcel_fragile, shop_errand, doc_requesting])

    db.commit()
    print("Database mockup seeding completed successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        seed_database(db)
    finally:
        db.close()


