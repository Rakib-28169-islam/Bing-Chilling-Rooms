import streamlit as st
from proxy.user_proxy import UserProxy

def render():
    st.title("Host Dashboard")
    
    user = st.session_state.get("user")
    proxy = UserProxy(user)
    
    st.write(f"Welcome back, **{user.getName()}**!")
    
    if st.button("Sign Out"):
        st.session_state.clear()
        st.rerun()
        return
        
    # Host-specific actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Create Listing"):
            try:
                result = proxy.execute("create_listing")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
        if st.button("Manage Bookings"):
            try:
                result = proxy.execute("manage_bookings")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
    with col2:
        if st.button("Browse Listings"):
            try:
                result = proxy.execute("browse_listings")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
        if st.button("View Earnings"):
            try:
                result = proxy.execute("view_earnings")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}") 