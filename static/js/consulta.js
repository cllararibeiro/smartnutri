// Função para calcular o IMC
function calcularIMC() {
    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value);

    if (isNaN(peso) || isNaN(altura) || altura === 0) {
        document.getElementById('imc').value = '';  
        return;
    }

    const imc = peso / (altura * altura);
    document.getElementById('imc').value = imc.toFixed(2);
}

// Função para alternar entre 3 e 7 dobras
function toggleDobras() {
    const metodo = document.getElementById('metodo').value;
    const sexo = document.getElementById('sexo').value;

    // Oculta todas as dobras inicialmente
    const dobras = [
        'dobraAbdominalDiv',
        'dobraPeitoralDiv',
        'dobraCoxaDiv',
        'dobraAxilarDiv',
        'dobraSubescapularDiv',
        'dobraSupraIliacaDiv',
        'dobraTricipitalDiv'
    ];
    
    dobras.forEach(id => {
        document.getElementById(id).style.display = 'none';
    });

    if (metodo === '3') {
        // Exibe dobras específicas para 3 dobras
        if (sexo === 'Feminino') {
            document.getElementById('dobraTricipitalDiv').style.display = 'block';
            document.getElementById('dobraSupraIliacaDiv').style.display = 'block';
        } else {
            document.getElementById('dobraPeitoralDiv').style.display = 'block';
            document.getElementById('dobraAbdominalDiv').style.display = 'block';
        }
        document.getElementById('dobraCoxaDiv').style.display = 'block'; // Coxa sempre aparece
    } else if (metodo === '7') {
        // Exibe todas as dobras para 7 dobras
        dobras.forEach(id => {
            document.getElementById(id).style.display = 'block';
        });
    }
}

// Função para calcular o percentual de gordura e massa magra
function calcularPercentualGordura() {
    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value);
    const idade = parseFloat(document.getElementById('idade').value) || 0;
    const sexo = document.getElementById('sexo').value;
    const metodo = document.getElementById('metodo').value;

    // Verificando se o peso e altura são válidos
    if (isNaN(peso) || isNaN(altura) || altura <= 0 || peso <= 0) {
        alert('Por favor, insira peso e altura válidos.');
        return;
    }

    // Verificar se idade e sexo são válidos
    if (!sexo || isNaN(idade) || idade <= 0) {
        alert('Por favor, insira uma idade válida e selecione o sexo.');
        return;
    }

    let percentualGordura = 0;
    let massaMagra = 0;

    if (metodo === '3') {
        // Captura os valores das dobras para 3 dobras
        const tricipital = parseFloat(document.getElementById('dobraTricipital').value) || 0;
        const supraIliaca = parseFloat(document.getElementById('dobraSupraIliaca').value) || 0;
        const coxa = parseFloat(document.getElementById('dobraCoxa').value) || 0;
        const peitoral = parseFloat(document.getElementById('dobraPeitoral').value) || 0;
        const abdominal = parseFloat(document.getElementById('dobraAbdominal').value) || 0;

        // Verificando se algum valor das dobras é NaN ou inválido
        if (isNaN(tricipital) || isNaN(supraIliaca) || isNaN(coxa) || isNaN(peitoral) || isNaN(abdominal)) {
            alert('Por favor, preencha todos os campos das dobras corretamente.');
            return; // Interrompe a execução se algum valor for inválido
        }

        let somaDobras = sexo === 'Masculino' ? peitoral + abdominal + coxa : tricipital + supraIliaca + coxa;

        // Fórmula de cálculo
        const DC = sexo === 'Masculino'
            ? 1.1093800 - 0.0008267 * somaDobras + 0.0000016 * (somaDobras ** 2) - 0.0002574 * idade
            : 1.0994921 - 0.0009929 * somaDobras + 0.0000023 * (somaDobras ** 2) - 0.0001392 * idade;

        percentualGordura = (495 / DC) - 450;
    } else if (metodo === '7') {
        // Captura os valores das 7 dobras
        const tricipital = parseFloat(document.getElementById('dobraTricipital').value) || 0;
        const subescapular = parseFloat(document.getElementById('dobraSubescapular').value) || 0;
        const peitoral = parseFloat(document.getElementById('dobraPeitoral').value) || 0;
        const axilar = parseFloat(document.getElementById('dobraAxilar').value) || 0;
        const abdominal = parseFloat(document.getElementById('dobraAbdominal').value) || 0;
        const supraIliaca = parseFloat(document.getElementById('dobraSupraIliaca').value) || 0;
        const coxa = parseFloat(document.getElementById('dobraCoxa').value) || 0;

        // Verificando se algum valor das 7 dobras é NaN ou inválido
        if (isNaN(tricipital) || isNaN(subescapular) || isNaN(peitoral) || isNaN(axilar) || isNaN(abdominal) || isNaN(supraIliaca) || isNaN(coxa)) {
            alert('Por favor, preencha todos os campos das dobras corretamente.');
            return; 
        }

        const somaDobras = tricipital + subescapular + peitoral + axilar + abdominal + supraIliaca + coxa;

        // Fórmula de cálculo para 7 dobras com base no sexo
        let DC;
        if (sexo === 'Masculino') {
            DC = 1.112 - 0.00043499 * somaDobras + 0.00000055 * (somaDobras ** 2) - 0.00028826 * idade;
        } else if (sexo === 'Feminino') {
            DC = 1.097 - 0.00043499 * somaDobras + 0.00000055 * (somaDobras ** 2) - 0.00028826 * idade;
        }

        percentualGordura = (495 / DC) - 450;
    }

    // Calculando a massa magra
    massaMagra = peso - (peso * (percentualGordura / 100));
    const massaGorda = peso - massaMagra;

    // Exibir os resultados
    console.log('Percentual de Gordura:', percentualGordura);  // Para depuração
    document.getElementById('percentualGordura').value = percentualGordura.toFixed(2);
    document.getElementById('massaMagra').value = massaMagra.toFixed(2);
    document.getElementById('massaGorda').value = massaGorda.toFixed(2);
    
}

function calcularTMB() {
    const peso = parseFloat(document.getElementById('peso').value);
    const altura = parseFloat(document.getElementById('altura').value) * 100; // altura em cm
    const idade = parseInt(document.getElementById('idade').value);
    const sexo = document.getElementById('sexo').value;

    let tmb = sexo === 'Masculino'
        ? 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
        : 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade);

    // Exibir o resultado da TMB
    document.getElementById('tmb').value = tmb.toFixed(2);
}

window.onload = toggleDobras;