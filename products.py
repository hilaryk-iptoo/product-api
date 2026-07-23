
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.database import get_session
from app.models.product import Product
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
    BulkPriceUpdate,
    StockAdjustment,
)
from app.utils.logger import logger

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# CREATE PRODUCT
@router.post("/", response_model=ProductRead, status_code=201)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
):
    existing = session.exec(
        select(Product).where(Product.sku == product.sku)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product with this SKU already exists.",
        )

    db_product = Product(**product.model_dump())

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    logger.info(f"Product created: {db_product.name}")

    return db_product


# GET ALL PRODUCTS
@router.get("/", response_model=list[ProductRead])
def get_products(
    session: Session = Depends(get_session),
):
    return session.exec(select(Product)).all()


# SEARCH PRODUCTS
@router.get("/search", response_model=list[ProductRead])
def search_products(
    keyword: str,
    session: Session = Depends(get_session),
):
    products = session.exec(select(Product)).all()

    keyword = keyword.lower()

    results = []

    for product in products:
        if (
            keyword in product.name.lower()
            or keyword in product.brand.lower()
            or keyword in product.category.lower()
        ):
            results.append(product)

    return results


# GET PRODUCT BY ID
@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    return product


# UPDATE PRODUCT
@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    update_data = product_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    product.updated_at = datetime.utcnow()

    session.add(product)
    session.commit()
    session.refresh(product)

    logger.info(f"Product updated: {product.name}")

    return product


# DELETE PRODUCT
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    session.delete(product)
    session.commit()

    logger.info(f"Product deleted: {product.name}")

    return {
        "message": "Product deleted successfully."
    }


# BULK PRICE UPDATE
@router.patch("/bulk-update")
def bulk_price_update(
    data: BulkPriceUpdate,
    session: Session = Depends(get_session),
):
    updated = 0

    for product_id in data.product_ids:
        product = session.get(Product, product_id)

        if product:
            product.price = round(
                product.price * (1 + data.percentage / 100),
                2,
            )

            product.updated_at = datetime.utcnow()

            session.add(product)

            updated += 1

    session.commit()

    return {
        "message": f"{updated} product(s) updated successfully."
    }


# STOCK ADJUSTMENT
@router.patch("/{product_id}/stock")
def adjust_stock(
    product_id: int,
    stock: StockAdjustment,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    new_stock = product.stock + stock.quantity

    if new_stock < 0:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock.",
        )

    product.stock = new_stock
    product.updated_at = datetime.utcnow()

    session.add(product)
    session.commit()
    session.refresh(product)

    logger.info(f"Stock adjusted for product {product.id}")

    return {
        "message": "Stock updated successfully.",
        "new_stock": product.stock,
    }