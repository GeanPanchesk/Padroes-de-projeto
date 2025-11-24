""" 
Meu site precisa de um catálogo central, carregado apenas uma vez, que todas as partes do sistema consultam.

Assim, usamos o Singleton para garantir que:

o catálogo só seja carregado uma única vez,

todas as páginas acessem a MESMA instância (mesmos filmes, sem duplicação).
"""
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CatalogoFilmes(metaclass=SingletonMeta):

    def __init__(self):
        self.filmes = []

    def adicionar_filme(self, titulo, ano):
        self.filmes.append({"titulo": titulo, "ano": ano})

    def listar_filmes(self):
        return self.filmes

    def buscar_filme(self, titulo):
        for filme in self.filmes:
            if filme["titulo"].lower() == titulo.lower():
                return filme
        return None


if __name__ == "__main__":
 #utilizando singleton no cliente
    cat1 = CatalogoFilmes()
    cat2 = CatalogoFilmes()

    cat1.adicionar_filme("O Senhor dos Anéis", 2001)
    cat1.adicionar_filme("Matrix", 1999)

    print("Filmes no catálogo:", cat2.listar_filmes())
    # cat1 e cat2 são a MESMA instância

    if id(cat1) == id(cat2):
        print("OK! CatalogoFilmes é Singleton.")
    else:
        print("Falhou: instâncias diferentes.")