from enum import Enum

class UserType(Enum):
    ADMIN = "admin"
    HOST = "host"
    GUEST = "guest"
    