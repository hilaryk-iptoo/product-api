from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.database import get_session
from app.models.supplier import (
    Supplier,
    SupplierCreate,
    SupplierUpdate,
    SupplierRead,
)

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


# Create Supplier
@router.post("/", response_model=SupplierRead, status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    session: Session = Depends(get_session)
):

    existing = session.exec(
        select(Supplier).where(Supplier.email == supplier.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Supplier email already exists."
        )

    db_supplier = Supplier.model_validate(supplier)

    session.add(db_supplier)
    session.commit()
    session.refresh(db_supplier)

    return db_supplier


# Get All Suppliers
@router.get("/", response_model=list[SupplierRead])
def get_suppliers(
    session: Session = Depends(get_session)
):

    suppliers = session.exec(select(Supplier)).all()

    return suppliers


# Get Supplier By ID
@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(
    supplier_id: int,
    session: Session = Depends(get_session)
):

    supplier = session.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    return supplier


# Update Supplier
@router.put("/{supplier_id}", response_model=SupplierRead)
def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    session: Session = Depends(get_session)
):

    supplier = session.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    update_data = supplier_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(supplier, key, value)

    session.add(supplier)
    session.commit()
    session.refresh(supplier)

    return supplier


# Delete Supplier
@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: int,
    session: Session = Depends(get_session)
):

    supplier = session.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found."
        )

    session.delete(supplier)
    session.commit()

    return {
        "message": "Supplier deleted successfully."
    }