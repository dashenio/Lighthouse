import pandas as pd
from pathlib import Path
import sqlalchemy as al
import time


def carregar_dados(diretorio_csv):

    # Conexão com o Postgres
    engine = al.create_engine('postgresql://postgres:root@localhost:5432/lh_nautical')

    schema_path = Path("schema.sql")
    sql_script = schema_path.read_text(encoding='utf-8')

    # Divide o arquivo em comandos individuais
    comandos = [comando.strip() for comando in sql_script.split(";") if comando.strip()]

   # Executa cada instrução DDL dentro de uma transação
    with engine.begin() as connection:
        for comando in comandos:
            connection.execute(al.text(comando))

    # Carregamento dos arquivos CSV em blocos (chunks)
    pasta = Path(diretorio_csv)

    for caminho_csv in pasta.glob("*.csv"):
         nome_tabela = caminho_csv.stem

        # pd.read_csv com chunksize retorna um iterador em vez de carregar tudo na RAM
         for chunk in pd.read_csv(caminho_csv, chunksize=10000, dtype=str):
             chunk.to_sql(
                 name=nome_tabela,      # Nome da tabela no PostgreSQL
                con=engine,
                 if_exists='append',    # Insere nas tabelas já criadas pelo schema.sql
                index=False
             )
    print('Arquivos carregados com sucesso.')
inicio = time.time()
carregar_dados('raw_data')
fim = time.time()
resultado = fim - inicio
print(f'Tempo de execução = {round(resultado,2)}s')