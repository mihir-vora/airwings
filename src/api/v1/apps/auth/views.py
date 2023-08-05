from db import bcrypt
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from itsdangerous import URLSafeTimedSerializer
from marshmallow.exceptions import ValidationError

from .models import User
from .schemas import UserSchema
from .send_email import send_mail



class UserRegistration(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            user_data = UserSchema().load(json_data)
        except ValidationError as err:
            return {'message': 'Validation error', 'errors': err.messages}, 400

        email = user_data['email']
        if self.is_email_exists(email):
            return {'message': 'enter email are already exists, pls enter different email!'}, 400

        hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user_data['password'] = hashed_password
        user_obj = User(**user_data)
        send_mail(email, json_data)
        user_obj.save()
        return {
            "status": "success",
            "detail": "user created successfully",
            "data" : UserSchema().dump(user_obj)
        }, 201

    def is_email_exists(self, email):
        return User.query.filter_by(email=email).first() is not None

class UserLogin(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = UserSchema(only=('email', 'password')).load(json_data)
        except ValidationError as err:
            return {
                'message': 'Validation Error',
                'errors': err.messages
            }, 400

        user = self.authenticate_user(data['email'], data['password'])

        if not user:
            return {'message': 'Invalid credentials!'}, 400

        generate_access_token = create_access_token(identity=user.id_)
        return {
            'access_token': generate_access_token
        }, 200

    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return None

        if not user.is_active:
            return None

        return user



class ActivateAccount(Resource):
    def get(self, token):
        # Verify the activation token and get the user's email
        serializer = URLSafeTimedSerializer('kjfjk1kj2kjkj32jkjksj2j1kjk1jwewkjfjsfkjbk2jkjkj')
        try:
            email = serializer.loads(token, salt='activate', max_age=300)
        except:
            return {'message': 'Activation link is invalid or expired.'}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'message': 'Activation link is invalid or expired.'}, 400
        if user.is_active:
            return {'message': 'Account already activated.'}, 400

        # Activate the user account
        user.is_active = True
        user.save()
        return {'message': 'Account activated successfully!'}, 200
