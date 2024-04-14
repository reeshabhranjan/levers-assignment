from sqlalchemy.orm import Session

from . import models, schemas


def create_bill(db: Session, bill: schemas.BillCreate):
    db_bill = models.Bill(total=bill.total)
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


def create_sub_bill(db: Session, sub_bill: schemas.SubBillCreate, bill_id: int):
    db_sub_bill = models.SubBill(**sub_bill.dict(), bill_id=bill_id)
    db.add(db_sub_bill)
    db.commit()
    db.refresh(db_sub_bill)
    return db_sub_bill


def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()
