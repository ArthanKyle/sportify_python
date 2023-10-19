from flask import Blueprint, request
from flask_restful import Resource, Api

from user_controller import (
    create_user,
    get_users,
    get_user_by_user_id,
    update_users,
    delete_user,
    login,
    get_user_by_user_email,
)
from auth.token_validation import check_token

user_blueprint = Blueprint("user", __name__)
api = Api(user_blueprint)

class UserCreate(Resource):
    def post(self):
        return create_user(request)

class Users(Resource):
    decorators = [check_token]

    def get(self):
        return get_users()

class UserById(Resource):
    decorators = [check_token]

    def get(self, user_id):
        return get_user_by_user_id(user_id)

    def patch(self):
        return update_users()

    def delete(self):
        return delete_user()

class UserLogin(Resource):
    def post(self):
        return login(request)

class UserByEmail(Resource):
    def post(self):
        return get_user_by_user_email(request)

# Routes
api.add_resource(UserCreate, "/create")
api.add_resource(Users, "/")
api.add_resource(UserById, "/<string:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserByEmail, "/email-check")

if __name__ == "__main__":
    pass
