from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal
from validators import validate_create_bill

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/bills/', response_model=schemas.Bill)
def create_bill(bill: schemas.BillCreateWithSubBills, db: Session = Depends(get_db)):
    validate_create_bill(bill, db)
    return crud.create_bill_with_sub_bills(db, bill)


@app.get('/bills/', response_model=list[schemas.Bill])
def get_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bills(db, skip, limit)
