 document.addEventListener('DOMContentLoaded', function() {
        // Adicionar primeira refeição
        addRefeicao();
        
        // Evento para adicionar refeição
        document.getElementById('btn-add-refeicao').addEventListener('click', addRefeicao);
        
        // Delegar eventos para elementos dinâmicos
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-remove-refeicao')) {
                e.target.closest('.refeicao').remove();
                updatePreview();
            }
            
            if (e.target.classList.contains('btn-add-alimento')) {
                addAlimento(e.target.closest('.refeicao').querySelector('.alimentos-container'), e.target.closest('.refeicao'));
            }
            
            if (e.target.classList.contains('btn-remove-alimento')) {
                e.target.closest('.alimento').remove();
                updatePreview();
            }
        });
        
        // Atualizar informações nutricionais quando alimento é selecionado
        document.addEventListener('change', function(e) {
            if (e.target.classList.contains('alimento-select')) {
                const alimento = e.target.options[e.target.selectedIndex];
                const container = e.target.closest('.alimento');
                
                container.querySelector('.calorias').textContent = alimento.dataset.calorias || '0';
                container.querySelector('.proteinas').textContent = alimento.dataset.proteinas || '0';
                container.querySelector('.carboidratos').textContent = alimento.dataset.carboidratos || '0';
                container.querySelector('.gorduras').textContent = alimento.dataset.gorduras || '0';
                
                updatePreview();
            }
            
            if (e.target.classList.contains('quantidade') || e.target.classList.contains('tipo-refeicao')) {
                updatePreview();
            }
        });

        // Atualiza o valor dos inputs refeicao_id dos alimentos toda vez que uma refeição é alterada
        document.addEventListener('change', function(e){
            if(e.target.classList.contains('tipo-refeicao')){
                updateRefeicaoIds();
            }
        });

        // Inicializa os inputs refeicao_id
        updateRefeicaoIds();
    });
    
    function addRefeicao() {
        const template = document.getElementById('template-refeicao');
        const clone = template.content.cloneNode(true);
        document.getElementById('refeicoes-container').appendChild(clone);
        updatePreview();
        updateRefeicaoIds();
    }
    
    function addAlimento(container, refeicaoElement) {
        const template = document.getElementById('template-alimento');
        const clone = template.content.cloneNode(true);
        container.appendChild(clone);
        updatePreview();
        updateRefeicaoIds();
    }

    function updateRefeicaoIds() {
        // Para cada refeição
        document.querySelectorAll('.refeicao').forEach(refeicao => {
            const tipoRefeicaoSelect = refeicao.querySelector('.tipo-refeicao');
            const refeicaoIdValue = tipoRefeicaoSelect.value;

            // Atualiza todos inputs ocultos refeicao_id dentro dos alimentos desta refeição
            refeicao.querySelectorAll('.alimento').forEach(alimentoDiv => {
                const refeicaoIdInput = alimentoDiv.querySelector('.refeicao-id-input');
                refeicaoIdInput.value = refeicaoIdValue;
            });
        });
    }
    
    function updatePreview() {
        const previewContainer = document.getElementById('preview-container');
        previewContainer.innerHTML = '<h3>Resumo da Dieta</h3>';
        
        const pacienteNome = document.getElementById('paciente')?.dataset.nome || 'Paciente não selecionado';
        
        previewContainer.innerHTML += `
            <p><strong>Paciente:</strong> ${pacienteNome}</p>
        `;
        
        let totalCalorias = 0;
        let totalProteinas = 0;
        let totalCarboidratos = 0;
        let totalGorduras = 0;
        
        document.querySelectorAll('.refeicao').forEach(refeicao => {
            const tipoRefeicao = refeicao.querySelector('.tipo-refeicao').value;
            const tipoRefeicaoNome = refeicao.querySelector('.tipo-refeicao option:checked')?.text || 'Refeição';
            
            let refeicaoHTML = `<div class="preview-refeicao"><h4>${tipoRefeicaoNome}</h4><ul>`;
            let refeicaoCalorias = 0;
            let refeicaoProteinas = 0;
            let refeicaoCarboidratos = 0;
            let refeicaoGorduras = 0;
            
            refeicao.querySelectorAll('.alimento').forEach(alimento => {
                const alimentoSelect = alimento.querySelector('.alimento-select');
                const alimentoNome = alimentoSelect.options[alimentoSelect.selectedIndex]?.text || 'Alimento não selecionado';
                const quantidade = alimento.querySelector('.quantidade').value || 0;
                const calorias = parseFloat(alimentoSelect.options[alimentoSelect.selectedIndex]?.dataset.calorias || 0);
                const proteinas = parseFloat(alimentoSelect.options[alimentoSelect.selectedIndex]?.dataset.proteinas || 0);
                const carboidratos = parseFloat(alimentoSelect.options[alimentoSelect.selectedIndex]?.dataset.carboidratos || 0);
                const gorduras = parseFloat(alimentoSelect.options[alimentoSelect.selectedIndex]?.dataset.gorduras || 0);
                
                const calTotal = (calorias * quantidade / 100).toFixed(2);
                const protTotal = (proteinas * quantidade / 100).toFixed(2);
                const carbTotal = (carboidratos * quantidade / 100).toFixed(2);
                const gordTotal = (gorduras * quantidade / 100).toFixed(2);
                
                refeicaoHTML += `
                    <li>
                        ${alimentoNome} - ${quantidade}g
                        (Cal: ${calTotal}kcal, P: ${protTotal}g, C: ${carbTotal}g, G: ${gordTotal}g)
                    </li>
                `;
                
                refeicaoCalorias += parseFloat(calTotal);
                refeicaoProteinas += parseFloat(protTotal);
                refeicaoCarboidratos += parseFloat(carbTotal);
                refeicaoGorduras += parseFloat(gordTotal);
            });
            
            refeicaoHTML += `</ul><p><strong>Total:</strong> ${refeicaoCalorias.toFixed(2)}kcal, P: ${refeicaoProteinas.toFixed(2)}g, C: ${refeicaoCarboidratos.toFixed(2)}g, G: ${refeicaoGorduras.toFixed(2)}g</p></div>`;
            previewContainer.innerHTML += refeicaoHTML;
            
            totalCalorias += refeicaoCalorias;
            totalProteinas += refeicaoProteinas;
            totalCarboidratos += refeicaoCarboidratos;
            totalGorduras += refeicaoGorduras;
        });
        
        previewContainer.innerHTML += `
            <div class="preview-total">
                <h4>Total Diário</h4>
                <p>Calorias: ${totalCalorias.toFixed(2)}kcal</p>
                <p>Proteínas: ${totalProteinas.toFixed(2)}g</p>
                <p>Carboidratos: ${totalCarboidratos.toFixed(2)}g</p>
                <p>Gorduras: ${totalGorduras.toFixed(2)}g</p>
            </div>
        `;
        
    }