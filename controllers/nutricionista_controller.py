from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.config import Session
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from models.models import Nutricionista, Paciente, Consulta, Dieta, RegistroConsulta, DadosAntropometricos, Alimento, TipoRefeicao, Cardapio, Substituicao
import logging
from fpdf import FPDF
from io import BytesIO
from models.models import Substituicao
from sqlalchemy.orm import aliased


nutricionista_bp = Blueprint('nutricionista', __name__, url_prefix='/nutricionista', template_folder='templates')

session = Session()

logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.INFO)


@nutricionista_bp.route('/dashboard')
@login_required
def dashboard():
    busca = request.args.get('busca','')
    print(f"Termo da busca: {busca}")
    pacientes = session.query(Paciente).filter(Paciente.pac_nome.like(f'%{busca}%'))\
    .filter_by(pac_nutri_id=current_user.nutri_id)\
    .order_by(desc(Paciente.pac_data_cadastro)).all() 
    consulta = (session.query(Consulta).filter_by(con_nutri_id=current_user.nutri_id).order_by(Consulta.con_data.desc()).first())


    return render_template('nutricionista/dashboard.html', pacientes=pacientes, consulta=consulta)

@nutricionista_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    nutricionista = session.query(Nutricionista).filter_by(nutri_id=current_user.nutri_id).first()
    erros = {}

    if request.method == 'POST':
        email = request.form['nutri_email']
        telefone = request.form['nutri_telefone']
        cpf = request.form['nutri_cpf']
        crn = request.form['nutri_crn']
        form = request.form

        if session.query(Nutricionista).filter(Nutricionista.nutri_email == email, Nutricionista.nutri_id != current_user.nutri_id).first():
            erros['nutri_email'] = 'Este e-mail já está em uso.'

        if session.query(Nutricionista).filter(Nutricionista.nutri_telefone == telefone, Nutricionista.nutri_id != current_user.nutri_id).first():
            erros['nutri_telefone'] = 'Este telefone já está em uso.'

        if session.query(Nutricionista).filter(Nutricionista.nutri_cpf == cpf, Nutricionista.nutri_id != current_user.nutri_id).first():
            erros['nutri_cpf'] = 'Este CPF já está em uso.'

        if session.query(Nutricionista).filter(Nutricionista.nutri_crn == crn, Nutricionista.nutri_id != current_user.nutri_id).first():
            erros['nutri_crn'] = 'Este CRN já está em uso.'

        if erros:
            return render_template('nutricionista/perfil.html', nutricionista=nutricionista, erros=erros, form=form)
        
        nutricionista.nutri_email = email
        nutricionista.nutri_telefone = telefone
        nutricionista.nutri_cpf = cpf
        nutricionista.nutri_crn = crn

        try:
            session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Ocorreu um erro ao atualizar o perfil: {str(e)}', 'danger')
        return redirect(url_for('nutricionista.perfil'))
    
    return render_template('nutricionista/perfil.html', nutricionista=nutricionista, erros={}, form={})


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
        erros = {}
        
        if session.query(Paciente).filter_by(pac_email=email).first():
            erros['email'] = 'Este e-mail já está cadastrado.'

        if session.query(Paciente).filter_by(pac_cpf=cpf).first():
            erros['cpf'] = 'Este CPF já está cadastrado.'

        if session.query(Paciente).filter_by(pac_tel=tel).first():
            erros['telefone'] = 'Este telefone já está cadastrado.'

        if erros:
            return render_template('nutricionista/cadastro_paciente.html', erros=erros, form=request.form)
        
        data_nasc_obj = datetime.strptime(data_nasc, '%Y-%m-%d') 
        
        hoje = datetime.today()
        idade = hoje.year - data_nasc_obj.year - ((hoje.month, hoje.day) < (data_nasc_obj.month, data_nasc_obj.day))

        paciente = Paciente(pac_nome=nome,pac_email=email,pac_data_nasc=data_nasc_obj,pac_idade=idade,
            pac_sexo=sexo,pac_tel=tel,pac_cpf=cpf,pac_doencas_preexistentes=doencas_preexistentes,
            pac_historico_familiar=historico_familiar,pac_nutri_id=current_user.nutri_id)
        
        
        session.add(paciente)
        session.commit()
        return redirect(url_for('nutricionista.dashboard'))

    return render_template('nutricionista/cadastro_paciente.html', erros={}, form={})

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
        return redirect(url_for('nutricionista.dieta', paciente_id=paciente_id, consulta_id=consulta_obj.con_id))
        
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
    dietas =  session.query(Consulta).filter_by(con_nutri_id=current_user.nutri_id, con_pac_id = paciente_id).all()

    return render_template('nutricionista/con_historico.html', consultas=consultas)

@nutricionista_bp.route('/detalhes_con/<int:consulta_id>', methods=['GET'])
@login_required
def detalhes_con(consulta_id):
    consulta = session.query(Consulta).filter_by(con_id=consulta_id).first()
    dados = session.query(DadosAntropometricos).filter_by(dad_con_id=consulta_id).first()
    paciente_id = consulta.con_pac_id
    dieta = (
        session.query(Dieta)
        .filter(Dieta.dieta_con_id == consulta_id)
        .first()
    )
    #dieta = (session.query(Dieta).join(Consulta, Dieta.dieta_con_id == Consulta.con_id).filter(Dieta.dieta_pac_id == paciente_id).order_by(Consulta.con_data.desc()).first())


    if consulta:
        paciente = session.query(Paciente).get(consulta.con_pac_id)
        data_nasc = paciente.pac_data_nasc
        data_nasc_ = datetime.strptime(str(data_nasc), '%Y-%m-%d')
        hoje = datetime.today().date()
        idade = hoje.year - data_nasc_.year - ((hoje.month, hoje.day) < (data_nasc_.month, data_nasc_.day))

        return render_template('nutricionista/detalhes_con.html',consulta=consulta, dados=dados, idade=idade, dieta=dieta)
    return redirect(url_for('nutricionista.historico_con'))

@nutricionista_bp.route('/dieta/<int:paciente_id>/<int:consulta_id>', methods=['GET', 'POST'])
@login_required
def dieta(paciente_id, consulta_id):
    if request.method == 'POST':
        try:
            # Criar nova dieta
            nova_dieta = Dieta(
                dieta_pac_id=paciente_id,
                dieta_con_id=consulta_id 
            )
            session.add(nova_dieta)
            session.commit()  # garante dieta_id para usar nos itens

            # Captura dos dados
            refeicoes = request.form.getlist('refeicao[]')  # lista de ids refeicoes
            alimentos = request.form.getlist('alimento[]')  # lista de alimentos (todos juntos)
            quantidades = request.form.getlist('quantidade[]')  # lista de quantidades (todos juntos)
            refeicao_ids = request.form.getlist('refeicao_id[]')  # lista paralela com qual refeicao cada alimento pertence

            # Verificações básicas
            if not refeicoes or not alimentos or not quantidades or not refeicao_ids:
                flash('Erro: Dados do formulário incompletos!', 'error')
                return redirect(url_for('nutricionista.dieta', paciente_id=paciente_id, consulta_id=consulta_id))

            # Todos os arrays devem ter o mesmo tamanho
            if not (len(alimentos) == len(quantidades) == len(refeicao_ids)):
                flash('Erro: Dados inconsistentes no formulário!', 'error')
                return redirect(url_for('nutricionista.dieta', paciente_id=paciente_id, consulta_id=consulta_id))

            # Iterar pelos alimentos
            for alimento_id, quantidade, ref_id in zip(alimentos, quantidades, refeicao_ids):
                try:
                    quantidade_float = float(quantidade)
                except ValueError:
                    flash(f'Erro na quantidade: {quantidade}', 'error')
                    return redirect(url_for('nutricionista.dieta', paciente_id=paciente_id, consulta_id=consulta_id))

                novo_item = Cardapio(
                    ref_id=ref_id,
                    alimento_id=alimento_id,
                    quantidade=quantidade_float,
                    dieta_id=nova_dieta.dieta_id
                )
                session.add(novo_item)

            session.commit()

            flash('Dieta cadastrada com sucesso!', 'success')
            return redirect(url_for('nutricionista.substituicoes', dieta_id=nova_dieta.dieta_id))

        except Exception as e:
            session.rollback()
            flash(f'Erro ao cadastrar dieta: {str(e)}', 'error')
            return redirect(url_for('nutricionista.dieta', paciente_id=paciente_id, consulta_id=consulta_id))

    pacientes = session.query(Paciente).filter_by(pac_nutri_id=current_user.nutri_id).all()
    alimentos = session.query(Alimento).order_by(Alimento.alimento_nome).all()
    tipos_refeicao = session.query(TipoRefeicao).all()

    return render_template(
        'nutricionista/dieta.html',
        pacientes=pacientes,
        alimentos=alimentos,
        tipos_refeicao=tipos_refeicao,
        paciente_id=paciente_id,
        consulta_id=consulta_id
    )

@nutricionista_bp.route('/substituicoes/<int:dieta_id>', methods=['GET', 'POST'])
@login_required
def substituicoes(dieta_id):
    dieta = session.query(Dieta).filter_by(dieta_id=dieta_id).first()
    if not dieta:
        flash('Dieta não encontrada.', 'error')
        return redirect(url_for('nutricionista.dashboard'))

    if request.method == 'POST':
        alimento_original_id = request.form.get('alimento_original')
        alimento_substituto_id = request.form.get('alimento_substituto')
        quantidadesub = request.form.get('quantidadesub')
        quantidade = request.form.get('quantidade')

        if alimento_original_id and alimento_substituto_id and quantidade and quantidadesub:
            try:
                quantidade_float = float(quantidade)
                quantidadesub_float = float(quantidadesub)
                nova_substituicao = Substituicao(
                    dieta_id=dieta_id,
                    alimento_original_id=alimento_original_id,
                    quantidade=quantidade_float,
                    alimento_substituto_id=alimento_substituto_id,
                    quantidadesub=quantidadesub_float
                )
                session.add(nova_substituicao)
                session.commit()
                flash('Substituição adicionada com sucesso!', 'success')
            except Exception as e:
                session.rollback()
                flash(f'Erro ao adicionar substituição: {str(e)}', 'error')
        else:
            flash('Preencha todos os campos da substituição.', 'error')

    # Buscar dados para o form
    cardapio = session.query(Cardapio).filter_by(dieta_id=dieta_id).all()
    alimentos = session.query(Alimento).order_by(Alimento.alimento_nome).all()

    return render_template('nutricionista/substituicoes.html',
                           dieta=dieta,
                           cardapio=cardapio,
                           alimentos=alimentos)



@nutricionista_bp.route('/visualizardieta/<int:dieta_id>')
@login_required
def visualizar_dieta(dieta_id):
    try:
        print(f"Tentando acessar dieta_id: {dieta_id}")  
        
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

        AlimentoOriginal = aliased(Alimento)
        AlimentoSubstituto = aliased(Alimento)

        substituicoes = session.query(Substituicao,AlimentoOriginal,AlimentoSubstituto).join(
        AlimentoOriginal, Substituicao.alimento_original_id == AlimentoOriginal.alimento_id).join(
        AlimentoSubstituto, Substituicao.alimento_substituto_id == AlimentoSubstituto.alimento_id).filter(
        Substituicao.dieta_id == dieta_id).all()
        
        # Cálculos nutricionais
        total_calorias = sum(item.Alimento.alimento_calorias * item.Cardapio.quantidade / 100 for item in cardapio)
        total_proteinas = sum(item.Alimento.alimento_proteinas * item.Cardapio.quantidade / 100 for item in cardapio)
        total_carboidratos = sum(item.Alimento.alimento_carboidratos * item.Cardapio.quantidade / 100 for item in cardapio)
        total_gorduras = sum(item.Alimento.alimento_gorduras * item.Cardapio.quantidade / 100 for item in cardapio)
        
       
        return render_template('nutricionista/visualizar_dieta_salva.html',
                               dieta=dieta,
                               cardapio=cardapio,
                               substituicoes=substituicoes,
                               total_calorias=total_calorias,
                               total_proteinas=total_proteinas,
                               total_carboidratos=total_carboidratos,
                               total_gorduras=total_gorduras)
    
    except Exception as e:
        print(f"Erro ao visualizar dieta: {str(e)}")  # Log para depuração
        flash(f'Erro ao visualizar dieta: {str(e)}', 'error')
    
    
@nutricionista_bp.route("/relatorio/<int:paciente_id>", methods=["GET"])
def relatorio_paciente(paciente_id):
    paciente = session.query(Paciente).get(paciente_id)
    consultas = session.query(Consulta).filter_by(con_pac_id=paciente_id).order_by(Consulta.con_data.desc()).all()
    
    con_ids = request.args.getlist("datas")
    dados = []

    if con_ids:
        for con_id in con_ids:
            consulta = session.query(Consulta).get(con_id)
            dad = session.query(DadosAntropometricos).filter_by(dad_con_id=con_id).first()
            dados.append({
                "data": consulta.con_data.strftime('%d/%m/%Y'),
                "peso": float(dad.dad_peso_atual) if dad.dad_peso_atual is not None else 0.0,
                "imc": float(dad.dad_imc)if dad.dad_imc is not None else 0.0,
                "altura": float(dad.dad_altura) * 100 if dad.dad_altura is not None else 0.0,
                "massa_gorda": float(dad.dad_massa_gorda) if dad.dad_massa_gorda is not None else 0.0,
                "massa_magra": float(dad.dad_massa_muscular) if dad.dad_massa_muscular is not None else 0.0,
                "dobra_abd": float(dad.dad_dobra_abdominal) if dad.dad_dobra_abdominal is not None else 0.0,
                "dobra_coxa": float(dad.dad_dobra_coxa) if dad.dad_dobra_coxa is not None else 0.0
            })

    return render_template("nutricionista/relatorio_paciente.html",
        paciente=paciente,
        consultas=consultas,
        datas=[d["data"] for d in dados],
        pesos=[d["peso"] for d in dados],
        imcs=[d["imc"] for d in dados],
        alturas=[d["altura"] for d in dados],
        massas_gordas=[d["massa_gorda"] for d in dados],
        massas_musculares=[d["massa_magra"] for d in dados],
        dobras_abd=[d["dobra_abd"] for d in dados],
        dobras_coxa=[d["dobra_coxa"] for d in dados]
    )


@nutricionista_bp.route('/editar_paciente/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
def editar_paciente(paciente_id):
    paciente = session.query(Paciente).get(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for('nutricionista.dashboard'))

    if request.method == 'POST':
        novo_email = request.form.get('email')
        novo_cpf = request.form.get('cpf')
        novo_tel = request.form.get('telefone')
        erros = {}
        
        if session.query(Paciente).filter_by(pac_email=novo_email).first():
            erros['email'] = 'Este e-mail já está cadastrado.'

        if session.query(Paciente).filter_by(pac_cpf=novo_cpf).first():
            erros['cpf'] = 'Este CPF já está cadastrado.'

        if session.query(Paciente).filter_by(pac_tel=novo_tel).first():
            erros['telefone'] = 'Este telefone já está cadastrado.'

        if erros:
            return render_template('nutricionista/editar_paciente.html', erros=erros, form=request.form, paciente=paciente)
    
        paciente.pac_nome = request.form.get('nome')
        paciente.pac_email = novo_email
        paciente.pac_data_nasc = datetime.strptime(request.form.get('data_nasc'), '%Y-%m-%d')
        paciente.pac_sexo = request.form.get('sexo')
        paciente.pac_tel = novo_tel
        paciente.pac_cpf = novo_cpf
        paciente.pac_doencas_preexistentes = request.form.get('doencas_preexistentes')
        paciente.pac_historico_familiar = request.form.get('historico_familiar')

        hoje = datetime.today().date()
        paciente.pac_idade = hoje.year - paciente.pac_data_nasc.year - (
                (hoje.month, hoje.day) < (paciente.pac_data_nasc.month, paciente.pac_data_nasc.day)
            )
            

        session.commit()
        return redirect(url_for('nutricionista.dashboard'))

    return render_template('nutricionista/editar_paciente.html', paciente=paciente, erros ={}, form={})

