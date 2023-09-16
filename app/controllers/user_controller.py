from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from werkzeug.exceptions import Conflict

from app.databases.postgres import postgres_connection
from app.models import User, UserProfile


@jwt_required()
def create_user(user_input):
    # sanitize user input
    cleaned_data = sanitize(["email", "username", "password"], user_input)
    username = cleaned_data["username"]
    email = cleaned_data["email"]
    hashed_password = cleaned_data["password"]

    # check for duplicate users
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user is not None:
        raise Conflict("The user with this username or email already exists.")

    # create new user
    new_user = User(username, email, hashed_password)
    postgres_connection.db.session.add(new_user)
    postgres_connection.db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


def get_all_users():
    pass


def get_user():
    pass


@jwt_required()
def get_user_by_id(user_id):
    identity = get_jwt_identity()
    allowed_services = ["access_control_service"]

    # Check if identity is in the list of allowed services
    if identity not in allowed_services or is_admin():
        return jsonify({"msg": "Access denied"}), 403  # Forbidden

    # Try to find the user by user_id, username, or email
    try:
        # Attempt to convert user_id to an integer (assuming it's user_id)
        user_id = int(user_id)

        # Query the User table by user_id
        user = User.query.get(user_id)

    except ValueError:
        # If user_id cannot be converted to an integer, assume it's either a username or email
        user = User.query.filter(
            (User.username == user_id) | (User.email == user_id)
        ).first()

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    # Retrieve the user's profile (if available)
    user_profile = UserProfile.query.filter_by(user_id=user.user_id).first()

    # Create a dictionary to represent the user's data
    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "hashed_password": user.password_hash,
        "verified": user.verified
    }

    # Add profile information if available
    if user_profile:
        user_data["profile"] = {
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "date_of_birth": user_profile.date_of_birth,
            # Add other profile fields as needed
        }

    return jsonify(user_data), 200


@jwt_required()
def update_user(user_id, user_data):
    identity = get_jwt_identity()
    allowed_services = ["access_control_service"]

    # Check if identity is in the list of allowed services
    if identity not in allowed_services or is_admin():
        return jsonify({"msg": "Access denied"}), 403  # Forbidden

    # Try to find the user by user_id, username, or email
    try:
        # Attempt to convert user_id to an integer (assuming it's user_id)
        user_id = int(user_id)

        # Query the User table by user_id
        user = User.query.get(user_id)

    except ValueError:
        # If user_id cannot be converted to an integer, assume it's either a username or email
        user = User.query.filter(
            (User.username == user_id) | (User.email == user_id)
        ).first()

    if user is None:
        return jsonify(msg="User not found"), 404

    # Update user's data
    for key, value in user_data.items():
        setattr(user, key, value)

    postgres_connection.db.session.commit()

    return jsonify(msg="User updated successfully"), 200


def delete_user(user_id):
    pass


def sanitize(allowed_fields, user_data):
    # Create a new dictionary to store the cleaned data
    cleaned_data = {}

    # Iterate through the user-provided dictionary
    for key, value in user_data.items():
        # Check if the field is in the allowed_fields list
        if key in allowed_fields:
            # If it's allowed, add it to the cleaned_data dictionary
            cleaned_data[key] = value

    # Return the cleaned data
    return cleaned_data


# We will utilize this function in the future.
# Users with an admin role will have access to view information for any user.
def is_admin():
    return False
