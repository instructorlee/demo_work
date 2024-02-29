import re
from flask import flash
from app.config.mysqlconnector import MySQLConnection

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    DB = "z_demo"

    def __init__(self, data):
        print(data)
        
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']

        self.pets = []

    @classmethod
    def get_all(cls):
        query ="""
            SELECT 
                * 
            FROM users;
        """

        results = MySQLConnection(cls.DB).query_db(query)

        return [cls(row) for row in results]

    @classmethod
    def get_by_id(cls, id):
        from app.models.pet import Pet
        
        query = """
            SELECT 
                * 
            FROM users

            LEFT JOIN pets ON pets.user_id = users.id

            WHERE
                users.id = %(id)s
            ;
        """

        results = MySQLConnection('z_demo').query_db(query, {"id": id})

        if not results:
            return False
        
        user = cls(results[0])

        for row in results:
            if row['pets.id'] is not None:
                user.pets.append(Pet({
                    "id": row['pets.id'],
                    "name": row['name'],
                    "species": row['species'],
                    "happiness": row['happiness'],
                    "energy": row['energy'],
                    "tricks": row['tricks'],
                    "created_at": row['created_at'],
                }))

        return user
    
    @classmethod
    def get_by_email(cls, email_address):
        
        query = """
            SELECT 
                * 
            FROM users

            WHERE
                users.email_address = %(email_address)s
            ;
        """

        results = MySQLConnection('z_demo').query_db(query, {"email_address": email_address})

        if results:
            return cls(results[0])
        else:
            return False

    @classmethod
    def create(cls, user_data):
        query = """
            INSERT INTO
                users
                (first_name, last_name, email_address, password)
                VALUES
                (%(first_name)s, %(last_name)s, %(email_address)s, %(password)s)
        """

        return MySQLConnection('z_demo').query_db(query, user_data)
    
    @staticmethod
    def validate_new_user(user_data):
        is_valid = True

        """
            check email format
            unique email address

            compare passwords
            password requirements
        """
        if not EMAIL_REGEX.match(user_data['email_address']):
            flash("Invalid email format")
            is_valid = False

        elif User.get_by_email(user_data['email_address']):
            flash("Email already used")
            is_valid = False

        if user_data['password'] != user_data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False

        return is_valid
