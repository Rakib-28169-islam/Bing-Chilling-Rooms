from database.mongodb import users_collection
from auth.user_factory import UserFactory
from users.user_type import UserType

class AuthService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AuthService()
        return cls._instance   
    
    def register_user(self,user):
        if users_collection.find_one({
            "email":user.getEmail()
        }):
            return "User already exists!"
        users_collection.insert_one({
            "name":user.getName(),
            "email":user.getEmail(),
            "password":user.getPassword(),
            "user_type":user.getUserType()
        }) 
        
        return f"User {user.getName()} registered successfully as {user.getUserType()}."
    
    def login_user(self,user):
        if users_collection.find_one({
            "email":user.getEmail(),
            "password":user.getPassword()
        }):
            return True,f"User {user.getName()} logged in successfully." 
        return False,"Invalid credentials!"
    
    def get_user(self,email,password):
        user = users_collection.find_one({"email":email , "password":password})
        if user:
            return UserFactory.create_user(user["user_type"],user["name"],user["email"],user["password"]),"User found!"
        return None,"User not found!"
        
        