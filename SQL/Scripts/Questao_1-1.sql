-- ######## QUESTÃO 1 - EDA ORDERS ########

/* Parte 1 - Visão geral da tabela orders
Informe: */

--	Quantidade total de linhas - 48.998
SELECT COUNT(*) AS total_linhas FROM orders o;

--	Quantidade total de colunas - 13
SELECT COUNT(*) AS total_colunas 
FROM pragma_table_info('orders');

-- Intervalo de datas analisado (data mínima e máxima) da coluna created_at
-- Data mínima: 01/01/2020 01:19:28
-- Data máxima: 31/12/2026 23:43:09
SELECT
	MAX(created_at) AS data_maxima,
	MIN(created_at) AS data_minima
FROM orders;

/* Parte 2 - Análise de valores numéricos
Para a coluna "total", calcule: */

-- Valor mínimo
SELECT 
	MIN(total)
FROM orders;	

-- Valor máximo
SELECT 
	MAX(total)
FROM orders;

-- Valor médio 
SELECT 
	ROUND(AVG(total), 2)
FROM orders;

/* Parte 3 - Interpretação
Responda de forma resumida:
Com base na análise exploratória realizada, escreva um breve diagnóstico sobre a confiabilidade da tabela o para análises futuras.
Comente sobre:

    possíveis outliers em "total",
    qualidade dos dados (valores nulos ou inconsistentes),
    e se você considera que o dataset está pronto para análises ou se exigiria tratamento prévio. */

-- Checagem de nulos
SELECT 
    COUNT(*) AS total_linhas,
    SUM(id IS NULL) AS nulls_id,
    SUM(order_number IS NULL) AS nulls_order_number,
    SUM(channel IS NULL) AS nulls_channel,
    SUM(customer_id IS NULL) AS nulls_customer_id,
    SUM(salesperson_id IS NULL) AS nulls_salesperson_id,
    SUM(location_id IS NULL) AS nulls_location_id,
    SUM(status IS NULL) AS nulls_status,
    SUM(subtotal IS NULL) AS nulls_subtotal,
    SUM(discount_amount IS NULL) AS nulls_discount_amount,
    SUM(total IS NULL) AS nulls_total,
    SUM(placed_at IS NULL) AS nulls_placed_at,
    SUM(created_at IS NULL) AS nulls_created_at,
    SUM(updated_at IS NULL) AS nulls_updated_at
FROM orders;
-- A checagem não mostra nulos, mas existem campos vazios em salesperson_id

SELECT 
    salesperson_id,
    LENGTH(salesperson_id) AS tamanho_texto,
    typeof(salesperson_id) AS tipo_dado
FROM orders
WHERE salesperson_id IS NOT NULL AND salesperson_id NOT IN ('interger')
LIMIT 10;
-- Os espaços vazios estão com tipo texto, então são provavelmente strings vazias


-- Checar por que os valores estão vazios
SELECT * FROM orders
WHERE TYPEOF(salesperson_id) == 'text'

-- Parece que o não preenchimento do id de vendedor se dá pelo meio de venda (ecommerce)
SELECT COUNT(*) AS vendedor_vazio FROM orders
WHERE TYPEOF(salesperson_id) == 'text'

SELECT COUNT(*) AS vendedor_vazio_ecommerce FROM orders
WHERE TYPEOF(salesperson_id) == 'text' AND channel == 'ecommerce';
-- As duas queries retornam o mesmo número de linhas (24131), então
-- o não preenchimento do id de vendedor é 100% por causa do meio de venda




