from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SubBillBase(BaseModel):
    amount: Decimal
    reference: str | None = None


class SubBillCreate(SubBillBase):
    pass


class SubBill(SubBillBase):
    id: int
    bill_id: int

    model_config = ConfigDict(from_attributes=True)


class BillBase(BaseModel):
    total: Decimal


class BillCreate(BillBase):
    pass


class BillCreateWithSubBills(BillCreate):
    sub_bills: list[SubBillCreate]


class Bill(BillBase):
    id: int
    sub_bills: list[SubBill] = []

    model_config = ConfigDict(from_attributes=True)
