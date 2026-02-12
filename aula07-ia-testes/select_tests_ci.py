#!/usr/bin/env python3
"""
🤖 Seletor de Testes com IA (versão CI/CD)

Uso:
    export GEMINI_API_KEY="sua-chave-aqui"
    python select_tests_ci.py

Debug no CI:
    export DEBUG_AI=1
"""
import subprocess
import requests
import os
import sys
from pathlib import Path


USE_GEMINI = True
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DEBUG_AI = os.getenv("DEBUG_AI", "0") == "1"


def get_changed_files() -> str:
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
    return ""


def normalize_changed_files(changed_files: str) -> str:
    base = Path.cwd().name  # ex: aula07-ia-testes
    prefix = f"{base}/"
    normalized = []

    for line in changed_files.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(prefix):
            line = line[len(prefix):]
        normalized.append(line)

    return "\n".join(normalized)


def deterministic_tests(changed_files: str) -> list:
    """
    Regras fixas (não dependem de IA).
    """
    mapping = {
        "src/calculadora.py": "tests/test_calculadora.py",
        "src/usuario.py": "tests/test_usuario.py",
    }

    tests = set()

    for f in changed_files.splitlines():
        f = f.strip()
        if not f:
            continue

        # Se alterou um teste, roda ele mesmo
        if f.startswith("tests/") and f.endswith(".py") and Path(f).exists():
            tests.add(f)

        # Se alterou src, roda o teste mapeado
        if f in mapping and Path(mapping[f]).exists():
            tests.add(mapping[f])

    return sorted(tests)


def ask_gemini(changed_files: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Erro: GEMINI_API_KEY não está configurada!")
        sys.exit(1)

    prompt = f"""Você é um assistente de CI/CD.

Arquivos modificados:
{changed_files}

Quais testes pytest devo rodar?

Regras:
- src/calculadora.py → tests/test_calculadora.py
- src/usuario.py → tests/test_usuario.py
- tests/*.py → o próprio arquivo

Responda APENAS os caminhos dos arquivos de teste, um por linha, sem explicação.
Não use bullets, não use markdown, não use texto extra.
Exemplo de resposta válida:
tests/test_calculadora.py
tests/test_usuario.py
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"

    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 200}
        },
        timeout=30
    )

    if DEBUG_AI:
        print("\n🧾 DEBUG: status Gemini:", response.status_code)
        # NÃO imprime a URL (pra não vazar key)
        print("🧾 DEBUG: response text (raw):")
        print(response.text)

    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def extract_tests_from_text(text: str) -> list:
    """
    Extrai qualquer ocorrência de tests/*.py mesmo que venha com lixo junto.
    """
    found = set()

    # pega tokens “quebrando” por whitespace e pontuação comum
    separators = ["\n", "\t", " ", ",", ";", ":", "|"]
    tokens = [text]
    for sep in separators:
        new_tokens = []
        for t in tokens:
            new_tokens.extend(t.split(sep))
        tokens = new_tokens

    for tok in tokens:
        tok = tok.strip().strip("`").strip('"').strip("'").strip().lstrip("-*•").strip()
        if "tests/" in tok:
            idx = tok.find("tests/")
            tok = tok[idx:]
        if tok.startswith("tests/") and tok.endswith(".py") and Path(tok).exists():
            found.add(tok)

    return sorted(found)


def main():
    api_name = "Gemini" if USE_GEMINI else "Groq"

    print("=" * 50)
    print(f"🤖 Seletor de Testes com IA ({api_name} API)")
    print("=" * 50)
    print("")

    print("🔍 Analisando mudanças...")
    changed_files = get_changed_files()
    changed_files = normalize_changed_files(changed_files)

    if not changed_files.strip():
        print("📝 Modificados: Nenhum arquivo modificado")
        changed_files = ""
    else:
        print(f"📝 Modificados: {changed_files}")

    # 1) Primeiro: determinístico (garante que sempre funcione)
    valid_tests = deterministic_tests(changed_files)

    # 2) IA como complemento (se quiser), mas não quebra pipeline
    print(f"\n🤖 Consultando {api_name} API...")
    try:
        suggestion = ask_gemini(changed_files if changed_files else "Nenhum arquivo modificado")
        ai_tests = extract_tests_from_text(suggestion)
        valid_tests = sorted(set(valid_tests) | set(ai_tests))
    except Exception as e:
        # Falhou IA? segue com determinístico.
        print(f"⚠️  IA falhou ({e}). Seguindo com seleção determinística.")

    if not valid_tests:
        print("\n⚠️  Nenhum teste válido sugerido.")
        valid_tests = []

    print("\n✅ Testes a executar:")
    for test in valid_tests:
        print(f"  {test}")

    with open("suggested_tests.txt", "w") as f:
        f.write("\n".join(valid_tests))

    print("\n📄 Salvo em: suggested_tests.txt")


if __name__ == "__main__":
    main()
