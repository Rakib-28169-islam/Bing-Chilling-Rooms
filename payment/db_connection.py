from pymongo import MongoClient
from typing import Dict, Any
import os
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is not set")

DB_NAME = "project"

def get_db():
    """Get MongoDB database connection"""
    try:
        print(f"Connecting to MongoDB using URI: {MONGODB_URI[:20]}...")  # Only show first 20 chars for security
        client = MongoClient(MONGODB_URI)
        # Test the connection
        client.admin.command('ping')
        db = client[DB_NAME]
        print(f"Successfully connected to database: {DB_NAME}")
        return db
    except Exception as e:
        error_msg = f"Failed to connect to MongoDB: {str(e)}"
        print(error_msg)
        raise ConnectionError(error_msg)

def initialize_dummy_accounts():
    """Initialize dummy accounts in MongoDB if they don't exist"""
    try:
        print("Attempting to connect to MongoDB...")
        db = get_db()
        print("Successfully connected to MongoDB")
        
        # Check if central account exists, create if not
        if db.central_account.count_documents({}) == 0:
            print("Creating central account...")
            db.central_account.insert_one({
                "account_number": "1234567890",
                "bank_code": "CENBANK",
                "email": "central@payment.com",
                "balance": 0.0
            })
            print("Central account created successfully")
        else:
            print("Central account already exists")
        
        # Check if credit card accounts exist, create if not
        if db.credit_cards.count_documents({}) == 0:
            print("Creating credit card accounts...")
            credit_cards = [
                {
                    "card_number": "1234567890123456",
                    "name": "John Doe",
                    "expiry": "12/25",
                    "cvv": "123",
                    "balance": 1000.0
                },
                {
                    "card_number": "9876543210987654",
                    "name": "Jane Smith",
                    "expiry": "06/24",
                    "cvv": "456",
                    "balance": 2000.0
                }
            ]
            db.credit_cards.insert_many(credit_cards)
            print("Credit card accounts created successfully")
        else:
            print("Credit card accounts already exist")
        
        # Check if PayPal accounts exist, create if not
        if db.paypal_accounts.count_documents({}) == 0:
            print("Creating PayPal accounts...")
            paypal_accounts = [
                {
                    "email": "user1@example.com",
                    "password": "password123",
                    "balance": 1500.0
                },
                {
                    "email": "user2@example.com",
                    "password": "password456",
                    "balance": 2500.0
                }
            ]
            db.paypal_accounts.insert_many(paypal_accounts)
            print("PayPal accounts created successfully")
        else:
            print("PayPal accounts already exist")
        
        # Check if bank accounts exist, create if not
        if db.bank_accounts.count_documents({}) == 0:
            print("Creating bank accounts...")
            bank_accounts = [
                {
                    "account_number": "111122223333",
                    "bank_code": "BANK1",
                    "balance": 3000.0
                },
                {
                    "account_number": "444455556666",
                    "bank_code": "BANK2",
                    "balance": 4000.0
                }
            ]
            db.bank_accounts.insert_many(bank_accounts)
            print("Bank accounts created successfully")
        else:
            print("Bank accounts already exist")
        
        print("Database initialization completed")
        return True
    except Exception as e:
        print(f"Error initializing dummy accounts: {str(e)}")
        return False

def get_central_account() -> Dict[str, Any]:
    """Get the central account details"""
    try:
        db = get_db()
        return db.central_account.find_one()
    except Exception as e:
        print(f"Error getting central account: {str(e)}")
        return None

def update_central_account_balance(amount: float) -> bool:
    """Update the central account balance"""
    try:
        db = get_db()
        result = db.central_account.update_one(
            {},
            {"$inc": {"balance": amount}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating central account balance: {str(e)}")
        return False

def create_payment_record(payment_id: str, booking_id: str, amount: float, status: str) -> bool:
    """Create a payment record in the database"""
    try:
        db = get_db()
        db.payments.insert_one({
            "payment_id": payment_id,
            "booking_id": booking_id,
            "amount": amount,
            "status": status,
            "timestamp": datetime.datetime.utcnow()
        })
        return True
    except Exception as e:
        print(f"Error creating payment record: {str(e)}")
        return False

def update_payment_status(payment_id: str, status: str) -> bool:
    """Update payment status in the database"""
    try:
        db = get_db()
        result = db.payments.update_one(
            {"payment_id": payment_id},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating payment status: {str(e)}")
        return False