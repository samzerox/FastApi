from enum import Enum
from pydantic import BaseModel, EmailStr,field_validator
from sqlmodel import Relationship, SQLModel, Field, Session, select

from typing import Optional
from db import engine

class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class CustomerPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)

class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: list['Customer'] = Relationship(
        back_populates="plans", link_model=CustomerPlan
)

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("This email is already registered")
        return value

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class TransactionBase(SQLModel):
    amount: int
    description: str

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total(self):
        return sum( transaction.amount for transaction in self.transactions)