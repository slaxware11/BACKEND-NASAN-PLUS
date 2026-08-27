from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel

# City
class CityBase(BaseModel):
    id: str
    name: str
    en_name: Optional[str] = None
    province: str
    lat: float
    lng: float

class CityOut(CityBase):
    class Config:
        from_attributes = True

# SubDistrict
class SubDistrictBase(BaseModel):
    id: str
    name_th: str
    name_en: Optional[str] = None
    postal_code: str = "84120"

class SubDistrictOut(SubDistrictBase):
    is_active: bool

    class Config:
        from_attributes = True

# Node & Node Location
class NodeLocationBase(BaseModel):
    id: str
    node_id: str
    sub_district_id: Optional[str] = None
    name: str
    polygon_data: Optional[Any] = None

class NodeLocationCreate(BaseModel):
    id: str
    node_id: str
    sub_district_id: Optional[str] = None
    name: str
    polygon_data: Optional[Any] = None

class NodeLocationOut(NodeLocationBase):
    class Config:
        from_attributes = True

class NodeBase(BaseModel):
    name: str
    code: str
    is_active: bool = True

class NodeCreate(NodeBase):
    id: str

class NodeOut(NodeBase):
    id: str
    created_at: datetime
    locations: List[NodeLocationOut] = []

    class Config:
        from_attributes = True

# Merchant User Binding
class MerchantUserBindingCreate(BaseModel):
    user_id: int
    shop_id: int
    merchant_role: str = "staff" # owner, manager, staff

class MerchantUserBindingOut(MerchantUserBindingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Node Manager Assignment
class NodeManagerAssignmentCreate(BaseModel):
    user_id: int
    node_id: str

class NodeManagerAssignmentOut(NodeManagerAssignmentCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User & Role Switch
class UserBase(BaseModel):
    name: str
    phone: str
    role: str = "customer"
    granted_roles: Optional[List[str]] = ["customer"]
    active_role: Optional[str] = "customer"
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    line_user_id: Optional[str] = None

class UserOut(UserBase):
    id: int
    line_user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserSwitchRoleRequest(BaseModel):
    target_role: str

class UserSwitchRoleResponse(BaseModel):
    success: bool
    user_id: int
    active_role: str
    granted_roles: List[str]
    auto_offline_triggered: bool = False
    toast_notification: Optional[str] = None

# Product
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    unit: str = "ชิ้น"
    badge: Optional[str] = None
    is_favorite: bool = False
    is_available: bool = True
    image_url: Optional[str] = None

class ProductOut(ProductBase):
    id: int
    shop_id: int

    class Config:
        from_attributes = True

# Shop
class ShopBase(BaseModel):
    name: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    category: str = "mart"
    sub_district_id: str
    province: str = "สุราษฎร์ธานี"
    origin_label: str = "บ้านนาสาร"
    courier_shipping: bool = False
    courier_from: float = 50.0
    lat: Optional[float] = None
    lng: Optional[float] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None

class ShopCreate(ShopBase):
    owner_id: int

class ShopOut(ShopBase):
    id: int
    owner_id: int
    status: str
    gp_rate: float
    rating: float
    is_open: bool
    created_at: datetime
    products: List[ProductOut] = []
    staff_bindings: List[MerchantUserBindingOut] = []

    class Config:
        from_attributes = True

# Order Item
class OrderItemCreate(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    note: Optional[str] = None

class OrderItemOut(OrderItemCreate):
    id: int
    subtotal: float

    class Config:
        from_attributes = True

class ShopSimpleOut(BaseModel):
    id: int
    name: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class UserSimpleOut(BaseModel):
    id: int
    name: str
    phone: str
    rider_profile: Optional['RiderProfileOut'] = None

    class Config:
        from_attributes = True

# Order
class OrderCreate(BaseModel):
    customer_id: int
    shop_id: Optional[int] = None
    sub_district_id: str
    total_amount: float
    delivery_fee: float = 25.0
    discount_amount: float = 0.0
    payment_method: str = "promptpay"
    payment_status: str = "pending"
    delivery_mode: str = "local"
    delivery_address: str
    notes: Optional[str] = None
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: str
    customer_id: int
    shop_id: Optional[int] = None
    rider_id: Optional[int] = None
    sub_district_id: str
    total_amount: float
    delivery_fee: float
    discount_amount: float
    final_amount: float
    status: str
    payment_method: str
    payment_status: str
    delivery_mode: str
    delivery_address: str
    eta: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    shop: Optional[ShopSimpleOut] = None
    rider: Optional[UserSimpleOut] = None
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True

# Rider Profile
class RiderProfileOut(BaseModel):
    id: int
    user_id: int
    vehicle_type: str
    vehicle: Optional[str] = None
    plate_number: str
    is_online: bool
    kyc_status: Optional[str] = "verified"
    inspection_status: Optional[str] = "passed"
    vehicle_details: Optional[Any] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    rating: float
    trips: int

    class Config:
        from_attributes = True

# Wallet
class WalletTransactionOut(BaseModel):
    id: int
    amount: float
    type: str
    ref_id: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class WalletOut(BaseModel):
    id: int
    user_id: int
    wallet_type: Optional[str] = "user_earning"
    balance: float
    pending_balance: float
    account_number: Optional[str] = None
    bank_name: Optional[str] = None
    transactions: List[WalletTransactionOut] = []

    class Config:
        from_attributes = True

class WalletWithdrawRequest(BaseModel):
    amount: float
    bank_code: str
    account_number: str
    account_name: str

# Reward
class RewardOut(BaseModel):
    id: str
    title: str
    detail: str
    cost: int
    code: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class UserRewardOut(BaseModel):
    id: int
    user_id: int
    reward_id: str
    code: str
    claimed_at: datetime

    class Config:
        from_attributes = True

# Ride Booking
class RideBookingCreate(BaseModel):
    customer_id: int
    service_type: str = "ride" # ride, parcel, shop, document
    mode: str = "passenger" # passenger, parcel
    vehicle_type: str = "motorcycle" # motorcycle, tuktuk, car, songthaew, truck
    origin_address: str
    origin_lat: Optional[float] = None
    origin_lng: Optional[float] = None
    destination_address: str
    destination_lat: Optional[float] = None
    destination_lng: Optional[float] = None
    distance_km: float = 1.0
    passenger_count: Optional[int] = 1
    is_fragile: Optional[bool] = False
    parcel_type: Optional[str] = None
    parcel_width_cm: Optional[float] = None
    parcel_length_cm: Optional[float] = None
    parcel_weight_kg: Optional[float] = None
    notes: Optional[str] = None
    base_fare: Optional[float] = 20.0
    surcharge_amount: Optional[float] = 0.0
    estimated_fare: float

class RideBookingOut(RideBookingCreate):
    id: str
    rider_id: Optional[int] = None
    status: str
    created_at: datetime
    rider: Optional[UserSimpleOut] = None

    class Config:
        from_attributes = True


