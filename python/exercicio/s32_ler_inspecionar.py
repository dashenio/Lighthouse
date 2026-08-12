import pandas as pd

# Lendo o CSV (Equivalente ao pd.read_csv('meu_arquivo.csv'))
df = pd.read_csv("exercicio\\teste.csv")

print("--- 1. df.head() -> Primeiras linhas ---")
print(df.head(3))

print("\n--- 2. df.shape -> Tamanho (Linhas, Colunas) ---")
print(df.shape)

print("\n--- 3. df.columns -> Nome das colunas ---")
print(df.columns.tolist())

print("\n--- 4. df.info() -> Resumo técnico ---")
df.info() # Repare que o info() já imprime direto no console