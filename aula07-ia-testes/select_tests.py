#!/usr/bin/env python3
"""
🤖 Seletor de Testes com IA (versão LOCAL)

Este script usa Ollama rodando localmente para analisar
quais arquivos foram modificados e sugerir quais testes rodar.

Uso:
    python select_tests.py

Pré-requisitos:
    1. Ollama instalado: curl -fsSL https://ollama.com/install.sh | sh
    2. Modelo baixado: ollama pull llama3.2
    3. Ollama rodando: ollama serve
"""
import subprocess
import requests
import sys


def get_changed_files():
    """
    Pega lista de arquivos modificados no último commit.
    
    Usa git diff para comparar com o commit anterior.
    Se não houver commit anterior, lista todos os arquivos.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"],
            capture_output=True, 
            text=True,
            check=True
        )
        files = result.stdout.strip()
        if files:
            return files
    except subprocess.CalledProcessError:
        pass
    
    # Fallback: listar todos os arquivos tracked
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def ask_ollama(changed_files: str) -> str:
    """
    Pergunta para IA local (Ollama) quais testes rodar.
    
    Args:
        changed_files: Lista de arquivos modificados
        
    Returns:
        Sugestão da IA sobre quais testes executar
    """
    
    prompt = f"""Você é um assistente de CI/CD especializado em Python.

Arquivos modificados no último commit:
{changed_files}

Baseado nos arquivos modificados, quais testes pytest devo executar?

Regras de mapeamento:
- Se mudou src/calculadora.py → rodar tests/test_calculadora.py
- Se mudou src/usuario.py → rodar tests/test_usuario.py  
- Se mudou um arquivo em tests/ → rodar esse teste específico
- Se mudou requirements.txt ou pyproject.toml → rodar todos os testes

Responda APENAS com os caminhos dos arquivos de teste, um por linha.
Não inclua explicações, apenas os caminhos.

Exemplo de resposta correta:
tests/test_calculadora.py
tests/test_usuario.py
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"].strip()
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Ollama não está rodando!")
        print("")
        print("Para iniciar o Ollama:")
        print("  1. Abra outro terminal")
        print("  2. Execute: ollama serve")
        print("")
        sys.exit(1)
        
    except requests.exceptions.Timeout:
        print("❌ Erro: Timeout na resposta do Ollama")
        sys.exit(1)


def main():
    """Função principal."""
    print("=" * 50)
    print("🤖 Seletor de Testes com IA (Ollama)")
    print("=" * 50)
    print("")
    
    # 1. Pegar arquivos modificados
    print("🔍 Analisando arquivos modificados...")
    changed_files = get_changed_files()
    
    if not changed_files:
        print("ℹ️  Nenhum arquivo modificado encontrado.")
        return
    
    print(f"\n📝 Arquivos modificados:")
    for f in changed_files.split('\n'):
        print(f"   - {f}")
    
    # 2. Consultar IA
    print("\n🤖 Consultando Ollama...")
    suggestion = ask_ollama(changed_files)
    
    # 3. Mostrar resultado
    print(f"\n✅ Testes sugeridos pela IA:")
    print("-" * 30)
    print(suggestion)
    print("-" * 30)
    
    # 4. Comando para rodar
    tests = " ".join(suggestion.split('\n'))
    print(f"\n💡 Comando para executar:")
    print(f"   pytest {tests} -v")


if __name__ == "__main__":
    main()
