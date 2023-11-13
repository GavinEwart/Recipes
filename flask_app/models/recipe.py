from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.controllers import recipes, users

class Recipe:
    db = "recipes_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.instructions = data.get('instructions')
        self.under_30 = data.get('under_30')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.date_made = data.get('date_made')
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
            WHERE id = %(recipe_id)s
            LIMIT 1;
        """
        result = connectToMySQL(cls.db).query_db(query, {'recipe_id': recipe_id})

        return cls(result[0]) if result else None
    
    @classmethod
    def update_recipe(cls, recipe_id, data):
        query = """
            UPDATE recipes
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,
                under_30 = %(under_30)s, date_made = %(date_made)s
            WHERE id = %(recipe_id)s;
        """
        data['recipe_id'] = recipe_id
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_recipe(cls, recipe_id):
        query = """
            DELETE FROM recipes
            WHERE id = %(recipe_id)s;
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
            SELECT id, user_id, name, description, instructions, under_30, created_at, updated_at, date_made
            FROM recipes;
        """
        results = connectToMySQL(cls.db).query_db(query)

        return [cls(result) for result in results] if results else []