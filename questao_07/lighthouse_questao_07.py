"""
Lighthouse_Questao_07.ipynb

"""
#@title Imports
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

#@title Carregar os arquivos products.csv, product_variants, orders.csv e order_items.csv

df_orders = pd.read_csv('orders.csv')
df_order_items = pd.read_csv('order_items.csv')
df_prod_var = pd.read_csv('product_variants.csv')
df_products = pd.read_csv('products.csv')

#@title Excluir colunas não necessárias

# 1.Colunas essenciais de cada tabela

df_orders_clean = df_orders[['id', 'customer_id', 'created_at', 'status']].copy()
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
df_unified = df_unified[['created_at', 'customer_id', 'product_id', 'name', 'quantity', 'status']].copy()

#@title Criar matriz de interação Cliente x Produto

# Criar uma coluna para indicar a interação (comprou = 1)
df_unified['interacao'] = 1

# Agrupar por customer_id e product_id e manter a primeira ocorrência (já que qualquer compra significa 1)
interacao_df = df_unified.groupby(['customer_id', 'product_id'])['interacao'].first().reset_index()

# Pivotar a tabela para criar a matriz de interação
matriz_cliente_produto = interacao_df.pivot_table(
    index='customer_id',
    columns='product_id',
    values='interacao'
).fillna(0).astype(int)

print(matriz_cliente_produto.head())

#@title Cálculo de Similaridade de Cosseno entre Produtos

# Transpor a matriz de interação para ter produtos como linhas e clientes como colunas
matriz_produto_cliente = matriz_cliente_produto.T

# Calcular a similaridade de cosseno entre os produtos
matriz_similaridade_produto = cosine_similarity(matriz_produto_cliente)

# Converter a matriz de similaridade para um DataFrame para melhor visualização
similaridade_produto_df = pd.DataFrame(
    matriz_similaridade_produto,
    index=matriz_produto_cliente.index,
    columns=matriz_produto_cliente.index
)

print("Matriz de Similaridade de Cosseno Produto x Produto (primeiras 5x5):")
print(similaridade_produto_df.head())

#@title Ranking de Produtos Similares ao 'Motor de Popa 1949'

# 1. Encontrar o product_id para 'Motor de Popa 1949'
nome_produto = 'Motor de Popa 1949'
id_produto = df_products_clean[df_products_clean['name'] == nome_produto]['id'].iloc[0]

# 2. Obter as similaridades para o produto de interesse
similaridades = similaridade_produto_df[id_produto]

# 3. Remover o próprio produto da lista de similaridade
similaridades = similaridades.drop(index=id_produto)

# 4. Classificar por similaridade em ordem decrescente e pegar os 5 primeiros
top_5_similar_ids = similaridades.nlargest(5).index.tolist()

# 5. Mapear os product_ids de volta para os nomes dos produtos
top_5_similar_nomes = df_products_clean[df_products_clean['id'].isin(top_5_similar_ids)]['name'].tolist()

print(f"Os 5 produtos mais similares a '{nome_produto}' são:")
for i, nome in enumerate(top_5_similar_nomes):
    print(f"{i+1}. {nome}")