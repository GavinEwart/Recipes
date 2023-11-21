# Recipes

## Overview

Recipe Share is a web application that allows users to share and manage their favorite recipes. Users can create, view, edit, and delete recipes. The project uses a MySQL database for data storage and is built using the Flask web framework.

## Features

- Create new recipes, including details such as name, description, instructions, and cook time.
- View a list of all recipes, including information about the user who created each recipe..
- Edit existing recipes to update their details.
- Delete recipes that users no longer want to share.

## Setup

To get a local copy up and running, follow these simple steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/GavinEwart/Recipes.git

2. Add clone into your VScode and open in an integrated terminal

3. Install the required dependencies by running the following command in your project directory:
   ```sh
   pipenv install

4. Start your shell
   ```sh
   pipenv shell

5. Start the Flask application:
   ```sh
   python server.py
  
6. Open your web browser and navigate to http://localhost:5000.

## What I Learned

### In this assignment, I gained valuable experience in several key areas:

- Database Operations: I learned how to perform one-to-many queries to retrieve and display data for tables, particularly when managing user-specific recipes.

- Login Validations: Implemented robust login validations to ensure data integrity and security. This included checking for required fields, verifying email uniqueness, and validating password complexity.

- Flash Messages: Leveraged Flask's flash messaging system to provide informative and user-friendly feedback for various actions, such as successful registrations, login failures, and invalid form submissions.

- MVC Implementation: Structured the application following the Model-View-Controller (MVC) pattern, separating concerns and making the codebase more modular and maintainable.

- Security Measures: Implemented measures to protect against potential security threats, including unauthorized access to pages and potential hacking attempts.

- User Authentication: Utilized Flask-Bcrypt for secure password hashing and validation during user registration and login processes.

- Dynamic HTML Templating: Integrated dynamic data into HTML templates using Flask's Jinja templating engine, allowing for the dynamic rendering of content.
  

Feel free to explore and modify the code as needed for your own projects.
