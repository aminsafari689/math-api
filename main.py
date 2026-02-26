from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import math

# create FastAPI app
app = FastAPI(title="Math API", version="1.1.0", description="Simple API with infinite error handling for math operations")

# ------------------------
# custom error classes
# ------------------------
class MathAPIException(HTTPException):
    # base class for all custom API exceptions
    def __init__(self, status_code: int = 400, detail: str = "An error occurred"):
        super().__init__(status_code=status_code, detail=detail)

class DivideByZeroError(MathAPIException):
    # error for division by zero
    def __init__(self):
        super().__init__(detail="Cannot divide by zero")

class NegativeSqrtError(MathAPIException):
    # error for square root of negative number
    def __init__(self):
        super().__init__(detail="Cannot take square root of a negative number")

# ------------------------
# handle all custom API exceptions
# ------------------------
@app.exception_handler(MathAPIException)
async def math_api_exception_handler(request: Request, exc: MathAPIException):
    # return standardized JSON response for all errors
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

# ------------------------
# input model for numbers
# ------------------------
class Numbers(BaseModel):
    n1: float
    n2: float

# ------------------------
# API endpoints
# ------------------------
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
        raise DivideByZeroError()
    return {"result": data.n1 / data.n2}

@app.post("/api/sqrt")
def sqrt_number(data: Numbers):
    if data.n1 < 0:
        raise NegativeSqrtError()
    return {"result": math.sqrt(data.n1)}

# ------------------------
# adding new errors is easy
# for example: OverflowError or InvalidInputError
# ------------------------
