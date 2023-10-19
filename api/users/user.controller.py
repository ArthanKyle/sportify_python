from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from bcrypt import hashpw, gensalt, checkpw
from jwt import encode, decode, InvalidTokenError
from user.service import create, getUserByUserId, getUsers, updateUser, deleteUser, getUserByUserEmail, emailCheck

app = Flask(__name__)
api = Api(app)

class UserController(Resource):
    def post(self):
        body = request.get_json()
        salt = gensalt(10)
        body["password"] = hashpw(body["password"].encode('utf-8'), salt)
        create(body)
        return jsonify(success=1, data=body), 200

    def get(self):
        results = getUsers()
        return jsonify(success=1, data=results), 200

class UserByIdController(Resource):
    def get(self, user_id):
        results = getUserByUserId(user_id)
        if not results:
            return jsonify(success=0, message="Record not found"), 404
        results["password"] = None
        return jsonify(success=1, data=results), 200

    def patch(self):
        body = request.get_json()
        salt = gensalt(10)
        body["password"] = hashpw(body["password"].encode('utf-8'), salt)
        results = updateUser(body)
        if not results:
            return jsonify(success=0, message="Failed to update user"), 404
        return jsonify(success=1, message="Updated successfully"), 200

    def delete(self):
        data = request.get_json()
        results = deleteUser(data)
        if not results:
            return jsonify(success=0, message="Record not found"), 404
        return jsonify(success=1, message="User deleted successfully"), 200

class UserLoginController(Resource):
    def post(self):
        body = request.get_json()
        results = getUserByUserEmail(body["email"])
        if not results:
            return jsonify(success=0, data="Invalid email or password"), 200
        result = checkpw(body["password"].encode('utf-8'), results["password"])
        if result:
            results["password"] = None
            jsontoken = encode({"result": results}, "qwe1234", algorithm="HS256")
            return jsonify(success=1, message="Login successfully", token=jsontoken), 200
        else:
            return jsonify(success=0, data="Invalid email or password"), 200

class UserByEmailController(Resource):
    def post(self):
        body = request.get_json()
        results = emailCheck(body["email"])
        if not results:
            return jsonify(success=False, message="Error checking email existence"), 500
        if not results:
            return jsonify(success=True, message="Email does not exist."), 200
        else:
            return jsonify(success=False, message="Email already exists!"), 200

# Routes
api.add_resource(UserController, "/create")
api.add_resource(UserController, "/")
api.add_resource(UserByIdController, "/<string:user_id>")
api.add_resource(UserByIdController, "/")
api.add_resource(UserLoginController, "/login")
api.add_resource(UserByEmailController, "/email-check")

if __name__ == "__main__":
    app.run(debug=True)
