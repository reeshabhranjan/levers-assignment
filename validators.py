from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud
import schemas


def validate_create_bill(bill: schemas.BillCreateWithSubBills, db: Session):
    references = [sub_bill.reference.lower() for sub_bill in bill.sub_bills if sub_bill.reference]

    if len(references) != 1 and len(set(references)) <= len(references):
        raise HTTPException(status_code=400, detail='Reference must be unique')

    if sum(sub_bill.amount for sub_bill in bill.sub_bills) != bill.total:
        raise HTTPException(status_code=400, detail='Sum of sub bills must be equal to total amount')

    # keeping it at the end to avoid unnecessary db queries
    if crud.sub_bills_exists(db, references):
        raise HTTPException(status_code=400, detail='One or more references already exist in the database')

    return bill
