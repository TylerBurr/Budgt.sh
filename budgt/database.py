
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
import datetime
import enum

DATABASE_URL = "sqlite:///budgt.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TransactionType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"

class AccountType(enum.Enum):
    CASH = "Cash"
    BANK_ACCOUNT = "Bank Account"
    CREDIT_CARD = "Credit Card"
    SAVINGS = "Savings"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    account_type = Column(Enum(AccountType))
    starting_balance = Column(Float, default=0.0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String, index=True)
    amount = Column(Float)
    transaction_type = Column(Enum(TransactionType))
    account_id = Column(Integer)
    category = Column(String)
    # For transfers: reference to the paired transaction in the other account
    transfer_pair_id = Column(Integer, nullable=True)

# Keep old Expense class for backward compatibility
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String, index=True)
    amount = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

