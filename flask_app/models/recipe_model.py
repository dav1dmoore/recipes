from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE
from flask_app.models.user import User


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        
        if data['name'] == "":
            flash("Name must not be empty", "error_registration_name")
            is_valid = False

        if data['description'] == "":
            flash("Description must not be empty", "error_registration_description")
            is_valid = False

        if data['cooked_date'] == "":
            flash("Cooked date must not be empty", "error_registration_cooked_date")
            is_valid = False
        
        if data['instructions'] == "":
            flash("Instructions must not be empty", "error_registration_instructions")
            is_valid = False

        return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, cooked_date, under_30, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30)s, %(users_id)s);" 

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id;"

        result = connectToMySQL(DATABASE).query_db(query)

        return result
    
    @classmethod
    def get_single_recipe(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result[0]

    @classmethod
    def delete_recipe(cls, data):

        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_recipe_to_edit(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)

        return result[0]
    
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET recipes WHERE recipes.id = %(id)s;"

        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_date = %(cooked_date)s, under_30 = %(under_30)s,  updated_at = NOW() WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)