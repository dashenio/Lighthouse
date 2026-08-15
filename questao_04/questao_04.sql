
-- ######### QUESTAO 4 - ANÁLISE DE CLIENTES #########


/*  - Faturamento Total: Soma da coluna total por cliente.
	- Frequência: Contagem total de transações (IDs de venda) por cliente.
	- Ticket Médio: Faturamento Total / Frequência.
	- Diversidade de Categorias: Quantidade de categorias distintas (category_id) que o cliente comprou.
	- Filtro de Elite: Apenas clientes que compraram produtos de 13 ou mais categorias distintas devem ser considerados no ranking.
	- Desempate: Em caso de empate no Ticket Médio, utilize o customer_id em ordem crescente. 
	- Filtre os 10 clientes com o maior Ticket Médio que atendam ao critério de diversidade (13 ou + categorias).
	- Para este grupo específico de 10 clientes, identifique qual categoria de produto concentra a maior quantidade total de itens comprados (sum(quantity)).*/

WITH diversidade_cliente AS (
    -- Ediversidade de categorias únicas por cliente (apenas pedidos pagos)
    SELECT 
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
    INNER JOIN products p ON p.id = pv.product_id
    WHERE o.status = 'paid'
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT p.category_id) >= 13
),
clientes_elite AS (
    -- dados exatos de faturamento e frequência direto da tabela orders
    SELECT 
        o.customer_id,
        COUNT(DISTINCT o.id) AS frequencia,
        SUM(o.total) AS faturamento_total,
        ROUND((SUM(o.total)::numeric / COUNT(DISTINCT o.id)), 2) AS ticket_medio,
        dc.diversidade_categorias
    FROM orders o
    INNER JOIN diversidade_cliente dc ON o.customer_id = dc.customer_id
    WHERE o.status = 'paid'
    GROUP BY 
        o.customer_id, 
        dc.diversidade_categorias
    ORDER BY 
        ticket_medio DESC, 
        o.customer_id ASC
    LIMIT 10
)
-- identifica a categoria com maior volume de itens (sum(quantity)) dos melhores clientes
SELECT 
    p.category_id,
    cat.name AS nome_categoria,
    SUM(oi.quantity) AS total_itens_comprados
FROM clientes_elite ce
INNER JOIN orders o ON ce.customer_id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN product_variants pv ON oi.product_variant_id = pv.id
INNER JOIN products p ON p.id = pv.product_id
INNER JOIN categories cat ON cat.id = p.category_id
WHERE o.status = 'paid'
GROUP BY 
    p.category_id, 
    cat.name
ORDER BY 
    total_itens_comprados DESC
LIMIT 1;
