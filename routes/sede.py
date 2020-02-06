from flask import Blueprint, request, jsonify
from models import db, Sede
from flask_jwt_extended import (
    jwt_required
)

route_sedes = Blueprint('route_sedes', __name__)

@route_sedes.route('/sedes', methods=['GET','POST'])
@route_sedes.route('/sedes/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def sedes(id=None):
    if request.method == 'GET':
        if id is not None:
            sede = Sede.query.get(id)
            if sede:
                return jsonify(sede.serialize()), 200
            else:
                return jsonify({"sede":"Not found"}), 404
        else:
            sedes = Sede.query.all()
            sedes = list(map(lambda sede: sede.serialize(),sedes))
            return jsonify(sedes), 200
    
    if request.method == 'POST':
        name=request.json.get('name')
        if not name:
            return jsonify({"msg": "name is required"}), 422  
        sede = Sede.query.filter_by(name=name).first()
        if sede:
            return jsonify({"msg": "Nombre de sede ocupado"}), 422          

        sede = Sede()
        sede.name = name

        db.session.add(sede)
        db.session.commit()

        return jsonify(sede.serialize()), 201
    
    if request.method == 'PUT':
        
        sede = Sede.query.get(id)
        sede.name = request.json.get('name')

        db.session.commit()

        return jsonify(sede.serialize()), 200

    if request.method == 'DELETE':
        
        sede = Sede.query.get(id)
        db.session.delete(sede)
        db.session.commit()

        return jsonify({'sede':'Deleted'}), 200