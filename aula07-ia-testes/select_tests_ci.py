#!/usr/bin/env python3
"""
🤖 Seletor de Testes com IA (versão CI/CD)

Este script usa a API do Google Gemini (grátis) para analisar
quais testes rodar no GitHub Actions.

Uso:
    export GEMINI_API_KEY="sua-chave-aqui"
    python select_tests_ci.py
"""
import subprocess
import requests
import os
import sys
from pathlib import Path


# ============================================================
# CONFIGURAÇÃO: Escolha qual API usar
# ============================================================

USE_GEMINI = True  # Mude para False para usar Groq


def get_changed_files() -> str:
    """
    Pega lista de arquivos modificados.

    No CI, compara com o commit anterior (HEAD~1).
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

    return "Nenhum arquivo modificado"


def normalize_changed_files(changed_files: str) -> str:
    """
    Normaliza paths vindos do git diff para o contexto do diretório atual.

    Exemplo: se você executa o script dentro de "aula07-ia-testes",
    o git diff pode retornar:
        aula07-ia-testes/src/calculadora.py
    e aqui transformamos em:
        src/calculadora.py
    """
    base = Path.cwd().name  # ex: "aula07-ia-testes"
    normalized = []

    for line in changed_files.splitlines():
        line = line.strip()
        if not line:
            continue

        # Remove prefixo "<pasta_atual>/" se existir
        prefix = f"{base}/"
        if line.startswith(prefix):
            line = line[len(prefix):]

        normalized.append(line)

    return "\n".join(normalized) if normalized else "Nenhum arquivo modificado"


def ask_gemini(changed_files: str) -> str:
    """
    Consulta a API do Google Gemini para sugestão de testes.

    Args:
        changed_files: Lista de arquivos modificados

    Returns:
        Sugestão de testes da IA
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("❌ Erro: GEMINI_API_KEY não está configurada!")
        print("")
        print("Para configurar:")
        print("  1. Acesse https://aistudio.google.com/apikey")
        print("  2. Clique em 'Create API Key'")
        print("  3. export GEMINI_API_KEY='sua-chave'")
        print("")
        sys.exit(1)

    prompt = f"""Você é um assistente de CI/CD.

Arquivos modificados:
{changed_files}

Quais testes pytest devo rodar?

Regras:
- src/calculadora.py → tests/test_calculadora.py
- src/usuario.py → tests/test_usuario.py
- tests/*.py → o próprio arquivo

Responda APENAS os caminhos dos arquivos de teste, um por linha, sem explicação."""

    try:
        response = requests.post(
            # ✅ modelo 2.5 funcionando no seu caso
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 200
                }
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro na API Gemini: {e}")
        print(f"   Response: {response.text}")
        sys.exit(1)


def to_repo_relative_test_path(line: str) -> str:
    """
    Converte uma linha retornada pela IA em um path relativo ao diretório atual,
    garantindo que comece em "tests/".

    Exemplos:
    - "tests/test_calculadora.py" -> "tests/test_calculadora.py"
    - "aula07-ia-testes/tests/test_calculadora.py" -> "tests/test_calculadora.py"
    - "./tests/test_calculadora.py" -> "tests/test_calculadora.py"
    """
    line = line.strip().lstrip("./")

    # Se vier com prefixo do cwd (ex: aula07-ia-testes/tests/...)
    base = Path.cwd().name
    prefix = f"{base}/"
    if line.startswith(prefix):
        line = line[len(prefix):]

    # Se ainda tiver "tests/" em algum lugar, corta do primeiro "tests/"
    idx = line.find("tests/")
    if idx != -1:
        line = line[idx:]

    return line


def filter_valid_tests(suggestion: str) -> list:
    """
    Filtra a sugestão da IA para manter apenas arquivos de teste válidos.

    ✅ Agora aceita respostas com prefixo (ex: aula07-ia-testes/tests/...)
    """
    valid_tests = []

    for raw in suggestion.split('\n'):
        raw = raw.strip()
        if not raw:
            continue

        line = to_repo_relative_test_path(raw)

        # Ignorar linhas que não são testes
        if not line.startswith('tests/'):
            continue
        if not line.endswith('.py'):
            continue
        if 'pytest' in line.lower():
            continue

        # Verificar se o arquivo existe (relativo ao cwd)
        if Path(line).exists():
            valid_tests.append(line)

    return list(set(valid_tests))


def main():
    """Função principal para CI."""
    api_name = "Gemini" if USE_GEMINI else "Groq"

    print("=" * 50)
    print(f"🤖 Seletor de Testes com IA ({api_name} API)")
    print("=" * 50)
    print("")

    # 1. Pegar arquivos modificados
    print("🔍 Analisando mudanças...")
    changed_files = get_changed_files()

    # ✅ normaliza para casar com as regras do prompt
    changed_files = normalize_changed_files(changed_files)

    print(f"📝 Modificados: {changed_files}")

    # 2. Consultar IA
    print(f"\n🤖 Consultando {api_name} API...")

    if USE_GEMINI:
        suggestion = ask_gemini(changed_files)
    else:
        print("❌ Groq não está habilitado. Descomente a função ask_groq.")
        sys.exit(1)

    # 3. Filtrar apenas testes válidos
    valid_tests = filter_valid_tests(suggestion)

    if not valid_tests:
        print("\n⚠️  Nenhum teste válido sugerido.")
        valid_tests = []

    # 4. Mostrar resultado
    print(f"\n✅ Testes a executar:")
    for test in valid_tests:
        print(f"  {test}")

    # 5. Salvar para uso no workflow
    with open("suggested_tests.txt", "w") as f:
        f.write("\n".join(valid_tests))

    print("\n📄 Salvo em: suggested_tests.txt")


if __name__ == "__main__":
    main()
