/* 
 	##################### QUESTÃO 5 - DIMENSÃO DE CALENDÁRIO ######################################
  
    O período de análise deve considerar todas as datas entre a menor e a data atual da venda presentes no arquivo.
    A loja esteve aberta em todos os dias do período (inclusive fins de semana).
    Considere apenas as lojas fisicas (= pos)
    Dias sem registro na tabela de vendas devem ser considerados como valor da venda = 0.
    “Vendas diárias” correspondem à soma de valor da venda por dia.
    A média de vendas por dia da semana deve considerar todos os dias do calendário, inclusive os dias sem venda.
    O nome do dia da semana deve ser apresentado em português (Segunda-feira, Terça-feira, etc.)
	LEFT JOIN entre o calendário e a tabela de vendas agregação de vendas por dia (soma de valor_venda), 
	substituição de valores nulos por zero para dias sem vendas

Tarefa:
    Construa uma dimensão de datas utilizando sql
    Cruze a dimensão de datas com a tabela de vendas para análise.*/

WITH dimensao_calendario AS (
    -- Geração das datas da Dimensão Calendário
    SELECT
        g.date::DATE AS date_id
    FROM 
        generate_series(
            '2020-01-01'::DATE, 
            '2026-12-31'::DATE, 
            INTERVAL '1 day'
        ) AS g(date)
),
vendas_diarias AS (
    -- Soma o total por cada data (dias sem vendas = 0)
    SELECT
        c.date_id,
        EXTRACT(DOW FROM c.date_id) AS numero_dia_semana,
        CASE EXTRACT(DOW FROM c.date_id)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terça-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sábado'
        END AS dia_semana,
        COALESCE(SUM(o.total), 0) AS total_dia
    FROM dimensao_calendario c
    LEFT JOIN orders o
		ON o.created_at::DATE = c.date_id
       	AND o.channel = 'pos'
       	AND o.status = 'paid'
    GROUP BY
        c.date_id
)
-- Agrupa por dia da semana e calcula a média geral
SELECT
    dia_semana,
    ROUND(AVG(total_dia), 2) AS media_vendas,
    COUNT(date_id) AS total_dias_analisados,
    SUM(total_dia) AS vendas_diarias
FROM vendas_diarias
GROUP BY
    numero_dia_semana,
    dia_semana
ORDER BY
    media_vendas ASC;


