# -*- coding: utf-8 -*-
"""
Gerador de PDF para roteiros de video.
Usa fpdf2 com suporte a UTF-8 e emojis simplificados.
"""

from fpdf import FPDF
from pathlib import Path
from datetime import datetime


class PDFRoteiro(FPDF):
    def __init__(self, titulo_video: str, tipo_nome: str):
        super().__init__()
        self.titulo_video = titulo_video
        self.tipo_nome = tipo_nome
        self.set_auto_page_break(auto=True, margin=20)
        self._setup_fonts()

    def _setup_fonts(self):
        # Fonte padrao que suporta UTF-8 (DejaVu vem embutido no fpdf2)
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)
        self.add_font("DejaVu", "I", "DejaVuSans-Oblique.ttf", uni=True)
        self.add_font("DejaVu", "BI", "DejaVuSans-BoldOblique.ttf", uni=True)

    def header(self):
        if self.page_no() == 1:
            self.set_font("DejaVu", "B", 20)
            self.set_text_color(30, 30, 30)
            self.cell(0, 14, self.titulo_video, ln=True, align="C")
            self.set_font("DejaVu", "I", 11)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, f"Tipo: {self.tipo_nome}", ln=True, align="C")
            self.cell(0, 6, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
            self.ln(6)
            self.set_draw_color(200, 200, 200)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(8)
        else:
            self.set_font("DejaVu", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, f"{self.titulo_video}  |  Pagina {self.page_no()}", ln=True, align="R")
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

    def secao_titulo(self, texto: str, duracao: str = ""):
        self.set_font("DejaVu", "B", 13)
        self.set_text_color(40, 80, 160)
        if duracao:
            self.cell(0, 10, f"{texto}  ({duracao})", ln=True)
        else:
            self.cell(0, 10, texto, ln=True)
        self.set_draw_color(40, 80, 160)
        self.set_line_width(0.4)
        self.line(15, self.get_y(), 60, self.get_y())
        self.ln(4)

    def paragrafo(self, texto: str):
        self.set_font("DejaVu", "", 11)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 7, texto)
        self.ln(3)

    def nota(self, texto: str):
        self.set_font("DejaVu", "I", 10)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 6, f"[Nota de producao] {texto}")
        self.ln(2)

    def dica(self, texto: str):
        self.set_font("DejaVu", "BI", 10)
        self.set_text_color(0, 120, 80)
        self.multi_cell(0, 6, f">>> DICA: {texto}")
        self.ln(2)

    def box_info(self, titulo: str, linhas: list):
        self.set_fill_color(245, 248, 252)
        self.set_draw_color(200, 210, 230)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(50, 50, 50)
        altura = 8 + (len(linhas) * 6)
        self.rect(15, self.get_y(), 180, altura, style="DF")
        self.cell(0, 8, f"  {titulo}", ln=True)
        self.set_font("DejaVu", "", 10)
        for linha in linhas:
            self.cell(0, 6, f"   - {linha}", ln=True)
        self.ln(4)


def gerar_pdf(roteiro: dict, caminho_saida: Path) -> Path:
    """
    Recebe um dicionario de roteiro e gera o PDF.

    Estrutura esperada de `roteiro`:
    {
        "titulo": str,
        "tipo_nome": str,
        "meta": {
            "tema": str,
            "publico": str,
            "tom": str,
            "duracao_estimada": str,
            "plataforma": str,
        },
        "blocos": [
            {"secao": str, "duracao": str, "texto": str, "nota": str (opcional)}
        ],
        "dicas": [str],
    }
    """
    pdf = PDFRoteiro(roteiro["titulo"], roteiro["tipo_nome"])
    pdf.add_page()

    # Caixa de metadados
    meta = roteiro.get("meta", {})
    linhas_meta = []
    if meta.get("tema"):
        linhas_meta.append(f"Tema: {meta['tema']}")
    if meta.get("publico"):
        linhas_meta.append(f"Publico: {meta['publico']}")
    if meta.get("tom"):
        linhas_meta.append(f"Tom de voz: {meta['tom']}")
    if meta.get("plataforma"):
        linhas_meta.append(f"Plataforma: {meta['plataforma']}")
    if meta.get("duracao_estimada"):
        linhas_meta.append(f"Duracao estimada: {meta['duracao_estimada']}")

    if linhas_meta:
        pdf.box_info("INFORMACOES DO PROJETO", linhas_meta)

    # Blocos do roteiro
    for bloco in roteiro.get("blocos", []):
        pdf.secao_titulo(bloco.get("secao", ""), bloco.get("duracao", ""))
        if bloco.get("texto"):
            pdf.paragrafo(bloco["texto"])
        if bloco.get("nota"):
            pdf.nota(bloco["nota"])
        pdf.ln(2)

    # Dicas gerais
    dicas = roteiro.get("dicas", [])
    if dicas:
        pdf.add_page()
        pdf.set_font("DejaVu", "B", 16)
        pdf.set_text_color(40, 80, 160)
        pdf.cell(0, 12, "DICAS DE PRODUCAO", ln=True, align="C")
        pdf.ln(6)
        for dica in dicas:
            pdf.dica(dica)

    # Salvar
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(caminho_saida))
    return caminho_saida
