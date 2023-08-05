from flask import Blueprint
from .views import (
    UserRegistration,
    UserLogin,
    ActivateAccount
)
from db import api

auth_bp = Blueprint('auth', __name__, url_prefix='auth')

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(ActivateAccount, '/activate/<string:token>')
