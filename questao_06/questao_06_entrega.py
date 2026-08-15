"""Lighthouse_Questao_06.ipynb
"""

#@title Imports
import pandas as pd
from sklearn.metrics import mean_absolute_error

"""

## 1. Preparação de dados

"""

#@title Carregar os arquivos products.csv, product_variants, orders.csv e order_items.csv

df_orders = pd.read_csv('orders.csv')
df_order_items = pd.read_csv('order_items.csv')
df_prod_var = pd.read_csv('product_variants.csv')
df_products = pd.read_csv('products.csv')


#@title Excluir colunas não necessárias

# 1.Colunas essenciais de cada tabela

df_orders_clean = df_orders[['id', 'created_at', 'status']].copy()
df_order_items_clean = df_order_items[['order_id', 'product_variant_id', 'quantity']].copy()
df_prod_var_clean = df_prod_var[['id', 'product_id']].copy()
df_products_clean = df_products[['id', 'name']].copy()


# 2. Merges sequenciais

# 'orders' com 'order_items'
df_unified = pd.merge(
    df_orders_clean,
    df_order_items_clean,
    left_on='id',
    right_on='order_id',
    how='inner'
)

# 'product_variants' (product_variant_id == id de product_variants)
df_unified = pd.merge(
    df_unified,
    df_prod_var_clean,
    left_on='product_variant_id',
    right_on='id',
    how='inner'
)

# 'products' (product_id == id de products)
df_unified = pd.merge(
    df_unified,
    df_products_clean,
    left_on='product_id',
    right_on='id',
    how='inner'
)

# Converter a coluna de data para o tipo datetime e manter apenas colunas finais limpas
df_unified['created_at'] = pd.to_datetime(df_unified['created_at'])
df_unified = df_unified[['created_at', 'name', 'quantity', 'status']].copy()
#df_unified

# @title Especificar o produto alvo da previsão

# Filtro
produto_alvo = 'Bússola de Bordo 702'
status_pago = 'paid'  # ajuste conforme o nome exato na sua base
data_limite = '2025-12-31 23:59:59'

# Filtragem produto, status pago e período(até 31/12/2025)
df_treino = df_unified[
    (df_unified['name'] == produto_alvo) &
    (df_unified['status'] == status_pago) &
    (df_unified['created_at'] <= data_limite)
].copy()

# Ordenar visualização
df_treino = df_treino.sort_values('created_at')

print(f"Total de vendas no período de treino: {len(df_treino)}")
print(f"Data mínima: {df_treino['created_at'].min()}")
print(f"Data máxima: {df_treino['created_at'].max()}")


"""

## 2. Calcular a previsão de vendas do 1º trimestre de 2026

"""

#@title Calcular a média móvel (10/2025 até 12/2025)

# 1. Agrupar as vendas por mês (soma da quantidade por mês)
vendas_mensais = (
    df_treino
    .set_index('created_at')
    .resample('MS')['quantity']
    .sum()
    .fillna(0) # Se algum mês não teve venda, preenche com 0
)

# 2. Filtrar os meses de Outubro, Novembro e Dezembro de 2025
ultimos_3_meses = vendas_mensais.loc['2025-10-01':'2025-12-01']

print("\n----- Vendas Mensais (Out, Nov, Dez de 2025) -----")
print(ultimos_3_meses)

# 3. Calcular a Média Móvel (Baseline)
media_movel_3m = ultimos_3_meses.mean()
print("="*56)
print(f"Média móvel dos últimos 3 meses: {media_movel_3m:.2f} unidades")
print("="*56)
#@title Calcula a previsão para o primeiro trimestre de 2026

# Primeiro trimestre
datas_previsao = pd.date_range(start='2026-01-01', periods=3, freq='MS')

# 3. Criar o DataFrame com as previsões mensais
df_previsoes = pd.DataFrame({
    'mes': datas_previsao,
    'previsao_vendas': [media_movel_3m] * 3
})

# Formatar a data para exibição no padrão 'AAAA-MM'
df_previsoes['mes_formatado'] = df_previsoes['mes'].dt.strftime('%Y-%m')

print("--- Previsão de Vendas: 1º Trimestre de 2026 ---")
print(df_previsoes[['mes_formatado', 'previsao_vendas']].to_string(index=False))

"""

## 3. Checar a previsão contra os dados reais de 2026
 
"""

# 1. Filtrar os dados de teste (01/2026 a 03/2026)
produto_alvo = 'Bússola de Bordo 702'
status_pago = 'paid'

df_teste = df_unified[
    (df_unified['name'] == produto_alvo) &
    (df_unified['status'] == status_pago) &
    (df_unified['created_at'] >= '2026-01-01 00:00:00') &
    (df_unified['created_at'] <= '2026-03-31 23:59:59')
].copy()

# 2. Agrupar as vendas reais por mês
vendas_reais_2026 = (
    df_teste
    .set_index('created_at')
    .resample('MS')['quantity']
    .sum()
    .reindex(pd.date_range('2026-01-01', '2026-03-01', freq='MS'), fill_value=0)
)

# 3. Montar a tabela comparativa
df_comparativo = pd.DataFrame({
    'mes': vendas_reais_2026.index.strftime('%Y-%m'),
    'vendas_reais': vendas_reais_2026.values,
    'previsao_baseline': [media_movel_3m] * len(vendas_reais_2026)
})

# Calcular o erro absoluto individual de cada mês
df_comparativo['erro_absoluto'] = (df_comparativo['vendas_reais'] - df_comparativo['previsao_baseline']).abs()

# 4. Calcular o MAE
mae = mean_absolute_error(df_comparativo['vendas_reais'], df_comparativo['previsao_baseline'])

# 5. Resultados
print("="*56)
print("----- Comparativo de Vendas (1º Trimestre de 2026) -----")
print(df_comparativo.to_string(index=False))
print("\n" + "="*56)
print(f"MAE (Erro Médio Absoluto): {mae:.2f} unidades")
print("="*56)