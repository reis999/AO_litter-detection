from fpdf import FPDF
from datetime import datetime

def gerar_relatorio_pdf(caminho_imagem, deteccoes_info, caminho_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatório de Reciclagem por Detecção de Lixo", ln=True)

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Imagem analisada: {caminho_imagem}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Resumo das Detecções:", ln=True)

    pdf.set_font("Arial", '', 12)
    for classe, info in deteccoes_info.items():
        pdf.multi_cell(0, 10, f"- {classe} (x{info['quantidade']}):\n"
                              f"  -> Ecoponto: {info['ecoponto']}\n"
                              f"  -> Como reciclar: {info['dica'] or 'Sem dica disponível'}\n")

    # Inserir imagem anotada
    try:
        pdf.image(caminho_imagem, w=pdf.w - 30)
    except RuntimeError as e:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, f"[Erro ao inserir imagem: {e}]", ln=True)
    pdf.output(caminho_pdf)
