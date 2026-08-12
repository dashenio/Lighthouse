# --- Prática: Slide 38 (Debugger) ---

def calcular_media_idades(lista_idades):
    """Função com um bug intencional para ser achado no Debugger do VSCode"""
    soma = 0
    for idade in lista_idades:
        if type(idade) == str:
            idade = int(idade)
        soma += idade
    
    if not len(lista_idades):
        return 0
    
    media = soma / len(lista_idades)
    return media

# Cenário 1: Funciona perfeitamente
# idades_equipe = [25, 30, 22, 27]
# print(f"Média Cenário 1: {calcular_media_idades(idades_equipe)}")

# Cenário 2
idades_sem_ninguem = [25, 30, '22', 27]
print(f"Média Cenário 2: {calcular_media_idades(idades_sem_ninguem)}")