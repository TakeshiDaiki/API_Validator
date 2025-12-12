"""
Pydantic models for user data validation.
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class UsuarioValidation(BaseModel):
    """Model for personal data validation."""

    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    age: Optional[int] = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v: str) -> str:
        """Validate that names have at least 2 characters and normalize."""
        if not v or len(v.strip()) < 2:
            raise ValueError('Must have at least 2 characters')
        return v.strip().capitalize()

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone contains only digits and has minimum length 7."""
        if v is None:
            return v

        v = v.strip()

        if not v.isdigit():
            raise ValueError('Phone must contain only digits')

        if len(v) < 7:
            raise ValueError('Phone must have at least 7 digits')

        return v

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: Optional[int]) -> Optional[int]:
        """Validate age is between 0 and 120."""
        if v is None:
            return v

        if v < 0 or v > 120:
            raise ValueError('Age must be between 0 and 120')

        return v

    class Config:
        """Model configuration and example."""
        json_schema_extra = {
            "example": {
                "first_name": "juan",
                "last_name": "perez",
                "email": "juan.perez@example.com",
                "phone": "1234567",
                "age": 30
            }
        }
