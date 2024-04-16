from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.bills import schemas, crud
from app.bills.validators import validate_create_bill
from app.db.database import SessionLocal

router = APIRouter(
    prefix='/bills',
    tags=['bills'],
    responses={404: {'description': 'Not found'}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('', response_model=schemas.Bill)
def create_bill(bill: schemas.BillCreateWithSubBills, db: Session = Depends(get_db)):
    validate_create_bill(bill, db)
    return crud.create_bill_with_sub_bills(db, bill)


@router.get('', response_model=list[schemas.Bill])
def get_bills(skip: int = 0, limit: int = 100, reference: str | None = None, total_from: Decimal | None = None,
              total_to: Decimal | None = None, db: Session = Depends(get_db)):
    return crud.get_bills(db, skip, limit, reference, total_from, total_to)
