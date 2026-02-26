# Math API

A FastAPI project for basic math operations with proper error handling.

## Endpoints

- `POST /api/sum` – Returns the sum of `n1` and `n2`
- `POST /api/mul` – Returns the product of `n1` and `n2`
- `POST /api/pow` – Returns `n1` raised to the power of `n2`
- `POST /api/sub` – Returns `n1 - n2`
- `POST /api/div` – Returns `n1 / n2` (error if `n2` is 0)
- `POST /api/sqrt` – Returns square root of `n1` (error if `n1 < 0`)

## Errors

All errors are returned in this format:

```json
{
  "error": "Cannot divide by zero"
}
