#Paso 1: importamos todas las librerias y herramientas que necesitamos
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash # Para contraseñas seguras
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

#Paso 2: creamos la aplicación Flask
app = Flask(__name__)

#Paso 3: configuramos la aplicación
#SECRET_KEY es necesaria para la seguridad de la sesion y los formularios
app.config['SECRET_KEY'] = 'alessandro12'

#hacemos conexion a base de datos usamos postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ghettoboy:alessandro12@localhost:5432/db1'
#desactivamos una función de SQLAlchemy que no necesitamos para evitar 'warnings' en la consola
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Paso 4: inicializar las extensiones que usaremos
#'db' será nuestro objeto para interactuar con la base de datos
db = SQLAlchemy(app)
#'login_manager' manejara todo el proceso de inicio de sesion
login_manager = LoginManager(app)
#si un usuario no logueado intenta ir a una página protegida, lo redirigirá a la función 'login'
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'

#Paso 5: importamos el archivo models y formularios
#se hace aquí para evitar un "error de importación circular", ya que los modelos necesitan el objeto 'db'
from models import User
from forms import LoginForm, RegistrationForm

#Paso 6: configuramos el "cargador de usuarios" de Flask-Login
#esta función le dice a Flask-Login cómo encontrar un usuario específico por su ID
@login_manager.user_loader
def load_user(user_id):
    # User.query.get() es una función de SQLAlchemy que busca un usuario por su clave primaria (el ID)
    return User.query.get(int(user_id))


#aqui van todas las RUTAS (las "páginas" de nuestra app)

#ruta para la página raíz del sitio web
@app.route('/')
def index():
    #aqui lo redirigimos a la pagina de login
    return redirect(url_for('login'))

#ruta para la página de "inicio" después de iniciar sesión
@app.route('/inicio')
@login_required #este decorador protege la ruta. Solo se puede acceder si has iniciado sesión.
def inicio():
    #mostramos la plantilla HTML que ve un usuario ya logueado
    return render_template('protegida.html')

#ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    #si el usuario ya tiene una sesión activa, lo mandamos directamente al inicio
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    form = LoginForm() #creamos una instancia del formulario de login
    #si el formulario fue enviado (POST) y todos los campos son válidos...
    if form.validate_on_submit():
        #buscamos en la base de datos un usuario con el nombre que se introdujo
        user = User.query.filter_by(username=form.username.data).first()
        #si el usuario existe y la contraseña es correcta...
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user) #iniciamos su sesión con Flask-Login
            return redirect(url_for('inicio')) # y lo redirigimos a la página de inicio
        else:
            #si el usuario no existe o la contraseña es incorrecta, mostramos un mensaje de error
            flash('Error: Usuario o contraseña incorrectos.')
    #si la petición es GET (la primera vez que se carga la página), solo mostramos el formulario
    return render_template('login.html', form=form)

#ruta para la página de registro de nuevos usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    #si el usuario ya tiene una sesión activa, lo mandamos al inicio
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    form = RegistrationForm() #creamos una instancia del formulario de registro
    if form.validate_on_submit():
        #creamos una versión "hasheada" osea (segura) de la contraseña para no guardarla en texto plano
        hashed_password = generate_password_hash(form.password.data)
        #creamos un nuevo objeto de usuario con los datos del formulario
        new_user = User(username=form.username.data, password_hash=hashed_password)
        #lo añadimos a la sesión de la base de datos (preparamos para guardar)
        db.session.add(new_user)
        #guardamos los cambios permanentemente en la base de datos
        db.session.commit()
        #mostramos un mensaje de éxito
        flash('¡Tu cuenta ha sido creada! Ya puedes iniciar sesión.')
        return redirect(url_for('login')) #lo redirigimos al login para que inicie sesión
    return render_template('register.html', form=form)

#ruta para cerrar la sesión
@app.route('/logout')
@login_required #solo un usuario logueado puede tener la necesidad de cerrar sesión
def logout():
    logout_user() #cerramos la sesión del usuario con Flask-Login
    return redirect(url_for('login'))

#ruta para mostrar mi perfil
@app.route('/miperfil')
@login_required
def miperfil():
    return render_template('miperfil.html')

@app.route('/protegida')
@login_required
def protegida():
    return render_template('protegida.html')