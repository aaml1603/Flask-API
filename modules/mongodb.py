import pymongo
from icecream import ic
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://aaml1603:Doral11386.@cluster0.lwei9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.accountsdb = self.client['accounts']
        self.userscol = self.accountsdb['users']
    
    def register(self, email, username, password):
        hashed_password = generate_password_hash(password)  # Securely hash the password
        user_data = {'email': email, 'username': username, 'password': hashed_password}
        email_query = {'email': email}
        username_query = {'username': username}
        x = self.userscol.find_one(email_query) 
        z = self.userscol.find_one(username_query)
        if x:
            return False, 'Email address already in use!'
        elif z:
            return False ,'Username is already in use!'
        else:
            self.userscol.insert_one(user_data)
            return True, 'Successfully registered'
        
    def login(self, username, password):
        query = {'username': username}
        user = self.userscol.find_one(query)
        if user:
            stored_hashed_password = user.get('password')
            print("Stored Hashed Password:", stored_hashed_password)  # Print stored hashed password for debugging
            print("Provided Password:", password)  # Print provided password for debugging
            password_match = check_password_hash(stored_hashed_password, password)
            if password_match:
                return True, 'Logged in!'
        return False, 'Invalid username or password.'