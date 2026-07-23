
from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True)
    description: str

    brand: str = Field(index=True)

    category: str = Field(index=True)

    price: float

    stock: int

    warranty_months: int

    sku: str = Field(index=True, unique=True)

    supplier_id: Optional[int] = Field(
        default=None,
        foreign_key="supplier.id"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)
