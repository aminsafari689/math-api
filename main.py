from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional, List
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
import math

# =========================
# Config
# =========================

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================
# Database Models
# =========================

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    operations = relationship("OperationDB", back_populates="user")

class OperationDB(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    operation_type = Column(String)
    n1 = Column(Float)
    n2 = Column(Float, nullable=True)
    result = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserDB", back_populates="operations")

Base.metadata.create_all(bind=engine)

# =========================
# Schemas
# =========================

class User(BaseModel):
    username: str
    password: str

class Numbers(BaseModel):
    n1: float
    n2: float

class SingleNumber(BaseModel):
    n1: float


class OperationOut(BaseModel):
    id: int
    operation_type: str
    n1: float
    n2: Optional[float]
    result: float
    timestamp: datetime

    class Config:
         orm_mode = True

# =========================
# Utils
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# =========================
# Auth Routes
# =========================

@app.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = UserDB(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(db_user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# Math Routes (Protected)
# =========================

def save_operation(db, user, op_type, n1, n2, result):
    operation = OperationDB(
        user_id=user.id,
        operation_type=op_type,
        n1=n1,
        n2=n2,
        result=result
    )
    db.add(operation)
    db.commit()
    db.refresh(operation)

@app.post("/api/sum")
def sum_numbers(data: Numbers, user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    result = data.n1 + data.n2
    save_operation(db, user, "sum", data.n1, data.n2, result)
    return {"result": result}

@app.post("/api/div")
def div_numbers(data: Numbers, user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.n2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    result = data.n1 / data.n2
    save_operation(db, user, "div", data.n1, data.n2, result)
    return {"result": result}

@app.post("/api/mul")
def mul_numbers(
    data: Numbers,
    user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = data.n1 * data.n2
    save_operation(db, user, "mul", data.n1, data.n2, result)
    return {"result": result}


@app.post("/api/sub")
def sub_numbers(
    data: Numbers,
    user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = data.n1 - data.n2
    save_operation(db, user, "sub", data.n1, data.n2, result)
    return {"result": result}


@app.post("/api/pow")
def pow_numbers(
    data: Numbers,
    user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = data.n1 ** data.n2
    save_operation(db, user, "pow", data.n1, data.n2, result)
    return {"result": result}


@app.post("/api/sqrt")
def sqrt_number(
    data: SingleNumber,
    user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.n1 < 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot calculate square root of negative number"
        )

    result = math.sqrt(data.n1)

    # چون sqrt فقط n1 دارد، n2 را None ذخیره می‌کنیم
    save_operation(db, user, "sqrt", data.n1, None, result)

    return {"result": result}

# =========================
# History Endpoints
# =========================

@app.get("/api/user/{user_id}/history/all", response_model=List[OperationOut])
def get_all_history(user_id: int,
                    db: Session = Depends(get_db),
                    user: UserDB = Depends(get_current_user)):

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    operations = db.query(OperationDB)\
        .filter(OperationDB.user_id == user_id)\
        .all()

    return operations


@app.get("/api/user/{user_id}/history/{operation_id}", response_model=OperationOut)
def get_operation(user_id: int,
                  operation_id: int,
                  db: Session = Depends(get_db),
                  user: UserDB = Depends(get_current_user)):

    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    operation = db.query(OperationDB).filter(
        OperationDB.user_id == user_id,
        OperationDB.id == operation_id
    ).first()

    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    return operation
