from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False)
    fullname=db.Column(db.String(50), nullable=False)
    phone=db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return 'User %r' % self.username

    def serialize(self):
        return{
            'id': self.id,
            'username': self.username,
            'fullname': self.fullname,
            'phone': self.phone,
        }

class Profesor(db.Model):
    __tablename__ = 'profesores'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)
    lastname=db.Column(db.String(50), nullable=False)
    rut=db.Column(db.String(50), nullable=False)
    phone=db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'Profesor %r' % self.rut

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'rut': self.rut,
            'phone': self.phone,
        }

class Sede(db.Model):
    __tablename__ = 'sedes'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'Sede %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
        }

class Curso(db.Model):
    __tablename__ = 'cursos'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return 'Curso %r' % self.name

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
        }

"""class DetailCurso(db.Model):
    __tablename__ = 'detailsCurso'
    id=db.Column(db.Integer, primary_key=True)
    fecha=db.Column(db.String(50), nullable=False)
    cupos=db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User)

    def __repr__(self):
        return 'DetailCurso %r' % self.curso

    def serialize(self):
        return{
            'id': self.id,
            'curso': self.curso,
        }

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id=db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User)

    detail_curso_id=db.Column(db.Integer, db.ForeignKey('detailsCurso.id'), nullable=False)
    detail_curso_fecha=db.Column(db.Integer, db.ForeignKey('detailsCurso.fecha'), nullable=False)
    detail_curso = db.relationship(DetailCurso)

    def __repr__(self):
        return 'Reserva %r' % self.user.username

    def serialize(self):
        return{
            'id': self.id,
            'fecha': self.fecha,
            'user': self.serialize.user,
            'detail_curso': self.serialize.detail_curso,
        } """
