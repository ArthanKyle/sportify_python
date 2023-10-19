from flask import jsonify, request
from jwt import decode, InvalidTokenError

def check_token(req, res, next):
    token = request.headers.get("Authorization")
    
    if token:
        token = token.split(" ")[1]
        
        try:
            decoded = decode(token, "qwe1234", algorithms=["HS256"])
            next()
        except InvalidTokenError:
            return jsonify({"success": 0, "message": "Invalid Token..."}), 401
    else:
        return jsonify({"success": 0, "message": "Access Denied! Unauthorized User"}), 401
