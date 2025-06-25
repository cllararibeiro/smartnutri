create database db_smartnutri;

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

CREATE TABLE tb_tipos_refeicoes (
    tipo_refeicao_id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_nome VARCHAR(255) NOT NULL
);

CREATE TABLE tb_alimentos (
    alimento_id INT AUTO_INCREMENT PRIMARY KEY,
    alimento_nome VARCHAR(500) NOT NULL,  
    alimento_categoria VARCHAR(255),  
    alimento_calorias DECIMAL(10, 2),  
    alimento_proteinas DECIMAL(10, 2),  
    alimento_carboidratos DECIMAL(10, 2),  
    alimento_gorduras DECIMAL(10, 2),  
    alimento_fibras DECIMAL(10, 2) 
);
 
 CREATE TABLE tb_dietas (
    dieta_id INT AUTO_INCREMENT PRIMARY KEY,
    dieta_pac_id INT NOT NULL,  
    dieta_con_id INT NOT NULL,
    FOREIGN KEY (dieta_pac_id) REFERENCES tb_pacientes(pac_id),
    FOREIGN KEY (dieta_con_id) REFERENCES tb_consultas(con_id)
);
 
  CREATE TABLE tb_substituicoes (
    substituicao_id INT AUTO_INCREMENT PRIMARY KEY,  
    dieta_id INT NOT NULL,
    alimento_original_id INT NOT NULL,  -- O alimento original que será substituído
    alimento_substituto_id INT NOT NULL,  -- O alimento que irá substituir o original
    quantidade DECIMAL(10, 2) NOT NULL,  -- Quantidade do alimento substituto 
    FOREIGN KEY (alimento_original_id) REFERENCES tb_alimentos(alimento_id),  
    FOREIGN KEY (dieta_id) REFERENCES tb_dietas(dieta_id),
    FOREIGN KEY (alimento_substituto_id) REFERENCES tb_alimentos(alimento_id) 
);
 
CREATE TABLE tb_cardapio (
    cardapio_id INT AUTO_INCREMENT PRIMARY KEY,
    ref_id INT NOT NULL,  
    alimento_id INT NOT NULL,  
    quantidade DECIMAL(10, 2) NOT NULL,  
    dieta_id INT NOT NULL,  
    FOREIGN KEY (ref_id) REFERENCES tb_tipos_refeicoes(tipo_refeicao_id),
    FOREIGN KEY (alimento_id) REFERENCES tb_alimentos(alimento_id),
    FOREIGN KEY (dieta_id) REFERENCES tb_dietas(dieta_id)  
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

INSERT INTO tb_tipos_refeicoes (tipo_nome) VALUES
('Café da Manhã'),
('Almoço'),
('Lanche'),
('Jantar'),
('Ceia');

INSERT INTO tb_alimentos (alimento_nome, alimento_categoria, alimento_calorias, alimento_proteinas, alimento_carboidratos, alimento_gorduras, alimento_fibras) VALUES
('Arroz Integral', 'Carboidrato', 111.00, 2.60, 23.00, 0.90, 1.80),
('Feijão Preto', 'Proteína', 127.00, 8.67, 22.50, 0.50, 8.00),
('Frango Grelhado', 'Proteína', 165.00, 31.00, 0.00, 3.60, 0.00),
('Brócolis', 'Vegetal', 55.00, 3.70, 11.00, 0.60, 5.10),
('Banana', 'Fruta', 89.00, 1.10, 22.80, 0.30, 2.60),
('Abacate', 'Fruta', 160.00, 2.00, 8.50, 14.66, 6.70),
('Ovos', 'Proteína', 68.00, 5.50, 0.60, 4.80, 0.00),
('Pão Integral', 'Carboidrato', 69.00, 3.60, 12.00, 1.10, 2.40);





