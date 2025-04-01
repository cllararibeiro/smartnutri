from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.config import Session
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from models.models import Nutricionista, Paciente, Consulta, Dieta, RegistroConsulta, DadosAntropometricos, Alimento, TipoRefeicao, Cardapio

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
        gordura_corporal = request.form.get('percentualGordura')
        massa_magra = request.form.get('massaMagra')
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
        
        registro_consulta = RegistroConsulta(reg_con_objetivos=objetivos,reg_con_rotina=rotina,reg_con_obs=observacoes,reg_con_preferencias=preferencias,reg_con_aversoes=aversoes)
        session.add(registro_consulta)
        session.commit()

        reg_con_id = registro_consulta.reg_con_id

        consulta_obj = Consulta(con_data=datetime.utcnow(),con_nutri_id=current_user.nutri_id, con_pac_id=paciente_id, con_reg_con_id=reg_con_id)
        session.add(consulta_obj)
        session.commit()

        dados_antro = DadosAntropometricos(dad_con_id=consulta_obj.con_id,dad_peso_atual=float(peso),dad_altura=float(altura),dad_imc=float(imc),
            dad_circun_abdomen=float(circun_abdomen) if circun_abdomen else None,dad_circun_quadri=float(circun_quadril) if circun_quadril else None,
            dad_gord_corporal=float(gordura_corporal) if gordura_corporal else None,dad_massa_muscular=float(massa_magra) if massa_magra else None,
            dad_massa_gorda=float(massa_gorda) if massa_gorda else None,dad_dobra_tricipital=float(dobra_tricipital) if dobra_tricipital else None,
            dad_dobra_subescapular=float(dobra_subescapular) if dobra_subescapular else None,dad_dobra_supra_iliaca=float(dobra_supra_iliaca) if dobra_supra_iliaca else None,
            dad_dobra_abdominal=float(dobra_abdominal) if dobra_abdominal else None,dad_dobra_peitoral=float(dobra_peitoral) if dobra_peitoral else None,
            dad_dobra_coxa=float(dobra_coxa) if dobra_coxa else None,dad_dobra_axilar=float(dobra_axilar) if dobra_axilar else None,dad_tmb=float(tmb) if tmb else None
        )
        session.add(dados_antro)
        session.commit()
        return redirect(url_for('nutricionista.dashboard'))
        
        return render_template('nutricionista/consulta.html', sexo=sexo, paciente = paciente, idade = idade)

    return render_template('nutricionista/consulta.html', sexo=sexo, paciente = paciente, idade = idade) 

@nutricionista_bp.route('/historico_con', methods=['GET'])
@login_required
def historico_con():
    consultas = session.query(Consulta).filter_by(con_nutri_id=current_user.nutri_id).all()
    
    return render_template('nutricionista/con_historico.html', consultas=consultas)

@nutricionista_bp.route('/historico_con_paciente/<int:paciente_id>', methods=['GET'])
@login_required
def historico_con_paciente(paciente_id):
    consultas = session.query(Consulta).filter_by(con_nutri_id=current_user.nutri_id, con_pac_id = paciente_id).all()
    
    return render_template('nutricionista/con_historico.html', consultas=consultas)

@nutricionista_bp.route('/detalhes_con/<int:consulta_id>', methods=['GET'])
@login_required
def detalhes_con(consulta_id):
    consulta = session.query(Consulta).filter_by(con_id=consulta_id).first()
    dados = session.query(DadosAntropometricos).filter_by(dad_con_id=consulta_id).first()
    if consulta:
        paciente = session.query(Paciente).get(consulta.con_pac_id)
        data_nasc = paciente.pac_data_nasc
        data_nasc_ = datetime.strptime(str(data_nasc), '%Y-%m-%d')
        hoje = datetime.today().date()
        idade = hoje.year - data_nasc_.year - ((hoje.month, hoje.day) < (data_nasc_.month, data_nasc_.day))

        return render_template('nutricionista/detalhes_con.html', consulta=consulta, dados = dados, idade = idade)
    return redirect(url_for('nutricionista.historico_con'))


@nutricionista_bp.route('/dieta', methods=['GET', 'POST'])
@login_required
def dieta():
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            paciente_id = request.form.get('paciente')
            objetivo = request.form.get('objetivo')
            
            # Criar nova dieta
            nova_dieta = Dieta(
                dieta_pac_id=paciente_id,
                dieta_objetivo=objetivo
            )
            session.add(nova_dieta)
            session.flush()  # Para obter o ID da dieta antes do commit
            
            # Processar itens do cardápio
            refeicoes = request.form.getlist('refeicao[]')
            alimentos = request.form.getlist('alimento[]')
            quantidades = request.form.getlist('quantidade[]')
            
            for refeicao_id, alimento_id, quantidade in zip(refeicoes, alimentos, quantidades):
                novo_item = Cardapio(
                    ref_id=refeicao_id,
                    alimento_id=alimento_id,
                    quantidade=quantidade,
                    dieta_id=nova_dieta.dieta_id
                )
                session.add(novo_item)
            
            session.commit()
            flash('Dieta cadastrada com sucesso!', 'success')
            return redirect(url_for('nutricionista.dieta'))
            
        except Exception as e:
            session.rollback()
            flash(f'Erro ao cadastrar dieta: {str(e)}', 'error')
            return redirect(url_for('nutricionista.dieta'))
    
    # Buscar dados para o formulário
    pacientes = session.query(Paciente).filter_by(pac_nutri_id=current_user.nutri_id).all()
    alimentos = session.query(Alimento).order_by(Alimento.alimento_nome).all()
    tipos_refeicao = session.query(TipoRefeicao).all()
    
    return render_template(
        'nutricionista/dieta.html',
        pacientes=pacientes,
        alimentos=alimentos,
        tipos_refeicao=tipos_refeicao
    )

@nutricionista_bp.route('/dieta/<int:dieta_id>')
@login_required
def visualizar_dieta(dieta_id):
    dieta = session.query(Dieta).filter_by(dieta_id=dieta_id).first()
    if not dieta or dieta.paciente.pac_nutri_id != current_user.nutri_id:
        flash('Dieta não encontrada', 'error')
        return redirect(url_for('nutricionista.dieta'))
    
    return render_template('nutricionista/visualizar_dieta.html', dieta=dieta)

@nutricionista_bp.route('/dieta/<int:dieta_id>/pdf')
@login_required
def gerar_pdf_dieta(dieta_id):
    dieta = session.query(Dieta).filter_by(dieta_id=dieta_id).first()
    if not dieta or dieta.paciente.pac_nutri_id != current_user.nutri_id:
        flash('Dieta não encontrada', 'error')
        return redirect(url_for('nutricionista.dieta'))
    
    # Implementar geração de PDF aqui (usando WeasyPrint ou outra biblioteca)
    # Retornar o PDF gerado

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
        
    
        session.add(paciente)
        session.commit()
        return redirect(url_for('nutricionista.dashboard'))

    return render_template('nutricionista/cadastro_paciente.html')


@nutricionista_bp.route('/dieta/<int:dieta_id>/visualizar')
@login_required
def visualizar_dieta_salva(dieta_id):
    try:
        print(f"Tentando acessar dieta_id: {dieta_id}")  # Log para depuração
        
        # Busca a dieta com o paciente relacionado
        dieta = session.query(Dieta).join(Paciente).filter(
            Dieta.dieta_id == dieta_id,
            Paciente.pac_nutri_id == current_user.nutri_id
        ).first()
        
        print(f"Dieta encontrada: {dieta is not None}")  # Log para depuração
        
        if not dieta:
            flash('Dieta não encontrada ou você não tem permissão para acessá-la', 'error')
            print("Redirecionando para dashboard - dieta não encontrada ou sem permissão")  # Log
            return redirect(url_for('nutricionista.dashboard'))
        
        # Busca os itens do cardápio
        cardapio = session.query(Cardapio, TipoRefeicao, Alimento)\
            .join(TipoRefeicao)\
            .join(Alimento)\
            .filter(Cardapio.dieta_id == dieta_id)\
            .order_by(TipoRefeicao.tipo_refeicao_id)\
            .all()
        
        print(f"Itens do cardápio encontrados: {len(cardapio)}")  # Log para depuração
        
        # Cálculos nutricionais
        total_calorias = sum(item.Alimento.alimento_calorias * item.Cardapio.quantidade / 100 for item in cardapio)
        total_proteinas = sum(item.Alimento.alimento_proteinas * item.Cardapio.quantidade / 100 for item in cardapio)
        total_carboidratos = sum(item.Alimento.alimento_carboidratos * item.Cardapio.quantidade / 100 for item in cardapio)
        total_gorduras = sum(item.Alimento.alimento_gorduras * item.Cardapio.quantidade / 100 for item in cardapio)
        
        return render_template('nutricionista/visualizar_dieta_salva.html',
                            dieta=dieta,
                            cardapio=cardapio,
                            total_calorias=total_calorias,
                            total_proteinas=total_proteinas,
                            total_carboidratos=total_carboidratos,
                            total_gorduras=total_gorduras)
    
    except Exception as e:
        print(f"Erro ao visualizar dieta: {str(e)}")  # Log para depuração
        flash(f'Erro ao visualizar dieta: {str(e)}', 'error')
        return redirect(url_for('nutricionista.dashboard'))