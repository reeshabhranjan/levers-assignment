from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SubBillBase(BaseModel):
    amount: Decimal = Field(gt=0)
    reference: str | None = None


class SubBillCreate(SubBillBase):
    pass


class SubBill(SubBillBase):
    model_config = ConfigDict(from_attributes=True)


class BillBase(BaseModel):
    total: Decimal = Field(gt=0)


class BillCreate(BillBase):
    pass


class BillCreateWithSubBills(BillCreate):
    sub_bills: list[SubBillCreate]


class Bill(BillBase):
    id: int
    sub_bills: list[SubBill] = []

    model_config = ConfigDict(from_attributes=True)
