import streamlit as st
from pages.Home import render as render_home
from pages.SignIn import render as render_signin
from pages.SignUp import render as render_signup
from pages.AdminHome import render as render_admin_home
from pages.HostHome import render as render_host_home
from pages.GuestHome import render as render_guest_home

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# Simple sidebar with debug info
# with st.sidebar:
#     st.write("Debug Info:")
#     st.write(f"Authenticated: {st.session_state['authenticated']}")
#     st.write(f"Current Page: {st.session_state['current_page']}")
#     if st.button("🔄 Reload App"):
#         st.rerun()

# Main content area
if st.session_state['authenticated']:
    # Get user type from session state
    user_type = st.session_state.get('user_type', 'guest')
    
    # Render appropriate home page based on user type
    if user_type == 'admin':
        render_admin_home()
    elif user_type == 'host':
        render_host_home()
    else:
        render_guest_home()
else:
    # Show authentication options for non-authenticated users
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        render_signin()
        
    with tab2:
        render_signup()