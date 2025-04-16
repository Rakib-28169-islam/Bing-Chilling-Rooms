# users/User.py 
from users.user_type import UserType
from database.mongodb import users_collection
class User:
    
    def __init__(self,name,email,password,user_type:UserType):
        self.__userId = None
        self.__name = name
        self.__email = email
        self.__password = password
        self.__userType = user_type
        self._id = None  # MongoDB _id
        
     
    def getName(self):
        return self.__name
    def getEmail(self):
        return self.__email
    def getPassword(self):
        return self.__password
    def getUserType(self):
        return self.__userType.value
    def getId(self):
        return self._id
    def showRooms(self):
        return "Showing rooms"
    def browse_listings(self):
        """Default browse listings method"""
        return f"{self.getName()} is browsing property listings."    
    

# user = User("james","james@123","1234",UserType.ADMIN)
# print(user.showRooms())    