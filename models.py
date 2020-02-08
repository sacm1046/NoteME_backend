from flask_sqlalchemy import SQLAlchemy
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
    user = db.relationship(User)

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
    agenda = db.relationship(Agenda)

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
    content=db.Column(db.Text(), nullable=False)

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    note = db.relationship(Note)

    def __repr__(self):
        return 'Text %r' % self.content

    def serialize(self):
        return{
            'id': self.id,
            'content': self.content,
            'note': self.note.serialize()
        }

class Image(db.Model):
    __tablename__ = 'images'
    id=db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String(255), nullable=False)

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    note = db.relationship(Note)

    def __repr__(self):
        return 'Image %r' % self.url

    def serialize(self):
        return{
            'id': self.id,
            'url': self.url,
            'note': self.note.serialize() 
        }

class Lista(db.Model):
    __tablename__ = 'listas'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255), nullable=False)

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    note = db.relationship(Note)

    def __repr__(self):
        return 'Lista %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'note': self.note.serialize() 
        }

class Listline(db.Model):
    __tablename__ = 'listlines'
    id=db.Column(db.Integer, primary_key=True)
    line=db.Column(db.String(255), nullable=False)

    lista_id = db.Column(db.Integer, db.ForeignKey('listas.id'), nullable=False)
    lista = db.relationship(Lista)

    def __repr__(self):
        return 'List %r' % self.line

    def serialize(self):
        return{
            'id': self.id,
            'line': self.line,
            'lista': self.lista.serialize() 
        }