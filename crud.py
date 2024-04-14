from typing import List

from sqlalchemy.orm import Session

import models
import schemas
from schemas import SubBillCreate


def create_bill(db: Session, bill: schemas.BillCreate):
    db_bill = models.Bill(total=bill.total)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


def create_sub_bill(db: Session, sub_bill: schemas.SubBillCreate, bill_id: int):
    db_sub_bill = models.SubBill(**sub_bill.model_dump(), bill_id=bill_id)
    db.add(db_sub_bill)
    db.commit()
    db.refresh(db_sub_bill)
    return db_sub_bill


def create_bill_with_sub_bills(db: Session, bill: schemas.BillCreateWithSubBills):
    # db_bill = create_bill(db, schemas.BillCreate(total=bill.total))
    # for sub_bill in bill.sub_bills:
    #     create_sub_bill(db, sub_bill, db_bill.id)
    # return db_bill

    bill_data = bill.dict()
    sub_bills_data: List[SubBillCreate] = bill_data.pop('sub_bills', None)
    db_bill = models.Bill(**bill_data)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)

    bill_id = db_bill.id
    if not (sub_bills_data is None):
        for sub_bill_data in sub_bills_data:
            db_sub_bill = models.SubBill(**sub_bill_data, bill_id=bill_id)
            db.add(db_sub_bill)
            db.commit()
            db.refresh(db_sub_bill)
        return db_bill


def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()
