import streamlit as st
import uuid
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payment.payment import Payment
from payment.payment_strategy import CreditCardStrategy, PayPalStrategy, BankTransferStrategy
from payment.db_connection import get_central_account, initialize_dummy_accounts

# Initialize MongoDB with dummy accounts
initialize_dummy_accounts()

# Initialize session state
if 'payment_method' not in st.session_state:
    st.session_state.payment_method = None

# Get booking details from session state
if 'booking_id' not in st.session_state:
    st.error("No booking found. Please go back to the booking page.")
    if st.button("Back to Booking"):
        st.switch_page("pages/BookingPage.py")
    st.stop()

if 'total_price' not in st.session_state:
    st.error("No total price found. Please go back to the booking page.")
    if st.button("Back to Booking"):
        st.switch_page("pages/BookingPage.py")
    st.stop()

# Set booking_id and amount from session state
st.session_state.booking_id = st.session_state.booking_id
st.session_state.amount = st.session_state.total_price

def show_payment_selection():
    st.title("Payment System")
    st.header("Select Payment Method")
    
    # Show central account balance
    central_account = get_central_account()
    st.sidebar.title("Central Account")
    st.sidebar.write(f"Balance: ${central_account['balance']:.2f}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Credit Card", use_container_width=True):
            st.session_state.payment_method = "Credit Card"
    with col2:
        if st.button("PayPal", use_container_width=True):
            st.session_state.payment_method = "PayPal"
    with col3:
        if st.button("Bank Transfer", use_container_width=True):
            st.session_state.payment_method = "Bank Transfer"

def show_credit_card():
    st.title("Credit Card Payment")
    st.button("← Back to Payment Methods", on_click=lambda: setattr(st.session_state, 'payment_method', None))
    
    st.header("Payment Details")
    booking_id = st.text_input("Booking ID", value=st.session_state.booking_id)
    amount = st.number_input("Amount ($)", min_value=0.01, value=st.session_state.amount, step=0.01)
    
    st.header("Card Details")
    st.info("Test Card: 1234567890123456, John Doe, 12/25, 123")
    st.info("Test Card: 9876543210987654, Jane Smith, 06/24, 456")
    
    card_number = st.text_input("Card Number")
    name_on_card = st.text_input("Name on Card")
    expiry_date = st.text_input("Expiry Date (MM/YY)")
    cvv = st.text_input("CVV", type="password")
    
    if st.button("Process Payment", use_container_width=True):
        if all([card_number, name_on_card, expiry_date, cvv]):
            strategy = CreditCardStrategy(card_number, name_on_card, expiry_date, cvv)
            payment = Payment(str(uuid.uuid4()), booking_id, amount, strategy)
            if payment.process_payment():
                st.success("Payment processed successfully!")
                st.write(payment.generate_receipt())
                central_account = get_central_account()
                st.write(f"Central Account Balance: ${central_account['balance']:.2f}")
                if st.button("Refund Payment"):
                    if payment.refund():
                        st.success("Refund processed successfully!")
                        st.write(payment.generate_receipt())
                        central_account = get_central_account()
                        st.write(f"Central Account Balance: ${central_account['balance']:.2f}")
            else:
                st.error("Payment failed. Please check your credentials and balance.")
        else:
            st.error("Please fill in all credit card details")

def show_paypal():
    st.title("PayPal Payment")
    st.button("← Back to Payment Methods", on_click=lambda: setattr(st.session_state, 'payment_method', None))
    
    st.header("Payment Details")
    booking_id = st.text_input("Booking ID", value=st.session_state.booking_id)
    amount = st.number_input("Amount ($)", min_value=0.01, value=st.session_state.amount, step=0.01)
    
    st.header("PayPal Details")
    st.info("Test Account: user1@example.com, password123")
    st.info("Test Account: user2@example.com, password456")
    
    email = st.text_input("PayPal Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Process Payment", use_container_width=True):
        if all([email, password]):
            strategy = PayPalStrategy(email, password)
            payment = Payment(str(uuid.uuid4()), booking_id, amount, strategy)
            if payment.process_payment():
                st.success("Payment processed successfully!")
                st.write(payment.generate_receipt())
                central_account = get_central_account()
                st.write(f"Central Account Balance: ${central_account['balance']:.2f}")
                if st.button("Refund Payment"):
                    if payment.refund():
                        st.success("Refund processed successfully!")
                        st.write(payment.generate_receipt())
                        central_account = get_central_account()
                        st.write(f"Central Account Balance: ${central_account['balance']:.2f}")
            else:
                st.error("Payment failed. Please check your credentials and balance.")
        else:
            st.error("Please fill in all PayPal details")

def show_bank_transfer():
    st.title("Bank Transfer Payment")
    st.button("← Back to Payment Methods", on_click=lambda: setattr(st.session_state, 'payment_method', None))
    
    st.header("Payment Details")
    booking_id = st.text_input("Booking ID", value=st.session_state.booking_id)
    amount = st.number_input("Amount ($)", min_value=0.01, value=st.session_state.amount, step=0.01)
    
    st.header("Bank Details")
    st.info("Test Account: 111122223333, BANK1")
    st.info("Test Account: 444455556666, BANK2")
    
    account_number = st.text_input("Account Number")
    bank_code = st.text_input("Bank Code")
    
    if st.button("Process Payment", use_container_width=True):
        if all([account_number, bank_code]):
            strategy = BankTransferStrategy(account_number, bank_code)
            payment = Payment(str(uuid.uuid4()), booking_id, amount, strategy)
            if payment.process_payment():
                st.success("Payment processed successfully!")
                st.write(payment.generate_receipt())
                central_account = get_central_account()
                st.write(f"Central Account Balance: ${central_account['balance']:.2f}")
                if st.button("Refund Payment"):
                    if payment.refund():
                        st.success("Refund processed successfully!")
                        st.write(payment.generate_receipt())
                        central_account = get_central_account()
                        st.write(f"Central Account Balance: ${central_account['balance']:.2f}")
            else:
                st.error("Payment failed. Please check your credentials and balance.")
        else:
            st.error("Please fill in all bank transfer details")

# Main app logic
if st.session_state.payment_method is None:
    show_payment_selection()
elif st.session_state.payment_method == "Credit Card":
    show_credit_card()
elif st.session_state.payment_method == "PayPal":
    show_paypal()
elif st.session_state.payment_method == "Bank Transfer":
    show_bank_transfer() 