from flask import Blueprint, request, jsonify
from models import db, Note
from flask_jwt_extended import (
    jwt_required
)

route_notes = Blueprint('route_notes', __name__)

@route_notes.route('/notes', methods=['GET','POST'])
@route_notes.route('/notes/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def notes(id=None):
    if request.method == 'GET':
        if id is not None:
            note = Note.query.get(id)
            if note:
                return jsonify(note.serialize()), 200
            else:
                return jsonify({"note":"Not found"}), 404
        else:
            notes = Note.query.all()
            notes = list(map(lambda note: note.serialize(),notes))
            return jsonify(notes), 200
    
    if request.method == 'POST':
        title=request.json.get('title')
        date=request.json.get('date')
        agenda_id=request.json.get('agenda_id')
        if not title:
            return jsonify({"msg": "title is required"}), 422  
        if not date:
            return jsonify({"msg": "date is required"}), 422  
        if not agenda_id:
            return jsonify({"msg": "agenda_id is required"}), 422  
           
        note = Note()
        note.title = title
        note.date = date
        note.agenda_id = agenda_id

        db.session.add(note)
        db.session.commit()

        return jsonify(note.serialize()), 201
    
    if request.method == 'PUT':
        
        note = Note.query.get(id)
        note.title = request.json.get('title')
        note.agenda_id = request.json.get('agenda_id')

        db.session.commit()

        return jsonify(note.serialize()), 200

    if request.method == 'DELETE':
        
        note = Note.query.get(id)
        db.session.delete(note)
        db.session.commit()

        return jsonify({'note':'Deleted'}), 200