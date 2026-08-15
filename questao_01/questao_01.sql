-- ######## QUESTÃO 1 - EDA ORDERS ########

/* Parte 1 - Visão geral da tabela orders
Informe: */

-- SCRIPT ESCRITO NO POSTGRES 18.04.0

--	Quantidade total de linhas - 48.998
SELECT COUNT(*) AS total_linhas FROM orders o;

--	Quantidade total de colunas - 13
SELECT 
	COUNT(*) AS total_colunas 
FROM information_schema.columns 
WHERE 
	table_name = 'orders';

-- Intervalo de datas analisado (data mínima e máxima) da coluna created_at
-- Data mínima: 01/01/2020 01:19:28
-- Data máxima: 31/12/2026 23:43:09
-- Intervalo: 2556 dias
SELECT
	MAX(created_at) AS data_maxima,
	MIN(created_at) AS data_minima,
	CAST(MAX(created_at) AS timestamp) - CAST(MIN(created_at)AS timestamp) AS intervalo_dias	
FROM orders;

/* Parte 2 - Análise de valores numéricos
Para a coluna "total", calcule: */

-- Valores calculados filtrando por status 'pago' (exluindo cancelled, draft e confirmed)
-- Valor mínimo - R$ 32,62
-- Valor máximo - R$ 127.262,02
-- Valor médio - R$ 28.684,45
SELECT 
	status,
	MIN(total) AS valor_minimo,
	MAX(total) AS valor_maximo,
	ROUND(CAST(AVG(total) AS decimal), 2) ticket_medio
FROM orders
	WHERE status = 'paid'
GROUP BY status;	


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
    SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) AS nulls_id,
    SUM(CASE WHEN order_number IS NULL THEN 1 ELSE 0 END) AS nulls_order_number,
    SUM(CASE WHEN channel IS NULL THEN 1 ELSE 0 END) AS nulls_channel,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS nulls_customer_id,
    SUM(CASE WHEN salesperson_id IS NULL THEN 1 ELSE 0 END) AS nulls_salesperson_id,
    SUM(CASE WHEN location_id IS NULL THEN 1 ELSE 0 END) AS nulls_location_id,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END) AS nulls_status,
    SUM(CASE WHEN subtotal IS NULL THEN 1 ELSE 0 END) AS nulls_subtotal,
    SUM(CASE WHEN discount_amount IS NULL THEN 1 ELSE 0 END) AS nulls_discount_amount,
    SUM(CASE WHEN total IS NULL THEN 1 ELSE 0 END) AS nulls_total,
    SUM(CASE WHEN placed_at IS NULL THEN 1 ELSE 0 END) AS nulls_placed_at,
    SUM(CASE WHEN created_at IS NULL THEN 1 ELSE 0 END) AS nulls_created_at,
    SUM(CASE WHEN updated_at IS NULL THEN 1 ELSE 0 END) AS nulls_updated_at
FROM orders;
-- A checagem mostra 24131 nulos em salesperson_id


-- Checar por que os valores estão vazios
SELECT * FROM orders
LIMIT 10;

-- Parece que o não preenchimento do id de vendedor se dá pelo meio de venda (ecommerce)
SELECT COUNT(*) AS vendedor_vazio FROM orders
WHERE salesperson_id IS NULL;


SELECT COUNT(*) AS vendedor_vazio_ecommerce 
FROM orders
WHERE salesperson_id IS NULL AND channel = 'ecommerce';
/* As duas queries retornam o mesmo número de linhas (24131), 
então o não preenchimento do id de vendedor é 100% por causa do meio de venda */

-- As colunas placed_at, created_at e updated_at parecem redundantes (iguais)
SELECT 
	COUNT(*)
FROM orders
WHERE placed_at = created_at AND placed_at = updated_at;
/* A query comparando as três colunas retorna o número total de
linhas da tabela, então as três colunas são identicas em todos os registros */

SELECT 
	COUNT(*)
FROM orders
WHERE placed_at = updated_at;


--  PROCURAR OUTLIERS

-- 1. Outliers por dia (apenas pedidos pagos)
WITH estatisticas AS (
    SELECT 
        percentile_cont(0.25) WITHIN GROUP (ORDER BY total) AS q1,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY total) AS q3
    FROM orders
    WHERE status = 'paid' -- Filtro aplicado na base do cálculo do IQR
),
limites AS (
    SELECT 
        q3 + (1.5 * (q3 - q1)) AS limite_superior,
        q1 - (1.5 * (q3 - q1)) AS limite_inferior
    FROM estatisticas
)
SELECT 
    DATE(o.created_at) AS data_pedido,
    COUNT(*) AS qtd_outliers,
    SUM(o.total) AS faturamento_outliers,
    ROUND(AVG(o.total)::numeric, 2) AS valor_medio_outlier,
    MIN(o.total) AS menor_outlier_do_dia,
    MAX(o.total) AS maior_outlier_do_dia
FROM orders o
CROSS JOIN limites l
WHERE o.status = 'paid' 
  AND (o.total > l.limite_superior OR o.total < l.limite_inferior) -- Filtro de status movido para o WHERE
GROUP BY DATE(o.created_at)
ORDER BY data_pedido ASC;


-- 2. Outliers por mês (apenas pedidos pagos)
WITH estatisticas AS (
    SELECT 
        percentile_cont(0.25) WITHIN GROUP (ORDER BY total) AS q1,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY total) AS q3
    FROM orders
    WHERE status = 'paid'
),
limites AS (
    SELECT 
        q3 + (1.5 * (q3 - q1)) AS limite_superior,
        q1 - (1.5 * (q3 - q1)) AS limite_inferior
    FROM estatisticas
)
SELECT 
    TO_CHAR(o.created_at::timestamp, 'YYYY-MM') AS ano_mes,
    COUNT(*) AS qtd_outliers,
    SUM(o.total) AS faturamento_outliers,
    ROUND(AVG(o.total)::numeric, 2) AS valor_medio_outlier,
    MIN(o.total) AS menor_outlier_do_mes,
    MAX(o.total) AS maior_outlier_do_mes
FROM orders o
CROSS JOIN limites l
WHERE o.status = 'paid'
  AND (o.total > l.limite_superior OR o.total < l.limite_inferior)
GROUP BY TO_CHAR(o.created_at::timestamp, 'YYYY-MM')
ORDER BY ano_mes ASC;


-- 3. Total de Outliers + Porcentagem em relação aos pedidos PAGOS
WITH estatisticas AS (
    SELECT 
        percentile_cont(0.25) WITHIN GROUP (ORDER BY total) AS q1,
        percentile_cont(0.75) WITHIN GROUP (ORDER BY total) AS q3
    FROM orders
    WHERE status = 'paid'
),
limites AS (
    SELECT 
        q3 + (1.5 * (q3 - q1)) AS limite_superior,
        q1 - (1.5 * (q3 - q1)) AS limite_inferior
    FROM estatisticas
)
SELECT 
    COUNT(*) AS total_outliers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders WHERE status = 'paid'), 2) AS porcentagem_total_de_pedidos_pagos
FROM orders o
CROSS JOIN limites l
WHERE o.status = 'paid'
  AND (o.total > l.limite_superior OR o.total < l.limite_inferior);



