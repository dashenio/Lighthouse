class User:
    def __init__(self, name, age, password):
        # Atributos públicos
        self.name = name
        self.age = age
        # Atributo "privado" (convenção com dois underlines)
        self.__password = password 
        
    # Princípio de Organização: Separação de funções. 
    # Cada método faz apenas uma coisa.
    def exibir_perfil(self):
        """Exibe as informações públicas do usuário."""
        print(f"Perfil -> Nome: {self.name} | Idade: {self.age}")
        
    def verificar_senha(self, tentativa_senha):
        """Lógica de segurança encapsulada dentro da classe."""
        if tentativa_senha == self.__password:
            return "✅ Acesso liberado!"
        else:
            return "❌ Senha incorreta!"

# 1. Instanciando objetos baseados na nossa Classe (Molde)
professor = User("Duarte Junior", 27, "senha_super_secreta")
aluno = User("João Silva", 20, "123456")

print("--- Sistema de Usuários Orientado a Objetos ---")
# 2. Chamando os métodos (ações) dos objetos
professor.exibir_perfil()
aluno.exibir_perfil()

print("\n--- Testando Encapsulamento (Segurança) ---")
# 3. O usuário de fora não consegue ver self.__password diretamente facilmente
print("Tentativa de login do João:")
print(aluno.verificar_senha("senha_errada"))
print(aluno.verificar_senha("123456"))