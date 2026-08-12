import csv
from datetime import datetime
from pathlib import Path


def tipo_postgres(valor: str) -> str:
    # Infere o tipo do Postgres
    
    valor = valor.strip()

    if not valor:
        return "UNKNOWN"

    # 1 - Checa Inteiro
    try:
        int(valor)
        return "INTEGER"
    except ValueError:
        pass

    # 2 - Checa Decimal/Float
    try:
        float(valor.replace(",", "."))
        return "NUMERIC"
    except ValueError:
        pass

    # 3 -  Checa Timestamp/Data
    formatos_data = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ]
    for fmt in formatos_data:
        try:
            datetime.strptime(valor, fmt)
            return (
                "TIMESTAMP" if (" " in valor or "T" in valor) else "DATE"
            )
        except ValueError:
            pass

    # 4 - Checa Boolean
    if valor.lower() in ("true", "false", "t", "f", "1", "0"):
        return "BOOLEAN"

    # Padrão
    return "VARCHAR"


def csv_para_schema_postgres(
    diretorio_csv: str, arquivo_saida_sql: str
) -> None:
    pasta = Path(diretorio_csv)
    comandos_sql = []

    prioridade = {
        "UNKNOWN": 0,
        "BOOLEAN": 1,
        "INTEGER": 2,
        "NUMERIC": 3,
        "DATE": 4,
        "TIMESTAMP": 5,
        "VARCHAR": 6,
    }

    for caminho_csv in pasta.glob("*.csv"):
        nome_tabela = caminho_csv.stem

        with open(caminho_csv, mode="r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            cabecalho = next(leitor, None)

            if not cabecalho:
                continue

            colunas = cabecalho
            tipos_colunas = {col: "UNKNOWN" for col in colunas}

            for i, linha in enumerate(leitor):
                if i >= 100:  # Checa as primeiras 100 linhas
                    break

                for col_nome, valor in zip(colunas, linha):
                    tipo_detectado = tipo_postgres(valor)

                    if (
                        prioridade[tipo_detectado]
                        > prioridade[tipos_colunas[col_nome]]
                    ):
                        tipos_colunas[col_nome] = tipo_detectado

            # Monta o DDL
            ddl = f"DROP TABLE IF EXISTS {nome_tabela} CASCADE;\n"
            ddl += f"CREATE TABLE {nome_tabela} (\n"

            definicoes_colunas = []
            for col_nome in colunas:
                tipo_final = tipos_colunas[col_nome]
                if tipo_final == "UNKNOWN":
                    tipo_final = "VARCHAR"

                definicoes_colunas.append(f"    {col_nome} {tipo_final}")

            ddl += ",\n".join(definicoes_colunas)
            ddl += "\n);\n"

            comandos_sql.append(ddl)

    with open(arquivo_saida_sql, mode="w", encoding="utf-8") as f_out:
        f_out.write("\n".join(comandos_sql))

    print(f"Schema gerado com sucesso em: {arquivo_saida_sql}")


csv_para_schema_postgres("raw_data", "schema.sql")