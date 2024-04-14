from decimal import Decimal

from pydantic import BaseModel


class SubBillBase(BaseModel):
    amount: Decimal
    reference: str | None = None


class SubBillCreate(SubBillBase):
    pass


class SubBill(SubBillBase):
    id: int
    bill_id: int

    class Config:
        orm_mode = True


class BillBase(BaseModel):
    total: Decimal


class BillCreate(BillBase):
    pass


class Bill(BillBase):
    id: int
    sub_bills: list[SubBill] = []

    class Config:
        orm_mode = True
