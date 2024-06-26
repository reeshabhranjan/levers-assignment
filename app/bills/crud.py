from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session

from app.bills import schemas
from app.db import models


def create_bill_with_sub_bills(db: Session, bill: schemas.BillCreateWithSubBills):
    bill_data = bill.model_dump()
    sub_bills_data: List[schemas.SubBillCreate] = bill_data.pop('sub_bills', None)
    db_bill = models.Bill(**bill_data)
    db.add(db_bill)
    db.commit()

    bill_id = db_bill.id
    if not (sub_bills_data is None):
        for sub_bill_data in sub_bills_data:
            if sub_bill_data['reference']:
                sub_bill_data['reference'] = sub_bill_data['reference'].lower()
            db_sub_bill = models.SubBill(**sub_bill_data, bill_id=bill_id)
            db.add(db_sub_bill)
        db.commit()
    db.refresh(db_bill)
    return db_bill


def get_bills(db: Session, skip: int = 0, limit: int = 100, reference: str | None = None,
              total_from: Decimal | None = None, total_to: Decimal | None = None):
    print(reference)
    query = db.query(models.Bill)
    if reference is not None:
        query = query.filter(models.Bill.sub_bills.any(models.SubBill.reference.contains(reference.lower())))
    if total_from is not None:
        query = query.filter(models.Bill.total >= total_from)
    if total_to is not None:
        print(f'total_to: {total_to} ({type(total_to)})')
        query = query.filter(models.Bill.total <= total_to)
    query = query.offset(skip).limit(limit).all()
    return query


def sub_bills_exists(db: Session, references: List[str]):
    return db.query(models.SubBill).filter(models.SubBill.reference.in_(references)).all()
