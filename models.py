#importamos el objeto 'db' que creamos en app.py
from app import db
#UserMixin es una clase de Flask-Login que nos da métodos útiles para el manejo de sesiones de usuario
from flask_login import UserMixin

#nuestra clase User ahora representa la tabla "user" en la base de datos.
#hereda de db.Model (para que SQLAlchemy la reconozca) y de UserMixin.
class User(UserMixin, db.Model):
    #definimos las columnas de nuestra tabla:

    #id: Será la clave primaria (un número único para cada usuario).
    id = db.Column(db.Integer, primary_key=True)

    #username: Guardará el nombre de usuario.
    #debe ser único (unique=True) y no puede estar vacío (nullable=False).
    username = db.Column(db.String(80), unique=True, nullable=False)

    #password_hash: Guardará la contraseña de forma segura (hasheada).
    #NUNCA guardamos la contraseña real directamente. No puede estar vacía.
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        #esta es una función opcional que ayuda al depurar.
        #nos muestra el nombre de usuario cuando imprimimos un objeto User.
        return f'<User {self.username}>'