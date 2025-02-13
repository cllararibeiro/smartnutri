from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.config import Session
from datetime import datetime
from models.models import Nutricionista, Paciente, Consulta, Dieta

nutricionista_bp = Blueprint('nutricionista', __name__, url_prefix='/nutricionista', template_folder='templates')

session = Session()

@nutricionista_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('nutricionista/dashboard.html')

@nutricionista_bp.route('/consulta', methods=['GET', 'POST'])
@login_required
def consulta():
    return render_template('nutricionista/consulta.html')

@nutricionista_bp.route('/dieta', methods=['GET', 'POST'])
@login_required
def dieta():
    return render_template('nutricionista/dieta.html')

@nutricionista_bp.route('/funcionalidades', methods=['GET', 'POST'])
@login_required
def funcionalidades():
    return render_template('nutricionista/funcionalidades.html')

@nutricionista_bp.route('/cadastro_paciente', methods=['GET', 'POST'])
@login_required
def cadastro_paciente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        data_nasc = request.form['data_nasc']
        idade = request.form['idade']
        sexo = request.form['sexo']
        tel = request.form['tel']
        cpf = request.form['cpf']
        doencas_preexistentes = request.form['doencas_preexistentes']
        historico_familiar = request.form['historico_familiar']
    
        paciente = Paciente(pac_nome=nome,pac_email=email,pac_data_nasc=datetime.strptime(data_nasc, '%Y-%m-%dT%H:%M'),pac_idade=idade,
            pac_sexo=sexo,pac_tel=tel,pac_cpf=cpf,pac_doencas_preexistentes=doencas_preexistentes,
            pac_historico_familiar=historico_familiar,pac_nutri_id=current_user.nutri_id)
        
        try:
            session.add(paciente)
            session.commit()
            flash("Paciente cadastrado com sucesso!", "success")
            return redirect(url_for('nutricionista.dashboard'))
        except IntegrityError:
            session.rollback()
            flash("Erro: Já existe um paciente com esse e-mail ou telefone.", "danger")
        except Exception as e:
            session.rollback()
            flash(f"Ocorreu um erro: {e}", "danger")

    return render_template('nutricionista/cadastro_paciente.html')
