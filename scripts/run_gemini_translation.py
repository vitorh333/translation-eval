import os
import json
from pathlib import Path
import google.generativeai as genai
import time

# ======================
# CONFIGURAÇÃO
# ======================

MODEL_NAME = "models/gemini-2.5-flash"  # free tier
INPUT_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/results/Gemini_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LANG_MAP = {
    "English-Portuguese, Brazilian.jsonl": "Portuguese (Brazil)",
    "English-French.jsonl": "French",
    "English-Italian.jsonl": "Italian",
    "English-German.jsonl": "German",
    "English-Spanish, Mexico.jsonl": "Spanish (Latin American)"
}

SYSTEM_PROMPT = """
You are an expert game localization and translation assistant,
specialized in translating strings used in digital games
(UI texts, menus, buttons, system messages, achievements,
tutorials, notifications, and marketing microcopy).

Translate the given English string into the target language.
Follow these rules strictly:

- Assume all strings belong to a video game or platform.
- Prefer short, clear, and natural phrasing suitable for UI.
- Preserve placeholders, variables, and formatting exactly.
- Preserve capitalization intent.
- Do NOT add explanations or comments.
- Output ONLY the translated text.
"""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(MODEL_NAME)

# ======================
# EXECUÇÃO - 1 FRASE POR VEZ
# ======================

REQUEST_INTERVAL = 12  # segundos entre requests para respeitar 5 req/min

for file_name, target_lang in LANG_MAP.items():

    input_path = INPUT_DIR / file_name
    output_path = OUTPUT_DIR / file_name

    print(f"\n▶ Traduzindo {file_name} → Gemini ({target_lang})")

    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:

        # pega apenas 1 frase de teste (linha 0)
        line = fin.readline()
        if not line:
            print("⚠ Input vazio")
            continue

        dado = json.loads(line)
        texto_ingles = dado.get("src")
        idx = dado.get("id", "N/A")

        prompt = f"""
{SYSTEM_PROMPT}

TARGET LANGUAGE: {target_lang}

SOURCE STRING:
{texto_ingles}
""".strip()

        try:
            response = model.generate_content(prompt)
            traducao = response.text.strip()

            resultado = {
                "id": idx,
                "src": texto_ingles,
                "hyp": traducao
            }

            fout.write(json.dumps(resultado, ensure_ascii=False) + "\n")
            fout.flush()

            print(f"✔ Tradução gerada para id {idx}: {traducao}")

        except Exception as e:
            print(f"❌ Erro no id {idx}: {e}")

        # delay fixo para respeitar 5 req/min
        time.sleep(REQUEST_INTERVAL)

print("\n✅ Tradução de teste finalizada.")

