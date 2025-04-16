# tests/test_property.py
import unittest
from property.property_factory import PropertyFactory
from property.property_service import PropertyService
from database.mongodb import properties_collection

class TestPropertyFunctionality(unittest.TestCase):
    def setUp(self):
        # Clean up test data from previous runs
        properties_collection.delete_many({"title": {"$regex": "^Test"}})
        
        # Sample property data
        self.apartment_data = {
            "host_id": "test@example.com",
            "title": "Test Apartment",
            "location": "New York",
            "price": 100,
            "floor_number": 5,
            "has_elevator": True,
            "amenities": ["WiFi", "Kitchen", "AC"]
        }
        
        self.house_data = {
            "host_id": "test@example.com",
            "title": "Test House",
            "location": "Los Angeles",
            "price": 150,
            "floors": 2,
            "has_garden": True,
            "amenities": ["WiFi", "Kitchen", "Parking", "Garden"]
        }
        
        self.villa_data = {
            "host_id": "test@example.com",
            "title": "Test Villa",
            "location": "Miami",
            "price": 300,
            "has_pool": True,
            "has_private_access": True,
            "amenities": ["WiFi", "Kitchen", "Pool", "BBQ", "Beach Access"]
        }
    
    def test_create_property_objects(self):
        """Test property factory creates correct objects"""
        # Create property objects
        apartment = PropertyFactory.create_property("apartment", self.apartment_data)
        house = PropertyFactory.create_property("house", self.house_data)
        villa = PropertyFactory.create_property("villa", self.villa_data)
        
        # Check property types
        self.assertEqual(apartment.get_type(), "apartment")
        self.assertEqual(house.get_type(), "house")
        self.assertEqual(villa.get_type(), "villa")
        
        # Check specific properties
        apartment_details = apartment.get_details()
        self.assertEqual(apartment_details["floor_number"], 5)
        self.assertTrue(apartment_details["has_elevator"])
        
        house_details = house.get_details()
        self.assertEqual(house_details["floors"], 2)
        self.assertTrue(house_details["has_garden"])
        
        villa_details = villa.get_details()
        self.assertTrue(villa_details["has_pool"])
        self.assertTrue(villa_details["has_private_access"])
    
    def test_property_service_crud(self):
        """Test property service CRUD operations"""
        service = PropertyService.get_instance()
        
        # Test create
        apartment_id, _ = service.create_property("test@example.com", "apartment", self.apartment_data)
        self.assertIsNotNone(apartment_id)
        
        # Test get
        apartment_obj, _ = service.get_property(apartment_id)
        self.assertEqual(apartment_obj.get_details()["title"], "Test Apartment")
        
        # Test update
        update_success, _ = service.update_property(apartment_id, {"price": 120})
        self.assertTrue(update_success)
        
        updated_apartment, _ = service.get_property(apartment_id)
        self.assertEqual(updated_apartment.get_details()["price"], 120)
        
        # Test list
        properties = service.list_properties({"host_id": "test@example.com"})
        self.assertTrue(len(properties) > 0)
        
        # Test delete
        delete_success, _ = service.delete_property(apartment_id)
        self.assertTrue(delete_success)
        
        # Verify deletion
        deleted_apartment, _ = service.get_property(apartment_id)
        self.assertIsNone(deleted_apartment)
    
    def test_create_multiple_properties(self):
        """Test creating multiple properties"""
        service = PropertyService.get_instance()
        
        # Create all property types
        apartment_id, _ = service.create_property("test@example.com", "apartment", self.apartment_data)
        house_id, _ = service.create_property("test@example.com", "house", self.house_data)
        villa_id, _ = service.create_property("test@example.com", "villa", self.villa_data)
        
        # Check they all exist
        self.assertIsNotNone(apartment_id)
        self.assertIsNotNone(house_id)
        self.assertIsNotNone(villa_id)
        
        # Get host properties
        host_properties = service.get_host_properties("test@example.com")
        self.assertEqual(len(host_properties), 3)
        
        # Clean up
        service.delete_property(apartment_id)
        service.delete_property(house_id)
        service.delete_property(villa_id)
    
    def tearDown(self):
        # Clean up test data
        properties_collection.delete_many({"title": {"$regex": "^Test"}})

if __name__ == "__main__":
    unittest.main()