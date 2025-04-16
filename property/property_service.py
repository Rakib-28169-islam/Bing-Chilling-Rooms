# property/property_service.py
from database.mongodb import db
from property.property_factory import PropertyFactory
from bson import ObjectId

# Create properties collection reference
properties_collection = db["properties"]

class PropertyService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PropertyService()
        return cls._instance
    
    def create_property(self, host_id, property_type, details):
        """Create a new property listing"""

        details["host_id"] = host_id
        
        property_obj = PropertyFactory.create_property(property_type, details)
        
        property_data = property_obj.get_details()
        
        result = properties_collection.insert_one(property_data)
        
        if result.inserted_id:
            return str(result.inserted_id), f"Property '{details['title']}' created successfully."
        return None, "Failed to create property."
    
    def get_property(self, property_id):
        """Get property by ID"""
        property_data = properties_collection.find_one({"property_id": property_id})
        
        if not property_data:
            return None, "Property not found."
        
        property_obj = PropertyFactory.create_property(
            property_data["type"], 
            property_data
        )
        
        return property_obj, "Property found."
    
    def update_property(self, property_id, details):
        """Update property details"""
        
        property_obj, message = self.get_property(property_id)
        
        if not property_obj:
            return False, message
        
        property_obj.update_details(details)
        
        result = properties_collection.update_one(
            {"property_id": property_id},
            {"$set": property_obj.get_details()}
        )
        
        if result.modified_count > 0:
            return True, "Property updated successfully."
        return False, "No changes made to property."
    
    def delete_property(self, property_id):
        """Delete a property"""
        result = properties_collection.delete_one({"property_id": property_id})
        
        if result.deleted_count > 0:
            return True, "Property deleted successfully."
        return False, "Property not found or could not be deleted."
    
    def list_properties(self, filters=None):
        """List properties with optional filters"""
        query = filters if filters else {}
        properties_data = properties_collection.find(query)
        
        properties_list = []
        for prop_data in properties_data:
            property_obj = PropertyFactory.create_property(
                prop_data["type"],
                prop_data
            )
            properties_list.append(property_obj.get_details())
        
        return properties_list
    
    def get_host_properties(self, host_id):
        """Get all properties for a specific host"""
        return self.list_properties({"host_id": host_id})