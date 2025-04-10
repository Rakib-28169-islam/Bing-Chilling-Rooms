### auth/user_factory.py
from users.Admin import Admin
from users.Host import Host
from users.Guest import Guest
from users.user_type import UserType

class UserFactory:
    @staticmethod
    def create_user(role, name, email, password):
        if role == UserType.ADMIN.value:
            return Admin(name, email, password, UserType.ADMIN)
        elif role == UserType.HOST.value:
            return Host(name, email, password, UserType.HOST)
        elif role == UserType.GUEST.value:
            return Guest(name, email, password, UserType.GUEST)
        else:
            raise ValueError("Invalid role")