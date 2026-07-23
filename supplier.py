from typing import Optional
import re

from pydantic import EmailStr, field_validator, ConfigDict
from sqlmodel import SQLModel, Field


class Supplier(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True, unique=True)
    contact_person: str
    email: EmailStr = Field(index=True, unique=True)
    phone: str
    is_active: bool = True


class SupplierCreate(SQLModel):
    name: str
    contact_person: str
    email: EmailStr
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        pattern = r"^(07\d{8}|\+2547\d{8})$"

        if not re.match(pattern, value):
            raise ValueError(
                "Phone number must be 07XXXXXXXX or +2547XXXXXXXX"
            )

        return value


class SupplierUpdate(SQLModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    contact_person: str
    email: EmailStr
    phone: str
    is_active: bool