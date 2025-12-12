# Examples for the Personal Data Validator API

## cURL examples

### 1) Health check
```bash
curl http://localhost:8000/health
```

### 2) API info
# Examples for the Personal Data Validator API

## cURL examples

### 1) Health check
```bash
curl http://localhost:8000/health
```

### 2) API info
```bash
curl http://localhost:8000/
```

### 3) Successful validation (all fields)
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "juan",
    "last_name": "perez",
    "email": "juan.perez@example.com",
    "phone": "1234567890",
    "age": 30
  }'
```

### 4) Validation with required fields only
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "maria",
    "last_name": "garcia",
    "email": "maria.garcia@example.com"
  }'
```

### 5) Invalid email example
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "carlos",
    "last_name": "lopez",
    "email": "invalid-email"
  }'
```

### 6) Save response to file
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "ana",
    "last_name": "martinez",
    "email": "ana@example.com"
  }' > response.json
```

### 7) Pretty-print JSON
```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "luis",
    "last_name": "rodriguez",
    "email": "luis@example.com",
    "age": 25
  }' | python -m json.tool
```

## Python (requests)

### Basic usage
```python
import requests

url = "http://localhost:8000/validate"
payload = {
    "first_name": "juan",
    "last_name": "perez",
    "email": "juan.perez@example.com",
    "phone": "1234567890",
    "age": 30
}

response = requests.post(url, json=payload)
print(response.json())
```

### Handling errors
```python
import requests

url = "http://localhost:8000/validate"
payload = {
    "first_name": "a",  # Too short
    "last_name": "perez",
    "email": "juan.perez@example.com"
}

response = requests.post(url, json=payload)
if response.status_code == 200:
    print("✓ OK", response.json())
elif response.status_code == 422:
    print("✗ Validation error", response.json())
else:
    print(f"✗ Server error: {response.status_code}")
```

### Validate multiple users
```python
import requests

users = [
    {
        "first_name": "juan",
        "last_name": "perez",
        "email": "juan@example.com",
        "phone": "1234567890",
        "age": 30
    },
    {
        "first_name": "maria",
        "last_name": "garcia",
        "email": "maria@example.com",
        "age": 25
    }
]

url = "http://localhost:8000/validate"
for user in users:
    resp = requests.post(url, json=user)
    if resp.status_code == 200:
        data = resp.json()["data"]
        print(f"✓ {data['first_name']} {data['last_name']} - {data['email']}")
    else:
        print(f"✗ Error validating: {user}")
```

## httpx (async)

```python
import httpx
import asyncio
import json

async def validate_user():
    async with httpx.AsyncClient() as client:
        payload = {
            "first_name": "juan",
            "last_name": "perez",
            "email": "juan@example.com"
        }
        resp = await client.post("http://localhost:8000/validate", json=payload)
        print(json.dumps(resp.json(), indent=2))

asyncio.run(validate_user())
```

## Testing (pytest)

Run the included test script:

```bash
python test_api.py
```

These examples cover common use cases and can be adapted to fit your needs.
    assert respuesta.status_code == 200
