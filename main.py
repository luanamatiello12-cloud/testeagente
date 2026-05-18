# -*- coding: utf-8 -*-
"""
Roteirista AI - Agente de criacao de roteiros para videos em PDF.

Modos de uso:
  1. Com API de IA (OpenAI, Groq, etc.) -> roteiro gerado automaticamente
  2. Sem API -> preenche templates manualmente com guia inteligente

Configurar API:
  export OPENAI_API_KEY="sk-..."
  export OPENAI_BASE_URL="https://api.openai.com/v1"  # ou Groq, etc.
  export OPENAI_MODEL="gpt-4o-mini"
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Adiciona diretorio do script ao path
sys.path.insert(0, str(Path(__file__).parent))

from templates import listar_tipos, obter_template, TIPOS_ROTEIRO
from pdf_generator import gerar_pdf
from ia_client import IAClient


def input_texto(label: str, padrao: str = "") -> str:
    if padrao:
        val = input(f"{label} [{padrao}]: ").strip()
        return val if val else padrao
    return input(f"{label}: ").strip()


def input_numero(label: str, opcoes_validas: list) -> str:
    while True:
        val = input(f"{label}: ").strip()
        if val in opcoes_validas:
            return val
        print(f"  Opcao invalida. Escolha uma de: {', '.join(opcoes_validas)}")


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    print("=" * 58)
    print("   ROTEIRISTA AI - Criador de Roteiros para Videos")
    print("   Gere roteiros profissionais e exporte em PDF")
    print("=" * 58)


def escolher_tipo() -> tuple:
    listar_tipos()
    print()
    tipo_id = input_numero("Escolha o numero do tipo", list(TIPOS_ROTEIRO.keys()))
    info = obter_template(tipo_id)
    print(f"\n[TIPO SELECIONADO] {info['nome']}")
    print(f"Descricao: {info['descricao']}\n")
    return tipo_id, info


def coletar_meta() -> dict:
    print("--- INFORMACOES DO VIDEO ---")
    tema = input_texto("Tema/Assunto do video")
    publico = input_texto("Publico-alvo (ex: jovens 18-25, empresarios)")
    tom = input_texto("Tom de voz", "conversacional")
    plataforma = input_texto("Plataforma principal", "YouTube")
    duracao = input_texto("Duracao estimada", "3-5 minutos")
    return {
        "tema": tema,
        "publico": publico,
        "tom": tom,
        "plataforma": plataforma,
        "duracao_estimada": duracao,
    }


def perguntar_uso_ia() -> IAClient:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    if api_key:
        print(f"\n[[IA]] API Key detectada ({api_key[:8]}...)")
        usar = input("Usar IA para gerar conteudo automatico? (s/n): ").strip().lower()
        if usar.startswith("s"):
            return IAClient()
    print("\n[[INFO]] Modo MANUAL ativado. Voce preenchera cada bloco do roteiro.")
    print("         (Para usar IA, configure OPENAI_API_KEY ou GROQ_API_KEY)\n")
    return IAClient(api_key="")


def coletar_blocos_manual(template_info: dict) -> list:
    blocos = []
    print("\n--- PREENCHIMENTO DO ROTEIRO ---")
    print("Digite o texto para cada secao. Pressione ENTER 2x para pular.\n")
    for secao, instrucao in template_info["estrutura"]:
        print(f">>> {secao}")
        print(f"    Guia: {instrucao}")
        linhas = []
        while True:
            try:
                linha = input("    > ")
            except EOFError:
                break
            if linha == "":
                if len(linhas) > 0 and linhas[-1] == "":
                    linhas.pop()
                    break
            linhas.append(linha)
        texto = "\n".join(linhas).strip()
        if not texto:
            texto = f"[Inserir conteudo para: {secao}]"
        blocos.append({
            "secao": secao.split("(")[0].strip(),
            "duracao": secao[secao.find("(")+1:secao.find(")")] if "(" in secao else "",
            "texto": texto,
            "nota": instrucao,
        })
        print()
    return blocos


def coletar_blocos_com_ia(ia: IAClient, template_info: dict, meta: dict) -> list:
    blocos = []
    print("\n[[IA]] Gerando conteudo com inteligencia artificial...\n")
    for secao, instrucao in template_info["estrutura"]:
        print(f"  Gerando: {secao} ...", end=" ")
        texto = ia.gerar_bloco(
            tema=meta["tema"],
            publico=meta["publico"],
            tom=meta["tom"],
            secao=secao.split("(")[0].strip(),
            instrucao=instrucao,
        )
        if texto:
            print("OK")
        else:
            print("FALHA (usando placeholder)")
            texto = f"[Inserir conteudo para: {secao}]"
        blocos.append({
            "secao": secao.split("(")[0].strip(),
            "duracao": secao[secao.find("(")+1:secao.find(")")] if "(" in secao else "",
            "texto": texto,
            "nota": instrucao,
        })
    return blocos


def confirmar_geracao(roteiro: dict) -> bool:
    print("\n" + "=" * 58)
    print("PREVISUALIZACAO DO ROTEIRO")
    print("=" * 58)
    print(f"Titulo: {roteiro['titulo']}")
    print(f"Tipo: {roteiro['tipo_nome']}")
    print(f"Blocos: {len(roteiro['blocos'])}")
    for b in roteiro['blocos'][:3]:
        preview = b['texto'][:60].replace("\n", " ")
        print(f"  - {b['secao']}: {preview}...")
    if len(roteiro['blocos']) > 3:
        print(f"  ... e mais {len(roteiro['blocos'])-3} blocos")
    print("=" * 58)
    ok = input("\nGerar PDF? (s/n): ").strip().lower()
    return ok.startswith("s")


def main():
    limpar_tela()
    banner()
    print()

    # Escolher tipo
    tipo_id, info = escolher_tipo()

    # Coletar metadados
    meta = coletar_meta()

    # Titulo do roteiro
    titulo = input_texto("Titulo do video", f"{meta['tema']} - Roteiro")

    # IA ou manual
    ia = perguntar_uso_ia()
    usar_ia = ia.ativo

    # Coletar blocos
    if usar_ia:
        blocos = coletar_blocos_com_ia(ia, info, meta)
    else:
        blocos = coletar_blocos_manual(info)

    # Montar roteiro
    roteiro = {
        "titulo": titulo,
        "tipo_nome": info["nome"],
        "meta": meta,
        "blocos": blocos,
        "dicas": info.get("dicas", []),
    }

    # Confirmar
    if not confirmar_geracao(roteiro):
        print("\nCancelado. Nenhum PDF foi gerado.")
        return

    # Gerar PDF
    slug = "".join(c if c.isalnum() else "_" for c in titulo).lower()[:40]
    nome_arquivo = f"roteiro_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pasta_saida = Path("roteiros_gerados")
    caminho_pdf = pasta_saida / nome_arquivo

    try:
        gerar_pdf(roteiro, caminho_pdf)
        print(f"\n[[SUCESSO]] PDF gerado!")
        print(f"Caminho: {caminho_pdf.resolve()}")
        print(f"\nDica: Abra o arquivo para revisar e ajustar antes de gravar.")
    except Exception as e:
        print(f"\n[[ERRO]] Falha ao gerar PDF: {e}")
        print("Verifique se fpdf2 esta instalado: pip install fpdf2")


def modo_rapido(tema: str, tipo_id: str = "1"):
    """
    Modo rapido via linha de comando:
        python main.py rapido "Como fazer bolo de caneca" 1
    """
    info = obter_template(tipo_id)
    if not info:
        print(f"Tipo invalido: {tipo_id}")
        sys.exit(1)

    ia = IAClient()
    meta = {
        "tema": tema,
        "publico": "geral",
        "tom": "conversacional",
        "plataforma": "YouTube",
        "duracao_estimada": "3-5 minutos",
    }

    if ia.ativo:
        print(f"[[IA]] Gerando roteiro rapido para: {tema}")
        blocos = coletar_blocos_com_ia(ia, info, meta)
    else:
        print("[[INFO]] Modo rapido sem IA. Use templates pre-definidos.")
        blocos = []
        for secao, instrucao in info["estrutura"]:
            blocos.append({
                "secao": secao.split("(")[0].strip(),
                "duracao": secao[secao.find("(")+1:secao.find(")")] if "(" in secao else "",
                "texto": f"[Inserir conteudo sobre {tema} - {instrucao}]",
                "nota": instrucao,
            })

    roteiro = {
        "titulo": tema,
        "tipo_nome": info["nome"],
        "meta": meta,
        "blocos": blocos,
        "dicas": info.get("dicas", []),
    }

    slug = "".join(c if c.isalnum() else "_" for c in tema).lower()[:40]
    nome_arquivo = f"roteiro_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pasta_saida = Path("roteiros_gerados")
    caminho_pdf = pasta_saida / nome_arquivo
    gerar_pdf(roteiro, caminho_pdf)
    print(f"[[SUCESSO]] PDF gerado: {caminho_pdf.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "rapido":
        modo_rapido(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "1")
    else:
        main()
