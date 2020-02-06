from flask import Blueprint, request, jsonify
from models import db, Curso
from flask_jwt_extended import (
    jwt_required
)

route_cursos = Blueprint('route_cursos', __name__)

@route_cursos.route('/cursos', methods=['GET','POST'])
@route_cursos.route('/cursos/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def cursos(id=None):
    if request.method == 'GET':
        if id is not None:
            curso = Curso.query.get(id)
            if curso:
                return jsonify(curso.serialize()), 200
            else:
                return jsonify({"curso":"Not found"}), 404
        else:
            cursos = Curso.query.all()
            cursos = list(map(lambda curso: curso.serialize(),cursos))
            return jsonify(cursos), 200
    
    if request.method == 'POST':
        name=request.json.get('name')
        if not name:
            return jsonify({"msg": "name is required"}), 422  
        curso = Curso.query.filter_by(name=name).first()
        if curso:
            return jsonify({"msg": "Nombre de curso ocupado"}), 422          

        curso = Curso()
        curso.name = name

        db.session.add(curso)
        db.session.commit()

        return jsonify(curso.serialize()), 201
    
    if request.method == 'PUT':
        
        curso = Curso.query.get(id)
        curso.name = request.json.get('name')

        db.session.commit()

        return jsonify(curso.serialize()), 200

    if request.method == 'DELETE':
        
        curso = Curso.query.get(id)
        db.session.delete(curso)
        db.session.commit()

        return jsonify({'curso':'Deleted'}), 200