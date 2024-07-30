from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,FileField
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
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")
            
class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao = SubmitField("Enviar")

