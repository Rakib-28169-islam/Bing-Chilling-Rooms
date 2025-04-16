import streamlit as st
from proxy.user_proxy import UserProxy

def render():
    st.title("Host Dashboard")
    
    user = st.session_state.get("user")
    proxy = UserProxy(user)
    
    st.write(f"Welcome back, **{user.getName()}**!")
    
    if st.button("Sign Out", key="host_signout"):
        st.session_state.clear()
        st.rerun()
        return
        
    # Host-specific actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Create Listing", key="create_listing_btn"):
            # Navigate to Property Page with My Properties section
            # st.session_state['current_page'] = 'properties'
            # st.session_state['property_section'] = 'my_properties'
            st.switch_page("pages\PropertyPage.py")
                
        if st.button("Manage Bookings", key="manage_bookings_btn"):
            try:
                result = proxy.execute("manage_bookings")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
    with col2:
        if st.button("Browse Listings", key="browse_listings_btn"):
            # Navigate to Property Page with browse section
            st.session_state['current_page'] = 'properties'
            st.session_state['property_section'] = 'browse'
            st.rerun()
                
        if st.button("View Earnings", key="view_earnings_btn"):
            try:
                result = proxy.execute("view_earnings")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")