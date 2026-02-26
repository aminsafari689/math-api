from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI()

class Numbers(BaseModel):
    n1: float
    n2: float

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
def sqrt_number(data: Numbers):
    if data.n1 < 0:
        raise HTTPException(status_code=400, detail="Cannot take square root of negative number")
    return {"result": math.sqrt(data.n1)}


