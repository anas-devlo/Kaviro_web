import uuid
from sqlalchemy import Column, String, Uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    # لو هتستخدمه في auth.py
    # لو رجّعت الـ id في الـ response، حوّله لنص:
    # return {"id": str(new_user.id), ...}
    # FastAPI غالباً بيحوّله لوحده، بس str() مضمونة
    uuid = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True, index=True)
    phone = Column(String, unique=True, nullable=True, index=True)
    password = Column(String, nullable=False)  # هاش مش نص عادي