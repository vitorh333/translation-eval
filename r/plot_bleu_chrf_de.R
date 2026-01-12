library(ggplot2)
library(tidyr)
library(dplyr)
library(readr)

# Caminho do CSV
csv_file <- "data/results/translation_metrics_final_bleu_chrf.csv"

# Ler dados
df <- read_csv(csv_file)

# Converter para formato longo (BLEU / CHRF)
df_long <- df %>%
  pivot_longer(
    cols = c(BLEU, CHRF),
    names_to = "metrica",
    values_to = "score"
  )

# Filtrar apenas o alemão
df_de <- df_long %>% filter(idioma == "de")

# Criar pasta graphs se não existir
if(!dir.exists("graphs")) dir.create("graphs")

# Caminho do PDF
pdf_file <- "graphs/translation_metrics_de.pdf"

# Abrir dispositivo PDF
pdf(pdf_file, width = 10, height = 5)

# Gerar e imprimir gráfico
print(
  ggplot(df_de, aes(x = metrica, y = score, fill = modelo)) +
    geom_bar(
      stat = "identity",
      position = position_dodge(width = 0.7),
      width = 0.6
    ) +
    labs(
      title = "BLEU e CHRF para Alemão",
      x = "",
      y = "Score",
      fill = "Modelo"
    ) +
    scale_fill_manual(values = c(
      "Gemini" = "#F4A300",
      "Claude" = "#E63946"
    )) +
    ylim(0, 80) +
    theme_minimal(base_size = 13) +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold"),
      legend.position = "top"
    )
)

# Fechar dispositivo PDF
dev.off()

cat("PDF salvo em:", pdf_file, "\n")

