# Roteirista AI

Agente de criacao de roteiros para videos com exportacao em PDF.

## Recursos

- 5 templates profissionais (Tutorial, Vlog, Review, Storytelling, Venda)
- Geracao com IA (OpenAI, Groq, ou qualquer API compativel)
- Modo manual com guia inteligente (funciona 100% offline)
- PDF formatado com indice, duracao, dicas de producao
- Suporte a UTF-8 (acentos, cedilha, etc.)

## Instalacao

```bash
cd roteirista_ai

# Criar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Modo interativo (recomendado)

```bash
python main.py
```

Siga as perguntas:
1. Escolha o tipo de roteiro
2. Informe tema, publico, tom de voz
3. Escolha usar IA ou preencher manualmente
4. Receba o PDF pronto!

### Modo rapido (via linha de comando)

```bash
# Com IA (precisa de OPENAI_API_KEY)
python main.py rapido "Como fazer bolo de caneca" 1

# Sem IA (template vazio preenchido)
python main.py rapido "Meu vlog de viagem" 2
```

### Configurar IA

Copie o arquivo de exemplo:

```bash
cp .env.example .env
# Edite .env com sua chave de API
```

Ou exporte diretamente:

```bash
# Windows
set OPENAI_API_KEY=sk-sua-chave-aqui

# Linux/Mac
export OPENAI_API_KEY=sk-sua-chave-aqui
```

**Dica:** Use [Groq](https://groq.com) para geracao rapida e barata. E gratis para testes!

## Tipos de Roteiro

| ID | Nome | Ideal para |
|---|---|---|
| 1 | Tutorial / Educativo | Ensinar passo a passo |
| 2 | Vlog / Dia a Dia | Acompanhar rotina |
| 3 | Review / Unboxing | Analisar produtos |
| 4 | Storytelling / Narrativa | Contar historias |
| 5 | Venda / Pitch | Vender ou convencer |

## Exemplo de PDF gerado

O PDF inclui:
- Capa com titulo e metadata
- Blocos com tempo estimado
- Texto do roteiro formatado
- Notas de producao
- Pagina extra com dicas especificas

## Estrutura do Projeto

```oteirista_ai/
  main.py           # CLI interativo
  pdf_generator.py  # Gerador de PDF
  ia_client.py      # Cliente de IA
  templates.py      # Templates de roteiro
  requirements.txt  # Dependencias
  .env.example      # Exemplo de configuracao
```
