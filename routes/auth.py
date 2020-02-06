from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import db, User
from libs.functions import sendMail
bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        return jsonify({"msg": "username is required"}), 422
    if not password:
        return jsonify({"msg": "password is required"}), 422
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"msg": "username not found"}), 404
    pw_hash = bcrypt.generate_password_hash(password)
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "username/password is wrong"}), 401
        
@auth.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    fullname = request.json.get('fullname')
    phone = request.json.get('phone')
    password = request.json.get('password')
    if not username:
        return jsonify({"msg": "username is required"}), 422
    if not fullname:
        return jsonify({"msg": "fullname is required"}), 422
    if not phone:
        return jsonify({"msg": "phone is required"}), 422              
    if not password:
        return jsonify({"msg": "password is required"}), 422
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"msg": "username is taken"}), 422
    user = User()
    user.username = username
    user.fullname = fullname
    user.phone = phone
    user.password = bcrypt.generate_password_hash(password)
    db.session.add(user)
    db.session.commit()

    sendMail("Welcome "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Welcome "+user.fullname)

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({"msg": "username/password is wrong"}), 401
