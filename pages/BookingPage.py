# pages/BookingPage.py
import streamlit as st
from property.property_service import PropertyService
from booking.booking_service import BookingService
from datetime import datetime, date, timedelta

def render():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please sign in to book a property.")
        if st.button("Go to Login"):
            st.switch_page("pages/Login.py")
        return
    
    # Get property_id from session state
    property_id = st.session_state.get("booking_property_id")
    if not property_id:
        st.error("No property selected for booking.")
        if st.button("Back to Properties"):
            st.switch_page("pages/PropertyPage.py")
        return
    
    # Get property details
    property_service = PropertyService.get_instance()
    property_obj, message = property_service.get_property(property_id)
    
    if not property_obj:
        st.error(f"Property not found: {message}")
        if st.button("Back to Properties"):
            st.switch_page("pages/PropertyPage.py")
        return
    
    property_details = property_obj.get_details()
    price_per_night = property_details.get('price', 0)
    
    st.title(f"Book {property_details['title']}")
    st.write(f"Location: {property_details['location']}")
    st.write(f"Price: ${price_per_night}/night")
    
    # Booking form
    with st.form(key="booking_form"):
        # Set min date to today
        today = date.today()
        check_in = st.date_input("Check-in Date", min_value=today)
        
        # Set check-out date with a fixed range instead of dynamic min_value
        # Default to check-in + 1 day
        default_check_out = check_in + timedelta(days=1)
        check_out = st.date_input("Check-out Date", value=default_check_out, min_value=today)
        
        guests = st.number_input("Number of Guests", min_value=1, value=1)
        special_requests = st.text_area("Special Requests (Optional)")
        
        # Calculate and display total price
        if check_in and check_out:
            delta = check_out - check_in
            num_days = delta.days
            total_price = price_per_night * num_days
            st.write(f"**Number of nights:** {num_days}")
            st.write(f"**Total price:** ${total_price}")
        
        # Submit button
        submit_button = st.form_submit_button(label="Make Payment")
        
        if submit_button:
            if check_in >= check_out:
                st.error("Check-out date must be after check-in date.")
            else:
                # Create booking
                booking_service = BookingService.get_instance()
                booking_id, message = booking_service.create_booking(
                    user.getEmail(),
                    property_id,
                    check_in,
                    check_out,
                    guests,
                    special_requests
                )
                
                if booking_id:
                    st.success(f"Booking confirmed! Your booking ID is: {booking_id}")
                    # Store booking details in session state
                    st.session_state["booking_id"] = booking_id
                    st.session_state["total_price"] = total_price
                    # Redirect to payment page
                    st.switch_page("pages/payment_page.py")
                else:
                    st.error(f"Booking failed: {message}")
    
    # Back button
    if st.button("Back to Properties"):
        st.switch_page("pages/PropertyPage.py")

# Call the render function to display the page
render() 