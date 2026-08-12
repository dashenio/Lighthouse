class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def exibir_info(self):
        # Usando a lógica que já aprendemos dentro da classe
        status = "Adulto" if self.age >= 18 else "Menor"
        print(f"Usuário: {self.name} | Idade: {self.age} | Status: {status}")

# Instanciando os objetos na memória
user1 = User("Duarte Junior", 27)
user2 = User("Ana Silva", 16)

# Chamando os métodos
print("\n--- Sistema de Usuários (Classes) ---")
user1.exibir_info()
user2.exibir_info()