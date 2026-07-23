from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
import re


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    brand: str
    category: str
    price: float
    stock: int
    warranty_months: int
    sku: str
    supplier_id: Optional[int] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value[0].isupper():
            raise ValueError("Product name must start with a capital letter.")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        categories = [
            "Laptops",
            "Monitors",
            "Storage",
            "Processors",
            "Memory",
            "Keyboards",
            "Mice",
            "Accessories",
        ]

        if value not in categories:
            raise ValueError("Invalid category.")

        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than zero.")
        return value

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, value):
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        return value

    @field_validator("warranty_months")
    @classmethod
    def validate_warranty(cls, value):
        if value < 0 or value > 36:
            raise ValueError("Warranty must be between 0 and 36 months.")
        return value

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value):
        pattern = r"^[A-Z]{3,4}-[A-Z]{2,4}-[0-9]{4}$"

        if not re.match(pattern, value):
            raise ValueError("Invalid SKU format.")

        return value


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    warranty_months: Optional[int] = None
    sku: Optional[str] = None
    supplier_id: Optional[int] = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    brand: str
    category: str
    price: float
    stock: int
    warranty_months: int
    sku: str
    supplier_id: Optional[int]
class BulkPriceUpdate(BaseModel):
    product_ids: list[int]
    percentage: float
class StockAdjustment(BaseModel):
    quantity: int