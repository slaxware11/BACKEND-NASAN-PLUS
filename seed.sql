-- =============================================================================
-- Nasan Plus+ Mockup Data Seeding (SQL Insert Script)
-- Perfectly matches all screens: Mart, ร้านอุ่นใจ, GI/OTOP, Food, Cart, Rewards, Rider
-- =============================================================================

-- 1. Cities
INSERT INTO cities (id, name, en_name, province, lat, lng) VALUES
('ban-na-san', 'บ้านนาสาร', 'Ban Na San', 'สุราษฎร์ธานี', 8.7896, 99.3547),
('mueang-surat', 'เมืองสุราษฎร์ธานี', 'Mueang Surat Thani', 'สุราษฎร์ธานี', 9.1382, 99.3215),
('bangkok', 'กรุงเทพมหานคร', 'Bangkok', 'กรุงเทพมหานคร', 13.7563, 100.5018),
('chiang-mai', 'เชียงใหม่', 'Chiang Mai', 'เชียงใหม่', 18.7883, 98.9853),
('phuket', 'ภูเก็ต', 'Phuket', 'ภูเก็ต', 7.8804, 98.3923)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, province = EXCLUDED.province;

-- 2. SubDistricts
INSERT INTO sub_districts (id, name_th, name_en, postal_code, is_active) VALUES
('nasan', 'นาสาร', 'Na San', '84120', TRUE),
('phru-phi', 'พรุพี', 'Phru Phi', '84120', TRUE),
('lamphun', 'ลำพูน', 'Lamphun', '84120', TRUE),
('phoem-phun-sap', 'เพิ่มพูนทรัพย์', 'Phoem Phun Sap', '84120', TRUE),
('khlong-prab', 'คลองปราบ', 'Khlong Prab', '84120', TRUE)
ON CONFLICT (id) DO UPDATE SET name_th = EXCLUDED.name_th;

-- 3. Users
INSERT INTO users (id, line_user_id, name, phone, role, avatar_url) VALUES
(1, 'U1001', 'คุณสมศรี ชุมชนนาสาร', '081-234-5678', 'customer', '/placeholder.svg'),
(2, 'U1002', 'ป้านวล สวนผักสด', '089-876-5432', 'merchant', '/placeholder.svg'),
(3, 'U1003', 'พี่ปรีชา เกษตรกรนาสาร', '086-555-4321', 'merchant', '/placeholder.svg'),
(4, 'U1004', 'พ่อเลี้ยงล้านนา เชียงใหม่', '053-111-222', 'merchant', '/placeholder.svg'),
(5, 'U1005', 'พี่บังอันดามัน ภูเก็ต', '076-333-444', 'merchant', '/placeholder.svg'),
(6, 'U1006', 'เจ๊ลี่ ตลาดนาสาร', '081-999-8888', 'merchant', '/placeholder.svg'),
(7, 'U1007', 'คุณแม่ ครัวคุณแม่', '088-777-6666', 'merchant', '/placeholder.svg'),
(8, 'U1008', 'พี่อุ่นใจ มินิมาร์ท', '082-111-2222', 'merchant', '/placeholder.svg'),
(9, 'U1009', 'สมชาย ใจกล้า', '0812345678', 'rider', '/placeholder.svg'),
(10, 'U1010', 'ผู้ดูแลระบบบ้านนาสาร', '077-341-111', 'admin', '/placeholder.svg'),
(11, 'U1011', 'วิชัย บริการดี', '089-111-2233', 'rider', '/placeholder.svg')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, phone = EXCLUDED.phone;

-- 4. Shops
INSERT INTO shops (id, owner_id, name, tagline, description, category, sub_district_id, province, origin_label, courier_shipping, courier_from, lat, lng, status, gp_rate, rating, image_url, phone, is_open) VALUES
(1, 2, 'สวนป้านวล', 'ผักสด เก็บเช้าทุกวัน', 'ผักสด ปลอดสารพิษ สดจากแปลงทุกเช้า บ้านนาสาร', 'fresh', 'nasan', 'สุราษฎร์ธานี', 'บ้านนาสาร', FALSE, 50.0, 8.7915, 99.3562, 'approved', 10.0, 4.9, '/products/vegetables.png', '089-876-5432', TRUE),
(2, 3, 'กลุ่มเกษตรกรนาสาร', 'มังคุด GI และของฝากขึ้นชื่อ', 'มังคุด GI และของฝากนาสารเกรดพรีเมียม ส่งทั่วไทย', 'gi-otop', 'nasan', 'สุราษฎร์ธานี', 'บ้านนาสาร', TRUE, 50.0, 8.7802, 99.3488, 'approved', 12.0, 5.0, '/products/mangosteen.png', '086-555-4321', TRUE),
(3, 4, 'ดอยคราฟต์ เชียงใหม่', 'กาแฟดอยและผ้าทอมือล้านนา', 'เมล็ดกาแฟดริปดอยช้าง GI และผ้าทอมือล้านนาพิถีพิถัน', 'gi-otop', 'nasan', 'เชียงใหม่', 'เชียงใหม่', TRUE, 60.0, 18.7883, 98.9853, 'approved', 12.0, 4.9, '/products/cm-coffee.png', '053-111-222', TRUE),
(4, 5, 'อันดามัน OTOP ภูเก็ต', 'เม็ดมะม่วงหิมพานต์และผ้าบาติก', 'ของฝากขึ้นชื่อภูเก็ต เม็ดมะม่วงหิมพานต์เคลือบน้ำผึ้งและผ้าบาติก', 'gi-otop', 'nasan', 'ภูเก็ต', 'ภูเก็ต', TRUE, 60.0, 7.8804, 98.3923, 'approved', 12.0, 4.8, '/products/pk-cashew.png', '076-333-444', TRUE),
(5, 6, 'ร้านเจ๊ลี่', 'อาหารใต้ ปรุงร้อนทุกจาน', 'ก๋วยเตี๋ยวและอาหารใต้รสเด็ด ตลาดนาสาร', 'food', 'nasan', 'สุราษฎร์ธานี', 'บ้านนาสาร', FALSE, 50.0, 8.7889, 99.3601, 'approved', 15.0, 4.8, '/products/noodles.png', '081-999-8888', TRUE),
(6, 7, 'ครัวคุณแม่', 'ข้าวแกงใต้ รสจัดจ้าน', 'ข้าวแกงใต้แท้ ปรุงสดใหม่ทุกวัน', 'food', 'nasan', 'สุราษฎร์ธานี', 'บ้านนาสาร', FALSE, 50.0, 8.7900, 99.3580, 'approved', 15.0, 4.7, '/products/noodles.png', '088-777-6666', TRUE),
(7, 8, 'ร้านอุ่นใจ มินิมาร์ท', 'ของใช้ประจำวัน ดื่ม-กิน ครบจบส่งไวถึงบ้าน', 'ร้านค้าอุ่นใจประจำชุมชน สินค้าอุปโภคบริโภค น้ำดื่ม ทิชชู่ ขนม ของใช้ในบ้านครบครัน', 'retail', 'nasan', 'สุราษฎร์ธานี', 'บ้านนาสาร', FALSE, 50.0, 8.7905, 99.3555, 'approved', 10.0, 4.9, '/products/rice.png', '082-111-2222', TRUE)
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, category = EXCLUDED.category;

-- 5. Products
INSERT INTO products (id, shop_id, name, description, category, price, original_price, unit, badge, is_favorite, is_available, image_url) VALUES
(1, 1, 'ผักสดรวมตะกร้า', 'ผักสดรวมตะกร้า ปลอดสารพิษ', 'ของสด', 60.0, 75.0, 'ตะกร้า', NULL, TRUE, TRUE, '/products/vegetables.png'),
(2, 1, 'ไข่ไก่สดฟาร์ม', 'ไข่ไก่สด แผง 30 ฟอง', 'ของสด', 95.0, 110.0, 'แผง 30 ฟอง', NULL, TRUE, TRUE, '/products/eggs.png'),
(3, 1, 'ข้าวหอมมะลิ', 'ข้าวหอมมะลิแท้ ถุง 5 กก.', 'ของใช้', 180.0, NULL, 'ถุง 5 กก.', NULL, TRUE, TRUE, '/products/rice.png'),
(4, 1, 'ผักบุ้งไทย', 'ผักบุ้งไทยสด', 'ของสด', 20.0, NULL, 'กำ', NULL, FALSE, TRUE, '/products/vegetables.png'),
(5, 1, 'ไข่ไก่ แผงเล็ก', 'ไข่ไก่ แผง 10 ฟอง', 'ของสด', 38.0, NULL, 'แผง 10 ฟอง', NULL, FALSE, TRUE, '/products/eggs.png'),
(6, 1, 'ข้าวสารถุงเล็ก', 'ข้าวสารถุงเล็ก 1 กก.', 'ของใช้', 45.0, NULL, 'ถุง 1 กก.', NULL, FALSE, TRUE, '/products/rice.png'),

(7, 2, 'มังคุดนาสาร GI', 'มังคุด GI บ้านนาสาร', 'ผลไม้ GI', 120.0, 150.0, 'กิโลกรัม', 'GI', TRUE, TRUE, '/products/mangosteen.png'),
(8, 2, 'กล้วยฉาบ OTOP', 'กล้วยฉาบ OTOP 5 ดาว', 'ของฝาก', 45.0, NULL, 'ถุง', 'OTOP', TRUE, TRUE, '/products/otop-snack.png'),
(9, 2, 'มังคุดกล่องของฝาก', 'มังคุดกล่อง 3 กก.', 'ของฝาก', 350.0, NULL, 'กล่อง 3 กก.', 'GI', TRUE, TRUE, '/products/mangosteen.png'),
(10, 2, 'ขนมพื้นบ้านรวม', 'ขนมพื้นบ้านรวมถุง', 'ของฝาก', 60.0, NULL, 'ถุง', NULL, FALSE, TRUE, '/products/otop-snack.png'),
(11, 2, 'มังคุดครึ่งกิโล', 'มังคุด 0.5 กก.', 'ผลไม้ GI', 65.0, NULL, '0.5 กก.', 'GI', FALSE, TRUE, '/products/mangosteen.png'),

(12, 3, 'กาแฟดริปดอยช้าง GI', 'กาแฟดริปดอยช้าง GI 250g', 'กาแฟ', 220.0, NULL, 'ถุง 250 ก.', 'GI', TRUE, TRUE, '/products/cm-coffee.png'),
(13, 3, 'ผ้าพันคอทอมือ', 'ผ้าพันคอทอมือล้านนา', 'หัตถกรรม', 350.0, NULL, 'ผืน', 'OTOP', TRUE, TRUE, '/products/cm-textile.png'),
(14, 3, 'เมล็ดกาแฟคั่วอ่อน', 'เมล็ดกาแฟคั่วอ่อน 250g', 'กาแฟ', 260.0, NULL, 'ถุง 250 ก.', 'GI', TRUE, TRUE, '/products/cm-coffee.png'),
(15, 3, 'กระเป๋าผ้าทอมือ', 'กระเป๋าผ้าทอมือ', 'หัตถกรรม', 180.0, NULL, 'ใบ', NULL, FALSE, TRUE, '/products/cm-textile.png'),

(16, 4, 'เม็ดมะม่วงหิมพานต์อบ', 'เม็ดมะม่วงหิมพานต์อบ 500g', 'ของฝาก', 190.0, NULL, 'ถุง 500 ก.', 'OTOP', TRUE, TRUE, '/products/pk-cashew.png'),
(17, 4, 'ผ้าบาติกลายอันดามัน', 'ผ้าบาติกลายอันดามัน', 'หัตถกรรม', 420.0, NULL, 'ผืน', 'OTOP', TRUE, TRUE, '/products/pk-batik.png'),
(18, 4, 'มะม่วงหิมพานต์เคลือบน้ำผึ้ง', 'มะม่วงหิมพานต์เคลือบน้ำผึ้ง', 'ของฝาก', 210.0, NULL, 'ถุง', NULL, TRUE, TRUE, '/products/pk-cashew.png'),
(19, 4, 'เสื้อบาติกพื้นเมือง', 'เสื้อบาติกพื้นเมือง', 'เครื่องแต่งกาย', 550.0, NULL, 'ตัว', NULL, FALSE, TRUE, '/products/pk-batik.png'),

(20, 5, 'ก๋วยเตี๋ยวหมูใต้', 'ก๋วยเตี๋ยวหมูใต้รสเด็ด', 'อาหาร', 50.0, NULL, 'ชาม', NULL, TRUE, TRUE, '/products/noodles.png'),
(21, 5, 'ก๋วยเตี๋ยวแห้งพิเศษ', 'ก๋วยเตี๋ยวแห้งพิเศษ', 'อาหาร', 55.0, NULL, 'ชาม', NULL, TRUE, TRUE, '/products/noodles.png'),
(22, 5, 'ก๋วยเตี๋ยวชามใหญ่', 'ก๋วยเตี๋ยวชามใหญ่', 'อาหาร', 65.0, NULL, 'ชาม', NULL, TRUE, TRUE, '/products/noodles.png'),
(23, 5, 'ก๋วยเตี๋ยวน้ำธรรมดา', 'ก๋วยเตี๋ยวน้ำธรรมดา', 'อาหาร', 45.0, NULL, 'ชาม', NULL, FALSE, TRUE, '/products/noodles.png'),

(24, 6, 'ข้าวแกงใต้', 'ข้าวแกงใต้ราดข้าว', 'อาหาร', 60.0, NULL, 'จาน', NULL, FALSE, TRUE, '/products/noodles.png'),
(25, 6, 'น้ำสมุนไพร', 'น้ำเก๊กฮวย/กระเจี๊ยบ/อัญชัน', 'เครื่องดื่ม', 25.0, NULL, 'ขวด', NULL, FALSE, TRUE, '/products/noodles.png'),

(26, 7, 'น้ำดื่มตราอุ่นใจ (แพ็ค 12 ขวด)', 'น้ำดื่มสะอาด 600ml แพ็ค 12 ขวด', 'เครื่องดื่ม', 55.0, NULL, 'แพ็ค', 'ยอดนิยม', TRUE, TRUE, '/products/rice.png'),
(27, 7, 'ทิชชู่ม้วนเปียกหนาพิเศษ', 'กระดาษทิชชู่เช็ดสะอาด แพ็ค 4 ม้วน', 'ของใช้', 45.0, NULL, 'แพ็ค 4 ม้วน', 'ขายดี', TRUE, TRUE, '/products/vegetables.png'),
(28, 7, 'เลย์ รสมันฝรั่งแท้', 'ขนมมันฝรั่งทอดกรอบ', 'ขนม', 30.0, NULL, 'ซอง', NULL, TRUE, TRUE, '/products/otop-snack.png'),
(29, 7, 'นมสดพาสเจอร์ไรส์ 830ml', 'นมสดพาสเจอร์ไรส์ รสจืด', 'เครื่องดื่ม', 48.0, NULL, 'ขวด', NULL, TRUE, TRUE, '/products/eggs.png'),
(30, 7, 'สบู่เหลวอาบน้ำถนอมผิว', 'สบู่เหลวถนอมผิว ขวด 400ml', 'ของใช้', 89.0, NULL, 'ขวด 400ml', NULL, FALSE, TRUE, '/products/otop-snack.png'),
(31, 7, 'บะหมี่ต้มยำกุ้ง (แพ็ค 5 ซอง)', 'บะหมี่กึ่งสำเร็จรูป รสต้มยำกุ้ง แพ็ค 5', 'อาหารแห้ง', 35.0, NULL, 'แพ็ค', 'อุ่นใจ', FALSE, TRUE, '/products/noodles.png')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, price = EXCLUDED.price;

-- 6. Orders
INSERT INTO orders (id, customer_id, shop_id, rider_id, sub_district_id, total_amount, delivery_fee, discount_amount, final_amount, status, payment_method, payment_status, delivery_mode, delivery_address, eta) VALUES
('NS-1043', 1, 6, NULL, 'nasan', 145.0, 20.0, 0.0, 165.0, 'pending', 'promptpay', 'pending', 'local', '123 ม.4 ต.นาสาร อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120', 'ร้านกำลังยืนยันออเดอร์'),
('NS-1042', 1, 5, 9, 'nasan', 100.0, 15.0, 0.0, 115.0, 'delivering', 'promptpay', 'paid', 'local', '88/2 ถ.เหมืองทวด ต.นาสาร อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120', 'ถึงใน 10 นาที'),
('NS-1039', 1, 1, NULL, 'nasan', 150.0, 20.0, 0.0, 170.0, 'preparing', 'promptpay', 'paid', 'local', '45 ม.1 ต.ท่าชี อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120', 'กำลังจัดของ'),
('NS-1021', 1, 2, NULL, 'nasan', 240.0, 0.0, 0.0, 240.0, 'completed', 'promptpay', 'paid', 'nationwide', '123 ม.4 ต.นาสาร อ.บ้านนาสาร จ.สุราษฎร์ธานี 84120', NULL)
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status;

-- 7. Order Items
INSERT INTO order_items (id, order_id, product_id, product_name, quantity, unit_price, subtotal) VALUES
(1, 'NS-1043', 24, 'ข้าวแกงใต้', 2, 60.0, 120.0),
(2, 'NS-1043', 25, 'น้ำสมุนไพร', 1, 25.0, 25.0),
(3, 'NS-1042', 20, 'ก๋วยเตี๋ยวหมูใต้', 2, 50.0, 100.0),
(4, 'NS-1039', 1, 'ผักสดรวมตะกร้า', 1, 120.0, 120.0),
(5, 'NS-1039', 5, 'ไข่ไก่ แผงเล็ก', 1, 30.0, 30.0),
(6, 'NS-1021', 7, 'มังคุดนาสาร GI', 2, 120.0, 240.0)
ON CONFLICT (id) DO UPDATE SET quantity = EXCLUDED.quantity;

-- 8. Rider Profiles
INSERT INTO rider_profiles (id, user_id, vehicle_type, vehicle, plate_number, is_online, current_lat, current_lng, rating, trips) VALUES
(1, 9, 'มอเตอร์ไซค์', 'มอเตอร์ไซค์ • ฮอนด้า เวฟ', 'กข 1234', TRUE, 8.7890, 99.3550, 4.9, 1240),
(2, 11, 'รถตุ๊กตุ๊ก', 'รถตุ๊กตุ๊ก • สีส้ม', 'กข 5678', TRUE, 8.7902, 99.3560, 4.8, 650)
ON CONFLICT (id) DO UPDATE SET is_online = EXCLUDED.is_online;

-- 9. Wallets
INSERT INTO wallets (id, user_id, balance, pending_balance) VALUES
(1, 1, 650.0, 0.0),
(2, 2, 4250.0, 0.0),
(3, 3, 3890.0, 0.0),
(4, 4, 5600.0, 0.0),
(5, 5, 4100.0, 0.0),
(6, 6, 2950.0, 0.0),
(7, 7, 1850.0, 0.0),
(8, 8, 3500.0, 0.0),
(9, 9, 1280.0, 0.0),
(10, 10, 24500.0, 0.0)
ON CONFLICT (id) DO UPDATE SET balance = EXCLUDED.balance;

-- 10. Point Logs
INSERT INTO point_logs (id, user_id, points_change, type, note) VALUES
(1, 1, 16, 'earn', 'ได้รับแต้มจากการสั่งซื้อ NS-1043'),
(2, 1, 11, 'earn', 'ได้รับแต้มจากการสั่งซื้อ NS-1042'),
(3, 1, 17, 'earn', 'ได้รับแต้มจากการสั่งซื้อ NS-1039'),
(4, 1, 24, 'earn', 'ได้รับแต้มจากการสั่งซื้อ NS-1021')
ON CONFLICT (id) DO NOTHING;

-- 11. Rewards & User Rewards
INSERT INTO rewards (id, title, detail, cost, code, image_url) VALUES
('d20', 'ส่วนลด ฿20', 'ใช้กับออเดอร์ถัดไป ไม่มีขั้นต่ำ', 100, 'PT20', '/products/vegetables.png'),
('ship', 'ส่งฟรีในตำบล', 'ยกเว้นค่าจัดส่งในเขตนาสาร 1 ครั้ง', 250, 'PTSHIP', '/products/noodles.png'),
('d60', 'ส่วนลด ฿60', 'เมื่อสั่งซื้อครบ 200 บาทขึ้นไป', 400, 'PT60', '/products/otop-snack.png'),
('d150', 'ส่วนลด ฿150', 'เมื่อสั่งซื้อครบ 500 บาทขึ้นไป', 600, 'PT150', '/products/mangosteen.png')
ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title;

INSERT INTO user_rewards (id, user_id, reward_id, code) VALUES
(1, 1, 'd20', 'PT20')
ON CONFLICT (id) DO NOTHING;

-- 12. Ride Bookings (Mockup Data matching Customer Rider UI)
INSERT INTO ride_bookings (id, customer_id, rider_id, service_type, mode, origin_address, origin_lat, origin_lng, destination_address, destination_lat, destination_lng, vehicle_type, passenger_count, is_fragile, parcel_type, parcel_width_cm, parcel_length_cm, parcel_weight_kg, notes, base_fare, surcharge_amount, estimated_fare, distance_km, status) VALUES
('R-312', 1, 9, 'ride', 'passenger', 'บ้านเลขที่ 88 หมู่ 3 ต.นาสาร', 8.7896, 99.3547, 'ตลาดนาสาร (หน้าธนาคาร)', 8.7900, 99.3555, 'motorcycle', 1, FALSE, NULL, NULL, NULL, NULL, 'รอที่หน้าบ้าน มีสัมภาระ 1 ชิ้น โทรก่อนถึง', 20.0, 0.0, 29.0, 1.5, 'matched'),
('R-311', 1, 9, 'ride', 'passenger', 'ตลาดนาสาร (หน้าธนาคาร)', 8.7900, 99.3550, 'โรงพยาบาลบ้านนาสาร', 8.7950, 99.3580, 'motorcycle', 1, FALSE, NULL, NULL, NULL, NULL, 'รอที่หน้าธนาคาร', 20.0, 0.0, 38.0, 3.0, 'completed'),
('R-313', 1, 9, 'parcel', 'parcel', 'ร้านเบเกอรี่ ตลาดนาสาร', 8.7889, 99.3601, 'บ้านเลขที่ 88 หมู่ 3 ต.นาสาร', 8.7896, 99.3547, 'car', 0, TRUE, 'ของแตกหักง่าย', 30.0, 30.0, 1.5, 'เค้กวันเกิด ระวังแตก วางตั้งเท่านั้น', 40.0, 20.0, 82.0, 2.2, 'on_the_way'),
('R-314', 1, 9, 'shop', 'passenger', 'ร้านอุ่นใจ มินิมาร์ท', 8.7905, 99.3555, 'บ้านเลขที่ 88 หมู่ 3 ต.นาสาร', 8.7896, 99.3547, 'motorcycle', 0, FALSE, NULL, NULL, NULL, NULL, 'ฝากซื้อไข่ไก่ 1 แผง น้ำดื่ม 1 แพ็ค โทรก่อนถึง', 40.0, 0.0, 51.0, 1.8, 'completed'),
('R-315', 1, NULL, 'document', 'parcel', 'สำนักงานเทศบาลเมืองบ้านนาสาร', 8.7920, 99.3570, 'ที่ทำการผู้ใหญ่บ้าน หมู่ 3 ต.นาสาร', 8.7850, 99.3450, 'motorcycle', 0, FALSE, 'เอกสาร', 21.0, 30.0, 0.5, 'เอกสารสำคัญ กรุณาใส่ซองกันน้ำ', 25.0, 0.0, 50.0, 4.1, 'requesting')
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status;
