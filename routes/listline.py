from flask import Blueprint, request, jsonify
from models import db, Listline
from flask_jwt_extended import (
    jwt_required
)

route_listlines = Blueprint('route_listlines', __name__)

@route_listlines.route('/listlines', methods=['GET','POST'])
@route_listlines.route('/listlines/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def listlines(id=None):
    if request.method == 'GET':
        if id is not None:
            listline = Listline.query.get(id)
            if listline:
                return jsonify(listline.serialize()), 200
            else:
                return jsonify({"listline":"Not found"}), 404
        else:
            listlines = Listline.query.all()
            listlines = list(map(lambda listline: listline.serialize(),listlines))
            return jsonify(listlines), 200
    
    if request.method == 'POST':
        line=request.json.get('line')
        lista_id=request.json.get('lista_id') 
        if not line:
            return jsonify({"msg": "line is required"}), 422  
        if not lista_id:
            return jsonify({"msg": "lista_id is required"}), 422  
           
        listline = Listline()
        listline.line = line
        listline.lista_id = lista_id

        db.session.add(listline)
        db.session.commit()

        return jsonify(listline.serialize()), 201
    
    if request.method == 'PUT':
        
        listline = Listline.query.get(id)
        listline.line = request.json.get('line')
        listline.lista_id = request.json.get('lista_id')

        db.session.commit()

        return jsonify(listline.serialize()), 200

    if request.method == 'DELETE':
        
        listline = Listline.query.get(id)
        db.session.delete(listline)
        db.session.commit()

        return jsonify({'listline':'Deleted'}), 200