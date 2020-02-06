from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from libs.functions import sendMail
from flask_jwt_extended import (
    jwt_required
)

bcrypt = Bcrypt()
route_users = Blueprint('route_users', __name__)

@route_users.route('/users', methods=['GET','POST'])
@route_users.route('/users/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def users(id=None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({"user":"Not found"}), 404
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(),users))
            return jsonify(users), 200
    
    if request.method == 'POST':
        password = request.json.get('password')

        user = User()
        user.username = request.json.get('username')
        user.fullname = request.json.get('fullname')
        user.phone = request.json.get('phone')
        user.password = bcrypt.generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        sendMail("Welcome "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Welcome "+user.fullname)

        return jsonify(user.serialize()), 201
    
    if request.method == 'PUT':
        password = request.json.get('password')
        user = User.query.get(id)
        user.username = request.json.get('username')
        user.fullname = request.json.get('fullname')
        user.phone = request.json.get('phone')
        user.password = bcrypt.generate_password_hash(password)

        db.session.commit()

        sendMail("Hello "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Successfully update "+user.fullname)

        return jsonify(user.serialize()), 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        sendMail("Bye "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Correct user deleting")

        return jsonify({'user':'Deleted'}), 200