# -*- coding: utf-8 -*-
"""
Cliente para geracao de conteudo com IA.
Suporta OpenAI, Groq, ou qualquer API compativel.
Modo fallback usa templates preenchidos manualmente.
"""

import os
import re

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class IAClient:
    """
    Cliente simples para APIs de chat completion.
    """

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.ativo = bool(self.api_key and HAS_REQUESTS)

    def gerar_conteudo_bloco(self, prompt: str, temperatura: float = 0.8, max_tokens: int = 800) -> str:
        if not self.ativo:
            return ""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Voce e um roteirista profissional de videos para internet. Escreve roteiros envolventes, diretos e otimizados para alta retencao de audiencia. Responda apenas com o texto do roteiro, sem explicacoes adicionais."},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperatura,
            "max_tokens": max_tokens,
        }

        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            texto = data["choices"][0]["message"]["content"]
            return texto.strip()
        except Exception as e:
            print(f"[[AVISO]] Falha na API de IA: {e}")
            return ""

    def gerar_hook(self, tema: str, publico: str, tom: str) -> str:
        prompt = (
            f"Crie um HOOK de ate 3 frases para um video sobre '{tema}'. "
            f"Publico-alvo: {publico}. Tom de voz: {tom}. "
            f"O hook deve prender atencao imediatamente, gerar curiosidade ou identificacao. "
            f"Use linguagem natural de internet (nao muito formal)."
        )
        return self.gerar_conteudo_bloco(prompt, temperatura=0.9, max_tokens=200)

    def gerar_bloco(self, tema: str, publico: str, tom: str, secao: str, instrucao: str) -> str:
        prompt = (
            f"Escreva a secao '{secao}' de um roteiro de video sobre '{tema}'. "
            f"Publico: {publico}. Tom: {tom}.\n\n"
            f"Instrucao para esta secao: {instrucao}\n\n"
            f"Escreva como se fosse o proprio apresentador falando. "
            f"Inclua sugestoes de imagem/tela entre colchetes [assim]. "
            f"Mantenha paragrafos curtos e diretos."
        )
        return self.gerar_conteudo_bloco(prompt, temperatura=0.8, max_tokens=400)


def detectar_links(texto: str) -> list:
    """Extrai URLs do texto para formatar como links no PDF."""
    padrao = re.compile(r'https?://[^\s\)\]]+')
    return padrao.findall(texto)
