import uuid
import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailMixin(BaseModel):
    email: EmailStr


class PasswordMixin(BaseModel):
    password: str

    @field_validator("password")
    def validate_password(cls, value: str):
        if len(value) <= 10:
            raise ValueError("Пароль должен быть больше 10 символов")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Пароль должен содержать букву")
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать цифру")
        return value


class UsernameMixin(BaseModel):
    username: str = Field(..., min_length=7)


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str

    model_config = {
        "from_attributes": True
    }


class UserRegisterIn(UsernameMixin, EmailMixin, PasswordMixin):
    pass


class UserRegisterOut(EmailMixin):
    id: uuid.UUID


class UserLoginIn(EmailMixin, PasswordMixin):
    pass


class UserLoginOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
