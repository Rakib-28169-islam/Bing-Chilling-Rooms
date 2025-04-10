### pages/SignUp.py
import streamlit as st
from auth.auth_service import AuthService
from users.user_type import UserType
from auth.user_factory import UserFactory
import traceback
import sys

def render():
    st.subheader("Create Account")
    
    name = st.text_input("Full Name 12323412 vewfewf", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    role = st.selectbox("Select Role", [role.value for role in UserType], key="signup_role")
    
    
    if st.button("Register", key="signup_button"):
        # Input validation
        if not name.strip():
            st.error("Please enter your full name")
            return
            
        if not email.strip():
            st.error("Please enter your email")
            return
            
        if not password.strip():
            st.error("Please enter your password")
            return

        # Debug information
        st.write("Debug Information:")
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Role: {role}")

        try:
            st.write("Step 1: Creating user...")
            user = UserFactory.create_user(role, name, email, password)
            st.write("User created successfully")
        except Exception as e:
            st.error("Error creating user:")
            st.error(str(e))
            st.error(traceback.format_exc())
            return

        try:
            st.write("Step 2: Getting AuthService instance...")
            auth_service = AuthService.get_instance()
            st.write("AuthService instance obtained")
        except Exception as e:
            st.error("Error getting AuthService:")
            st.error(str(e))
            st.error(traceback.format_exc())
            return

        try:
            st.write("Step 3: Registering user...")
            result = auth_service.register_user(user)
            st.write("Registration complete")
            st.success(result)
        except Exception as e:
            st.error("Error registering user:")
            st.error(str(e))
            st.error(traceback.format_exc())
            return