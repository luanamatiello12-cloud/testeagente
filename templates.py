# -*- coding: utf-8 -*-
"""
Templates e estruturas de roteiro por tipo de video.
"""

TIPOS_ROTEIRO = {
    "1": {
        "nome": "Tutorial / Educativo",
        "descricao": "Ensina algo passo a passo",
        "estrutura": [
            ("HOOK (0-15s)", "Chamada inicial que prende atencao. Mostre o resultado final ou a dor do espectador."),
            ("APRESENTACAO (15-30s)", "Quem voce e e o que vai ensinar hoje. Defina a promessa do video."),
            ("MATERIAL / PRE-REQUISITOS (30-60s)", "O que o espectador precisa ter ou saber antes de comecar."),
            ("PASSO 1 (60-120s)", "Primeira acao concreta. Mostre em tela, explique devagar."),
            ("PASSO 2 (120-180s)", "Segunda acao. Continue o fluxo logico."),
            ("PASSO 3 (180-240s)", "Terceira acao ou ajustes finais."),
            ("RESULTADO (240-270s)", "Mostre o antes e depois. Prove que funciona."),
            ("CTA / ENCERRAMENTO (270-300s)", "Chamada para acao: curta, comente, siga, acesse link, etc."),
        ],
        "dicas": [
            "Use zoom na tela ou close nas maos durante acoes importantes",
            "Cortes rapidos entre passos mantem o ritmo",
            "Legendas aumentam retencao em 40%",
        ],
    },
    "2": {
        "nome": "Vlog / Dia a Dia",
        "descricao": "Acompanhe um dia ou momento da vida real",
        "estrutura": [
            ("HOOK VISUAL (0-10s)", "Imagem chamativa: paisagem, reacao, ou pergunta na tela."),
            ("INTRO / BOM DIA (10-30s)", "Apresente o dia, o lugar ou o plano. Seja autentico."),
            ("MOMENTO 1 (30-90s)", "Primeira atividade. Mostre detalhes sensoriais (sons, cheiros, texturas)."),
            ("TRANSICAO (90-100s)", "Corte criativo: time-lapse, musica, ou mudanca de cenario."),
            ("MOMENTO 2 (100-180s)", "Segunda atividade. Crie conflito leve ou surpresa."),
            ("REFLEXAO / APRENDIZADO (180-220s)", "O que voce aprendeu ou sentiu. Conecte com o publico."),
            ("ENCERRAMENTO / DESPEDIDA (220-250s)", "Agradecimento e preview do proximo conteudo."),
        ],
        "dicas": [
            "Grave em 60fps para transicoes suaves em slow motion",
            "Audio ambiente real aumenta a imersao",
            "Fale com a camera como se fosse um amigo proximo",
        ],
    },
    "3": {
        "nome": "Review / Unboxing",
        "descricao": "Analise ou apresentacao de produto",
        "estrutura": [
            ("HOOK (0-15s)", "Pergunta polemica ou promessa: 'Sera que vale a pena?' / 'O que veio me surpreendeu...'"),
            ("APRESENTACAO DO PRODUTO (15-40s)", "Mostre a caixa, a marca, o preço. Contextualize."),
            ("UNBOXING / PRIMEIRAS IMPRESSOES (40-90s)", "Abra devagar. Mostre cada item. Reacao genuina."),
            ("ESPECIFICACOES (90-120s)", "Dados tecnicos: peso, dimensoes, compatibilidade. Use texto na tela."),
            ("TESTE PRATICO (120-200s)", "Use o produto. Mostre funcoes na pratica."),
            ("PROS E CONTRAS (200-240s)", "Seja honesto. 3 pontos positivos e 2 negativos."),
            ("VEREDICTO (240-270s)", "Para quem e indicado? Vale o preço?"),
            ("CTA (270-300s)", "Link na descricao, cupom, ou pergunte a opiniao."),
        ],
        "dicas": [
            "Iluminacao difusa evita reflexos no produto",
            "Use macro para detalhes de textura e acabamento",
            "Comparacao lado a lado com concorrente gera engajamento",
        ],
    },
    "4": {
        "nome": "Storytelling / Narrativa",
        "descricao": "Conta uma historia com comeco, meio e fim",
        "estrutura": [
            ("GANCHO (0-20s)", "Inicie no meio da acao ou com uma pergunta intrigante."),
            ("CENARIO (20-50s)", "Apresente personagens, lugar e momento. Crie identificacao."),
            ("CONFLITO (50-120s)", "O problema aparece. Eleve a tensao gradualmente."),
            ("CLIMAX (120-180s)", "O momento mais intenso. A virada, a descoberta, a superacao."),
            ("RESOLUCAO (180-220s)", "Como tudo se resolve. A licao aprendida."),
            ("MORAL / MENSAGEM (220-260s)", "Conecte a historia com a vida do espectador."),
            ("ENCERRAMENTO (260-300s)", "Feche o ciclo. CTA sutil ou reflexao final."),
        ],
        "dicas": [
            "Regra dos 3 atos: setup -> confronto -> resolucao",
            "Use B-roll para cobrir cortes no audio principal",
            "Musica de fundo deve subir e descer com a tensao",
        ],
    },
    "5": {
        "nome": "Venda / Pitch",
        "descricao": "Venda um produto, servico ou ideia",
        "estrutura": [
            ("PROBLEMA (0-20s)", "Agite a dor. O espectador precisa se sentir representado."),
            ("AMPLIFICACAO (20-45s)", "Mostre as consequencias de NAO resolver. Crie urgencia."),
            ("SOLUCAO (45-75s)", "Apresente sua oferta como a resposta natural."),
            ("PROVA SOCIAL (75-110s)", "Depoimentos, numeros, cases. Terceiros validam."),
            ("OFERTA (110-140s)", "O que inclui, quanto custa, garantia. Seja transparente."),
            ("ESCASSEZ / BONUS (140-170s)", "Prazo, vagas limitadas, ou bonus por tempo."),
            ("GARANTIA (170-200s)", "Remova o risco. Dinheiro de volta, teste gratis."),
            ("CTA FORTE (200-240s)", "Instrucao clara: 'Clique no link', 'Comente EU QUERO', etc."),
        ],
        "dicas": [
            "Fale da dor 60% do tempo, da solucao 40%",
            "Use contagem regressiva na tela para urgencia",
            "Repetir o CTA 3x aumenta conversao significativamente",
        ],
    },
}


def listar_tipos():
    print("\n" + "=" * 50)
    print("TIPOS DE ROTEIRO DISPONIVEIS")
    print("=" * 50)
    for chave, info in TIPOS_ROTEIRO.items():
        print(f"  [{chave}] {info['nome']} - {info['descricao']}")
    print("=" * 50)


def obter_template(tipo_id: str):
    return TIPOS_ROTEIRO.get(tipo_id)
