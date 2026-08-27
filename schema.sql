-- =============================================================================
-- Nasan Plus+ Super-App Database Schema (PostgreSQL DDL)
-- Covers Customer, Merchant, Rider, Admin, Node Manager, Orders, Wallet & Loyalty Systems
-- =============================================================================

-- 1. Cities
CREATE TABLE IF NOT EXISTS cities (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    en_name VARCHAR(255),
    province VARCHAR(255) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL
);

-- 2. Sub-Districts
CREATE TABLE IF NOT EXISTS sub_districts (
    id VARCHAR(50) PRIMARY KEY,
    name_th VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    postal_code VARCHAR(10) DEFAULT '84120',
    is_active BOOLEAN DEFAULT TRUE
);

-- 2.1 Multi-Location Nodes & Polygons
CREATE TABLE IF NOT EXISTS nodes (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS node_locations (
    id VARCHAR(50) PRIMARY KEY,
    node_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    sub_district_id VARCHAR(50) REFERENCES sub_districts(id),
    name VARCHAR(255) NOT NULL,
    polygon_data JSONB
);

-- 3. Users (Customer, Merchant, Rider, Node Manager, Admin)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    line_user_id VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    role VARCHAR(50) DEFAULT 'customer',
    granted_roles JSONB DEFAULT '["customer"]'::jsonb,
    active_role VARCHAR(50) DEFAULT 'customer',
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_line_id ON users(line_user_id);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_active_role ON users(active_role);

-- 3.1 Merchant Multi-User Staff Bindings
CREATE TABLE IF NOT EXISTS merchant_user_bindings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
    merchant_role VARCHAR(50) DEFAULT 'owner', -- 'owner', 'manager', 'staff'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3.2 Node Manager Scoped Assignments
CREATE TABLE IF NOT EXISTS node_manager_assignments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    node_id VARCHAR(50) NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Shops (Stores, Farms & Retail Outlets)
CREATE TABLE IF NOT EXISTS shops (
    id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    tagline VARCHAR(255),
    description TEXT,
    category VARCHAR(50) NOT NULL DEFAULT 'mart', -- 'fresh', 'gi-otop', 'food', 'retail'
    sub_district_id VARCHAR(50) NOT NULL REFERENCES sub_districts(id),
    province VARCHAR(255) DEFAULT 'สุราษฎร์ธานี',
    origin_label VARCHAR(255) DEFAULT 'บ้านนาสาร',
    courier_shipping BOOLEAN DEFAULT FALSE,
    courier_from DOUBLE PRECISION DEFAULT 50.0,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    status VARCHAR(50) DEFAULT 'approved', -- 'pending', 'approved', 'suspended'
    gp_rate DOUBLE PRECISION DEFAULT 15.0,
    rating DOUBLE PRECISION DEFAULT 4.8,
    image_url TEXT,
    phone VARCHAR(50),
    is_open BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_shops_category ON shops(category);
CREATE INDEX IF NOT EXISTS idx_shops_sub_district ON shops(sub_district_id);

-- 5. Products & Menus
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    shop_id INT NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    price DOUBLE PRECISION NOT NULL,
    original_price DOUBLE PRECISION,
    unit VARCHAR(50) DEFAULT 'ชิ้น',
    badge VARCHAR(50), -- 'GI', 'OTOP', 'ขายดี', 'ยอดนิยม', 'อุ่นใจ'
    is_favorite BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    image_url TEXT
);
CREATE INDEX IF NOT EXISTS idx_products_shop ON products(shop_id);

-- 6. Orders
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(100) PRIMARY KEY, -- e.g. "NS-1043"
    customer_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    shop_id INT REFERENCES shops(id) ON DELETE SET NULL,
    rider_id INT REFERENCES users(id) ON DELETE SET NULL,
    sub_district_id VARCHAR(50) NOT NULL REFERENCES sub_districts(id),
    total_amount DOUBLE PRECISION NOT NULL,
    delivery_fee DOUBLE PRECISION DEFAULT 25.0,
    discount_amount DOUBLE PRECISION DEFAULT 0.0,
    final_amount DOUBLE PRECISION NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'preparing', 'delivering', 'completed', 'cancelled'
    payment_method VARCHAR(50) DEFAULT 'promptpay',
    payment_status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'paid'
    delivery_mode VARCHAR(50) DEFAULT 'local', -- 'local', 'nationwide'
    delivery_address TEXT NOT NULL,
    eta VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_shop ON orders(shop_id);
CREATE INDEX IF NOT EXISTS idx_orders_rider ON orders(rider_id);

-- 7. Order Items
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE SET NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DOUBLE PRECISION NOT NULL,
    subtotal DOUBLE PRECISION NOT NULL,
    note VARCHAR(255)
);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);

-- 8. Rider Profiles
CREATE TABLE IF NOT EXISTS rider_profiles (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_type VARCHAR(100) DEFAULT 'มอเตอร์ไซค์',
    vehicle VARCHAR(255),
    plate_number VARCHAR(100) NOT NULL,
    is_online BOOLEAN DEFAULT FALSE,
    kyc_status VARCHAR(50) DEFAULT 'verified',
    inspection_status VARCHAR(50) DEFAULT 'passed',
    vehicle_details JSONB,
    current_lat DOUBLE PRECISION,
    current_lng DOUBLE PRECISION,
    rating DOUBLE PRECISION DEFAULT 4.9,
    trips INT DEFAULT 0
);

-- 9. Wallets & Transactions
CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    wallet_type VARCHAR(50) DEFAULT 'user_earning', -- 'holding', 'operating', 'user_earning'
    balance DOUBLE PRECISION DEFAULT 0.0,
    pending_balance DOUBLE PRECISION DEFAULT 0.0,
    account_number VARCHAR(100),
    bank_name VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wallet_transactions (
    id SERIAL PRIMARY KEY,
    wallet_id INT NOT NULL REFERENCES wallets(id) ON DELETE CASCADE,
    amount DOUBLE PRECISION NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'earning', 'fee_deduction', 'withdrawal', 'topup', 'holding_transfer'
    ref_id VARCHAR(100),
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Point Logs (Customer Loyalty)
CREATE TABLE IF NOT EXISTS point_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points_change INT NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'earn', 'redeem'
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Rewards & User Rewards (Loyalty Catalog)
CREATE TABLE IF NOT EXISTS rewards (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    detail TEXT NOT NULL,
    cost INT NOT NULL,
    code VARCHAR(50) NOT NULL,
    image_url TEXT
);

CREATE TABLE IF NOT EXISTS user_rewards (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reward_id VARCHAR(50) NOT NULL REFERENCES rewards(id) ON DELETE CASCADE,
    code VARCHAR(50) NOT NULL,
    claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Ride Bookings (On-Demand Transport & Express Delivery)
CREATE TABLE IF NOT EXISTS ride_bookings (
    id VARCHAR(100) PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rider_id INT REFERENCES users(id) ON DELETE SET NULL,
    service_type VARCHAR(50) DEFAULT 'ride', -- 'ride', 'parcel', 'shop', 'document'
    mode VARCHAR(50) DEFAULT 'passenger', -- 'passenger', 'parcel'
    vehicle_type VARCHAR(50) DEFAULT 'motorcycle', -- 'motorcycle', 'tuktuk', 'car', 'songthaew', 'truck'
    origin_address TEXT NOT NULL,
    origin_lat DOUBLE PRECISION,
    origin_lng DOUBLE PRECISION,
    destination_address TEXT NOT NULL,
    destination_lat DOUBLE PRECISION,
    destination_lng DOUBLE PRECISION,
    distance_km DOUBLE PRECISION DEFAULT 1.0,
    passenger_count INT DEFAULT 1,
    is_fragile BOOLEAN DEFAULT FALSE,
    parcel_type VARCHAR(100),
    parcel_width_cm DOUBLE PRECISION,
    parcel_length_cm DOUBLE PRECISION,
    parcel_weight_kg DOUBLE PRECISION,
    notes TEXT,
    base_fare DOUBLE PRECISION DEFAULT 20.0,
    surcharge_amount DOUBLE PRECISION DEFAULT 0.0,
    estimated_fare DOUBLE PRECISION NOT NULL,
    status VARCHAR(50) DEFAULT 'requesting', -- 'requesting', 'finding', 'matched', 'accepted', 'on_the_way', 'completed', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

