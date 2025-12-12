# Personal Data Validator API

FastAPI REST API for validating personal data using Pydantic.

Features
- Validate and normalize `first_name` and `last_name`
- Validate `email` using a robust validator
- Optional `phone` (digits only, min 7) and `age` (0-120)
- Automatic name capitalization
- Swagger UI and ReDoc documentation
- Logging and global error handling

Quick Start
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
uvicorn main:app --host localhost --port 8000
```

4. Open Swagger UI: http://localhost:8000/docs

Endpoints
- `GET /` — API information and metadata
- `GET /health` — Health check
 - `POST /validate` — Validate personal data (JSON body)

Example Request

```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"juan","last_name":"perez","email":"juan@example.com","phone":"1234567","age":30}'
```

Example Response

```json
{
  "valid": true,
  "message": "Data validated successfully",
  "data": {
    "first_name": "Juan",
    "last_name": "Perez",
    "email": "juan@example.com",
    "phone": "1234567",
    "age": 30
  },
  "timestamp": "2025-12-11T22:56:11.327998"
}
```

Testing

Run the automated test suite:

```bash
python test_api.py
```

License

This project is licensed under the MIT License — see the `LICENSE` file for details.

Contributing

Contributions are welcome. Open an issue or a pull request on GitHub.

## Personal Data Validator API

This repository contains a production-ready FastAPI application (Python 3.12) that validates and normalizes personal data fields using Pydantic models and field validators. The project includes automated tests, complete documentation, and examples.

## Features

- Robust validation with Pydantic
- Automatic normalization of first and last names (capitalization)
- Email validation using a dedicated validator
- Phone validation (digits only, minimum 7 characters)
- Age validation (integer between 0 and 120)
- Auto-generated Swagger UI and ReDoc documentation
- Centralized error handling and structured logging

## Requirements

- Python 3.11 or later
- pip

## Installation

1. Clone the repository and enter the project folder:

```bash
git clone https://github.com/Pantuflito01/API_Validadora-.git
cd API_Validadora
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the application with Uvicorn:

```bash
uvicorn main:app --host localhost --port 8000
```

The API will be available at http://localhost:8000.

## API Documentation

Open the interactive API docs at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

1) `GET /` — API information and metadata

Example response (200):

```json
{
  "name": "Personal Data Validator API",
  "version": "1.0.0",
  "description": "Personal data validation REST API",
  "documentation": "http://localhost:8000/docs",
  "timestamp": "2025-12-11T22:50:31.132924"
}
```

2) `GET /health` — Health check

Example response (200):

```json
{
  "status": "healthy",
  "timestamp": "2025-12-11T22:50:31.134761"
}
```

3) `POST /validate` — Validate personal data

Request schema (JSON):

- `first_name` (string, required): minimum 2 characters
- `last_name` (string, required): minimum 2 characters
- `email` (string, required): valid email format
- `phone` (string, optional): digits only, minimum 7 digits
- `age` (integer, optional): 0-120

Example request:

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "juan",
    "last_name": "perez",
    "email": "juan.perez@example.com",
    "phone": "1234567",
    "age": 30
  }'
```

Successful response (200):

```json
{
  "valid": true,
  "message": "Data validated successfully",
  "data": {
    "first_name": "Juan",
    "last_name": "Perez",
    "email": "juan.perez@example.com",
    "phone": "1234567",
    "age": 30
  },
  "timestamp": "2025-12-11T22:50:31.141245"
}
```

Validation error example (422):

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "a",
    "last_name": "perez",
    "email": "invalid-email"
  }'
```

The server will return a 422 response with details about the failing fields.

## Testing

Run the automated test suite:

```bash
python test_api.py
```

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

## Contributing

Contributions are welcome. Please open an issue or a pull request on GitHub.


**Error response (422):**

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "first_name"],
      "msg": "Value error, Must have at least 2 characters",
      "input": "a"
    },
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
      "input": "invalid-email"
    }
  ]
}
```

---

## 🧪 Tests

### Run automated test script

```bash
python test_api.py
```

The test script runs 11 tests including:

- Root endpoint
- Health check
- Successful validation
- Validation without optional fields
- Error: First name too short
- Error: Invalid email
- Error: Phone too short
- Error: Phone not numeric
- Error: Age out of range
- Error: Missing required fields
- Name normalization

**Expected output:**
```
============================================================
PERSONAL DATA VALIDATOR TESTS
============================================================
✓ API available at http://localhost:8000
...
Passed tests: 11/11
============================================================

All tests passed successfully!
```

---

## 🧩 Project Structure

```
API_Validadora/
├── main.py                 # Main application (FastAPI)
├── app/
│   ├── __init__.py        # Package initializer
│   ├── models.py          # Pydantic models with validators
│   └── validators.py      # Custom validation helpers
├── test_api.py            # Automated test script
├── requirements.txt       # Project dependencies
└── README.md              # This file
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.104.1 | Web framework |
| `pydantic` | 2.5.0 | Data validation |
| `pydantic-extra-types` | 2.1.0 | Additional Pydantic types |
| `uvicorn[standard]` | 0.24.0 | ASGI server |
| `email-validator` | 2.1.0 | Email validation |
| `python-multipart` | 0.0.6 | multipart/form-data parsing |
| `requests` | (used in test_api.py) | HTTP client for tests |

---

## 🔍 Swagger UI (Interactive Documentation)

Open the interactive docs and try endpoints in real time:

**URL:** http://localhost:8000/docs

In Swagger UI you can:
- View all available endpoints
- Try requests live
- See generated JSON schemas
- View sample responses

---

## 📊 Implemented Validations

### First and Last Names
- ✅ Minimum 2 characters
- ✅ Automatically capitalized (first letter uppercase, rest lowercase)
- ✅ Trims unnecessary whitespace

### Email
- ✅ Valid format per RFC 5322
- ✅ Validation with `email-validator` library
- ✅ Required field

### Phone
- ✅ Digits only (0-9)
- ✅ Minimum 7 digits
- ✅ Optional (can be null)
- ✅ Trims whitespace

### Age
- ✅ Range 0-120
- ✅ Integer type
- ✅ Optional (can be null)

---

## 📝 Logging

The API automatically logs:
- Exact timestamp of each request
- Requested endpoint
- The validated user data (as permitted by your logging policy)
- Validation result
- Errors and exceptions

**Example logs:**
```
2025-12-11 22:50:31 - main - INFO - Personal Data Validator API started
2025-12-11 22:50:31 - main - INFO - POST /validate - Email: juan.perez@example.com, First: juan, Last: perez
2025-12-11 22:50:31 - main - INFO - Validation successful for: juan.perez@example.com
```

---

## 🚀 Complete Usage Example

### 1. Start the API
```bash
python -m uvicorn main:app --host localhost --port 8000
```

### 2. Make a request (from another terminal or Postman)

```bash
curl -X POST http://localhost:8000/validate \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "carlos",
    "last_name": "martinez",
    "email": "carlos.martinez@gmail.com",
    "phone": "1234567890",
    "age": 25
  }' | python -m json.tool
```

### 3. Expected response

```json
{
  "valid": true,
  "message": "Data validated successfully",
  "data": {
    "first_name": "Carlos",
    "last_name": "Martinez",
    "email": "carlos.martinez@gmail.com",
    "phone": "1234567890",
    "age": 25
  },
  "timestamp": "2025-12-11T22:50:31.141245"
}
```

---

## 🛠️ Customization

### Change port
```bash
python -m uvicorn main:app --host localhost --port 9000
```

### Change host
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Development mode (auto-reload)
```bash
python -m uvicorn main:app --host localhost --port 8000 --reload
```

---

## 📈 Scalability

This project is designed to be scalable:

- ✅ Modular structure with separation of concerns
- ✅ Reusable validators
- ✅ Global error handlers
- ✅ Centralized logging
- ✅ Easy to add new endpoints
- ✅ Compatible with databases (SQLAlchemy, etc.)
- ✅ Compatible with authentication (JWT, OAuth2, etc.)

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Fix:** Install dependencies: `pip install -r requirements.txt`

### Error: "Address already in use: ('localhost', 8000)"
**Fix:** Port 8000 is already in use. Use another port:
```bash
python -m uvicorn main:app --host localhost --port 8001
```

### Validations not working
**Fix:** Ensure you are sending JSON with the header `Content-Type: application/json`

---

## 📜 License

Open-source for educational and professional use.

---

## 👨‍💻 Author

Personal Data Validator API project - December 2025

---

## 📞 Support

If you have issues or questions, check:
1. Interactive docs: http://localhost:8000/docs
2. This README
3. Comments in the source code

---

## ✨ Implementation Checklist

- ✅ Functional REST API with FastAPI
  - ✅ Endpoints: POST /validate, GET /, GET /health
- ✅ Validation using Pydantic
- ✅ Name normalization
- ✅ Email validation
- ✅ Phone validation (numeric, 7+ digits)
- ✅ Age validation (0-120)
  - ✅ Required fields: first_name, last_name, email
  - ✅ Optional fields: phone, age
- ✅ Global error handling
- ✅ Request logging
- ✅ Auto-generated Swagger UI
- ✅ Modular, clean code
- ✅ Complete requirements.txt
- ✅ Automated test script (11/11 ✅)
- ✅ Runs on localhost:8000 with uvicorn
- ✅ Production-ready

The API is ready to use! 🎉
