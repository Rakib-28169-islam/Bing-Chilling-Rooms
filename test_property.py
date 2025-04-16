# tests/test_property.py
import unittest
from property.property_factory import PropertyFactory
from property.property_service import PropertyService
from database.mongodb import properties_collection
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestPropertyFunctionality(unittest.TestCase):
    def setUp(self):
        print("\n=== Setting up test environment ===")
        # Clean up test data from previous runs
        deleted = properties_collection.delete_many({"title": {"$regex": "^Test"}})
        print(f"Cleaned up {deleted.deleted_count} test properties from previous runs")
        
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
        print("Sample property data created")
    
    def test_create_property_objects(self):
        """Test property factory creates correct objects"""
        print("\n=== Testing Property Factory ===")
        # Get creators from factory and create property objects
        print("Creating different property types using factory...")
        apartment_creator = PropertyFactory.get_creator("apartment")
        house_creator = PropertyFactory.get_creator("house")
        villa_creator = PropertyFactory.get_creator("villa")
        
        apartment = apartment_creator.create_property(self.apartment_data)
        house = house_creator.create_property(self.house_data)
        villa = villa_creator.create_property(self.villa_data)
        
        # Check property types
        print("Verifying property types...")
        self.assertEqual(apartment.get_type(), "apartment")
        self.assertEqual(house.get_type(), "house")
        self.assertEqual(villa.get_type(), "villa")
        print("✓ Property types match expected values")
        
        # Check specific properties
        print("Checking specific property attributes...")
        apartment_details = apartment.get_details()
        self.assertEqual(apartment_details["floor_number"], 5)
        self.assertTrue(apartment_details["has_elevator"])
        print(f"✓ Apartment: Floor {apartment_details['floor_number']}, Elevator: {apartment_details['has_elevator']}")
        
        house_details = house.get_details()
        self.assertEqual(house_details["floors"], 2)
        self.assertTrue(house_details["has_garden"])
        print(f"✓ House: {house_details['floors']} floors, Garden: {house_details['has_garden']}")
        
        villa_details = villa.get_details()
        self.assertTrue(villa_details["has_pool"])
        self.assertTrue(villa_details["has_private_access"])
        print(f"✓ Villa: Pool: {villa_details['has_pool']}, Private Access: {villa_details['has_private_access']}")
    
    def test_property_service_crud(self):
        """Test property service CRUD operations"""
        print("\n=== Testing Property Service CRUD Operations ===")
        service = PropertyService.get_instance()
        
        # Test create
        print("Creating a new apartment...")
        apartment_id, message = service.create_property("test@example.com", "apartment", self.apartment_data)
        self.assertIsNotNone(apartment_id)
        print(f"✓ Property created with ID: {apartment_id}")
        print(f"  Message: {message}")
        
        # Test get
        print("\nRetrieving apartment details...")
        apartment_obj, message = service.get_property(apartment_id)
        self.assertEqual(apartment_obj.get_details()["title"], "Test Apartment")
        print(f"✓ Retrieved property: {apartment_obj.get_details()['title']}")
        print(f"  Message: {message}")
        
        # Test update
        print("\nUpdating apartment price from $100 to $120...")
        update_success, message = service.update_property(apartment_id, {"price": 120})
        self.assertTrue(update_success)
        print(f"✓ Update result: {update_success}")
        print(f"  Message: {message}")
        
        updated_apartment, _ = service.get_property(apartment_id)
        self.assertEqual(updated_apartment.get_details()["price"], 120)
        print(f"✓ New price verified: ${updated_apartment.get_details()['price']}")
        
        # Test list
        print("\nListing properties for host: test@example.com")
        properties = service.list_properties({"host_id": "test@example.com"})
        self.assertTrue(len(properties) > 0)
        print(f"✓ Found {len(properties)} properties")
        for i, prop in enumerate(properties, 1):
            print(f"  {i}. {prop['title']} in {prop['location']} - ${prop['price']}")
        
        # Test delete
        print("\nDeleting test apartment...")
        delete_success, message = service.delete_property(apartment_id)
        self.assertTrue(delete_success)
        print(f"✓ Deletion result: {delete_success}")
        print(f"  Message: {message}")
        
        # Verify deletion
        print("Verifying property was deleted...")
        deleted_apartment, message = service.get_property(apartment_id)
        self.assertIsNone(deleted_apartment)
        print(f"✓ Property no longer exists. Message: {message}")
    
    def test_create_multiple_properties(self):
        """Test creating multiple properties"""
        print("\n=== Testing Multiple Property Creation and Host Listing ===")
        service = PropertyService.get_instance()
        
        # Create all property types
        print("Creating multiple properties (apartment, house, villa)...")
        apartment_id, _ = service.create_property("test@example.com", "apartment", self.apartment_data)
        house_id, _ = service.create_property("test@example.com", "house", self.house_data)
        villa_id, _ = service.create_property("test@example.com", "villa", self.villa_data)
        
        # Check they all exist
        self.assertIsNotNone(apartment_id)
        self.assertIsNotNone(house_id)
        self.assertIsNotNone(villa_id)
        print(f"✓ Created apartment ID: {apartment_id}")
        print(f"✓ Created house ID: {house_id}")
        print(f"✓ Created villa ID: {villa_id}")
        
        # Get host properties
        print("\nFetching all properties for host: test@example.com")
        host_properties = service.get_host_properties("test@example.com")
        self.assertEqual(len(host_properties), 3)
        print(f"✓ Host has {len(host_properties)} properties")
        
        print("Property listing:")
        for i, prop in enumerate(host_properties, 1):
            print(f"  {i}. [{prop['type'].upper()}] {prop['title']} in {prop['location']} - ${prop['price']}")
            print(f"     Amenities: {', '.join(prop['amenities'])}")
        
        # Clean up
        print("\nCleaning up test properties...")
        service.delete_property(apartment_id)
        service.delete_property(house_id)
        service.delete_property(villa_id)
        print("✓ All test properties deleted")
    
    def tearDown(self):
        # Clean up test data
        deleted = properties_collection.delete_many({"title": {"$regex": "^Test"}})
        print(f"\n=== Tear down: Removed {deleted.deleted_count} test properties ===")

if __name__ == "__main__":
    print("=" * 70)
    print("STARTING PROPERTY SYSTEM TESTS")
    print("=" * 70)
    unittest.main()