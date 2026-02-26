from fastapi import FastAPI
from pydantic import BaseModel

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