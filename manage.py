import os
from flask import Flask, render_template, jsonify, request, Blueprint, send_from_directory 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_jwt_extended import (
    JWTManager
)
from models import db, User, Curso, Agenda, Note, Text, Image, Lista, Listline 
from routes.user import route_users
from routes.curso import route_cursos
from routes.agenda import route_agendas
from routes.note import route_notes
from routes.text import route_texts
from routes.image import route_images
from routes.lista import route_listas
from routes.listline import route_listlines
from routes.auth import auth

from libs.functions import allowed_file
from werkzeug.utils import secure_filename

from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/img')
ALLOWED_EXTENSIONS = {'jpg','png','jpeg','pdf'}

app=Flask(__name__)
app.url_map.strict_slashes = False #Slashes
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'cm.seb90@gmail.com'
app.config['MAIL_PASSWORD'] = 'tdrzlquykyzmnsch' 

app.config['JWT_SECRET_KEY'] = 'super-secrets'
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False #inhabilita la expiración del token
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3) #inhabilita en tres dias el token

jwt = JWTManager(app)
db.init_app(app)

mail = Mail(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

CORS(app)

@app.route('/')
def home():
    return render_template('index.html', name='home')

app.register_blueprint(auth)
app.register_blueprint(route_users, url_prefix='/api')
app.register_blueprint(route_cursos, url_prefix='/api')
app.register_blueprint(route_agendas, url_prefix='/api')
app.register_blueprint(route_notes, url_prefix='/api')
app.register_blueprint(route_texts, url_prefix='/api')
app.register_blueprint(route_images, url_prefix='/api')
app.register_blueprint(route_listas, url_prefix='/api')
app.register_blueprint(route_listlines, url_prefix='/api')

@app.route('/sendmail', methods=['POST'])
def sendmail():
    subject = request.json.get('subject',None)
    to_email = 'cm.seb90@gmail.com'
    name = request.json.get('name',None)
    from_email = request.json.get('from',None)
    message = request.json.get('message',None)

    if not subject:
        return jsonify({"subject":"Subject is required"}),422
    if not name:
        return jsonify({"name":"Name is required"}),422
    if not from_email:
        return jsonify({"from":"From is required"}),422
    if not message:
        return jsonify({"message":"Message is required"}),422

    msg = Message(subject, sender=[name, from_email], recipients=[to_email])
    msg.body = message
    mail.send(msg)

    return jsonify({"msg":"Email send successfully"}),200

@app.route('/upload', methods=['POST'])
@app.route('/upload/<filename>', methods=['GET'])
def upload_file(filename=None):
    if request.method == 'GET':
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error":"not files present"}), 422

        file = request.files['file']
        if file.filename == '':
            return jsonify({"msg":"Please select a file"}), 422
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"msg":"file uploaded"}), 200
        else:
            return jsonify({"msg":"file not allowed"}), 400 

if __name__ == '__main__':
    manager.run()