from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError
from Site.models import Usuario

# formularios do site
class FormLogin(FlaskForm):
    email = StringField("E-mail", validators = [DataRequired(),Email()])
    senha = PasswordField("Senha", validators = [DataRequired()])
    botao = SubmitField("Fazer login")

class FormCriarConta(FlaskForm):
    username =StringField("nome de usuario", validators = [DataRequired()])
    email = StringField("E-mail", validators = [DataRequired(),Email()])
    senha = PasswordField("Senha", validators = [DataRequired(), Length(5,20)])
    confirmacao_senha = PasswordField("Confirmar Senha", validators = [DataRequired(),EqualTo("senha")])
    botao = SubmitField("Criar conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if usuario:
            return ValidationError("Email ja cadastrado")

