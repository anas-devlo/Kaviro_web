from uuid import uuid4
from sqlalchemy import Column, String, Uuid, CheckConstraint
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL OR phone IS NOT NULL",
            name="email_or_phone_required",
        ),
    )

    uuid = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True, index=True)
    phone = Column(String, unique=True, nullable=True, index=True)
    password = Column(String, nullable=False)  # هاش مش نص عادي