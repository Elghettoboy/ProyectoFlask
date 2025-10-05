#Paso 1: Importamos todas las librerias y herramientas que necesitamos
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash # Para contraseñas seguras
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

#Paso 2: Creamos la aplicación Flask
app = Flask(__name__)

#Paso 3: Configuramos la aplicación
#SECRET_KEY es necesaria para la seguridad de la sesion y los formularios
app.config['SECRET_KEY'] = 'alessandro12'

#Hacemos conexion a base de datos usamos postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ghettoboy:alessandro12@localhost:5432/db1'
#Desactivamos una función de SQLAlchemy que no necesitamos para evitar 'warnings' en la consola
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Paso 4: Inicializar las extensiones que usaremos
#'db' será nuestro objeto para interactuar con la base de datos
db = SQLAlchemy(app)
#'login_manager' manejara todo el proceso de inicio de sesion
login_manager = LoginManager(app)
#Si un usuario no logueado intenta ir a una página protegida, lo redirigirá a la función 'login'
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'

#Paso 5: Importamos el archivo models y formularios
#Se hace aquí para evitar un "error de importación circular", ya que los modelos necesitan el objeto 'db'
from models import User
from forms import LoginForm, RegistrationForm

#Paso 6: Configuramos el "cargador de usuarios" de Flask-Login
#Esta función le dice a Flask-Login cómo encontrar un usuario específico por su ID
@login_manager.user_loader
def load_user(user_id):
    # User.query.get() es una función de SQLAlchemy que busca un usuario por su clave primaria (el ID)
    return User.query.get(int(user_id))


#Aqui van todas las RUTAS (las "páginas" de nuestra app)

#Ruta para la página raíz del sitio web
@app.route('/')
def index():
    #Aqui lo redirigimos a la pagina de login
    return redirect(url_for('login'))

#Ruta para la página de "inicio" después de iniciar sesión
@app.route('/inicio')
@login_required #Este decorador protege la ruta. Solo se puede acceder si has iniciado sesión.
def inicio():
    #Renderizamos la plantilla HTML que ve un usuario ya logueado
    return render_template('protegida.html')

#Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    #Si el usuario ya tiene una sesión activa, lo mandamos directamente al inicio
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    form = LoginForm() #Creamos una instancia del formulario de login
    # Si el formulario fue enviado (POST) y todos los campos son válidos...
    if form.validate_on_submit():
        # Buscamos en la base de datos un usuario con el nombre que se introdujo
        user = User.query.filter_by(username=form.username.data).first()
        # Si el usuario existe y la contraseña es correcta...
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user) # ...iniciamos su sesión con Flask-Login
            return redirect(url_for('inicio')) # y lo redirigimos a la página de inicio
        else:
            # Si el usuario no existe o la contraseña es incorrecta, mostramos un mensaje de error
            flash('Error: Usuario o contraseña incorrectos.')
    # Si la petición es GET (la primera vez que se carga la página), solo mostramos el formulario
    return render_template('login.html', form=form)

# Ruta para la página de registro de nuevos usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Si el usuario ya tiene una sesión activa, lo mandamos al inicio
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    form = RegistrationForm() # Creamos una instancia del formulario de registro
    if form.validate_on_submit():
        # Creamos una versión "hasheada" (segura) de la contraseña para no guardarla en texto plano
        hashed_password = generate_password_hash(form.password.data)
        # Creamos un nuevo objeto de usuario con los datos del formulario
        new_user = User(username=form.username.data, password_hash=hashed_password)
        # Lo añadimos a la sesión de la base de datos (preparamos para guardar)
        db.session.add(new_user)
        # Guardamos los cambios permanentemente en la base de datos
        db.session.commit()
        # Mostramos un mensaje de éxito
        flash('¡Tu cuenta ha sido creada! Ya puedes iniciar sesión.')
        return redirect(url_for('login')) # Lo redirigimos al login para que inicie sesión
    return render_template('register.html', form=form)

# Ruta para cerrar la sesión
@app.route('/logout')
@login_required # Solo un usuario logueado puede tener la necesidad de cerrar sesión
def logout():
    logout_user() # Cerramos la sesión del usuario con Flask-Login
    return redirect(url_for('login'))

