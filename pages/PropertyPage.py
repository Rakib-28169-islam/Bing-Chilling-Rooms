# pages/PropertyPage.py
import streamlit as st
from property.property_service import PropertyService
from users.user_type import UserType

def render():
    user = st.session_state.get("user")
    if not user:
        st.warning("Please sign in to access property listings.")
        return
    
    st.title("Property Listings")
    
    # Set tab selection based on property_section in session state
    tab_options = ["browse", "my_properties"]
    default_tab = "browse"
    
    # Get desired tab from session state and clear it
    if 'property_section' in st.session_state:
        if st.session_state['property_section'] == 'my_properties':
            default_tab = "my_properties"
        # Remove it from session state after use
        st.session_state.pop('property_section')
        
    # Create tabs
    selected_tab = st.radio("Select view:", tab_options, 
                          format_func=lambda x: "Browse Properties" if x == "browse" else "My Properties",
                          index=tab_options.index(default_tab),
                          horizontal=True,
                          label_visibility="collapsed")
    
    st.divider()
    
    # Render content based on selected tab
    if selected_tab == "browse":
        browse_properties()
    else:  # my_properties
        # Only hosts and admins can see their properties
        user_type = user.getUserType()
        if user_type == "host" or user_type == "admin":
            my_properties()
        else:
            st.info("Only hosts can manage properties.")

def browse_properties():
    """Browse all available properties"""
    property_service = PropertyService.get_instance()
    properties = property_service.list_properties()
    
    if not properties:
        st.info("No properties are currently available.")
        return
    
    st.subheader(f"Found {len(properties)} properties")
    
    # Display properties
    for prop in properties:
        with st.expander(f"{prop['title']} - {prop['location']} (${prop['price']}/night)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Type:** {prop['type'].capitalize()}")
                st.write(f"**Location:** {prop['location']}")
                st.write(f"**Price:** ${prop['price']}/night")
                
                # Show property-specific details
                if prop['type'] == 'apartment':
                    st.write(f"**Floor:** {prop['floor_number']}")
                    st.write(f"**Elevator:** {'Yes' if prop['has_elevator'] else 'No'}")
                elif prop['type'] == 'house':
                    st.write(f"**Floors:** {prop['floors']}")
                    st.write(f"**Garden:** {'Yes' if prop['has_garden'] else 'No'}")
                elif prop['type'] == 'villa':
                    st.write(f"**Pool:** {'Yes' if prop['has_pool'] else 'No'}")
                    st.write(f"**Private Access:** {'Yes' if prop['has_private_access'] else 'No'}")
                
            with col2:
                if prop['amenities']:
                    st.write("**Amenities:**")
                    for amenity in prop['amenities']:
                        st.write(f"- {amenity}")
                
            # Add booking button for guests
            user = st.session_state.get("user")
            if user and user.getUserType() == "guest":
                if st.button(f"Book this property", key=f"book_{prop['property_id']}"):
                    # Store property_id in session state and switch to booking page
                    st.session_state["booking_property_id"] = prop['property_id']
                    st.switch_page("pages/BookingPage.py")

def my_properties():
    """Show and manage host's own properties"""
    user = st.session_state.get("user")
    if not user or user.getUserType() != "host":
        return
    
    property_service = PropertyService.get_instance()
    host_properties = property_service.get_host_properties(user.getEmail())
    
    if not host_properties:
        st.info("You don't have any properties listed yet.")
    else:
        st.subheader(f"You have {len(host_properties)} property listings")
        
        for prop in host_properties:
            with st.expander(f"{prop['title']} - {prop['location']}"):
                st.write(f"**Type:** {prop['type'].capitalize()}")
                st.write(f"**Price:** ${prop['price']}/night")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{prop['property_id']}"):
                        st.session_state["editing_property"] = prop
                        st.rerun()
                        
                with col2:
                    if st.button("Delete", key=f"delete_{prop['property_id']}"):
                        success, message = property_service.delete_property(prop['property_id'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    # Add property form
    st.subheader("Add New Property")
    
    with st.form("add_property_form"):
        property_type = st.selectbox("Property Type", ["apartment", "house", "villa"])
        title = st.text_input("Title")
        location = st.text_input("Location")
        price = st.number_input("Price per Night", min_value=1.0, value=50.0, step=5.0)
        
        # Type-specific fields
        if property_type == "apartment":
            floor_number = st.number_input("Floor Number", min_value=0, value=1)
            has_elevator = st.checkbox("Has Elevator")
            specific_details = {"floor_number": floor_number, "has_elevator": has_elevator}
        elif property_type == "house":
            floors = st.number_input("Number of Floors", min_value=1, value=1)
            has_garden = st.checkbox("Has Garden")
            specific_details = {"floors": floors, "has_garden": has_garden}
        else:  # villa
            has_pool = st.checkbox("Has Pool")
            has_private_access = st.checkbox("Has Private Access")
            specific_details = {"has_pool": has_pool, "has_private_access": has_private_access}
        
        amenities = st.text_input("Amenities (comma separated)")
        
        submit = st.form_submit_button("Create Listing")
        
        if submit:
            if not title or not location:
                st.error("Title and location are required.")
            else:
                # Prepare property details
                property_details = {
                    "title": title,
                    "location": location,
                    "price": price,
                    "amenities": [a.strip() for a in amenities.split(",")] if amenities else [],
                    **specific_details
                }
                
                # Create property
                property_id, message = property_service.create_property(
                    user.getEmail(),
                    property_type,
                    property_details
                )
                
                if property_id:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

# Call the render function to display the page
render()