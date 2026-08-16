import pandas as pd
from pathlib import Path
import sqlalchemy as al

def carregar_dados(diretorio_csv): # argumento é a string do caminho

    # Conexão com o Postgres
    # É preciso criar o banco de dados antes
    engine = al.create_engine('postgresql://postgres:root@localhost:5432/lh_nautical')

    schema_path = Path("schema.sql")
    sql_script = schema_path.read_text(encoding='utf-8')

    # Divide o arquivo em comandos individuais
    comandos = [comando.strip() for comando in sql_script.split(";") if comando.strip()]

   # Executa cada comando DDL dentro de uma transação
    with engine.begin() as connection:
        for comando in comandos:
            connection.execute(al.text(comando))

    # Carregamento dos arquivos CSV em chunks
    pasta = Path(diretorio_csv)

    for caminho_csv in pasta.glob("*.csv"):
         nome_tabela = caminho_csv.stem

        # pd.read_csv com chunksize, trabalha com pedaços em vez de tentar inserir tudo de uma vez
         for chunk in pd.read_csv(caminho_csv, chunksize=10000, dtype=str):
             chunk.to_sql(
                name=nome_tabela,      
                con=engine,
                if_exists='append',    
                index=False
             )
    print('Arquivos carregados com sucesso.')

carregar_dados('raw_data')
