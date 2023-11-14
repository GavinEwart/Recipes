from flask import render_template, redirect, request, session, url_for, flash
from flask_app import app
from flask_app.models import user  # Import only the User class
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app) # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller



# Read Users Controller

@app.route('/')
def welcome_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user_data = {"email": email, "password": password}

        # Check if user is valid
        user_in_db = user.User.get_by_email(user_data)
        if user_in_db and bcrypt.check_password_hash(user_in_db.password, password):
            # Add user_id to session upon successful login
            session['user_id'] = user_in_db.id
            return redirect('/recipes')
        else:
            flash("Invalid email/password", "login")
            return redirect('/')
    else:
        flash("Invalid form data", "login")
        print(flash)
        return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password']
    }

    confirm_password = request.form['confirm_password']

    if user.User.validate_user(user_data, confirm_password):
        user.User.create_user(user_data, confirm_password)
        flash("Account Created", "success")
        return redirect('/')
    else:
        flash("Invalid registration data", "register")
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/recipes')
def homepage():
    if 'user_id' in session:
        user_id = session['user_id']
        user_in_db = user.User.get_by_id(user_id)

        # Fetch all recipes
        all_recipes = Recipe.get_all_recipes()
        return render_template('home_page.html', user_in_db=user_in_db, recipes=all_recipes)
    else:
        flash("Please log in to access this page", "login")
        return redirect(url_for('welcome_page'))
# Update Users Controller



# Delete Users Controller


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.