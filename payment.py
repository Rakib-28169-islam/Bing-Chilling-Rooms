from payment_strategy import PaymentStrategy
from db_connection import create_payment_record, update_payment_status, update_central_account_balance, get_db

class Payment:
    def __init__(self, payment_id: str, booking_id: str, amount: float, strategy: PaymentStrategy):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.strategy = strategy
        # Create initial payment record
        create_payment_record(payment_id, booking_id, amount, "pending")
        # Set initial status from database
        self._update_status_from_db()

    def _update_status_from_db(self):
        """Update status from database"""
        db = get_db()
        payment = db.payments.find_one({"payment_id": self.payment_id})
        if payment:
            self.status = payment["status"]
        else:
            self.status = "pending"

    def process_payment(self) -> bool:
        result = self.strategy.process_payment(self.amount)
        if result:
            update_payment_status(self.payment_id, "success")
        else:
            update_payment_status(self.payment_id, "failed")
        # Update local status from database
        self._update_status_from_db()
        return result

    def refund(self) -> bool:
        try:
            # Get current status from database
            self._update_status_from_db()
            
            # Only process refund if payment was successful
            if self.status != "success":
                print(f"Cannot refund payment {self.payment_id} with status {self.status}")
                return False
                
            # Update central account balance
            if not update_central_account_balance(-self.amount):
                print(f"Failed to update central account balance for refund {self.payment_id}")
                return False
                
            # Update payment status in database
            update_payment_status(self.payment_id, "refunded")
            # Update local status
            self._update_status_from_db()
            print(f"Successfully refunded payment {self.payment_id}")
            return True
        except Exception as e:
            print(f"Error processing refund for payment {self.payment_id}: {str(e)}")
            return False

    def generate_receipt(self) -> str:
        # Ensure status is up to date
        self._update_status_from_db()
        return f"Receipt: Payment ID {self.payment_id}, Amount ${self.amount}, Status: {self.status}"
