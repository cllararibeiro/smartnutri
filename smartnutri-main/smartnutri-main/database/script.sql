create DATABASE db_smartnutri;

USE db_smartnutri;

CREATE TABLE tb_nutricionista (
    nutri_id INT AUTO_INCREMENT PRIMARY KEY,
    nutri_nome VARCHAR(500) NOT NULL,
    nutri_email VARCHAR(500) NOT NULL UNIQUE,
    nutri_senha VARCHAR(500) NOT NULL,
    nutri_cpf VARCHAR(20) NOT NULL UNIQUE,
    nutri_telefone VARCHAR(15) NOT NULL,
    nutri_crn VARCHAR(15) NOT NULL UNIQUE
);

CREATE TABLE tb_pacientes (
    pac_id INT AUTO_INCREMENT PRIMARY KEY,
    pac_nutri_id INT NOT NULL,
    pac_nome VARCHAR(500) NOT NULL,
    pac_email VARCHAR(500) NOT NULL UNIQUE,
    pac_data_nasc DATE NOT NULL,
    pac_idade INT NOT NULL,
    pac_sexo ENUM('Masculino', 'Feminino') NOT NULL,
    pac_tel VARCHAR(15) NOT NULL UNIQUE,
    pac_cpf VARCHAR(20) NOT NULL UNIQUE,
    pac_doencas_preexistentes TEXT,
    pac_historico_familiar TEXT,
    pac_data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pac_nutri_id) REFERENCES tb_nutricionista(nutri_id)
);

CREATE TABLE tb_registro_consulta (
    reg_con_id INT AUTO_INCREMENT PRIMARY KEY,
    reg_con_objetivos TEXT,
    reg_con_rotina TEXT,
    reg_con_obs TEXT,
    reg_con_preferencias TEXT,
    reg_con_aversoes TEXT
);

CREATE TABLE tb_exames (
    exame_id INT AUTO_INCREMENT PRIMARY KEY,
    exame_nome VARCHAR(500) NOT NULL,
    tipo_exame VARCHAR(500) NOT NULL
);

CREATE TABLE tb_consultas (
    con_id INT AUTO_INCREMENT PRIMARY KEY,
    con_data DATETIME NOT NULL,
    con_nutri_id INT NOT NULL,
    con_pac_id INT NOT NULL,
    con_reg_con_id INT NOT NULL,
    FOREIGN KEY (con_nutri_id) REFERENCES tb_nutricionista(nutri_id),
    FOREIGN KEY (con_pac_id) REFERENCES tb_pacientes(pac_id),
    FOREIGN KEY (con_reg_con_id) REFERENCES tb_registro_consulta(reg_con_id)
);

CREATE TABLE tb_resultados_exames (
    res_exame_id INT AUTO_INCREMENT PRIMARY KEY,
    res_exame_con_id INT NOT NULL,
    res_exame_exame_id INT NOT NULL,
    res_exame_resultado VARCHAR(500) NOT NULL,
    FOREIGN KEY (res_exame_con_id) REFERENCES tb_consultas(con_id),
    FOREIGN KEY (res_exame_exame_id) REFERENCES tb_exames(exame_id)
);

CREATE TABLE tb_refeicoes (
    ref_id INT AUTO_INCREMENT PRIMARY KEY,
    ref_nome VARCHAR(500) NOT NULL,
    ref_opcao1 TEXT NOT NULL,
    ref_opcao2 TEXT DEFAULT NULL,
    ref_observacoes TEXT DEFAULT NULL
);

CREATE TABLE tb_dietas (
    dieta_id INT AUTO_INCREMENT PRIMARY KEY,
    dieta_pac_id INT NOT NULL,
    dieta_ref_id INT NOT NULL,
    FOREIGN KEY (dieta_pac_id) REFERENCES tb_pacientes(pac_id),
    FOREIGN KEY (dieta_ref_id) REFERENCES tb_refeicoes(ref_id)
);

CREATE TABLE tb_dados_antro (
    dad_id INT AUTO_INCREMENT PRIMARY KEY,
    dad_con_id INT NOT NULL,
    dad_peso_atual DECIMAL(5,2) NOT NULL,
    dad_imc DECIMAL(5,2) NOT NULL,
    dad_altura DECIMAL(5,2) NOT NULL,
    dad_circun_abdomen DECIMAL(5,2) DEFAULT NULL,
    dad_circun_quadri DECIMAL(5,2) DEFAULT NULL,
    dad_gord_corporal DECIMAL(5,2) DEFAULT NULL,
    dad_massa_muscular DECIMAL(5,2) DEFAULT NULL,
    dad_massa_gorda DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_tricipital DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_subescapular DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_supra_iliaca DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_abdominal DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_peitoral DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_coxa DECIMAL(5,2) DEFAULT NULL,
    dad_dobra_axilar DECIMAL(5,2) DEFAULT NULL,
    dad_tmb DECIMAL(6,2) DEFAULT NULL,
    FOREIGN KEY (dad_con_id) REFERENCES tb_consultas(con_id)
);
