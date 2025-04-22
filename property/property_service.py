# property/property_service.py
from database.mongodb import db
from property.property_factory import PropertyFactory
from bson import ObjectId

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
        creator = PropertyFactory.get_creator(property_type)
        property_obj = creator.create_property(details)
        property_data = property_obj.get_details()
        result = properties_collection.insert_one(property_data)
        
        if result.inserted_id:
            return str(result.inserted_id), f"Property '{details['title']}' created successfully."
        return None, "Failed to create property."
    
    def get_property(self, property_id):
        """Get property by ID"""
        try:
            property_data = properties_collection.find_one({"_id": ObjectId(property_id)})
            
            if not property_data:
                return None, "Property not found."
            
            creator = PropertyFactory.get_creator(property_data["type"])
            property_obj = creator.create_property(property_data)
            
            return property_obj, "Property found."
        except Exception as e:
            return None, f"Error retrieving property: {str(e)}"
    
    def update_property(self, property_id, details):
        """Update property details"""
        
        property_obj, message = self.get_property(property_id)
        
        if not property_obj:
            return False, message
        
        property_obj.update_details(details)
        
        result = properties_collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$set": property_obj.get_details()}
        )
        
        if result.modified_count > 0:
            return True, "Property updated successfully."
        return False, "No changes made to property."
    
    def delete_property(self, property_id):
        """Delete a property"""
        try:
            result = properties_collection.delete_one({"_id": ObjectId(property_id)})
            
            if result.deleted_count > 0:
                return True, "Property deleted successfully."
            return False, "Property not found or could not be deleted."
        except Exception as e:
            return False, f"Error deleting property: {str(e)}"
    
    def list_properties(self, filters=None):
        """List properties with optional filters"""
        query = filters if filters else {}
        properties_data = properties_collection.find(query)
        
        properties_list = []
        for prop_data in properties_data:
            # Ensure _id is properly serialized to string
            prop_data_copy = dict(prop_data)
            prop_data_copy['_id'] = str(prop_data_copy['_id'])
            
            creator = PropertyFactory.get_creator(prop_data_copy["type"])
            property_obj = creator.create_property(prop_data_copy)
            
            details = property_obj.get_details()
            properties_list.append(details)
        
        return properties_list
    
    def get_host_properties(self, host_id):
        """Get all properties for a specific host"""
        return self.list_properties({"host_id": host_id})