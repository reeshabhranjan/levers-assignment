from typing import List

from sqlalchemy.orm import Session

import models
import schemas
from schemas import SubBillCreate


def create_bill_with_sub_bills(db: Session, bill: schemas.BillCreateWithSubBills):
    bill_data = bill.dict()
    sub_bills_data: List[SubBillCreate] = bill_data.pop('sub_bills', None)
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


def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()


def sub_bills_exists(db: Session, references: List[str]):
    return db.query(models.SubBill).filter(models.SubBill.reference.in_(references)).all()
