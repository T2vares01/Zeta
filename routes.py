from flask import Flask, render_template as rt, url_for,redirect
from flask_login import login_required, login_user, logout_user,current_user
from Site import app, database, bcrypt
from Site.forms import FormLogin,FormCriarConta
from Site.models import Usuario, Post

#criação dos links

@app.route("/",methods = ["GET","POST"])
def home():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", usuario=usuario.username))
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
        return redirect(url_for("perfil", usuario=usuario.username))
    else:
        print(formcriarconta.errors)
    return rt("newacount.html", form = formcriarconta)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
    return rt("usuario.html", usuario = usuario)

@app.route("/chat")
@login_required
def chat():
    pass

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