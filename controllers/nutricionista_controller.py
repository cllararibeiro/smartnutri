from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.config import Session
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from models.models import Nutricionista, Paciente, Consulta, Dieta

nutricionista_bp = Blueprint('nutricionista', __name__, url_prefix='/nutricionista', template_folder='templates')

session = Session()

@nutricionista_bp.route('/dashboard')
@login_required
def dashboard():
    busca = request.args.get('busca', '')
    pacientes = session.query(Paciente).filter(Paciente.pac_nome.like(f'%{busca}%'))\
    .filter_by(pac_nutri_id=current_user.nutri_id)\
    .order_by(desc(Paciente.pac_data_cadastro)).all() 
    return render_template('nutricionista/dashboard.html', pacientes=pacientes)

@nutricionista_bp.route('/consulta/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def consulta(paciente_id):
    paciente = session.query(Paciente).get(paciente_id)
    sexo = paciente.pac_sexo if paciente else None
    data_nasc = paciente.pac_data_nasc
    data_nasc_ = datetime.strptime(str(data_nasc), '%Y-%m-%d')

    hoje = datetime.today().date() 
    idade = hoje.year - data_nasc_.year - ((hoje.month, hoje.day) < (data_nasc_.month, data_nasc_.day))


    if request.method == 'POST': 

        peso = request.form.get('peso')
        altura = request.form.get('altura')
        imc = request.form.get('imc')
        circun_abdomen = request.form.get('circunferenciaAbdominal')
        circun_quadril = request.form.get('circunferenciaQuadril')
        gordura_corporal = request.form.get('gorduraCorporal')
        massa_muscular = request.form.get('massaMuscular')
        massa_gorda = request.form.get('massaGorda')
        dobra_tricipital = request.form.get('dobraTricipital')
        dobra_subescapular = request.form.get('dobraSubescapular')
        dobra_supra_iliaca = request.form.get('dobraSupraIliaca')
        dobra_abdominal = request.form.get('dobraAbdominal')
        dobra_peitoral = request.form.get('dobraPeitoral')
        dobra_coxa = request.form.get('dobraCoxa')
        dobra_axilar = request.form.get('dobraAxilar')
        tmb = request.form.get('tmb')

        objetivos = request.form.get('objetivos')
        rotina = request.form.get('rotina')
        observacoes = request.form.get('obs')
        preferencias = request.form.get('preferencias')
        aversoes = request.form.get('aversoes')

        consulta_obj = Consulta(con_data=datetime.utcnow(),con_nutri_id=current_user.nutri_id, con_pac_id=paciente_id)
        session.add(consulta_obj)
        session.commit()

        registro_consulta = RegistroConsulta(reg_con_objetivos=objetivos,reg_con_rotina=rotina,reg_con_obs=observacoes,reg_con_preferencias=preferencias,reg_con_aversoes=aversoes)
        session.add(registro_consulta)
        session.commit()

        dados_antro = DadosAntropometricos(dad_con_id=consulta_obj.con_id,dad_peso_atual=float(peso),dad_altura=float(altura),dad_imc=float(imc),
            dad_circun_abdomen=float(circun_abdomen) if circun_abdomen else None,dad_circun_quadri=float(circun_quadril) if circun_quadril else None,
            dad_gord_corporal=float(gordura_corporal) if gordura_corporal else None,dad_massa_muscular=float(massa_muscular) if massa_muscular else None,
            dad_massa_gorda=float(massa_gorda) if massa_gorda else None,dad_dobra_tricipital=float(dobra_tricipital) if dobra_tricipital else None,
            dad_dobra_subescapular=float(dobra_subescapular) if dobra_subescapular else None,dad_dobra_supra_iliaca=float(dobra_supra_iliaca) if dobra_supra_iliaca else None,
            dad_dobra_abdominal=float(dobra_abdominal) if dobra_abdominal else None,dad_dobra_peitoral=float(dobra_peitoral) if dobra_peitoral else None,
            dad_dobra_coxa=float(dobra_coxa) if dobra_coxa else None,dad_dobra_axilar=float(dobra_axilar) if dobra_axilar else None,dad_tmb=float(tmb) if tmb else None
        )
        session.add(dados_antro)
        session.commit()
        
        return render_template('nutricionista/consulta.html', sexo=sexo, paciente = paciente, idade = idade)

    return render_template('nutricionista/consulta.html', sexo=sexo, paciente = paciente, idade = idade) 

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
        data_nasc = request.form.get('data_nasc')
        sexo = request.form.get('sexo')  
        tel = request.form['telefone']
        cpf = request.form['cpf']
        doencas_preexistentes = request.form['doencas_preexistentes']
        historico_familiar = request.form['historico_familiar']
    
        data_nasc_obj = datetime.strptime(data_nasc, '%Y-%m-%d') 
        
        hoje = datetime.today()
        idade = hoje.year - data_nasc_obj.year - ((hoje.month, hoje.day) < (data_nasc_obj.month, data_nasc_obj.day))

        paciente = Paciente(pac_nome=nome,pac_email=email,pac_data_nasc=data_nasc_obj,pac_idade=idade,
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
