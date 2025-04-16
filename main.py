# main.py
import streamlit as st
from pages.Home import render as render_home
from pages.SignIn import render as render_signin
from pages.SignUp import render as render_signup
from pages.AdminHome import render as render_admin_home
from pages.HostHome import render as render_host_home
from pages.GuestHome import render as render_guest_home
from pages.PropertyPage import render as render_property_page

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# Main content area
if st.session_state['authenticated']:
    # Add navigation
    nav_options = ["Dashboard", "Properties"]
    selected_nav = st.sidebar.radio("Navigation", nav_options)
    
    # Update current_page based on navigation selection
    if selected_nav == "Dashboard":
        st.session_state['current_page'] = 'dashboard'
    elif selected_nav == "Properties":
        st.session_state['current_page'] = 'properties'
    
    # Render appropriate page based on current_page
    if st.session_state['current_page'] == 'dashboard':
        # Get user type from session state
        user_type = st.session_state.get('user_type', 'guest')
        
        # Render appropriate home page based on user type
        if user_type == 'admin':
            render_admin_home()
        elif user_type == 'host':
            render_host_home()
        else:
            render_guest_home()
    elif st.session_state['current_page'] == 'properties':  # Properties page
        render_property_page()
        
    # Add sign out button to sidebar
    if st.sidebar.button("Sign Out", key="signout_button"):
        st.session_state.clear()
        st.rerun()
else:
    # Show authentication options for non-authenticated users
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        render_signin()
        
    with tab2:
        render_signup()