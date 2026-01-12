import json
import csv
import sacrebleu

# Função para ler JSONL
def ler_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                data.append(json.loads(linha))
            except json.JSONDecodeError as e:
                print(f"⚠️ Erro ao ler objeto: {e}")
    return data

# Arquivos de tradução corrigidos
arquivos = {
    "Gemini": "data/results/Gemini/all_translations_Gemini_fixed_safe.jsonl",
    "Claude": "data/results/Claude/all_translations_Claude_fixed_safe.jsonl"
}

# CSV de saída
saida_csv = "data/results/translation_metrics_final_bleu_chrf.csv"

# Lista para armazenar resultados
resultados = []

for modelo, arquivo in arquivos.items():
    data = ler_jsonl(arquivo)
    if not data:
        print(f"⚠️ Nenhum dado válido encontrado para {modelo}")
        continue
    
    idiomas = list(data[0]["translations"].keys())
    
    for idioma in idiomas:
        refs = [item["source"] for item in data]  # Referência: sempre a coluna source
        hyps = [item["translations"][idioma] for item in data]
        
        # Calcular BLEU
        bleu = sacrebleu.corpus_bleu(hyps, [refs])
        
        # Calcular CHRF
        chrf = sacrebleu.corpus_chrf(hyps, [refs])
        
        resultados.append({
            "modelo": modelo,
            "idioma": idioma,
            "BLEU": round(bleu.score, 2),
            "CHRF": round(chrf.score, 2),
            "objetos": len(data)
        })

# Salvar CSV
with open(saida_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["modelo", "idioma", "BLEU", "CHRF", "objetos"])
    writer.writeheader()
    writer.writerows(resultados)

print(f"✅ Métricas BLEU + CHRF salvas em {saida_csv}")

