import streamlit as st
from proxy.user_proxy import UserProxy

def render():
    st.title("Guest Dashboard")
    
    user = st.session_state.get("user")
    proxy = UserProxy(user)
    
    st.write(f"Welcome back, **{user.getName()}**!")
    
    if st.button("Sign Out"):
        st.session_state.clear()
        st.rerun()
        return
        
    # Guest-specific actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Browse Listings"):
            try:
                result = proxy.execute("browse_listings")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                
    with col2:
        if st.button("Book Accommodation"):
            try:
                result = proxy.execute("book_accommodation")
                st.info(result)
            except Exception as e:
                st.error(f"Error: {str(e)}") 