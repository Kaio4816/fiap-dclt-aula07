# 🎬 Vídeo 7.1 - Otimização de Testes com IA

## 📋 Informações do Vídeo

| Item | Detalhe |
|------|---------|
| **Duração** | ~15 minutos |
| **Tema** | IA para seleção inteligente de testes |
| **Ferramentas** | Ollama (local) + Groq API (CI) |
| **Custo** | $0 (100% gratuito) |
| **Pré-requisito** | Python 3.9+, Git |

---

## 🎯 Objetivo

Ensinar como usar **IA gratuita** para analisar código e sugerir quais testes executar, economizando tempo no CI/CD.

---

## 🧠 Arquitetura e Conceito

### O Problema

Em projetos grandes, rodar **todos os testes** a cada commit é lento e caro:

```
Projeto com 500 testes
├── Tempo: 30 minutos por PR
├── Custo: Minutos de CI consumidos
└── Feedback: Desenvolvedor espera muito
```

### A Solução: IA para Seleção Inteligente

A IA analisa **quais arquivos mudaram** e sugere **apenas os testes relacionados**:

```
Mudou: src/calculadora.py
   ↓
IA entende: "Calculadora foi modificada"
   ↓
Sugere: tests/test_calculadora.py
   ↓
Resultado: 5 testes em 30 segundos (em vez de 500 em 30 min)
```

### 📊 Diagrama: Visão Geral

```mermaid
graph TB
    subgraph "Sem IA (Tradicional)"
        A1[Push] --> A2[Roda TODOS os testes]
        A2 --> A3[500 testes = 30 min]
    end
    
    subgraph "Com IA (Inteligente)"
        B1[Push] --> B2[IA analisa mudanças]
        B2 --> B3[Sugere testes relevantes]
        B3 --> B4[10 testes = 1 min]
    end
    
    style A3 fill:#ef4444
    style B4 fill:#10b981
```

### 📊 Diagrama: Fluxo Detalhado

```mermaid
sequenceDiagram
    participant Dev as Desenvolvedor
    participant Git as Git
    participant IA as Ollama/Groq
    participant CI as CI/CD
    
    Dev->>Git: git commit (modifica calculadora.py)
    Git->>IA: Quais arquivos mudaram?
    IA->>IA: Analisa: calculadora.py
    IA->>IA: Mapeia: calculadora → test_calculadora
    IA-->>CI: Rodar: test_calculadora.py
    CI->>Dev: ✅ Passou (30 seg)
```

### Ferramentas Utilizadas

| Ferramenta | Onde Usa | Por quê? |
|------------|----------|----------|
| **Ollama** | Local (desenvolvimento) | IA grátis, roda offline |
| **Groq API** | CI/CD (GitHub Actions) | API grátis, sem download |

### Por que duas ferramentas?

```mermaid
graph LR
    subgraph "Local"
        A[Ollama] --> B[Modelo 2GB local]
        B --> C[Funciona offline]
    end
    
    subgraph "CI/CD"
        D[Groq API] --> E[Modelo na nuvem]
        E --> F[Sem download]
    end
    
    style A fill:#10b981
    style D fill:#3b82f6
```

- **Ollama no CI** = Baixar 2GB a cada run ❌
- **Groq no CI** = Chamada HTTP de 1 segundo ✅

---

## 📊 Diagrama: Conceito Simples

```mermaid
graph LR
    A[📝 Código Mudou] --> B[🤖 IA Analisa]
    B --> C[🎯 Sugere Testes]
    C --> D[✅ Roda só o necessário]
    
    style B fill:#10b981
```

**Benefício:** Em vez de rodar 100 testes (30 min), roda só 10 relevantes (3 min).

---

## 🛠️ Parte 1: Configurar Ollama (Local)

### Passo 1: Instalar Ollama

```bash
# macOS/Linux - Um comando!
curl -fsSL https://ollama.com/install.sh | sh

# Windows - Baixar instalador em:
# https://ollama.com/download
```

### Passo 2: Baixar um modelo leve

```bash
# Modelo pequeno e rápido (~2GB)
ollama pull llama3.2

# Testar se funcionou
ollama run llama3.2 "Olá, tudo bem?"
```

> 💡 **Dica:** O modelo fica salvo. Só precisa baixar uma vez!

### Passo 3: Verificar API rodando

**Mac/Linux:**
```bash
curl http://localhost:11434/api/tags
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

**Saída esperada:**
```json
{
  "models": [{"name": "llama3.2:latest"}]
}
```

---

## 🐍 Parte 2: Explorar o Projeto

O projeto já está pronto na pasta `aula07-ia-testes/`.

### Estrutura dos Arquivos

```
aula07-ia-testes/
├── src/
│   ├── calculadora.py      # Funções: somar, subtrair, etc
│   └── usuario.py          # Funções: criar_usuario, validar_email
├── tests/
│   ├── test_calculadora.py # Testes da calculadora
│   └── test_usuario.py     # Testes do usuário
├── select_tests.py         # 🤖 Seletor com Ollama (LOCAL)
├── select_tests_ci.py      # 🤖 Seletor com Groq (CI)
└── requirements.txt
```

### Passo 4: Entrar no projeto e instalar dependências

```bash
cd aula07-ia-testes

# Instalar dependências
pip install -r requirements.txt
```

### Passo 5: Rodar os testes (modo tradicional)

```bash
# Roda TODOS os testes
pytest tests/ -v
```

**Saída:**
```
tests/test_calculadora.py::test_somar PASSED
tests/test_calculadora.py::test_subtrair PASSED
tests/test_calculadora.py::test_multiplicar PASSED
tests/test_calculadora.py::test_dividir PASSED
tests/test_calculadora.py::test_dividir_por_zero PASSED
tests/test_usuario.py::test_criar_usuario PASSED
tests/test_usuario.py::test_validar_email_valido PASSED
tests/test_usuario.py::test_validar_email_invalido PASSED

8 passed in 0.05s
```

---

## 🤖 Parte 3: Usar o Seletor com IA

### Passo 6: Inicializar Git e fazer commit

```bash
# Inicializar repositório
git init

# Primeiro commit
git add .
git commit -m "Estrutura inicial do projeto"
```

### Passo 7: Simular uma modificação

**Mac/Linux:**
```bash
# Modificar apenas a calculadora
echo "" >> src/calculadora.py
echo "# Nova feature" >> src/calculadora.py

# Commit da mudança
git add .
git commit -m "Modificar calculadora"
```

**Windows (PowerShell):**
```powershell
# Modificar apenas a calculadora
Add-Content src/calculadora.py "`n# Nova feature"

# Commit da mudança
git add .
git commit -m "Modificar calculadora"
```

### Passo 8: Rodar o seletor com IA

```bash
python select_tests.py
```

**Saída esperada:**
```
==================================================
🤖 Seletor de Testes com IA (Ollama)
==================================================

🔍 Analisando arquivos modificados...

📝 Arquivos modificados:
   - src/calculadora.py

🤖 Consultando Ollama...

✅ Testes sugeridos pela IA:
------------------------------
tests/test_calculadora.py
------------------------------

💡 Comando para executar:
   pytest tests/test_calculadora.py -v
```

### Passo 9: Rodar apenas os testes sugeridos

```bash
# Agora roda SÓ o que a IA sugeriu!
pytest tests/test_calculadora.py -v
```

**Resultado:** 5 testes em vez de 8! 🎉

---

## 📊 Diagrama: O que aconteceu

```mermaid
sequenceDiagram
    participant Dev as Você
    participant Script as select_tests.py
    participant Git as Git
    participant Ollama as Ollama (IA)
    
    Dev->>Script: python select_tests.py
    Script->>Git: git diff --name-only HEAD~1
    Git-->>Script: src/calculadora.py
    Script->>Ollama: "Quais testes rodar?"
    Ollama-->>Script: tests/test_calculadora.py
    Script-->>Dev: ✅ Rodar: test_calculadora.py
```

---

## ☁️ Parte 4: Preparar para CI/CD (Gemini API)

### Por que API na nuvem em vez de Ollama no CI?

| Aspecto | Ollama no CI | Gemini/Groq API |
|---------|--------------|-----------------|
| Download | 2GB por run ❌ | 0 ✅ |
| Tempo | +10 min ❌ | +2 seg ✅ |
| Custo | Consome minutos | Grátis ✅ |

### Passo 10: Criar conta no Google AI Studio (grátis)

1. Acesse: https://aistudio.google.com/apikey
2. Faça login com sua conta Google
3. Clique em **Create API Key**
4. Copie a chave

> 💡 **Alternativa:** Se preferir usar Groq, acesse https://console.groq.com

### Passo 11: Testar localmente com Gemini

**Mac/Linux:**
```bash
# Configurar a chave
export GEMINI_API_KEY="sua_chave_aqui"

# Rodar versão CI
python select_tests_ci.py
```

**Windows (PowerShell):**
```powershell
# Configurar a chave
$env:GEMINI_API_KEY="sua_chave_aqui"

# Rodar versão CI
python select_tests_ci.py
```

**Saída:**
```
==================================================
🤖 Seletor de Testes com IA (Gemini API)
==================================================

🔍 Analisando mudanças...
📝 Modificados: src/calculadora.py

🤖 Consultando Gemini API...

✅ Testes sugeridos:
tests/test_calculadora.py

📄 Salvo em: suggested_tests.txt
```

---

## 🚀 Parte 5: Criar Workflow (FAZER JUNTOS NA AULA)

> ⚠️ **Esta parte faremos juntos durante a videoaula!**

O workflow será criado em `.github/workflows/ai-tests.yml` e vai:

1. Detectar arquivos modificados
2. Chamar Groq API para sugerir testes
3. Rodar apenas os testes sugeridos

---

## 📊 Diagrama: Fluxo Completo

```mermaid
graph TB
    subgraph "💻 Local (Desenvolvimento)"
        A[Código] --> B[select_tests.py]
        B --> C[Ollama Local]
        C --> D[Sugestão de Testes]
    end
    
    subgraph "☁️ CI (GitHub Actions)"
        E[Push/PR] --> F[select_tests_ci.py]
        F --> G[Groq API]
        G --> H[pytest]
    end
    
    style C fill:#10b981
    style G fill:#3b82f6
```

---

## ✅ Checklist de Aprendizado

Após este vídeo, você sabe:

- [ ] Instalar e usar Ollama localmente
- [ ] Fazer chamadas HTTP para LLMs
- [ ] Integrar IA com Git (arquivos modificados)
- [ ] Usar Groq API (grátis) no CI
- [ ] Criar GitHub Action com IA

---

## 🎯 Resumo

| Ambiente | Ferramenta | Custo | Velocidade |
|----------|------------|-------|------------|
| **Local** | Ollama | Grátis | ~2s |
| **CI/CD** | Groq API | Grátis | ~1s |

### Economia Real

```
Sem IA:  100 testes × 30 min = 30 min por PR
Com IA:  10 testes × 3 min = 3 min por PR

Economia: 90% do tempo! 🚀
```

---

## 🔗 Links Úteis

- **Ollama**: https://ollama.com
- **Groq Console**: https://console.groq.com
- **Modelos Groq**: https://console.groq.com/docs/models

---

## ⏭️ Próximo Vídeo

**Vídeo 7.2**: Detecção de Falhas com IA
- Analisar logs automaticamente
- Detectar padrões de erro
- Alertas inteligentes

---

**FIM DO VÍDEO 7.1** ✅
