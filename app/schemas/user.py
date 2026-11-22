from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)
    is_admin: bool = False

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes (bcrypt limit)")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        return value


class UserResponse(UserBase):
    id: int
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
