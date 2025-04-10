### pages/Home.py
import streamlit as st
from proxy.user_proxy import UserProxy

def render():
    st.subheader("Home Dashboard")
    
    # Check if user is authenticated
    if "user" not in st.session_state:
        st.warning("Please sign in to access the dashboard.")
        return
        
    user = st.session_state.get("user")
    proxy = UserProxy(user)

    st.write(f"Welcome back, **{user.getName()}**!")

    if st.button("Sign Out"):
        st.session_state.pop("user", None)
        st.session_state.pop("authenticated", None)
        st.success("You have been signed out.")
        st.rerun()
        return

    # Get all actions this user can perform
    user_actions = proxy.permissions

    # Show each action as a button
    for action in user_actions:
        # Convert action name to display name (e.g., "browse_listings" -> "Browse Listings")
        display_name = action.replace("_", " ").title()
        
        if st.button(display_name):
            try:
                # Execute the action when button is clicked
                result = proxy.execute(action)
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    user_type = user.getUserType().lower()
    
    if user_type == "admin":
        if st.button("Manage Users"):
            try:
                result = proxy.execute("manage_users")
                st.info(result)
            except Exception as e:
                st.error(f"Error managing users: {str(e)}")
                
        if st.button("View Reports"):
            try:
                result = proxy.execute("view_reports")
                st.info(result)
            except Exception as e:
                st.error(f"Error viewing reports: {str(e)}")

    elif user_type == "host":
        if st.button("Create Listing"):
            try:
                result = proxy.execute("create_listing")
                st.info(result)
            except Exception as e:
                st.error(f"Error creating listing: {str(e)}")
                
        if st.button("Manage Bookings"):
            try:
                result = proxy.execute("manage_bookings")
                st.info(result)
            except Exception as e:
                st.error(f"Error managing bookings: {str(e)}")
                
        if st.button("View Earnings"):
            try:
                result = proxy.execute("view_earnings")
                st.info(result)
            except Exception as e:
                st.error(f"Error viewing earnings: {str(e)}")

    elif user_type == "guest":
        if st.button("Book Accommodation"):
            try:
                result = proxy.execute("book_accommodation")
                st.info(result)
            except Exception as e:
                st.error(f"Error booking accommodation: {str(e)}")