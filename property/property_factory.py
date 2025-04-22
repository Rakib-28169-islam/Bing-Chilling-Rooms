# property/property_factory.py
from property.property import Apartment, House, Villa
from abc import ABC, abstractmethod

class PropertyCreator(ABC):
    @abstractmethod
    def factory_method(self, details):
        """
        Subclasses should implement this to return specific property instances.
        """
        pass

    def create_property(self, details):
        """
        Calls the factory method to create the property.
        """
        return self.factory_method(details)


class ApartmentCreator(PropertyCreator):
    def factory_method(self, details):
        property_id = details.get("_id", details.get("property_id", None))
        host_id = details.get("host_id")
        title = details.get("title")
        location = details.get("location")
        price = details.get("price")
        amenities = details.get("amenities", [])
        images = details.get("images", [])
        availability = details.get("availability", [])
        floor_number = details.get("floor_number", 1)
        has_elevator = details.get("has_elevator", False)

        return Apartment(property_id, host_id, title, location, price,
                         floor_number, has_elevator, amenities, images, availability)


class HouseCreator(PropertyCreator):
    def factory_method(self, details):
        property_id = details.get("_id", details.get("property_id", None))
        host_id = details.get("host_id")
        title = details.get("title")
        location = details.get("location")
        price = details.get("price")
        amenities = details.get("amenities", [])
        images = details.get("images", [])
        availability = details.get("availability", [])
        floors = details.get("floors", 1)
        has_garden = details.get("has_garden", False)

        return House(property_id, host_id, title, location, price,
                     floors, has_garden, amenities, images, availability)


class VillaCreator(PropertyCreator):
    def factory_method(self, details):
        property_id = details.get("_id", details.get("property_id", None))
        host_id = details.get("host_id")
        title = details.get("title")
        location = details.get("location")
        price = details.get("price")
        amenities = details.get("amenities", [])
        images = details.get("images", [])
        availability = details.get("availability", [])
        has_pool = details.get("has_pool", False)
        has_private_access = details.get("has_private_access", False)

        return Villa(property_id, host_id, title, location, price,
                     has_pool, has_private_access, amenities, images, availability)

# Factory registry to get correct creator based on property type
class PropertyFactory:
    @staticmethod
    def get_creator(property_type):
        creators = {
            "apartment": ApartmentCreator(),
            "house": HouseCreator(),
            "villa": VillaCreator()
        }
        
        creator = creators.get(property_type.lower())
        if not creator:
            raise ValueError(f"Invalid property type: {property_type}")
        
        return creator
