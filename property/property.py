# property/property.py
from abc import ABC, abstractmethod
from bson import ObjectId

class Property(ABC):
    def __init__(self, property_id, host_id, title, location, price, amenities=None, images=None, availability=None):
        self._property_id = property_id if property_id else str(ObjectId())
        self._host_id = host_id
        self._title = title
        self._location = location
        self._price = price
        self._amenities = amenities if amenities else []
        self._images = images if images else []
        self._availability = availability if availability else []
        
    def get_id(self):
        return self._property_id
        
    def get_host_id(self):
        return self._host_id
        
    def get_details(self):
        return {
            "_id": self._property_id,
            "host_id": self._host_id,
            "title": self._title,
            "location": self._location,
            "price": self._price,
            "amenities": self._amenities,
            "images": self._images,
            "availability": self._availability,
            "type": self.get_type()
        }
    
    def update_details(self, details):
        if "title" in details:
            self._title = details["title"]
        if "location" in details:
            self._location = details["location"]
        if "price" in details:
            self._price = details["price"]
        if "amenities" in details:
            self._amenities = details["amenities"]
        if "images" in details:
            self._images = details["images"]
        if "availability" in details:
            self._availability = details["availability"]
        return True
    
    def check_availability(self, dates):
        # Simple availability check (can be enhanced)
        for available_range in self._availability:
            if dates["start_date"] >= available_range["start_date"] and dates["end_date"] <= available_range["end_date"]:
                return True
        return False
    
    @abstractmethod
    def get_type(self):
        pass

class Apartment(Property):
    def __init__(self, property_id, host_id, title, location, price, floor_number, has_elevator, amenities=None, images=None, availability=None):
        super().__init__(property_id, host_id, title, location, price, amenities, images, availability)
        self._floor_number = floor_number
        self._has_elevator = has_elevator
        
    def get_type(self):
        return "apartment"
        
    def get_details(self):
        details = super().get_details()
        details.update({
            "floor_number": self._floor_number,
            "has_elevator": self._has_elevator
        })
        return details

class House(Property):
    def __init__(self, property_id, host_id, title, location, price, floors, has_garden, amenities=None, images=None, availability=None):
        super().__init__(property_id, host_id, title, location, price, amenities, images, availability)
        self._floors = floors
        self._has_garden = has_garden
        
    def get_type(self):
        return "house"
        
    def get_details(self):
        details = super().get_details()
        details.update({
            "floors": self._floors,
            "has_garden": self._has_garden
        })
        return details

class Villa(Property):
    def __init__(self, property_id, host_id, title, location, price, has_pool, has_private_access, amenities=None, images=None, availability=None):
        super().__init__(property_id, host_id, title, location, price, amenities, images, availability)
        self._has_pool = has_pool
        self._has_private_access = has_private_access
        
    def get_type(self):
        return "villa"
        
    def get_details(self):
        details = super().get_details()
        details.update({
            "has_pool": self._has_pool,
            "has_private_access": self._has_private_access
        })
        return details

