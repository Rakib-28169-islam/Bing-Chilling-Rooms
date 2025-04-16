# property/property_factory.py
from property.property import Apartment, House, Villa

class PropertyFactory:
    @staticmethod
    def create_property(property_type, details):
        """
        Factory method to create different types of properties
        """
        property_id = details.get("property_id", None)
        host_id = details.get("host_id")
        title = details.get("title")
        location = details.get("location")
        price = details.get("price")
        amenities = details.get("amenities", [])
        images = details.get("images", [])
        availability = details.get("availability", [])
        
        if property_type == "apartment":
            floor_number = details.get("floor_number", 1)
            has_elevator = details.get("has_elevator", False)
            return Apartment(property_id, host_id, title, location, price, floor_number, has_elevator, amenities, images, availability)
            
        elif property_type == "house":
            floors = details.get("floors", 1)
            has_garden = details.get("has_garden", False)
            return House(property_id, host_id, title, location, price, floors, has_garden, amenities, images, availability)
            
        elif property_type == "villa":
            has_pool = details.get("has_pool", False)
            has_private_access = details.get("has_private_access", False)
            return Villa(property_id, host_id, title, location, price, has_pool, has_private_access, amenities, images, availability)
            
        else:
            raise ValueError(f"Invalid property type: {property_type}")