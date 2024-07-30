from flask import Flask, render_template as rt, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "50a9156b31c864267d3a13571672c5104cd27288baa95f61c5e702345e4c14e9"
app.config["UPLOAD_FOLDER"] = "static/fotos_post"
io = SocketIO(app)

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "home"

from Site import routes
