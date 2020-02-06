from flask import Blueprint, request, jsonify
from models import db, Profesor

from flask_jwt_extended import (
    jwt_required
)

route_profesores = Blueprint('route_profesores', __name__)

@route_profesores.route('/profesores', methods=['GET','POST'])
@route_profesores.route('/profesores/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def profesores(id=None):
    if request.method == 'GET':
        if id is not None:
            profesor = Profesor.query.get(id)
            if profesor:
                return jsonify(profesor.serialize()), 200
            else:
                return jsonify({"profesor":"Not found"}), 404
        else:
            profesores = Profesor.query.all()
            profesores = list(map(lambda profesor: profesor.serialize(),profesores))
            return jsonify(profesores), 200
    
    if request.method == 'POST':
        name=request.json.get('name')
        lastname = request.json.get('lastname')
        rut = request.json.get('rut')
        phone = request.json.get('phone')
        if not name:
            return jsonify({"msg": "name is required"}), 422
        if not lastname:
            return jsonify({"msg": "lastname is required"}), 422
        if not rut:
            return jsonify({"msg": "rut is required"}), 422
        if not phone:
            return jsonify({"msg": "phone is required"}), 422  
        profesor = Profesor.query.filter_by(rut=rut).first()
        if profesor:
            return jsonify({"msg": "rut de profesor ocupado"}), 422          

        profesor = Profesor()
        profesor.name = name
        profesor.lastname = lastname
        profesor.rut = rut
        profesor.phone = phone

        db.session.add(profesor)
        db.session.commit()

        return jsonify(profesor.serialize()), 201
    
    if request.method == 'PUT':
        
        profesor = Profesor.query.get(id)
        profesor.name = request.json.get('name')
        profesor.lastname = request.json.get('lastname')
        profesor.rut = request.json.get('rut')
        profesor.phone = request.json.get('phone')

        db.session.commit()

        return jsonify(profesor.serialize()), 200

    if request.method == 'DELETE':
        
        profesor = Profesor.query.get(id)
        db.session.delete(profesor)
        db.session.commit()

        return jsonify({'profesor':'Deleted'}), 200