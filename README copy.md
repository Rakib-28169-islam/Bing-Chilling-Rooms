# Airbnb Clone

A Streamlit-based Airbnb clone with user authentication and role-based access control.

## Features

- User Authentication (Sign In/Sign Up)
- Role-based Access Control (Admin/Host/Guest)
- Dynamic Dashboard based on User Role
- MongoDB Database Integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
- Copy `.env.example` to `.env`
- Update the MongoDB connection string in `.env`

3. Run the application:
```bash
streamlit run main.py
```

## User Roles

- **Admin**: Can manage users, view reports, and browse listings
- **Host**: Can create listings, manage bookings, and view earnings
- **Guest**: Can browse listings and book accommodations

## Project Structure

```
├── auth/              # Authentication related code
├── database/          # Database configuration
├── pages/            # Streamlit pages
├── proxy/            # User proxy for role-based access
├── users/            # User type definitions
├── .env              # Environment variables
├── main.py           # Main application entry
 