document.getElementById('btn-gerar-pdf').addEventListener('click', () => {
  const { jsPDF } = window.jspdf;

  // Captura a área que você quer no PDF - aqui capturando o body todo
  html2canvas(document.getElementById('conteudo-dieta'), { scale: 2 }).then(canvas => {
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    
    // Tamanho da página A4 em mm
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();

    // Ajustar altura para manter proporção
    const imgProps = pdf.getImageProperties(imgData);
    const imgHeight = (imgProps.height * pdfWidth) / imgProps.width;

    // Se a imagem for maior que a página, vai quebrar em múltiplas páginas
    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
    heightLeft -= pdfHeight;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, imgHeight);
      heightLeft -= pdfHeight;
    }

    pdf.save('dieta.pdf');
  });
});