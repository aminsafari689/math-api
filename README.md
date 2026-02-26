## Simple Math API with User Authentication
This is a basic FastAPI application that provides user registration and login with JWT authentication, along with simple mathematical operations like addition, multiplication, exponentiation, subtraction, division, and square root calculation.
The user data is stored in an in-memory database (not persistent across restarts). Passwords are hashed using bcrypt, and authentication tokens are generated using JWT.


## Features
User registration and login.
JWT-based authentication (though math endpoints are public in this version).
Basic math operations via POST requests.
Error handling for invalid inputs (e.g., division by zero, square root of negative numbers).


## Requirements
Python 3.8 or higher
FastAPI
Uvicorn (for running the server)
Pydantic
Passlib (with bcrypt)
python-jose


## Usage
Run the application using Uvicorn:
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000. Access the interactive Swagger UI documentation at http://127.0.0.1:8000/docs.


## Example Requests
You can use tools like curl or Postman to test the endpoints.

Register a user:
curl -X POST "http://127.0.0.1:8000/register" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'

Login:
curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'

Perform addition:
curl -X POST "http://127.0.0.1:8000/api/sum" -H "Content-Type: application/json" -d '{"n1": 5, "n2": 3}'


## API Endpoints
Authentication Endpoints
POST /register: Register a new user. Body: {"username": "str", "password": "str"}
POST /login: Login and get JWT token. Body: {"username": "str", "password": "str"}


## Math Endpoints
All accept JSON bodies and return {"result": float}.

POST /api/sum: Add two numbers. Body: {"n1": float, "n2": float}

POST /api/mul: Multiply two numbers. Body: {"n1": float, "n2": float}

POST /api/pow: Exponentiate (n1 ^ n2). Body: {"n1": float, "n2": float}

POST /api/sub: Subtract n2 from n1. Body: {"n1": float, "n2": float}

POST /api/div: Divide n1 by n2. Body: {"n1": float, "n2": float} (Error if n2=0)

POST /api/sqrt: Square root of n1. Body: {"n1": float} (Error if n1<0)











