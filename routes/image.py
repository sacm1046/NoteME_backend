from flask import Blueprint, request, jsonify
from models import db, Image
from flask_jwt_extended import (
    jwt_required
)

route_images = Blueprint('route_images', __name__)

@route_images.route('/images', methods=['GET','POST'])
@route_images.route('/images/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def images(id=None):
    if request.method == 'GET':
        if id is not None:
            image = Image.query.get(id)
            if image:
                return jsonify(image.serialize()), 200
            else:
                return jsonify({"image":"Not found"}), 404
        else:
            images = Image.query.all()
            images = list(map(lambda image: image.serialize(),images))
            return jsonify(images), 200
    
    if request.method == 'POST':
        url=request.json.get('url')
        note_id=request.json.get('note_id') 
        if not url:
            return jsonify({"msg": "url is required"}), 422  
        if not note_id:
            return jsonify({"msg": "note_id is required"}), 422  
           
        image = Image()
        image.url = url
        image.note_id = note_id

        db.session.add(image)
        db.session.commit()

        return jsonify(image.serialize()), 201
    
    if request.method == 'PUT':
        
        image = Image.query.get(id)
        image.url = request.json.get('url')
        image.note_id = request.json.get('note_id')

        db.session.commit()

        return jsonify(image.serialize()), 200

    if request.method == 'DELETE':
        
        image = Image.query.get(id)
        db.session.delete(image)
        db.session.commit()

        return jsonify({'image':'Deleted'}), 200