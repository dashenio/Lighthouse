import pandas as pd

# Recapitulando Dicionários
dados = {
    'Nome': ['João', 'Maria', 'Pedro', 'Ana', 'Lucas'],
    'Idade': [28, 22, 35, 19, 42],
    'Departamento': ['TI', 'RH', 'TI', 'Financeiro', 'Vendas']
}

# Criando nosso DataFrame
df = pd.DataFrame(dados)

print("\n--- Inspecionando os Dados ---")
print("1. df.head():")
print(df.head(3)) 

print("\n2. df.shape (Linhas x Colunas):", df.shape)

print("\n--- Operações com Pandas ---")
# Equivalente a SELECT * FROM table WHERE Departamento = 'TI'
df_ti = df[df['Departamento'] == 'TI']

print("Funcionários exclusivos de TI:")
print(df_ti)