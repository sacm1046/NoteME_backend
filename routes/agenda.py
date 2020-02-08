from flask import Blueprint, request, jsonify
from models import db, Agenda
from flask_jwt_extended import (
    jwt_required
)

route_agendas = Blueprint('route_agendas', __name__)

@route_agendas.route('/agendas', methods=['GET','POST'])
@route_agendas.route('/agendas/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def agendas(id=None):
    if request.method == 'GET':
        if id is not None:
            agenda = Agenda.query.get(id)
            if agenda:
                return jsonify(agenda.serialize()), 200
            else:
                return jsonify({"agenda":"Not found"}), 404
        else:
            agendas = Agenda.query.all()
            agendas = list(map(lambda agenda: agenda.serialize(),agendas))
            return jsonify(agendas), 200
    
    if request.method == 'POST':
        title = request.json.get('title')
        user_id = request.json.get('user_id')
        if not title:
            return jsonify({"msg": "title is required"}), 422 
        if not user_id:
            return jsonify({"msg": "user_id is required"}), 422 

        agenda = Agenda()
        agenda.title = title
        agenda.user_id = user_id

        db.session.add(agenda)
        db.session.commit()

        return jsonify(agenda.serialize()), 201
    
    if request.method == 'PUT':
        
        agenda = Agenda.query.get(id)
        agenda.title = request.json.get('title')
        agenda.user_id = request.json.get('user_id')

        db.session.commit()

        return jsonify(agenda.serialize()), 200

    if request.method == 'DELETE':
        
        agenda = Agenda.query.get(id)
        db.session.delete(agenda)
        db.session.commit()

        return jsonify({'agenda':'Deleted'}), 200