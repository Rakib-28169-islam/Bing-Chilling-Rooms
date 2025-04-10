import streamlit as st
from auth.auth_service import AuthService
from users.user_type import UserType

def render():
    st.title("Sign In")
    
    with st.form("signin_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In")
        
        if submit:
            try:
                # Get user from database - unpack the tuple
                user, message = AuthService.get_instance().get_user(email,password)
                
                if not user:
                    st.error("User not found!")
                    return
                    
                # Verify password using login_user method
                success, message = AuthService.get_instance().login_user(user)
                if not success:
                    st.error("Invalid password!")
                    return
                
                
                # Store user info in session state
                st.session_state["user"] = user
                st.session_state["authenticated"] = True
                st.session_state["user_type"] = user.getUserType()  # This is already a string
                
                # Set the appropriate home page based on user type
                user_type = user.getUserType()  # This returns a string like "admin", "host", or "guest"
                if user_type == "admin":
                    st.session_state["current_page"] = "admin_home"
                elif user_type == "host":
                    st.session_state["current_page"] = "host_home"
                else:
                    st.session_state["current_page"] = "guest_home"
                
                # Show success message and auto-redirect
                st.success("Login successful! Redirecting...")
                st.rerun()  # This will refresh the page and show the appropriate home page
                
            except Exception as e:
                st.error(f"Error during sign in: {str(e)}")

