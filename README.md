# Math API

A simple API built with **FastAPI**.

## Endpoints

- `POST /api/sum` – Adds `n1` and `n2`
- `POST /api/mul` – Multiplies `n1` and `n2`
- `POST /api/pow` – Raises `n1` to the power of `n2`
- `POST /api/sub` – Subtracts `n2` from `n1`
- `POST /api/div` – Divides `n1` by `n2` (returns error if `n2` is 0)
- `POST /api/sqrt` – Calculates square root of `n1` (returns error if `n1 < 0`)

## Run

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
