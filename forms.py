# Importamos las clases necesarias de las librerias
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
# Importamos el modelo User para poder hacer consultas a la base de datos y validar datos
from models import User

class LoginForm(FlaskForm):
   
    # Campo para el nombre de usuario. Es un campo de texto (StringField).
    # 'Nombre de Usuario' es la etiqueta que se mostrará en el HTML.
    # 'validators=[DataRequired()]' significa que este campo no puede dejarse vacío.
    username = StringField('Nombre de Usuario', validators=[DataRequired()])

    # Campo para la contraseña. Es un campo de contraseña (PasswordField) que oculta el texto.
    password = PasswordField('Contraseña', validators=[DataRequired()])

    # Botón para enviar el formulario.
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
    
    # Campo para el nombre de usuario, igual que en el login.
    username = StringField('Nombre de Usuario', validators=[DataRequired()])

    # Campo para la contraseña.
    password = PasswordField('Contraseña', validators=[DataRequired()])

    # Campo para que el usuario repita la contraseña y así confirmarla.
    # El validador 'EqualTo('password')' asegura que el contenido de este campo
    # sea exactamente igual al del campo 'password'. Si no lo es, muestra el mensaje de error.
    password2 = PasswordField(
        'Repetir Contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir.')])

    # Botón para enviar el formulario de registro.
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        
        # Se busca en la base de datos si ya existe un usuario con el nombre que se está intentando registrar.
        user = User.query.filter_by(username=username.data).first()
        # Si la consulta encuentra un usuario (es decir, 'user' no es None)...
        if user:
            # ...se lanza un error de validación con un mensaje para el usuario.
            raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')

