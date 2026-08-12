print("--- 1. SELECT e WHERE (Filtrando dados) ---")
# SQL: SELECT nome, salario FROM df WHERE departamento = 'Engenharia'
filtro = df['departamento'] == 'Engenharia'
df_engenharia = df.loc[filtro, ['nome', 'salario']]
print(df_engenharia)

print("\n--- 2. GROUP BY e AVG (Agrupando e calculando média) ---")
# SQL: SELECT departamento, AVG(salario) FROM df GROUP BY departamento
media_salarial = df.groupby('departamento')['salario'].mean()
print(media_salarial)

print("\n--- 3. ORDER BY (Ordenando dados) ---")
# SQL: ORDER BY salario DESC
df_ordenado = df.sort_values(by='salario', ascending=False)
print(df_ordenado[['nome', 'salario']])

print("\n--- 4. ALTER TABLE ADD COLUMN (Criando nova coluna) ---")
# Vamos dar um bônus de 10% para todos
df['salario_com_bonus'] = df['salario'] * 1.10
print(df[['nome', 'salario', 'salario_com_bonus']].head())