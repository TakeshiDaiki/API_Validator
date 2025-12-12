
"""
Test script for the Personal Data Validator API.
Performs example requests against the API endpoints.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Colores para la salida
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_result(title: str, response: requests.Response):
    """Print formatted request result."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Status Code: {response.status_code}")
    print("Response:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(str(e))
        print(response.text)


def test_endpoint_root():
    """Test the root endpoint."""
    print(f"\n{YELLOW}Testing root endpoint...{RESET}")
    response = requests.get(f"{BASE_URL}/")
    print_result("GET /", response)
    return response.status_code == 200


def test_health_check():
    """Test the health check endpoint."""
    print(f"\n{YELLOW}Testing health check...{RESET}")
    response = requests.get(f"{BASE_URL}/health")
    print_result("GET /health", response)
    return response.status_code == 200


def test_successful_validation():
    """Test a successful validation."""
    print(f"\n{YELLOW}Testing successful validation...{RESET}")

    payload = {
        "first_name": "juan",
        "last_name": "perez",
        "email": "juan.perez@example.com",
        "phone": "1234567",
        "age": 30
    }

    response = requests.post(
        f"{BASE_URL}/validate",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print_result("POST /validate - Successful Validation", response)
    return response.status_code == 200


def test_validation_without_optional_fields():
    """Test validation without optional fields."""
    print(f"\n{YELLOW}Testing validation without phone and age...{RESET}")

    payload = {
        "first_name": "maria",
        "last_name": "garcia",
        "email": "maria.garcia@example.com"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Without phone and age", response)
    return response.status_code == 200


def test_name_too_short():
    """Test error: name too short."""
    print(f"\n{YELLOW}Testing error: name too short...{RESET}")

    payload = {
        "first_name": "a",
        "last_name": "perez",
        "email": "test@example.com"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Name too short", response)
    return response.status_code == 422


def test_invalid_email():
    """Test error: invalid email."""
    print(f"\n{YELLOW}Testing error: invalid email...{RESET}")

    payload = {
        "first_name": "juan",
        "last_name": "perez",
        "email": "invalid-email"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Invalid email", response)
    return response.status_code == 422


def test_phone_too_short():
    """Test error: phone too short."""
    print(f"\n{YELLOW}Testing error: phone too short...{RESET}")

    payload = {
        "first_name": "juan",
        "last_name": "perez",
        "email": "juan@example.com",
        "phone": "123"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Phone too short", response)
    return response.status_code == 422


def test_phone_not_numeric():
    """Test error: phone not numeric."""
    print(f"\n{YELLOW}Testing error: phone not numeric...{RESET}")

    payload = {
        "first_name": "juan",
        "last_name": "perez",
        "email": "juan@example.com",
        "phone": "123-456-7890"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Phone not numeric", response)
    return response.status_code == 422


def test_age_out_of_range():
    """Test error: age out of range."""
    print(f"\n{YELLOW}Testing error: age out of range...{RESET}")

    payload = {
        "first_name": "juan",
        "last_name": "perez",
        "email": "juan@example.com",
        "age": 150
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Age out of range", response)
    return response.status_code == 422


def test_missing_required_fields():
    """Test error: missing required fields."""
    print(f"\n{YELLOW}Testing error: missing required fields...{RESET}")

    payload = {
        "first_name": "juan"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Missing required fields", response)
    return response.status_code == 422


def test_name_normalization():
    """Test name normalization."""
    print(f"\n{YELLOW}Testing name normalization...{RESET}")

    payload = {
        "first_name": "jUaN",
        "last_name": "pEReZ",
        "email": "test@example.com"
    }

    response = requests.post(f"{BASE_URL}/validate", json=payload)
    print_result("POST /validate - Name normalization", response)

    if response.status_code == 200:
        data = response.json()
        first = data.get('data', {}).get('first_name')
        last = data.get('data', {}).get('last_name')

        if first == "Juan" and last == "Perez":
            print(f"{GREEN}✓ Normalization correct: {first} {last}{RESET}")
            return True
        else:
            print(f"{RED}✗ Normalization failed: {first} {last}{RESET}")
            return False

    return False


def main():
    """Run all tests."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}PERSONAL DATA VALIDATOR TESTS{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    # Wait for the API to be available
    import time
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            print(f"{GREEN}✓ API available at {BASE_URL}{RESET}")
            break
        except requests.exceptions.ConnectionError:
            if attempt < max_attempts - 1:
                print(f"{YELLOW}Waiting for API to be available... ({attempt + 1}/{max_attempts}){RESET}")
                time.sleep(1)
            else:
                print(f"{RED}✗ Could not connect to the API{RESET}")
                return
    
    # Tests list
    tests = [
        ("Root endpoint", test_endpoint_root),
        ("Health check", test_health_check),
        ("Successful validation", test_successful_validation),
        ("Validation without optional fields", test_validation_without_optional_fields),
        ("Error: Name too short", test_name_too_short),
        ("Error: Invalid email", test_invalid_email),
        ("Error: Phone too short", test_phone_too_short),
        ("Error: Phone not numeric", test_phone_not_numeric),
        ("Error: Age out of range", test_age_out_of_range),
        ("Error: Missing required fields", test_missing_required_fields),
        ("Name normalization", test_name_normalization),
    ]
    
    resultados = []
    for nombre, test in tests:
        try:
            resultado = test()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"{RED}✗ Error in test {nombre}: {str(e)}{RESET}")
            resultados.append((nombre, False))
    
    # Resumen de resultados
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST RESULTS SUMMARY{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    passed = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)

    for nombre, resultado in resultados:
        symbol = f"{GREEN}✓{RESET}" if resultado else f"{RED}✗{RESET}"
        print(f"{symbol} {nombre}")

    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"Passed tests: {GREEN}{passed}/{total}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    if passed == total:
        print(f"\n{GREEN}All tests passed successfully!{RESET}")
    else:
        print(f"\n{YELLOW}Some tests failed. Check the errors above.{RESET}")


if __name__ == "__main__":
    main()
