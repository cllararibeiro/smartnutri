from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from database.config import Session
from models.models import Nutricionista,  Paciente
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')
session = Session()

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = session.query(Nutricionista).get(int(user_id)) 
    if user is None:
        user = session.query(Paciente).get(int(user_id))
    return user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        nutricionista = session.query(Nutricionista).filter_by(nutri_email=email).first()

        erros = {}

        if not nutricionista:
            erros['email'] = 'E-mail não encontrado.'
        elif not nutricionista.check_password(senha):
            erros['senha'] = 'Senha incorreta.'

        if erros:
            return render_template('auth/login.html', erros=erros, form=request.form)


        if nutricionista and nutricionista.check_password(senha):
            login_user(nutricionista)
            flash('Login realizado com sucesso!')
            return redirect(url_for('nutricionista.dashboard'))
        else:
            flash('Email ou senha incorretos.')

    return render_template('auth/login.html', erros={}, form={})

@auth_bp.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']
        crn = request.form['crn']
        telefone = request.form['telefone']
        erros = {}

        if session.query(Nutricionista).filter_by(nutri_email=email).first():
            erros['email'] = 'E-mail já cadastrado.'
        if session.query(Nutricionista).filter_by(nutri_cpf=cpf).first():
            erros['cpf'] = 'CPF já cadastrado.'
        if session.query(Nutricionista).filter_by(nutri_crn=crn).first():
            erros['crn'] = 'CRN já cadastrado.'
        if session.query(Nutricionista).filter_by(nutri_telefone=telefone).first():
            erros['telefone'] = 'Telefone já cadastrado.'

        if erros:
            return render_template("auth/cadastro.html", erros=erros, form=request.form)

        novo_nutricionista = Nutricionista(nutri_nome=nome,nutri_email=email,nutri_cpf=cpf,nutri_telefone=telefone,nutri_senha=senha, nutri_crn=crn)
        novo_nutricionista.set_password(senha)
        session.add(novo_nutricionista)
        session.commit()
        login_user(novo_nutricionista)
        return redirect(url_for('auth.login'))

    return render_template("auth/cadastro.html", erros={}, form={})

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.')
    return redirect(url_for('index'))
