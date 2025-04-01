from sqlalchemy import create_engine, Integer, String, Date, Enum,\
Text, ForeignKey, DECIMAL, DATETIME, DateTime
from sqlalchemy.orm import mapped_column, sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from database.config import Base
from datetime import datetime

class Nutricionista(Base, UserMixin):
    __tablename__ = 'tb_nutricionista'

    nutri_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nutri_nome = mapped_column(String(500), nullable=False)
    nutri_email = mapped_column(String(500), nullable=False, unique=True)
    nutri_senha = mapped_column(String(500), nullable=False)
    nutri_cpf = mapped_column(String(20), nullable=False, unique=True)
    nutri_telefone = mapped_column(String(15), nullable=False)
    nutri_crn = mapped_column(String(15), nullable=False, unique=True)

    pacientes = relationship('Paciente', back_populates='nutricionista')
    consultas = relationship('Consulta', back_populates='nutricionista')

    
    def set_password(self, password: str):
        self.nutri_senha = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.nutri_senha, password)

    def get_id(self):
        return str(self.nutri_id)

class Paciente(Base):
    __tablename__ = 'tb_pacientes'

    pac_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    pac_nutri_id = mapped_column(Integer, ForeignKey('tb_nutricionista.nutri_id'), nullable=False)
    pac_nome = mapped_column(String(500), nullable=False)
    pac_email = mapped_column(String(500), nullable=False, unique=True)
    pac_data_nasc = mapped_column(Date, nullable=False)
    pac_idade = mapped_column(Integer, nullable=False)
    pac_sexo = mapped_column(Enum('Masculino', 'Feminino'), nullable=False)
    pac_tel = mapped_column(String(15), nullable=False, unique=True)
    pac_cpf = mapped_column(String(20), nullable=False, unique=True)
    pac_doencas_preexistentes = mapped_column(Text)
    pac_historico_familiar = mapped_column(Text)
    pac_data_cadastro = mapped_column(DateTime, default=datetime.utcnow) 

    nutricionista = relationship('Nutricionista', back_populates='pacientes')
    consultas = relationship('Consulta', back_populates='paciente')

    dietas = relationship('Dieta', back_populates='paciente')


class RegistroConsulta(Base):
    __tablename__ = 'tb_registro_consulta'

    reg_con_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    reg_con_objetivos = mapped_column(Text)
    reg_con_rotina = mapped_column(Text)
    reg_con_obs = mapped_column(Text)
    reg_con_preferencias = mapped_column(Text)
    reg_con_aversoes = mapped_column(Text)

    consultas = relationship('Consulta', back_populates='registro_consulta')


class Exame(Base):
    __tablename__ = 'tb_exames'

    exame_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    exame_nome = mapped_column(String(500), nullable=False)
    tipo_exame = mapped_column(String(500), nullable=False)

    resultados_exames = relationship('ResultadoExame', back_populates='exame')


class ResultadoExame(Base):
    __tablename__ = 'tb_resultados_exames'

    res_exame_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    res_exame_con_id = mapped_column(Integer, ForeignKey('tb_consultas.con_id'), nullable=False)
    res_exame_exame_id = mapped_column(Integer, ForeignKey('tb_exames.exame_id'), nullable=False)
    res_exame_resultado = mapped_column(String(500), nullable=False)

    exame = relationship('Exame', back_populates='resultados_exames')
    consulta = relationship('Consulta', back_populates='resultados_exames')


class TipoRefeicao(Base):
    __tablename__ = 'tb_tipos_refeicoes'

    tipo_refeicao_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_nome = mapped_column(String(255), nullable=False)

    cardapios = relationship('Cardapio', back_populates='tipo_refeicao')


class Alimento(Base):
    __tablename__ = 'tb_alimentos'

    alimento_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    alimento_nome = mapped_column(String(500), nullable=False)
    alimento_categoria = mapped_column(String(255))
    alimento_calorias = mapped_column(DECIMAL(10, 2))
    alimento_proteinas = mapped_column(DECIMAL(10, 2))
    alimento_carboidratos = mapped_column(DECIMAL(10, 2))
    alimento_gorduras = mapped_column(DECIMAL(10, 2))
    alimento_fibras = mapped_column(DECIMAL(10, 2))

    substituicoes = relationship('Substituicao', back_populates='alimento_original', foreign_keys='Substituicao.alimento_original_id')
    substituicoes_substitutos = relationship('Substituicao', back_populates='alimento_substituto', foreign_keys='Substituicao.alimento_substituto_id')


class Substituicao(Base):
    __tablename__ = 'tb_substituicoes'

    substituicao_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    alimento_original_id = mapped_column(Integer, ForeignKey('tb_alimentos.alimento_id'), nullable=False)
    alimento_substituto_id = mapped_column(Integer, ForeignKey('tb_alimentos.alimento_id'), nullable=False)
    quantidade = mapped_column(DECIMAL(10, 2), nullable=False)

    alimento_original = relationship('Alimento', foreign_keys=[alimento_original_id], back_populates='substituicoes')
    alimento_substituto = relationship('Alimento', foreign_keys=[alimento_substituto_id], back_populates='substituicoes_substitutos')


class Cardapio(Base):
    __tablename__ = 'tb_cardapio'

    cardapio_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    ref_id = mapped_column(Integer, ForeignKey('tb_tipos_refeicoes.tipo_refeicao_id'), nullable=False)
    alimento_id = mapped_column(Integer, ForeignKey('tb_alimentos.alimento_id'), nullable=False)
    quantidade = mapped_column(DECIMAL(10, 2), nullable=False)
    dieta_id = mapped_column(Integer, ForeignKey('tb_dietas.dieta_id'), nullable=False)

    tipo_refeicao = relationship('TipoRefeicao', back_populates='cardapios')
    alimento = relationship('Alimento')
    dieta = relationship("Dieta", back_populates="cardapios")


class Dieta(Base):
    __tablename__ = 'tb_dietas'

    dieta_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    dieta_pac_id = mapped_column(Integer, ForeignKey('tb_pacientes.pac_id'), nullable=False)
    dieta_objetivo = mapped_column(String(255))

    paciente = relationship('Paciente', back_populates='dietas')
    cardapios = relationship("Cardapio", back_populates="dieta", cascade="all, delete-orphan")

class Consulta(Base):
    __tablename__ = 'tb_consultas'

    con_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    con_data = mapped_column(DATETIME, nullable=False)
    con_nutri_id = mapped_column(Integer, ForeignKey('tb_nutricionista.nutri_id'), nullable=False)
    con_pac_id = mapped_column(Integer, ForeignKey('tb_pacientes.pac_id'), nullable=False)
    con_reg_con_id = mapped_column(Integer, ForeignKey('tb_registro_consulta.reg_con_id'), nullable=True)

    nutricionista = relationship('Nutricionista', back_populates='consultas')
    paciente = relationship('Paciente', back_populates='consultas')
    registro_consulta = relationship('RegistroConsulta', back_populates='consultas')
    dados_antropometricos = relationship('DadosAntropometricos', back_populates='consulta')
    resultados_exames = relationship('ResultadoExame', back_populates='consulta')


class DadosAntropometricos(Base):
    __tablename__ = 'tb_dados_antro'

    dad_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    dad_con_id = mapped_column(Integer, ForeignKey('tb_consultas.con_id'), nullable=False)
    dad_peso_atual = mapped_column(DECIMAL(5, 2), nullable=False)
    dad_imc = mapped_column(DECIMAL(5, 2), nullable=False)
    dad_altura = mapped_column(DECIMAL(5, 2), nullable=False)
    dad_circun_abdomen = mapped_column(DECIMAL(5, 2))
    dad_circun_quadri = mapped_column(DECIMAL(5, 2))
    dad_gord_corporal = mapped_column(DECIMAL(5, 2))
    dad_massa_muscular = mapped_column(DECIMAL(5, 2))
    dad_massa_gorda = mapped_column(DECIMAL(5, 2))

    dad_dobra_tricipital = mapped_column(DECIMAL(5, 2))
    dad_dobra_subescapular = mapped_column(DECIMAL(5, 2))
    dad_dobra_supra_iliaca = mapped_column(DECIMAL(5, 2))
    dad_dobra_abdominal = mapped_column(DECIMAL(5, 2))
    dad_dobra_peitoral = mapped_column(DECIMAL(5, 2))
    dad_dobra_coxa = mapped_column(DECIMAL(5, 2))
    dad_dobra_axilar = mapped_column(DECIMAL(5, 2))
    dad_tmb = mapped_column(DECIMAL(6, 2))
    
    consulta = relationship('Consulta', back_populates='dados_antropometricos')
