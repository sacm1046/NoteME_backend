from flask import Blueprint, request, jsonify
from models import db, Text
from flask_jwt_extended import (
    jwt_required
)

route_texts = Blueprint('route_texts', __name__)

@route_texts.route('/texts', methods=['GET','POST'])
@route_texts.route('/texts/note/<int:note_id>', methods=['GET','POST'])
@route_texts.route('/texts/<int:id>', methods=['GET','PUT','DELETE'])
@route_texts.route('/texts/note/<int:note_id>/text/<int:id>', methods=['GET','POST'])
@jwt_required
def texts(note_id=None, id=None):
    if request.method == 'GET':
        if id is not None and note_id is not None:
            text = Text.query.filter_by(note_id=note_id, id=id).first()
            if text:
                return jsonify(text.serialize()), 200
            else:
                return jsonify({"text":"Not found"}), 404
        elif id is not None:
            text = Text.query.get(id)
            if text:
                return jsonify(text.serialize()), 200
            else:     
                return jsonify({"text":"Not found"}), 404
        elif note_id is not None:
            texts = Text.query.filter_by(note_id = note_id).all()
            texts = list(map(lambda text: text.serialize(),texts))
            return jsonify(texts), 200
        else:
            texts = Text.query.all()
            texts = list(map(lambda text: text.serialize(), texts))
            return jsonify(texts), 200
    
    if request.method == 'POST':       
        text = Text()
        text.date = request.json.get('date')
        text.time = request.json.get('time')
        text.content = request.json.get('content')
        text.url = request.json.get('url')
        text.note_id = request.json.get('note_id')

        db.session.add(text)
        db.session.commit()

        return jsonify(text.serialize()), 201
    
    if request.method == 'PUT':
        
        text = Text.query.get(id)
        text.content = request.json.get('content')
        text.url = request.json.get('url')
        text.note_id = request.json.get('note_id')

        db.session.commit()

        return jsonify(text.serialize()), 200

    if request.method == 'DELETE':
        
        text = Text.query.get(id)
        db.session.delete(text)
        db.session.commit()

        return jsonify({'text':'Deleted'}), 200