## قاعدة البيانات (Database)

الجزء ده بيشرح ملفين بس: `backend/database.py` و `backend/models.py`.
بنستخدم **SQLAlchemy** للتعامل مع **PostgreSQL** من بايثون.

---

### `backend/database.py`

مسؤول عن الاتصال بالداتا بيز.

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL مش موجود")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

| العنصر | وظيفته |
|---|---|
| `env_path` | تحديد مكان ملف `.env` (في الفولدر الرئيسي للمشروع) |
| `load_dotenv` | قراءة ملف `.env` |
| `DATABASE_URL` | رابط الاتصال بالداتا بيز، متقري من `.env` |
| `RuntimeError` | بيوقف البرنامج برسالة واضحة لو الرابط مش موجود |
| `engine` | الاتصال الفعلي بـ PostgreSQL |
| `SessionLocal` | مصنع بيعمل جلسة (Session) جديدة مع الداتا بيز |
| `Base` | الكلاس الأب اللي كل الجداول بترث منه |
| `get_db()` | بتفتح جلسة، وتدّيها للـ endpoint، وتقفلها بعد ما يخلص |

**تفاصيل `sessionmaker`:**

- `bind=engine`: الجلسة تستخدم الاتصال ده.
- `autocommit=False`: التعديلات متتحفظش غير لما نعمل `db.commit()`.
- `autoflush=False`: التعديلات متتبعتش للداتا بيز تلقائياً قبل كل بحث.

**شكل رابط الاتصال في `.env`:**

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
```

| الجزء | معناه |
|---|---|
| `postgresql+psycopg` | نوع الداتا بيز + الدرايفر |
| `user:password` | اسم المستخدم والباسورد |
| `localhost:5432` | الجهاز والبورت |
| `dbname` | اسم الداتا بيز |

---

### `backend/models.py`

مسؤول عن تعريف شكل الجداول.

```python
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
```

الكلاس `User` بيرث من `Base`، فبيتحول لجدول اسمه `users` (`__tablename__`)، وكل object منه بيمثل صف (مستخدم) في الجدول.

| العمود | النوع | الخصائص |
|---|---|---|
| `uuid` | Integer | مفتاح أساسي (`primary_key`)، بيزيد تلقائياً، عليه فهرس (`index`) |
| `name` | String | إجباري (`nullable=False`) |
| `email` | String | فريد (`unique`)، ممكن يبقى فاضي، عليه فهرس |
| `phone` | String | فريد (`unique`)، ممكن يبقى فاضي، عليه فهرس |
| `password` | String | إجباري، المفروض يتخزن مهشّر (Hash) مش نص عادي |

**ملاحظات:**

- `unique=True`: مفيش مستخدمين بنفس الإيميل أو الرقم.
- `nullable=True` في الإيميل والرقم لأن المستخدم يسجّل بواحد منهم بس.
- الرقم نوعه `String` عشان الأصفار اللي في الأول متتمسحش.
- `index=True`: بيسرّع البحث بالعمود ده.

---

### المكتبات المستخدمة في الملفين

```
sqlalchemy
python-dotenv
psycopg[binary]
```

(`os` و `pathlib` جاية مع بايثون، و`database` ده ملف المشروع نفسه.)