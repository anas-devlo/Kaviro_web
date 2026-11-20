from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

fake_users_db = {}

class RegisterRequest(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str

@router.post("/register")
def register(user: RegisterRequest):
    if not user.email and not user.phone:
        raise HTTPException(status_code=400, detail="لازم تدخل إيميل أو رقم تليفون")
    key = user.email or user.phone
    if key in fake_users_db:
        raise HTTPException(status_code=400, detail="الحساب ده موجود قبل كده")
    fake_users_db[key] = {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "password": user.password
    }
    return {"message": "تم إنشاء الحساب بنجاح", "user": user.name}

@router.post("/login")
def login(user: LoginRequest):
    stored_user = fake_users_db.get(user.email_or_phone)
    if not stored_user:
        raise HTTPException(status_code=404, detail="الحساب مش موجود")
    if stored_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="الباسورد غلط")
    return {"message": f"أهلاً بيك يا {stored_user['name']}، تم تسجيل الدخول بنجاح"}
