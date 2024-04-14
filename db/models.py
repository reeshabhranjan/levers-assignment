from sqlalchemy import Column, Numeric, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)  # do we need index=True if it's primary key?
    total = Column(Numeric(10, 2), nullable=False)


class SubBill(Base):
    __tablename__ = "sub_bills"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    reference = Column(String(), nullable=True, default=None, unique=True)
    bill_id = Column(Integer, ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="sub_bills")
