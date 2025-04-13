from abc import ABC, abstractmethod
import smtplib
from email.message import EmailMessage

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# Concrete Observers
class EmailNotification(Observer):
    def __init__(self, email: str):
        self.email = email

    def update(self, message: str):
        print(f"Sending email to {self.email}: {message}")
        self._send_email(message)

    def _send_email(self, message: str):
        # Simulate sending an email
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'BingChilling Rooms Notification'
        msg['From'] = 'notifications@bingchilling.com'
        msg['To'] = self.email

        try:
            with smtplib.SMTP('localhost', 1025) as s:
                s.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")


class SMSNotification(Observer):
    def __init__(self, phone: str):
        self.phone = phone

    def update(self, message: str):
        print(f"Sending SMS to {self.phone}: {message}")


class PushNotification(Observer):
    def __init__(self, device_token: str):
        self.device_token = device_token

    def update(self, message: str):
        print(f"Sending push notification to device {self.device_token}: {message}")
