
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "recipes_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added here for class association?


    @staticmethod #method for making sure every input in the form is filled out a filled out correctly
    def validate_user(user, confirm_password=None, data=None):
        is_valid = True

        if data is None: 
            # This is a login attempt
            user_in_db = User.get_by_email(user)
            if not user_in_db or not bcrypt.check_password_hash(user_in_db.password, user['password']):
                flash("Invalid Email/Password")
                is_valid = False

        else:
            # This is a registration attempt
            if len(user['first_name']) < 1:
                flash("Missing first name")
                is_valid = False

            if len(user['last_name']) < 1:
                flash("Missing last name")
                is_valid = False

            if not EMAIL_REGEX.match(user['email']):
                flash("Invalid email address")
                is_valid = False

            if User.email_exists(user['email']):
                flash("Email already exists")
                is_valid = False

            if len(user['password']) < 8 or not any(char.isdigit() for char in user['password']) or not any(char.isupper() for char in user['password']):
                flash("Password must be at least 8 characters long, contain at least 1 capital letter, and 1 number")
                is_valid = False

            if user['password'] != confirm_password:
                flash("Your password does not match")
                is_valid = False

            return is_valid
    
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                LIMIT 1
                ;
                """
        result = connectToMySQL(cls.db).query_db(query, data)

        return cls(result[0]) if result else None
    @classmethod
    def email_exists(cls, email):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                ;
                """
        result = connectToMySQL(cls.db).query_db(query, {'email': email})

        return len(result) > 0

    @classmethod
    def create_user(cls, data, confirm_password):

        if not cls.validate_user(data, confirm_password):
            return False
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data['password'] = hashed_password

        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                ;
                """
        result = connectToMySQL(cls.db).query_db(query, data)

        if result:
            return result
        else:
            return None




    # Create Users Models



    # Read Users Models



    # Update Users Models



    # Delete Users Models