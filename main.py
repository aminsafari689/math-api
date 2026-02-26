from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import math

app = FastAPI()

# -----------------------
# Security Config
# -----------------------
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake in-memory database
fake_users_db = {}

# -----------------------
# Models
# -----------------------

class Numbers(BaseModel):
    n1: float
    n2: float

class SingleNumber(BaseModel):
    n1: float

class User(BaseModel):
    username: str
    password: str

# -----------------------
# Utility Functions
# -----------------------

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -----------------------
# Auth Routes
# -----------------------

@app.post("/register")
def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed = hash_password(user.password)
    fake_users_db[user.username] = hashed
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    if user.username not in fake_users_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    hashed_password = fake_users_db[user.username]
    
    if not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------
# Math Routes
# -----------------------

@app.post("/api/sum")
def sum_numbers(data: Numbers):
    return {"result": data.n1 + data.n2}

@app.post("/api/mul")
def mul_numbers(data: Numbers):
    return {"result": data.n1 * data.n2}

@app.post("/api/pow")
def pow_numbers(data: Numbers):
    return {"result": data.n1 ** data.n2}

@app.post("/api/sub")
def sub_numbers(data: Numbers):
    return {"result": data.n1 - data.n2}

@app.post("/api/div")
def div_numbers(data: Numbers):
    if data.n2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": data.n1 / data.n2}

@app.post("/api/sqrt")
def sqrt_number(data: SingleNumber):
    if data.n1 < 0:
        raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")
    return {"result": math.sqrt(data.n1)}
