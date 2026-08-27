from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import engine, Base, get_db
import app.models as models
import app.schemas as schemas
import app.crud as crud
from app.seed import seed_database

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

# Auto seed database if empty
with next(get_db()) as db_session:
    seed_database(db_session)

app = FastAPI(
    title="Nasan Plus API",
    description="Backend REST API service for Nasan Plus digital community marketplace",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "app": "Nasan Plus Digital Marketplace API",
        "district": "Ban Na San, Surat Thani",
        "docs": "/docs"
    }

# ---------------------------------------------
# Cities & Sub-Districts
# ---------------------------------------------
@app.get("/api/cities", response_model=List[schemas.CityOut])
def list_cities(db: Session = Depends(get_db)):
    return crud.get_cities(db)

@app.get("/api/sub-districts", response_model=List[schemas.SubDistrictOut])
def list_sub_districts(db: Session = Depends(get_db)):
    return crud.get_sub_districts(db)

# ---------------------------------------------
# Users & RBAC Role Switching
# ---------------------------------------------
@app.get("/api/users", response_model=List[schemas.UserOut])
def list_users(role: Optional[str] = None, db: Session = Depends(get_db)):
    if role:
        return crud.get_users_by_role(db, role)
    return db.query(models.User).all()

@app.get("/api/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/api/users/{user_id}/switch-role", response_model=schemas.UserSwitchRoleResponse)
def switch_user_role(user_id: int, payload: schemas.UserSwitchRoleRequest, db: Session = Depends(get_db)):
    return crud.switch_user_role(db, user_id, payload.target_role)

# ---------------------------------------------
# Multi-Location Node Architecture
# ---------------------------------------------
@app.get("/api/nodes", response_model=List[schemas.NodeOut])
def list_nodes(db: Session = Depends(get_db)):
    return crud.get_nodes(db)

@app.post("/api/nodes", response_model=schemas.NodeOut)
def create_node(node_in: schemas.NodeCreate, db: Session = Depends(get_db)):
    return crud.create_node(db, node_in)

@app.get("/api/nodes/{node_id}/locations", response_model=List[schemas.NodeLocationOut])
def list_node_locations(node_id: str, db: Session = Depends(get_db)):
    return crud.get_node_locations(db, node_id)

@app.post("/api/nodes/{node_id}/locations", response_model=schemas.NodeLocationOut)
def create_node_location(node_id: str, loc_in: schemas.NodeLocationCreate, db: Session = Depends(get_db)):
    loc_in.node_id = node_id
    return crud.create_node_location(db, loc_in)

@app.get("/api/node-managers/{user_id}/scoped-data")
def get_node_manager_scoped_data(user_id: int, db: Session = Depends(get_db)):
    return crud.get_node_manager_scoped_data(db, user_id)

# ---------------------------------------------
# Merchant Multi-User Staff Bindings
# ---------------------------------------------
@app.get("/api/shops/{shop_id}/users", response_model=List[schemas.MerchantUserBindingOut])
def list_merchant_bindings(shop_id: int, db: Session = Depends(get_db)):
    return crud.get_merchant_bindings(db, shop_id)

@app.post("/api/shops/{shop_id}/users", response_model=schemas.MerchantUserBindingOut)
def create_merchant_binding(shop_id: int, binding_in: schemas.MerchantUserBindingCreate, db: Session = Depends(get_db)):
    binding_in.shop_id = shop_id
    return crud.create_merchant_binding(db, binding_in)

# ---------------------------------------------
# Shops & Products
# ---------------------------------------------
@app.get("/api/shops", response_model=List[schemas.ShopOut])
def list_shops(
    category: Optional[str] = Query(None, description="gi-otop, mart, or food"),
    sub_district_id: Optional[str] = Query(None, description="Sub-district ID e.g. nasan"),
    db: Session = Depends(get_db)
):
    return crud.get_shops(db, category=category, sub_district_id=sub_district_id)

@app.get("/api/shops/{shop_id}", response_model=schemas.ShopOut)
def get_shop(shop_id: str, db: Session = Depends(get_db)):
    shop = crud.get_shop_by_id(db, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop

@app.get("/api/shops/{shop_id}/products", response_model=List[schemas.ProductOut])
def list_shop_products(shop_id: str, db: Session = Depends(get_db)):
    shop = crud.get_shop_by_id(db, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return crud.get_products_by_shop(db, shop.id)

# ---------------------------------------------
# Orders
# ---------------------------------------------
@app.post("/api/orders", response_model=schemas.OrderOut)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order_in)

@app.get("/api/orders", response_model=List[schemas.OrderOut])
def list_orders(
    customer_id: Optional[int] = None,
    shop_id: Optional[int] = None,
    rider_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_orders(db, customer_id=customer_id, shop_id=shop_id, rider_id=rider_id)

# ---------------------------------------------
# Rewards & Loyalty
# ---------------------------------------------
@app.get("/api/rewards", response_model=List[schemas.RewardOut])
def list_rewards(db: Session = Depends(get_db)):
    return crud.get_rewards(db)

@app.post("/api/rewards/redeem", response_model=schemas.UserRewardOut)
def redeem_reward(user_id: int, reward_id: str, db: Session = Depends(get_db)):
    res = crud.redeem_reward(db, user_id, reward_id)
    if not res:
        raise HTTPException(status_code=400, detail="Unable to redeem reward")
    return res

# ---------------------------------------------
# Ride Bookings
# ---------------------------------------------
@app.post("/api/rides", response_model=schemas.RideBookingOut)
def create_ride(ride_in: schemas.RideBookingCreate, db: Session = Depends(get_db)):
    return crud.create_ride_booking(db, ride_in)

@app.get("/api/rides", response_model=List[schemas.RideBookingOut])
def list_rides(customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_ride_bookings(db, customer_id=customer_id)

# ---------------------------------------------
# Rider Jobs Database Operations
# ---------------------------------------------
@app.get("/api/riders/jobs")
def list_rider_jobs(db: Session = Depends(get_db)):
    return crud.get_all_rider_jobs(db)

@app.post("/api/riders/jobs")
def create_rider_job(job_data: dict, db: Session = Depends(get_db)):
    return crud.create_rider_job_in_db(db, job_data)

@app.put("/api/riders/jobs/{job_id}/phase")
def update_rider_job_phase_endpoint(job_id: str, payload: dict, db: Session = Depends(get_db)):
    phase = payload.get("phase", "available")
    return crud.update_rider_job_phase(db, job_id, phase)


# ---------------------------------------------
# Wallets & Payouts
# ---------------------------------------------
@app.get("/api/wallets/{user_id}", response_model=schemas.WalletOut)
def get_wallet(user_id: int, db: Session = Depends(get_db)):
    wallet = crud.get_user_wallet(db, user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.post("/api/wallets/{user_id}/withdraw", response_model=schemas.WalletOut)
def withdraw_wallet(user_id: int, withdraw_in: schemas.WalletWithdrawRequest, db: Session = Depends(get_db)):
    try:
        return crud.process_wallet_withdrawal(db, user_id, withdraw_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------
# Seed Database Trigger
# ---------------------------------------------
@app.post("/api/seed")
def trigger_seed(db: Session = Depends(get_db)):
    seed_database(db)
    return {"message": "Seed database process completed"}