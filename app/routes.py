from flask import Blueprint, request, jsonify
from . import db
from .models import User  # Import the User model from the updated models.py file

routes = Blueprint('routes', __name__)

@routes.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user.
    Expects JSON: { "name": "string", "email": "string" }
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    try:
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/users', methods=['GET'])
def get_users():
    """
    Get a list of all users.
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a user by ID.
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update user information.
    Expects JSON: { "name": "string", "email": "string" }
    """
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by ID.
    """
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
