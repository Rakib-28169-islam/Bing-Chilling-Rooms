# import random
# from users.user_type import UserType
from users.User import User
from users.user_type import UserType
# from database.mongodb import users_collection
from property.property_service import PropertyService

class Admin(User):
    def __init__(self, name, email, password, user_type: UserType):
        super().__init__(name, email, password, user_type)
    
    def manage_users(self):
        return f"{self.getName()} is managing user accounts."

    def view_reports(self):
        return f"{self.getName()} is viewing business reports."

    def delete_account(self, user):
        return f"{self.getName()} deleted {user}'s account."
    
    def browse_listings(self, filters=None):
        """Browse property listings"""
        property_service = PropertyService.get_instance()
        properties = property_service.list_properties(filters)
        
        if not properties:
            return "No properties found."
            
        return f"Found {len(properties)} properties as admin."

        
    