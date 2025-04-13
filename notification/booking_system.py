from datetime import datetime

 

class BookingSystem:
    def __init__(self):
        self._observers = []
        self.bookings = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

    def create_booking(self, guest, host, property_id, start_date, end_date):
        booking_id = len(self.bookings) + 1
        booking = {
            'id': booking_id,
            'guest': guest,
            'host': host,
            'property_id': property_id,
            'start_date': start_date,
            'end_date': end_date,
            'status': 'pending',
            'created_at': datetime.now()
        }
        self.bookings.append(booking)

        # Notify Guest and Host about the booking
        self.attach(guest)
        self.attach(host)
        self.notify(f"Booking #{booking_id} created for property {property_id}. Status: Pending payment.")

        return booking_id

    def process_payment(self, booking_id, payment_method, amount):
        booking = next((b for b in self.bookings if b['id'] == booking_id), None)
        if not booking:
            raise ValueError("Booking not found")

        # Simulate payment processing
        payment_result = self._process_payment(amount, payment_method)
        if payment_result['success']:
            booking['status'] = 'confirmed'
            booking['payment_id'] = payment_result['payment_id']
            booking['paid_at'] = datetime.now()

            # Notify Guest and Host about successful payment
            self.notify(f"Payment successful for Booking #{booking_id}. Your booking is now confirmed.")

            host_notification = EmailNotification("host@example.com")
            host_notification.update(f"New booking #{booking_id} for your property by guest {booking['guest'].getName()}")

            return True
        else:
            booking['status'] = 'payment_failed'
            self.notify(f"Payment failed for Booking #{booking_id}. Please try another payment method.")
            return False

    def _process_payment(self, amount, payment_method):
        # Simulate payment processing logic
        print(f"Processing payment of ${amount} via {payment_method}")
        return {
            'success': True,
            'payment_id': f"pay_{datetime.now().timestamp()}",
            'message': 'Payment processed successfully'
        }
