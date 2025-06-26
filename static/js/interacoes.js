// Botões de ação com feedback
document.querySelectorAll('.acao-btn').forEach(btn => {
    const original = btn.dataset.originalText;
    btn.addEventListener('click', () => {
      btn.classList.add('btn-success');
      btn.innerText = 'Em breve!';
      setTimeout(() => {
        btn.classList.remove('btn-success');
        btn.innerText = original;
      }, 1500);
    });
  });
  
  // Botão Experimente
  document.getElementById('btn-experimente').addEventListener('click', () => {
    alert('Redirecionando para cadastro!');
  });
  
  // Benefício: animação de escala
  document.querySelectorAll('.beneficio-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'scale(1.05)';
      card.style.transition = 'transform 0.3s ease';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'scale(1)';
    });
  });
  