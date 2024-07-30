from Site import database ,login_manager
from datetime import datetime
from flask_login import UserMixin

# o modelo do site

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False ,unique = True)
    email = database.Column(database.String, nullable = False,unique = True)
    senha = database.Column(database.String, nullable = False)
    post = database.relationship("Post", backref = "usuario",lazy = True)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    post = database.Column(database.String, default = "default.png")
    data = database.Column(database.DateTime, nullable = False, default = datetime.utcnow())
    id_usuario = database.Column(database.Integer,database.ForeignKey('usuario.id'), nullable = False)
