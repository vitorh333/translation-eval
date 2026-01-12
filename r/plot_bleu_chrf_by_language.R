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

# Renomear idiomas para nomes bonitos (para título)
idiomas_bonitos <- c(
  "pt-BR" = "Portuguese (Brazil)",
  "fr"    = "French",
  "de"    = "German",
  "it"    = "Italian",
  "es-MX" = "Spanish (Mexico)"
)

# Criar pasta graphs se não existir
if(!dir.exists("graphs")) dir.create("graphs")

# Caminho do PDF único
pdf_file <- "graphs/translation_metrics_all_languages.pdf"

# Abrir dispositivo PDF
pdf(pdf_file, width = 10, height = 5)

# Loop sobre todos os idiomas
for (idioma in names(idiomas_bonitos)) {
  
  # Filtrar dados para o idioma atual
  df_id <- df_long %>% filter(idioma == idioma)
  
  # Nome bonito para título
  titulo <- paste("BLEU e CHRF para", idiomas_bonitos[idioma])
  
  # Gerar e imprimir gráfico (cada print() gera uma nova página)
  print(
    ggplot(df_id, aes(x = metrica, y = score, fill = modelo)) +
      geom_bar(
        stat = "identity",
        position = position_dodge(width = 0.7),
        width = 0.6
      ) +
      labs(
        title = titulo,
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
}

# Fechar dispositivo PDF
dev.off()

cat("PDF com todos os idiomas salvo em:", pdf_file, "\n")

