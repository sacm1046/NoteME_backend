from flask import Blueprint, request, jsonify
from models import db, Lista
from flask_jwt_extended import (
    jwt_required
)

route_listas = Blueprint('route_listas', __name__)

@route_listas.route('/listas', methods=['GET','POST'])
@route_listas.route('/listas/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def listas(id=None):
    if request.method == 'GET':
        if id is not None:
            lista = Lista.query.get(id)
            if lista:
                return jsonify(lista.serialize()), 200
            else:
                return jsonify({"lista":"Not found"}), 404
        else:
            listas = Lista.query.all()
            listas = list(map(lambda lista: lista.serialize(),listas))
            return jsonify(listas), 200
    
    if request.method == 'POST':
        name=request.json.get('name')
        note_id=request.json.get('note_id') 
        if not name:
            return jsonify({"msg": "name is required"}), 422  
        if not note_id:
            return jsonify({"msg": "note_id is required"}), 422  
           
        lista = Lista()
        lista.name = name
        lista.note_id = note_id

        db.session.add(lista)
        db.session.commit()

        return jsonify(lista.serialize()), 201
    
    if request.method == 'PUT':
        
        lista = Lista.query.get(id)
        lista.name = request.json.get('name')
        lista.note_id = request.json.get('note_id')

        db.session.commit()

        return jsonify(lista.serialize()), 200

    if request.method == 'DELETE':
        
        lista = Lista.query.get(id)
        db.session.delete(lista)
        db.session.commit()

        return jsonify({'lista':'Deleted'}), 200