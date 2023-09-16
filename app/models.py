from datetime import datetime

from app.databases.postgres import postgres_connection
from flask_login import UserMixin
db = postgres_connection.db


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.role_id'))
                      )


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=user_roles, back_populates='users')
    verified = db.Column(db.Boolean, default=False)
    profile = db.relationship('UserProfile', back_populates='user', uselist=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f"<User {self.username}>"

    def get_id(self):
        return str(self.user_id)


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(10))
    users = db.relationship('User', secondary=user_roles, back_populates='roles')

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return f'<Role {self.role_name}>'


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    full_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.TIMESTAMP)
    profile_picture = db.Column(db.String(255))
    other_profile_info = db.Column(db.JSON)
    user = db.relationship('User', back_populates='profile')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f'<UserProfile {self.profile_id}>'
