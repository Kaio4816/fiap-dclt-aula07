# 🤖 Resposta Automática a Incidentes

Projeto de demonstração da **Aula 07 - FIAP** (Vídeo 7.3).

Mostra como usar IA para classificar incidentes e executar runbooks automaticamente.

## 📁 Estrutura

```
aula07-ia-incident/
├── alerts/
│   ├── high_memory.json     # Alerta de memória alta
│   ├── database_down.json   # Alerta de DB fora
│   └── high_cpu.json        # Alerta de CPU alta
├── runbooks/
│   ├── clear_memory.py      # Runbook: limpar memória
│   ├── restart_service.py   # Runbook: reiniciar serviço
│   └── scale_resources.py   # Runbook: escalar recursos
├── logs/
│   └── incidents.log        # Histórico de incidentes
├── incident_handler.py      # Orquestrador principal
└── requirements.txt
```

## 🚀 Quick Start

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Testar um alerta

```bash
# Alerta de memória alta
python incident_handler.py alerts/high_memory.json

# Alerta de database
python incident_handler.py alerts/database_down.json

# Alerta de CPU
python incident_handler.py alerts/high_cpu.json
```

## 🎯 Fluxo

```
Alerta JSON → IA Classifica → Seleciona Runbook → Executa → Resolve!
```

## 📋 Runbooks Disponíveis

| Tipo | Runbook | Ação |
|------|---------|------|
| memory | clear_memory.py | Limpa cache, força GC |
| database | restart_service.py | Reinicia serviço |
| cpu | scale_resources.py | Escala réplicas |

## 🔗 Links

- [Ollama](https://ollama.com)
