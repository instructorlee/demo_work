from flask import flash
from app.config.mysqlconnector import MySQLConnection
from app.models.user import User
from app.models.base_class import BaseClass

# comment

class Pet(BaseClass):

    """
    
    """

    json_fields = ['id', 'name', 'species', 'tricks', 'happiness', 'energy', 'likes_count']

    def __init__(self, data): # data is a dictionary
        
        self.id = data['id']
        self.name = data['name']
        self.species = data['species']
        self.tricks = data['tricks']
        self.happiness = data['happiness']
        self.energy = data['energy']
        self.created_at = data['created_at']
        self.likes_count = data['likes_count'] if 'likes_count' in data else 0
        self.file_name = data['file_name']

        self.owner = None
        self.likers = []

    def is_liker(self, user_id):
        found = False

        for liker in self.likers:
            if liker.id == user_id:
                found = True

        return found

    @classmethod
    def add(cls, data):
        query = """
            INSERT INTO
                pets
            (name, species, tricks, happiness, energy, file_name)
            VALUES
            (%(name)s, %(species)s, %(tricks)s, %(happiness)s, %(energy)s, %(file_name)s )
        """

        result = MySQLConnection('z_demo').query_db(query, data)

        if not result:
            flash("Could not save pet!")

        return result

    @classmethod
    def delete(cls, id):
        query = """
            DELETE FROM
                pets
            WHERE
                pets.id = %(id)s
        """
        
        return MySQLConnection('z_demo').query_db(query, {"id": id})

    @classmethod
    def get_all(cls):
        query ="""
            SELECT 
                *,
                (
                    SELECT
                        count(id) AS likes_count
                    FROM
                        favorites
                        
                        WHERE
                            favorites.pet_id = pets.id
                ) AS likes_count -- alias
                
            FROM 
                pets
                
            LEFT JOIN users ON users.id = pets.user_id
        """

        results = MySQLConnection('z_demo').query_db(query)
        all_pets = []
        for row in results:
            pet = cls(row)
            pet.owner = User({
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email_address": row['email_address'],
                "password": row['password'],
            })
            
            all_pets.append(pet)

        return all_pets
    
    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT 
                * 
            FROM 
                pets

            LEFT JOIN users ON users.id = pets.user_id

            LEFT JOIN favorites ON favorites.pet_id = pets.id
            LEFT JOIN users AS fav_users ON fav_users.id = favorites.user_id

            WHERE
                pets.id = %(id)s
            ;
        """

        results = MySQLConnection('z_demo').query_db(query, {"id": id})

        if not results:
            return False
        
        pet = cls(results[0])
        pet.owner = User({
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email_address": results[0]["email_address"],
            "password": results[0]["password"]
        })

        for row in results:
            if row['fav_users.id'] is not None:
                pet.likers.append(User({
                    "id": row["fav_users.id"],
                    "first_name": row["fav_users.first_name"],
                    "last_name": row["fav_users.last_name"],
                    "email_address": row["fav_users.email_address"],
                    "password": row["fav_users.password"]
                }))

        return pet

    @classmethod
    def update(cls,data):
        query = """
            UPDATE
                pets
            SET
                name = %(name)s,
                species = %(species)s,
                tricks = %(tricks)s,
                happiness = %(happiness)s,
                energy = %(energy)s,
                file_name = %(file_name)s
                
            WHERE
                pets.id = %(id)s
        """

        return MySQLConnection('z_demo').query_db(query, data)

    @classmethod
    def like(cls, pet_id, user_id):
        query = """
            INSERT INTO
            favorites
            (user_id, pet_id)
            VALUES
            (%(user_id)s, %(pet_id)s)
        """
        return MySQLConnection('z_demo').query_db(query, {"pet_id": pet_id, "user_id": user_id})

    @classmethod
    def unlike(cls, pet_id, user_id):
        query = """
            DELETE FROM
                favorites

            WHERE
                pet_id=%(pet_id)s AND user_id=%(user_id)s
        """

        return MySQLConnection('z_demo').query_db(query, {"pet_id": pet_id, "user_id": user_id})
