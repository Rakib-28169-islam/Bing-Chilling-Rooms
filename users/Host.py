### users/Host.py
from users.User import User
from users.user_type import UserType
from property.property_service import PropertyService

class Host(User):
    def __init__(self, name, email, password, user_type: UserType):
        super().__init__(name, email, password, user_type)

    # def create_listing(self):
    #     return f"{self.getName()} created a new listing."
    
    def create_listing(self, property_type=None, property_details=None):
        """Create a new property listing"""
        if not property_type or not property_details:
            return f"{self.getName()} created a new listing."  # Default message for UI button click
        
        # Add actual property creation logic
        property_service = PropertyService.get_instance()
        property_id, message = property_service.create_property(
            self.getEmail(),  # Using email as host_id
            property_type,
            property_details
        )
        
        if property_id:
            return f"Property listing '{property_details.get('title')}' created successfully."
        return f"Failed to create property: {message}"

    def manage_bookings(self):
        return f"{self.getName()} is managing bookings."

    def view_earnings(self):
        return f"{self.getName()} is viewing earnings."

    def browse_listings(self, filters=None):
        """Browse property listings"""
        property_service = PropertyService.get_instance()
        properties = property_service.list_properties(filters)
        
        if not properties:
            return "No properties found."
            
        return f"Found {len(properties)} properties."
        
    def delete_listing(self, property_id):
        """Delete a property listing"""
        property_service = PropertyService.get_instance()
        host_properties = property_service.get_host_properties(self.getEmail())
        
        # Check if property belongs to this host
        if not any(prop["property_id"] == property_id for prop in host_properties):
            return "You don't have permission to delete this property."
            
        success, message = property_service.delete_property(property_id)
        return message