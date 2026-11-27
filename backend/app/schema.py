import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Literal
class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=4, max_length=100)
    email: EmailStr = Field(..., min_length=4, max_length=20)
    shop_name:str = Field(...,max_length=100)
    password: str = Field(...,min_length=8, max_length=100)
    confirm_password: str= Field(...,min_length=8, max_length=100)

    @field_validator("full_name","shop_name")
    @classmethod
    def validate_non_blank(cls, v:str) -> str:
        cleaned=v.strip()
        if not cleaned:
            raise ValueError("Field cannot be blank")
        return cleaned

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v:str) -> str:
        return v.strip().lower()

    @model_validator(mode="after")
    def password_match(self) -> "RegisterRequest":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
class RegisterResponse(BaseModel):
    user_id: uuid.UUID
    shop_id: uuid.UUID
    full_name:str
    email:EmailStr
    created_at: datetime
    message: str = "Account registering successful"


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=4, max_length=20)
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    message: str = "Login successful"


class SessionResponse(BaseModel):
    user_id: uuid.UUID
    shop_id: uuid.UUID
    email: str
    expires_at: datetime

class StockAdjustmentRequest(BaseModel):
    adjustment_type: Literal["increase","decrease","set"]
    quantity: int = Field(..., ge=0)
    reason: str = Field(...,min_length=1,max_length=255)

    @field_validator("reason")
    @classmethod
    def validate_reason_not_blank(cls, v:str) -> str:
            cleaned=v.strip()
            if not cleaned:
                raise ValueError("Field cannot be blank")
            return cleaned
    @model_validator(mode="after")
    def validate_positve(self) -> "StockAdjustmentRequest":
        if self.adjustment in ("increase","decrease") and self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0 for increase or decrease")
        return self

class InventoryItemResponse(BaseModel):
    product_id: uuid.UUID
    shop_id: uuid.UUID
    stock_quantity: int
    updated_at: datetime

class InventoryAdjustmentRequest(BaseModel):
    adjustment_id:uuid.UUID
    product_id: uuid.UUID
    shop_id: uuid.UUID
user_id: uuid.UUID
adjustment_type: Literal["increase", "decrease", "set"]
previous_quantity: int
quantity_change: int
new_quantity: int
reason: str
created_at: datetime
