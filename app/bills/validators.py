from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.bills import crud, schemas


def validate_create_bill(bill: schemas.BillCreateWithSubBills, db: Session):
    references = [sub_bill.reference.lower() for sub_bill in bill.sub_bills if sub_bill.reference]
    print(references)

    if len(references) != 1 and len(set(references)) < len(references):
        raise HTTPException(status_code=400, detail='Reference must be unique')

    sum_bill_amount_total = sum(sub_bill.amount for sub_bill in bill.sub_bills)
    if sum_bill_amount_total > bill.total:
        raise HTTPException(status_code=400, detail=f'Sum of the sub_bill is greater than the total amount of the '
                                                    'bill! (total: {bill.total}, sum: {sum_bill_amount_total})')

    if sum_bill_amount_total < bill.total:
        raise HTTPException(status_code=400, detail=f'Sum of the sub_bill is less than the total amount of the bill! ('
                                                    'total: {bill.total}, sum: {sum_bill_amount_total})')

    # keeping it at the end to avoid unnecessary db queries
    if crud.sub_bills_exists(db, references):
        raise HTTPException(status_code=400, detail='One or more references already exist in the database')

    return bill
