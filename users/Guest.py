### users/Guest.py
from users.User import User
from users.user_type import UserType

class Guest(User):
    def __init__(self, name, email, password, user_type: UserType):
        super().__init__(name, email, password, user_type)

    def book_accommodation(self):
        return f"{self.getName()} booked an accommodation."