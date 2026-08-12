import math       # Módulo para operações matemáticas
import os         # Módulo para interagir com o sistema operacional
from datetime import datetime # Importando uma parte específica de um módulo

print("--- Explorando Módulos Nativos ---")

# Usando o módulo math
raiz = math.sqrt(25)
print(f"A raiz quadrada de 25 é: {raiz}")

# Usando o datetime
agora = datetime.now()
print(f"Data e hora atuais: {agora.strftime('%d/%m/%Y %H:%M:%S')}")

# Usando o os (Exemplo: Qual é a pasta atual em que este código está rodando?)
pasta_atual = os.getcwd()
print(f"Diretório atual de trabalho: {pasta_atual}")