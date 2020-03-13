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
        user.password = bcrypt.generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        #sendMail("Bienvenid@ "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Bienvenid@ "+user.fullname)

        return jsonify(user.serialize()), 201
    
    if request.method == 'PUT':
        user = User.query.get(id)
        user.fullname = request.json.get('fullname')
        user.isAdmin = request.json.get('isAdmin')
        user.active = request.json.get('active')

        db.session.commit()

        #sendMail("Hola "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Modificación realizada con éxito, "+user.fullname)

        return jsonify(user.serialize()), 200

    if request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        #sendMail("Hasta pronto "+user.fullname , user.username, "cm.seb90@gmail.com", user.username, "Usuario eliminado con éxito")

        return jsonify({'user':'Deleted'}), 200