# -*- coding: utf-8 -*-
"""
Gerador de PDF para orcamentos de producao de video.
"""

from fpdf import FPDF
from pathlib import Path
from datetime import datetime, timedelta


class PDFOrcamento(FPDF):
    def __init__(self, dados: dict):
        super().__init__()
        self.dados = dados
        self.set_auto_page_break(auto=True, margin=20)
        self._setup_fonts()

    def _setup_fonts(self):
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)
        self.add_font("DejaVu", "I", "DejaVuSans-Oblique.ttf", uni=True)
        self.add_font("DejaVu", "BI", "DejaVuSans-BoldOblique.ttf", uni=True)

    def header(self):
        if self.page_no() == 1:
            self.set_font("DejaVu", "B", 24)
            self.set_text_color(102, 126, 234)
            self.cell(0, 14, "ORCAMENTO", ln=True, align="C")
            self.set_font("DejaVu", "I", 10)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, f"N {self.dados['numero']}  |  {self.dados['data_emissao']}", ln=True, align="C")
            self.ln(4)
            self.set_draw_color(102, 126, 234)
            self.set_line_width(0.5)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

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
            self.cell(0, 6, f"   {linha}", ln=True)
        self.ln(4)

    def secao_titulo(self, texto: str):
        self.set_font("DejaVu", "B", 13)
        self.set_text_color(40, 80, 160)
        self.cell(0, 10, texto, ln=True)
        self.set_draw_color(40, 80, 160)
        self.set_line_width(0.4)
        self.line(15, self.get_y(), 60, self.get_y())
        self.ln(4)

    def tabela_itens(self, itens: list):
        # Cabecalho
        self.set_fill_color(102, 126, 234)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 10)
        self.cell(80, 10, "  ITEM", border=0, fill=True)
        self.cell(25, 10, "  QTD", border=0, align="C", fill=True)
        self.cell(35, 10, "  UNIT", border=0, align="R", fill=True)
        self.cell(40, 10, "  TOTAL", border=0, align="R", fill=True)
        self.ln()

        # Linhas
        self.set_text_color(30, 30, 30)
        self.set_font("DejaVu", "", 10)
        fill = False
        total_geral = 0.0
        for item in itens:
            if fill:
                self.set_fill_color(248, 249, 252)
            else:
                self.set_fill_color(255, 255, 255)

            desc = item.get("descricao", "")
            qtd = item.get("quantidade", 1)
            unit = float(item.get("unitario", 0))
            total = qtd * unit
            total_geral += total

            # Quebra de linha automatica para descricao longa
            altura_linha = 8
            self.cell(80, altura_linha, f"  {desc}", border=0, fill=True)
            self.cell(25, altura_linha, f"  {qtd}", border=0, align="C", fill=True)
            self.cell(35, altura_linha, f"  R$ {unit:,.2f}", border=0, align="R", fill=True)
            self.cell(40, altura_linha, f"  R$ {total:,.2f}", border=0, align="R", fill=True)
            self.ln()
            fill = not fill

        # Total
        self.ln(2)
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(40, 80, 160)
        self.cell(140, 10, "TOTAL DO ORCAMENTO", align="R")
        self.cell(40, 10, f"R$ {total_geral:,.2f}", align="R")
        self.ln(10)

        return total_geral


def gerar_pdf_orcamento(dados: dict, caminho_saida: Path) -> Path:
    pdf = PDFOrcamento(dados)
    pdf.add_page()

    # Dados do prestador e cliente
    prestador = dados.get("prestador", {})
    cliente = dados.get("cliente", {})

    pdf.set_font("DejaVu", "B", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(90, 8, "DE:")
    pdf.cell(0, 8, "PARA:", ln=True)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(80, 80, 80)

    de_linhas = [
        prestador.get("nome", ""),
        prestador.get("email", ""),
        prestador.get("telefone", ""),
        prestador.get("cnpj", ""),
    ]
    para_linhas = [
        cliente.get("nome", ""),
        cliente.get("email", ""),
        cliente.get("telefone", ""),
        cliente.get("empresa", ""),
    ]

    for i in range(max(len(de_linhas), len(para_linhas))):
        de = de_linhas[i] if i < len(de_linhas) else ""
        para = para_linhas[i] if i < len(para_linhas) else ""
        pdf.cell(90, 6, de)
        pdf.cell(0, 6, para, ln=True)
    pdf.ln(6)

    # Descricao do projeto
    if dados.get("projeto_descricao"):
        pdf.secao_titulo("DESCRICAO DO PROJETO")
        pdf.set_font("DejaVu", "", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 6, dados["projeto_descricao"])
        pdf.ln(4)

    # Tabela de itens
    pdf.secao_titulo("ITENS E SERVICOS")
    total = pdf.tabela_itens(dados.get("itens", []))

    # Prazo e entrega
    pdf.secao_titulo("PRAZO E ENTREGA")
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, f"Prazo de execucao: {dados.get('prazo', 'A combinar')}\n"
                          f"Formato de entrega: {dados.get('formato_entrega', 'Arquivo digital em alta resolucao')}")
    pdf.ln(4)

    # Condicoes de pagamento
    pdf.secao_titulo("CONDICOES DE PAGAMENTO")
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, dados.get("condicoes_pagamento", "50% na aprovacao do orcamento, 50% na entrega final."))
    pdf.ln(4)

    # Validade
    pdf.set_font("DejaVu", "BI", 10)
    pdf.set_text_color(180, 60, 60)
    pdf.cell(0, 8, f"Validade do orcamento: {dados.get('validade', '15 dias')}", ln=True)
    pdf.ln(6)

    # Assinaturas (nova pagina se necessario)
    if pdf.get_y() > 240:
        pdf.add_page()

    pdf.set_draw_color(100, 100, 100)
    pdf.line(30, pdf.get_y() + 20, 90, pdf.get_y() + 20)
    pdf.line(120, pdf.get_y() + 20, 180, pdf.get_y() + 20)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(90, 8, "Assinatura do Prestador", align="C")
    pdf.cell(0, 8, "Assinatura do Cliente", align="C", ln=True)

    # Salvar
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(caminho_saida))
    return caminho_saida
