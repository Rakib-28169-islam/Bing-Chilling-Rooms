from database.mongodb import booking_collection
from datetime import datetime, date
from property.property_service import PropertyService
import uuid
from database.mongodb import db
from database.mongodb import users_collection




class BookingService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = BookingService()
        return cls._instance
    
    def get_user_id_by_email(self, email):
        """Get MongoDB _id of a user by email"""
        user = users_collection.find_one({"email": email})
        if user:
            return str(user["_id"])
        return None
    
    def create_booking(self, guest_email, property_id, check_in, check_out, guests, special_requests=""):
        """Create a new booking"""
        # Convert dates to datetime objects if they're not already
        if isinstance(check_in, str):
            check_in = datetime.strptime(check_in, "%Y-%m-%d")
        elif isinstance(check_in, date):
            # Convert date to datetime
            check_in = datetime.combine(check_in, datetime.min.time())
            
        if isinstance(check_out, str):
            check_out = datetime.strptime(check_out, "%Y-%m-%d")
        elif isinstance(check_out, date):
            # Convert date to datetime
            check_out = datetime.combine(check_out, datetime.min.time())
        guest_id =  self.get_user_id_by_email(guest_email)
        
        if not guest_id:
            return None, "Guest not found."
        
        # Calculate number of days
        delta = check_out - check_in
        num_days = delta.days
        
        # Get property price
        property_service = PropertyService.get_instance()
        property_obj, _ = property_service.get_property(property_id)
        if not property_obj:
            return None, "Property not found."
        
        property_details = property_obj.get_details()
        price_per_night = property_details.get('price', 0)
        
        # Calculate total price
        total_price = price_per_night * num_days
        
        # Create booking document
        booking_data = {
            "guest_id": guest_id,
            "property_id": property_id,
            "check_in": check_in,
            "check_out": check_out,
            "num_days": num_days,
            "price_per_night": price_per_night,
            "total_price": total_price,
            "guests": guests,
            "special_requests": special_requests,
            "status": "confirmed",
            "created_at": datetime.now()
        }
        
        # Insert booking into database
        result = booking_collection.insert_one(booking_data)
        
        if result.inserted_id:
            # Use the MongoDB ObjectId as the booking_id
            booking_id = str(result.inserted_id)
            
            # Update the document with the booking_id
            booking_collection.update_one(
                {"_id": result.inserted_id},
                {"$set": {"booking_id": booking_id}}
            )
            
            return booking_id, "Booking created successfully."
        return None, "Failed to create booking."
    
    def get_booking(self, booking_id):
        """Get booking by ID"""
        booking_data = booking_collection.find_one({"booking_id": booking_id})
        
        if not booking_data:
            return None, "Booking not found."
        
        return booking_data, "Booking found."
    
    def get_guest_bookings(self, guest_id):
        """Get all bookings for a specific guest"""
        bookings_data = booking_collection.find({"guest_id": guest_id})
        
        bookings_list = []
        for booking_data in bookings_data:
            bookings_list.append(booking_data)
        
        return bookings_list
    
    def get_property_bookings(self, property_id):
        """Get all bookings for a specific property"""
        bookings_data = booking_collection.find({"property_id": property_id})
        
        bookings_list = []
        for booking_data in bookings_data:
            bookings_list.append(booking_data)
        
        return bookings_list
    
    def cancel_booking(self, booking_id):
        """Cancel a booking"""
        result = booking_collection.update_one(
            {"booking_id": booking_id},
            {"$set": {"status": "cancelled"}}
        )
        
        if result.modified_count > 0:
            return True, "Booking cancelled successfully."
        return False, "Booking not found or could not be cancelled." 