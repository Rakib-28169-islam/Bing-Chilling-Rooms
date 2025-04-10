### users/Host.py
from users.User import User
from users.user_type import UserType

class Host(User):
    def __init__(self, name, email, password, user_type: UserType):
        super().__init__(name, email, password, user_type)

    def create_listing(self):
        return f"{self.getName()} created a new listing."

    def manage_bookings(self):
        return f"{self.getName()} is managing bookings."

    def view_earnings(self):
        return f"{self.getName()} is viewing earnings."