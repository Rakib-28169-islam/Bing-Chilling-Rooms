import streamlit as st
from proxy.user_proxy import UserProxy

def render():
    st.title("Admin Dashboard")
    
    user = st.session_state.get("user")
    proxy = UserProxy(user)
    
    st.write(f"Welcome back, **{user.getName()}**!")
    
    if st.button("Sign Out"):
        st.session_state.clear()
        st.rerun()
        return
        
    # Admin-specific actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Manage Users"):
            try:
                result = proxy.execute("manage_users")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
        if st.button("View Reports"):
            try:
                result = proxy.execute("view_reports")
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
                
        if st.button("Delete Account"):
            try:
                result = proxy.execute("delete_account")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}") 