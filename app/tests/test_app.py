from decimal import Decimal

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.bills import schemas, crud
from app.bills.api import get_db
from app.bills.validators import validate_create_bill
from app.db.database import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

fake = Faker()


@pytest.fixture(autouse=True)
def setup():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    for reference_prefix in ['ref', 'inv', 'bill']:
        sub_bills = [
            schemas.SubBillCreate(
                amount=Decimal(fake.random_number(digits=2)),
                reference=f'{reference_prefix}_{reference_suffix}'
            ) for reference_suffix in range(1, 3)
        ]
        total_amount = sum(sub.amount for sub in sub_bills)
        bill_data = schemas.BillCreateWithSubBills(
            total=total_amount,
            sub_bills=sub_bills
        )
        validated_bill = validate_create_bill(bill_data, db)
        crud.create_bill_with_sub_bills(db, validated_bill)
        db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_bills():
    response = client.get('/bills/')
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_bills_with_reference():
    response = client.get('/bills/?reference=ref')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_post_bills():
    response = client.post('/bills/', json={
        'total': 100,
        'sub_bills': [
            {'amount': 50, 'reference': 'invoice-1'},
            {'amount': 50, 'reference': 'invoice-2'}
        ]
    })

    assert response.status_code == 200

    assert len(crud.get_bills(TestingSessionLocal())) == 4
