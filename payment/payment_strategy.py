from abc import ABC, abstractmethod
from db_connection import get_db, get_central_account, update_central_account_balance


# Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

    def verify_credentials(self) -> bool:
        pass

    def transfer_to_central(self, amount: float) -> bool:
        return update_central_account_balance(amount)


# Concrete Strategies
class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number, name_on_card, expiry_date, cvv):
        self.card_number = card_number
        self.name_on_card = name_on_card
        self.expiry_date = expiry_date
        self.cvv = cvv
        self._update_account_from_db()

    def _update_account_from_db(self):
        """Update account data from database"""
        db = get_db()
        self.account = db.credit_cards.find_one({
            "card_number": self.card_number,
            "name": self.name_on_card,
            "expiry": self.expiry_date,
            "cvv": self.cvv
        })

    def verify_credentials(self) -> bool:
        self._update_account_from_db()
        return self.account is not None

    def process_payment(self, amount: float) -> bool:
        if not self.verify_credentials():
            print("Invalid credit card credentials")
            return False
            
        if self.account["balance"] < amount:
            print("Insufficient funds")
            return False
            
        # Update account balance in database
        db = get_db()
        result = db.credit_cards.update_one(
            {"card_number": self.card_number},
            {"$inc": {"balance": -amount}}
        )
        
        if result.modified_count > 0:
            # Update local account data
            self._update_account_from_db()
            return self.transfer_to_central(amount)
        return False


class PayPalStrategy(PaymentStrategy):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._update_account_from_db()

    def _update_account_from_db(self):
        """Update account data from database"""
        db = get_db()
        self.account = db.paypal_accounts.find_one({
            "email": self.email,
            "password": self.password
        })

    def verify_credentials(self) -> bool:
        self._update_account_from_db()
        return self.account is not None

    def process_payment(self, amount: float) -> bool:
        if not self.verify_credentials():
            print("Invalid PayPal credentials")
            return False
            
        if self.account["balance"] < amount:
            print("Insufficient funds")
            return False
            
        # Update account balance in database
        db = get_db()
        result = db.paypal_accounts.update_one(
            {"email": self.email},
            {"$inc": {"balance": -amount}}
        )
        
        if result.modified_count > 0:
            # Update local account data
            self._update_account_from_db()
            return self.transfer_to_central(amount)
        return False


class BankTransferStrategy(PaymentStrategy):
    def __init__(self, account_number, bank_code):
        self.account_number = account_number
        self.bank_code = bank_code
        self._update_account_from_db()

    def _update_account_from_db(self):
        """Update account data from database"""
        db = get_db()
        self.account = db.bank_accounts.find_one({
            "account_number": self.account_number,
            "bank_code": self.bank_code
        })

    def verify_credentials(self) -> bool:
        self._update_account_from_db()
        return self.account is not None

    def process_payment(self, amount: float) -> bool:
        if not self.verify_credentials():
            print("Invalid bank account credentials")
            return False
            
        if self.account["balance"] < amount:
            print("Insufficient funds")
            return False
            
        # Update account balance in database
        db = get_db()
        result = db.bank_accounts.update_one(
            {"account_number": self.account_number},
            {"$inc": {"balance": -amount}}
        )
        
        if result.modified_count > 0:
            # Update local account data
            self._update_account_from_db()
            return self.transfer_to_central(amount)
        return False
