# -*- coding: utf-8 -*-
"""
Interface web para o Roteirista AI.
Acesse: http://127.0.0.1:5000
"""

import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, render_template, request, send_file, jsonify
from threading import Thread
import time

from templates import obter_template, TIPOS_ROTEIRO
from pdf_generator import gerar_pdf
from pdf_orcamento import gerar_pdf_orcamento
from ia_client import IAClient

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

# Estado global para acompanhar geracoes
JOBS = {}


def gerar_roteiro_job(job_id: str, dados: dict):
    """Executa geracao em background."""
    try:
        JOBS[job_id]["status"] = "gerando"
        JOBS[job_id]["log"].append("Iniciando criacao do roteiro...")

        tipo_id = dados["tipo_id"]
        info = obter_template(tipo_id)
        meta = {
            "tema": dados["tema"],
            "publico": dados["publico"],
            "tom": dados["tom"],
            "plataforma": dados["plataforma"],
            "duracao_estimada": dados["duracao"],
        }

        # IA
        api_key = dados.get("api_key", "").strip()
        usar_ia = dados.get("usar_ia") == "on" and api_key
        ia = IAClient(api_key=api_key) if usar_ia else IAClient(api_key="")

        JOBS[job_id]["log"].append(f"Modo: {'IA' if usar_ia else 'Manual'}")
        JOBS[job_id]["log"].append(f"Template: {info['nome']}")

        blocos = []
        for secao, instrucao in info["estrutura"]:
            nome_secao = secao.split("(")[0].strip()
            duracao = secao[secao.find("(")+1:secao.find(")")] if "(" in secao else ""

            if usar_ia:
                JOBS[job_id]["log"].append(f"Gerando secao: {nome_secao}...")
                texto = ia.gerar_bloco(
                    tema=meta["tema"],
                    publico=meta["publico"],
                    tom=meta["tom"],
                    secao=nome_secao,
                    instrucao=instrucao,
                )
                if not texto:
                    texto = f"[Inserir conteudo para: {nome_secao}]"
            else:
                texto = f"[Inserir conteudo para: {nome_secao} - {instrucao}]"

            blocos.append({
                "secao": nome_secao,
                "duracao": duracao,
                "texto": texto,
                "nota": instrucao,
            })
            time.sleep(0.1)

        roteiro = {
            "titulo": dados["titulo"],
            "tipo_nome": info["nome"],
            "meta": meta,
            "blocos": blocos,
            "dicas": info.get("dicas", []),
        }

        slug = "".join(c if c.isalnum() else "_" for c in dados["titulo"]).lower()[:40]
        nome_arquivo = f"roteiro_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pasta_saida = Path("roteiros_gerados")
        caminho_pdf = pasta_saida / nome_arquivo

        JOBS[job_id]["log"].append("Gerando PDF...")
        gerar_pdf(roteiro, caminho_pdf)

        JOBS[job_id]["status"] = "pronto"
        JOBS[job_id]["arquivo"] = str(caminho_pdf)
        JOBS[job_id]["nome_arquivo"] = nome_arquivo
        JOBS[job_id]["log"].append("PDF gerado com sucesso!")

    except Exception as e:
        JOBS[job_id]["status"] = "erro"
        JOBS[job_id]["log"].append(f"Erro: {str(e)}")


@app.route("/")
def index():
    return render_template("index.html", tipos=TIPOS_ROTEIRO)


@app.route("/gerar", methods=["POST"])
def gerar():
    job_id = f"job_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(4).hex()}"

    dados = {
        "tipo_id": request.form.get("tipo", "1"),
        "titulo": request.form.get("titulo", "Roteiro sem titulo"),
        "tema": request.form.get("tema", ""),
        "publico": request.form.get("publico", "geral"),
        "tom": request.form.get("tom", "conversacional"),
        "plataforma": request.form.get("plataforma", "YouTube"),
        "duracao": request.form.get("duracao", "3-5 minutos"),
        "usar_ia": request.form.get("usar_ia"),
        "api_key": request.form.get("api_key", ""),
    }

    JOBS[job_id] = {
        "status": "iniciando",
        "log": [],
        "arquivo": None,
        "nome_arquivo": None,
    }

    thread = Thread(target=gerar_roteiro_job, args=(job_id, dados))
    thread.daemon = True
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    job = JOBS.get(job_id, {"status": "desconhecido", "log": []})
    return jsonify(job)


@app.route("/download/<job_id>")
def download(job_id):
    job = JOBS.get(job_id)
    if not job or not job.get("arquivo"):
        return "Arquivo nao encontrado", 404
    return send_file(job["arquivo"], as_attachment=True, download_name=job["nome_arquivo"])


@app.route("/orcamento")
def pagina_orcamento():
    return render_template("orcamento.html")


@app.route("/gerar_orcamento", methods=["POST"])
def gerar_orcamento():
    try:
        numero = f"ORC-{datetime.now().strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"

        itens = []
        descricoes = request.form.getlist("item_desc[]")
        qtds = request.form.getlist("item_qtd[]")
        units = request.form.getlist("item_unit[]")
        for i in range(len(descricoes)):
            try:
                q = int(qtds[i]) if i < len(qtds) else 1
                u = float(units[i].replace(",", ".")) if i < len(units) else 0
            except ValueError:
                q, u = 1, 0
            itens.append({
                "descricao": descricoes[i],
                "quantidade": q,
                "unitario": u,
            })

        dados = {
            "numero": numero,
            "data_emissao": datetime.now().strftime("%d/%m/%Y"),
            "prestador": {
                "nome": request.form.get("prestador_nome", ""),
                "email": request.form.get("prestador_email", ""),
                "telefone": request.form.get("prestador_telefone", ""),
                "cnpj": request.form.get("prestador_cnpj", ""),
            },
            "cliente": {
                "nome": request.form.get("cliente_nome", ""),
                "email": request.form.get("cliente_email", ""),
                "telefone": request.form.get("cliente_telefone", ""),
                "empresa": request.form.get("cliente_empresa", ""),
            },
            "projeto_descricao": request.form.get("projeto_descricao", ""),
            "itens": itens,
            "prazo": request.form.get("prazo", "A combinar"),
            "formato_entrega": request.form.get("formato_entrega", "Arquivo digital"),
            "condicoes_pagamento": request.form.get("condicoes_pagamento", ""),
            "validade": request.form.get("validade", "15 dias"),
        }

        slug = "".join(c if c.isalnum() else "_" for c in request.form.get("projeto_titulo", "orcamento")).lower()[:30]
        nome_arquivo = f"orcamento_{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pasta_saida = Path("orcamentos_gerados")
        caminho_pdf = pasta_saida / nome_arquivo

        gerar_pdf_orcamento(dados, caminho_pdf)

        return jsonify({
            "ok": True,
            "download_url": f"/download_orcamento/{nome_arquivo}",
            "nome": nome_arquivo,
        })
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)})


@app.route("/download_orcamento/<nome>")
def download_orcamento(nome):
    caminho = Path("orcamentos_gerados") / nome
    if not caminho.exists():
        return "Arquivo nao encontrado", 404
    return send_file(str(caminho), as_attachment=True, download_name=nome)


if __name__ == "__main__":
    print("=" * 50)
    print("ROTEIRISTA AI - Interface Web")
    print("Acesse: http://127.0.0.1:5001")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5001, debug=False)
