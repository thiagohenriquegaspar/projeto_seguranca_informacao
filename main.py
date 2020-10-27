from flask import Flask, render_template, request, flash
from hashlib import md5
import os

app = Flask(__name__)
app.secret_key = f"S3gur4n@c0"

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastro():
    
    if request.method == 'POST':
        login = request.form.get('username')
        login_arquivo = f"{login}.txt"
        senha = request.form.get('password')
        senha_md5 = md5(f"{senha}".encode()).hexdigest()

        if len(login) > 4 or len(senha) > 4:
            flash('Não é possivel registrar login e senha com mais de 4 caracteres', 'danger')
            return render_template("cadastrar.html")

        for _, _, files in os.walk('./sessoes/'):
            if login_arquivo in files:
                flash('Já existe um registro com o login informado', 'danger')
            else:
                with open(f"./sessoes/{login_arquivo}", "w") as arquivo:
                    arquivo.write(senha_md5)
                flash(f"{login} foi registrado", 'success')

        

    return render_template("cadastrar.html")

@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        login = request.form.get('username')
        login_arquivo = f"{login}.txt"
        senha = request.form.get('password')
        senha_md5 = md5(f"{senha}".encode()).hexdigest()
        login_ok = False

        if len(login) > 4 or len(senha) > 4:
            flash('Não é possivel registrar login e senha com mais de 4 caracteres', 'danger')
            return render_template("cadastrar.html")

        for _, _, files in os.walk('./sessoes/'):
            if login_arquivo in files:
                with open(f"./sessoes/{login_arquivo}", "r") as arquivo:
                    senha_arquivo = arquivo.readline()
                    if senha_arquivo == senha_md5:
                        login_ok = True
        
        if login_ok:
            flash("Login OK", 'success')
        else:
            flash("Login e/ou Senha incorreto(s)", 'warning')

    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)