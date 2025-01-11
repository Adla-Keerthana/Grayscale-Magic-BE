from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import Token, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
from app.database import users_collection, user_helper
from app.models import UserInDB
from datetime import timedelta

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserInDB)
async def register_user(
    username: str = Body(...),
    password: str = Body(...),
    email: str = Body(...),
    full_name: str = Body(...),
):
    hashed_password = get_password_hash(password)
    user = {
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "disabled": False
    }
    new_user = await users_collection.insert_one(user)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return UserInDB(**user_helper(created_user))
