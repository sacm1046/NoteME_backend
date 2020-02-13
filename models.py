from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255), nullable=False)
    fullname=db.Column(db.String(255), nullable=False)
    isAdmin=db.Column(db.Boolean, default=False)
    active=db.Column(db.Boolean, default=True)
    password=db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return 'User %r' % self.username

    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'isAdmin': self.isAdmin,
            'active': self.active,
        }

class Curso(db.Model):
    __tablename__ = 'cursos'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return 'Curso %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
        }

class Agenda(db.Model):
    __tablename__ = 'agendas'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255), nullable=False, default="Agenda")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User, backref=backref("children", cascade="all,delete"))

    def __repr__(self):
        return 'Agenda %r' % self.title

    def serialize(self):
        return{
            'id': self.id,
            'title': self.title,
            'user': self.user.serialize() 
        }

class Note(db.Model):
    __tablename__ = 'notes'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255), nullable=False)
    date=db.Column(db.String(255), nullable=False)

    agenda_id = db.Column(db.Integer, db.ForeignKey('agendas.id'), nullable=False)
    agenda = db.relationship(Agenda, backref=backref("children", cascade="all,delete"))

    def __repr__(self):
        return 'Note %r' % self.title

    def serialize(self):
        return{
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'agenda': self.agenda.serialize()
        }

class Text(db.Model):
    __tablename__ = 'texts'
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.Text(), nullable=True)
    url=db.Column(db.String(255), nullable=True)
    date=db.Column(db.String(255), nullable=False)
    time=db.Column(db.String(255), nullable=False)

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    note = db.relationship(Note , backref=backref("children", cascade="all,delete"))

    def __repr__(self):
        return 'Text %r' % self.content

    def serialize(self):
        return{
            'id': self.id,
            'content': self.content,
            'url': self.url,
            'date': self.date,
            'time': self.time,
            'note': self.note.serialize()
        }