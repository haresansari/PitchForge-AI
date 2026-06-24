from app.services.auth_service import hash_password, verify_password
from fastapi import APIRouter, HTTPException, Header
from app.models.auth_models import UserSignup, UserLogin
from fastapi import Query
from app.database.connection import get_db
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

users = []

@router.get("/test")
def test_auth():
    return {
        "message": "Authentication route working"
    }
@router.post("/signup")
def signup(user: UserSignup):

    db = get_db()

    if db is None:
        raise HTTPException(
            status_code=500,
            detail="Database not connected"
        )

    user_collection = db["users"]

    existing_user = user_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    user_collection.insert_one({
    "name": user.name,
    "email": user.email,
    "password": hashed_password
})

    return {
        "success": True,
        "message": "User registered successfully"
    }
@router.post("/login")
def login(user: UserLogin):

    db = get_db()

    if db is None:
        raise HTTPException(
            status_code=500,
            detail="Database not connected"
        )

    user_collection = db["users"]

    existing_user = user_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/profile")
def profile(token: str = Query(None)):

    print("TOKEN =", token)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "message": "Protected route accessed",
        "email": email
    }