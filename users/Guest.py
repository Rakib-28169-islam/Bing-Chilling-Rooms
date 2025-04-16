# users/Guest.py
from users.User import User
from users.user_type import UserType
from property.property_service import PropertyService

class Guest(User):
    def __init__(self, name, email, password, user_type: UserType):
        super().__init__(name, email, password, user_type)

    def book_accommodation(self):
        return f"{self.getName()} booked an accommodation."
        
    def browse_listings(self, filters=None):
        """Browse property listings"""
        property_service = PropertyService.get_instance()
        properties = property_service.list_properties(filters)
        
        if not properties:
            return "No properties found."
            
        return f"Found {len(properties)} properties for browsing."