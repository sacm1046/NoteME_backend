from flask import Blueprint, request, jsonify
from models import db, Agenda
from flask_jwt_extended import (
    jwt_required
)

route_agendas = Blueprint('route_agendas', __name__)

@route_agendas.route('/agendas', methods=['GET','POST'])
@route_agendas.route('/agendas/user/<int:user_id>', methods=['GET','POST'])
@route_agendas.route('/agendas/<int:id>', methods=['GET','PUT','DELETE'])
@route_agendas.route('/agendas/user/<int:user_id>/agenda/<int:id>', methods=['GET, POST'])
@jwt_required
def agendas(user_id=None, id=None):
    if request.method == 'GET':
        if id is not None and user_id is not None:
            agenda = Agenda.query.filter_by(user_id=user_id, id=id).first()
            if agenda:
                return jsonify(agenda.serialize()), 200
            else:
                return jsonify({"agenda":"Not found"}), 404
        elif id is not None:
            agenda = Agenda.query.get(id)
            if agenda:
                return jsonify(agenda.serialize()), 200
            else:
                return jsonify({"agenda":"Not found"}), 404
        elif user_id is not None:
            agendas = Agenda.query.filter_by(user_id = user_id).all()
            agendas = list(map(lambda agenda: agenda.serialize(),agendas))
            return jsonify(agendas), 200
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