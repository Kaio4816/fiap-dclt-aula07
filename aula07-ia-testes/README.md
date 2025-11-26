# 🤖 Seletor de Testes com IA

Projeto de demonstração da **Aula 07 - FIAP**.

Mostra como usar IA para selecionar apenas os testes relevantes baseado nos arquivos modificados.

## 📁 Estrutura

```
aula07-ia-testes/
├── src/
│   ├── calculadora.py    # Funções matemáticas
│   └── usuario.py        # Gerenciamento de usuários
├── tests/
│   ├── test_calculadora.py
│   └── test_usuario.py
├── select_tests.py       # Seletor com Ollama (local)
├── select_tests_ci.py    # Seletor com Groq (CI)
└── requirements.txt
```

## 🚀 Quick Start

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar testes (tradicional)

```bash
pytest tests/ -v
```

### 3. Usar seletor com IA (local)

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixar modelo
ollama pull llama3.2

# Rodar seletor
python select_tests.py
```

### 4. Usar seletor com IA (CI)

```bash
# Configurar API key
export GROQ_API_KEY="sua-chave"

# Rodar seletor
python select_tests_ci.py
```

## 🎯 Conceito

```
Sem IA:  Roda TODOS os testes (100 testes = 30 min)
Com IA:  Roda só os relevantes (10 testes = 3 min)
```

## 🔗 Links

- [Ollama](https://ollama.com)
- [Groq Console](https://console.groq.com)
