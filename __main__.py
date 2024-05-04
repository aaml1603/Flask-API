from flask import Flask, request, jsonify
from flask_cors import CORS
from modules import mongodb
import re
from icecream import ic
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)
database = mongodb.Database()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

@app.route('/register', methods=['POST'])
def reg():
    register_data = request.json
    if 'email' not in register_data: 
        return 'Please provide an email address.'
    elif 'username' not in register_data or len(register_data['username']) <= 6: 
        return 'Username must be longer than 6 characters.'
    elif 'password' not in register_data or len(register_data['password']) <= 10: 
        return 'Password must be longer than 10 characters.'
    else:
        if is_valid_email(register_data['email']):
            register = database.register(register_data['email'], register_data['username'], register_data['password'])
            ic(register)
            if register[0]:
                return 'Successfully registered account!'
            else:
                return register[1]
        else:
            return 'Email is not a valid email address.'

@app.route('/login', methods=['POST'])
def log():
    login_data = request.json
    if 'username' not in login_data:
        return 'Please provide a username.'
    elif 'password' not in login_data:
        return 'Please provide a password'
    else:
        login = database.login(login_data['username'], login_data['password'])
        ic(login)
        if login[0]:
            return 'Login successful!'  
        else:
            return 'Invalid username or password.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
