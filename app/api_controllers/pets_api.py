from app import app
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from app.models.pet import Pet
from app.models.user import User


@app.route('/api/pet', methods=['POST'])
def api_add_pet():
    id = Pet.add(request.get_json())
    return jsonify(Pet.get_by_id(id).serialize()), 201

@app.route('/api/pet/<int:id>')
def api_get_pet(id):
    return jsonify(Pet.get_by_id(id).serialize()), 200

@app.route('/api/pet/delete/<int:id>')
def api_delete_pet(id):
    pass

@app.route('/pet/like/<int:id>')
def api_like_pet(id):
    pass

@app.route('/pet/unlike/<int:id>')
def api_unlike_pet(id):
    pass

@app.route('/api/pet')
def api_get_all_pets():
    return jsonify([pet.serialize() for pet in Pet.get_all()]), 200
