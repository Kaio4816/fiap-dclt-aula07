# 🤖 Analisador de Logs com IA

Projeto de demonstração da **Aula 07 - FIAP** (Vídeo 7.2).

Mostra como usar IA para analisar logs e detectar problemas automaticamente.

## 📁 Estrutura

```
aula07-ia-logs/
├── logs/
│   └── app.log              # Logs de exemplo
├── analyze_logs.py          # Analisador com Ollama (local)
├── analyze_logs_ci.py       # Analisador com Groq (CI)
└── requirements.txt
```

## 🚀 Quick Start

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Analisar logs localmente (Ollama)

```bash
# Certifique que Ollama está rodando
ollama serve

# Rodar análise
python analyze_logs.py
```

### 3. Analisar logs no CI (Groq)

```bash
export GROQ_API_KEY="sua-chave"
python analyze_logs_ci.py
```

## 🎯 Conceito

```
Logs da aplicação → IA analisa → Detecta problemas → Alerta
```

## 🔗 Links

- [Ollama](https://ollama.com)
- [Groq Console](https://console.groq.com)
