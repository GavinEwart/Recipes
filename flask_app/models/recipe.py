from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Recipe:
    db = "recipes_schema" #which database are you using for this project
    def __init__(self, data):
        self.recipes_table_id = data.get('recipes_table_id')
        self.user_id = data.get('user_id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.instructions = data.get('instructions')
        self.under_30 = data.get('under_30')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.date_made = data.get('date_made') 
        self.made_by_user = None
        #What needs to be added here for class association?

    @classmethod
    def get_user_recipes(cls, user_id):
        query = """
            SELECT * FROM recipes
            WHERE user_id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})

        return [cls(result) for result in results] if results else []
    
    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        query = """
            SELECT * FROM recipes
            WHERE recipes_table_id = %(recipe_id)s
            LIMIT 1;
        """
        result = connectToMySQL(cls.db).query_db(query, {'recipe_id': recipe_id})

        return cls(result[0]) if result else None
    
    @classmethod
    def create_recipe(cls, data):
        query = """
            INSERT INTO recipes (user_id, name, description, instructions, under_30, date_made)
            VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s);
        """
        result = connectToMySQL(cls.db).query_db(query, data)

        if result:
            return result
        else:
            return None
    
    @classmethod
    def update_recipe(cls, recipe_id, data):
        query = """
            UPDATE recipes
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,
                under_30 = %(under_30)s, date_made = %(date_made)s
            WHERE recipes_table_id = %(recipe_id)s;  # Change this line
        """
        data['recipe_id'] = recipe_id
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_recipe(cls, recipe_id):
        query = """
            DELETE FROM recipes
            WHERE recipes_table_id = %(recipe_id)s;
        """
        connectToMySQL(cls.db).query_db(query, {'recipe_id': recipe_id})

    @classmethod
    def get_user_recipes(cls, users_id):
        query = """
            SELECT * FROM recipes
            WHERE user_id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'users_id': users_id})

        return [cls(result) for result in results] if results else []
    
    @classmethod
    def get_all_recipes(cls):
        query = """
            SELECT *
            FROM recipes
            JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []

        for result in results:
            one_result = cls(result)

            one_recipe_user_data = {
            'id': result['id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['created_at'],
            'updated_at': result['updated_at']
            }
            made_by_user = user.User(one_recipe_user_data)
            one_result.made_by_user = made_by_user
            all_recipes.append(one_result)

        return all_recipes
    
    @classmethod 
    def get_recipe_by_user_id(cls, recipes_table_id):
        query ="""
                SELECT *
                FROM recipes
                JOIN users ON users.id = recipes.user_id
                WHERE recipes_table_id = %(id)s;
                """
        data = {
            'id': recipes_table_id
        }
        results = connectToMySQL(cls.db).query_db(query, data)

        return cls(results[0]) if results else None
        



