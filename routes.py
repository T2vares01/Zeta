from flask import Flask, render_template as rt, url_for,redirect
from flask_login import login_required, login_user, logout_user,current_user
from Site import app, database, bcrypt, io
from Site.forms import FormLogin,FormCriarConta ,FormFoto
from Site.models import Usuario, Post
from flask_socketio import emit, send
import os
from werkzeug.utils import secure_filename

#criação dos links
messages = []

@app.route("/",methods = ["GET","POST"])
def home():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
        else:
            print(formlogin.errors)
    return rt("home.html", form = formlogin)

@app.route("/newacount",methods = ["GET","POST"])
def newacount():
    formcriarconta = FormCriarConta()
    #bcrypt.check_password_hash() descriptografar a senha
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username = formcriarconta.username.data,
                          email = formcriarconta.email.data,
                          senha = senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    else:
        print(formcriarconta.errors)
    return rt("newacount.html", form = formcriarconta)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuario ta vendo o perfil dele
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome = secure_filename(arquivo.filename)
            # salvar o arquivo dentro da pasta certa
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config["UPLOAD_FOLDER"],
                                   nome)
            arquivo.save(caminho)
            # criar a foto no banco com o item "imagem" sendo o nome do arqivo
            foto = Post(post = nome, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()
        return rt("usuario.html", usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return rt("usuario.html", usuario=usuario, form=None)

@app.route("/feed")
@login_required
def feed():
    fotos = Post.query.order_by(Post.data.desc()).all()
    return rt("feed.html", post = fotos)

@app.route("/chat")
@login_required
def chat():
    return rt('chat.html',usuario = current_user )

@io.on('sendMessage')
def send_message_handler(msg):
    messages.append(msg)
    emit('getMessage', msg, json=True)

@io.on('message')
def message_handler(msg):
    send(messages)

@app.route("/room")
@login_required
def room():
    pass

@app.route("/project")
@login_required
def project():
    pass

@app.route("/Questions")
@login_required
def Questions():
    pass
