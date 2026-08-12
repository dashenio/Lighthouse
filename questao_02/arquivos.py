from pathlib import Path
import json


def read_file():

    # abrir
    file = open('raw_data/orders.csv', 'r')

    # ler
    # content = file.read()
    # print(content)

    ################
    # loopa pelas linhas
    # lines = file.readlines()
    # for line in lines:
    #     print(line)

    # fechar
    file.close()

    return

letras = ['A','B', 'C','D', 'E', 'F']

def write_to_file(filename):
    file = open(filename, 'w+') # com o + pode ler o arquivo tbm
    for l in letras:
        file.write('Letra ' + l + '\n')

    file.seek(0,0) # coloca o cursor de volta no início do arquivo

    content = file.read()
    print(content)
    file.close()
    return

def append_to_file(filename): 
    file = open(filename, 'a+') # escreve o texto depois do que já está
    # no arquivo em vez dde deletar e escrever de novo
    for l in letras:
        file.write('Letra ' + l + '\n')

    file.seek(0,0)
    content = file.read()
    print(content)

    file.close()
    return

#################### Pathlib Module ###########################
def create_path():
    script_dir = Path(__file__).parent
    path = script_dir / 'coisas'
    # parents=True para criar os pais se não existirem
    # exist_ok=True se a pasta já existir simplesmente não dá erro
    # e não tenta criar de novo
    path.mkdir(parents=True, exist_ok=True)

    # diz onde colocar o novo arquivo
    path = path / 'zelda.txt' 

    # cria o arquivo com 'w'
    # file = path.open('r')
    # file.write('\nSword')

    # content = file.read()
    # print(content)

    # le o conteúdo do arquivo direto pelo path object
    content = path.read_text()
    print(content)
    
    # file.close()
    
    return

#   EXCEPTIONS 

def open_file():
    path = Path(__file__).parent
    path = path / 'does' / 'not' / 'exist.txt'

    try:
        file = path.open('r')
        content = file.read()
        print(content)
        file.close()      
    except FileNotFoundError:
        print(f'The path "{path}" does not exist.')
    except Exception as e:
        print(f'Unexpect error {e}')
    print('End of function.')

    # CONTEXT MANAGERS
    
def open_file1():
    path = Path(__file__).parent / 'letras.txt'
    data = ['A','B', 'C','D', 'E', 'F']

    # context managers --> autoclose
    with path.open('w') as file:
        for l in data:
            file.write(l + '\n')

#    JSON

path = Path(__file__).parent / 'pares.json'

pares = [
    {'A': 1, 'ant': 0},
    {'B': 2, 'ant': 1}, 
    {'C': 3, 'ant': 2},
    {'D': 4, 'ant': 3}, 
    {'E': 5, 'ant': 4}, 
    {'F': 6, 'ant': 5}
    ]

def write_json():
    with path.open('w') as file:
        json.dump(pares, file, indent=2)
    return

def read_json():
    with path.open('r') as file:
        data = json.load(file)
    return data



def main():
    # write_to_file('questao_02/teste.txt')
    # append_to_file('questao_02/teste.txt')
    # create_path()
    # open_file()
    # open_file1()
    write_json()
    print(read_json())
    return
if __name__ == '__main__':
    main()