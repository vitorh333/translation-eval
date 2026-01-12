import pandas as pd
import json
from pathlib import Path

# ======================
# CONFIGURAÇÃO
# ======================

CSV_PATH = "data/raw/all_languages.csv"
SRC_LANG = "English"
TARGET_LANGS = [
    "Portuguese, Brazilian",
    "French",
    "Italian",
    "German",
    "Spanish, Mexico"
]
N_SAMPLES = 50
RANDOM_SEED = 42

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ======================
# LEITURA DO CSV
# ======================

df = pd.read_csv(
    CSV_PATH,
    engine="python",
    sep=",",
    quotechar='"',
    encoding="utf-8",
    on_bad_lines="skip"
)

# ======================
# VERIFICAÇÃO DE COLUNAS
# ======================

required_cols = [SRC_LANG] + TARGET_LANGS
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Colunas faltando no CSV: {missing}")

# cria id se não existir
if "id" not in df.columns:
    df = df.reset_index(drop=True)
    df["id"] = df.index + 1

# ======================
# AMOSTRAGEM FIXA
# ======================

df_sample = df.sample(n=N_SAMPLES, random_state=RANDOM_SEED)

# ======================
# GERAÇÃO DOS JSONL
# ======================

for tgt in TARGET_LANGS:
    output_file = OUTPUT_DIR / f"{SRC_LANG}-{tgt}.jsonl"

    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df_sample.iterrows():

            if pd.isna(row[SRC_LANG]) or pd.isna(row[tgt]):
                continue

            example = {
                "id": int(row["id"]),
                "src": str(row[SRC_LANG]).strip(),
                "ref": str(row[tgt]).strip()
            }

            f.write(json.dumps(example, ensure_ascii=False) + "\n")

    print(f"✔ Gerado: {output_file}")

print("\nPronto. JSONL criados com 50 frases fixas.")

