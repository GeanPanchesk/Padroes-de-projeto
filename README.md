# Padroes-de-projeto
1° – Singleton (Gerenciador de Catálogo de Filmes)
-------------------------------------------------------
class SingletonMeta(type):
    """
    Metaclasse responsável por garantir que uma classe tenha apenas
    uma instância durante todo o ciclo de vida da aplicação.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CatalogoFilmes(metaclass=SingletonMeta):
    """
    Representa o catálogo de filmes do site de aluguel.
    Deve existir apenas uma instância.
    """

    def __init__(self):
        # Carregaria de um banco de dados na vida real
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
    # Cliente utilizando o singleton

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
-------------------------------------------------------
Diagrama: 

classDiagram
    class SingletonMeta {
        -instances
        +__call__()
    }

    class CatalogoFilmes {
        -filmes
        +adicionar_filme()
        +listar_filmes()
        +buscar_filme()
    }

    SingletonMeta <|-- CatalogoFilmes

Esse código usa o padrão Singleton para garantir que o catálogo de filmes exista em uma única instância em toda a aplicação.
Com isso, qualquer parte do sistema que acesse o catálogo verá sempre os mesmos filmes, evitando duplicação e inconsistência. Ele representa bem algo centralizado, como o catálogo principal de um site de aluguel.

2° – Adapter (Integração com Serviço Externo de Filmes)
-------------------------------------------------------
class CatalogoTarget:
    """
    Interface esperada pelo sistema de aluguel de filmes.
    O cliente entende que buscar_filme() deve retornar um dicionário padronizado.
    """

    def buscar_filme(self, titulo: str) -> dict:
        return {"titulo": titulo, "status": "Filme encontrado no catálogo interno"}


class ServicoExternoAdaptee:
    """
    Serviço externo de filmes, com uma interface incompatível.
    Ele retorna o título do filme invertido (simulando formato estranho).
    """

    def buscar_especifico(self, titulo: str) -> str:
        return titulo[::-1]  # Devolve o título invertido


class FilmeAdapter(CatalogoTarget):
    """
    Adapter: transforma a resposta estranha do serviço externo
    em algo que o sistema entende (um dicionário padrão).
    """

    def __init__(self, adaptee: ServicoExternoAdaptee):
        self.adaptee = adaptee

    def buscar_filme(self, titulo: str) -> dict:
        titulo_invertido = self.adaptee.buscar_especifico(titulo)
        titulo_normal = titulo_invertido[::-1]  # Corrige de volta

        return {
            "titulo": titulo_normal,
            "status": "Filme encontrado usando serviço externo (via Adapter)"
        }


def client_code(target: CatalogoTarget):
    """
    Código cliente, que só entende a interface CatalogoTarget.
    """
    resultado = target.buscar_filme("Matrix")
    print(resultado)


if __name__ == "__main__":
    print("Cliente: Usando catálogo interno:")
    catalogo = CatalogoTarget()
    client_code(catalogo)

    print("\nCliente: Serviço externo tem formato estranho:")
    externo = ServicoExternoAdaptee()
    print("Retorno bruto do serviço externo:", externo.buscar_especifico("Matrix"))

    print("\nCliente: Agora consigo usá-lo por meio do Adapter:")
    adapter = FilmeAdapter(externo)
    client_code(adapter)
-------------------------------------------------------
Diagrama:

classDiagram
    class CatalogoTarget {
        +buscar_filme(titulo)
    }

    class ServicoExternoAdaptee {
        +buscar_especifico(titulo)
    }

    class FilmeAdapter {
        -adaptee
        +buscar_filme(titulo)
    }

    CatalogoTarget <|-- FilmeAdapter
    FilmeAdapter --> ServicoExternoAdaptee


Esse código demonstra o padrão Adapter, adaptando um serviço externo que retorna dados em um formato incompatível com o sistema.
O Adapter converte a resposta estranha (título invertido) para o formato padrão usado internamente. Assim, o sistema consegue usar serviços externos sem precisar ser modificado.

3° – Observer (Notificações ao Adicionar Filmes)
-------------------------------------------------------
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


# ========== SUBJECT ==========

class CatalogoFilmes(ABC):
    """
    Interface do Subject. Gerencia os observadores.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class Catalogo(CatalogoFilmes):
    """
    O catálogo mantém uma lista de filmes e notifica os observadores
    quando um novo filme é adicionado.
    """

    def __init__(self):
        self._filmes = []
        self._observers: List[Observer] = []
        self._ultimo_filme_adicionado = None

    def attach(self, observer: Observer) -> None:
        print("Catalogo: Observer registrado.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        print("Catalogo: Observer removido.")
        self._observers.remove(observer)

    def notify(self) -> None:
        print("Catalogo: Notificando serviços...")
        for observer in self._observers:
            observer.update(self)

    def adicionar_filme(self, titulo: str) -> None:
        print(f"\nCatalogo: Adicionando filme '{titulo}'...")
        self._filmes.append(titulo)
        self._ultimo_filme_adicionado = titulo
        self.notify()

    @property
    def ultimo_filme(self):
        return self._ultimo_filme_adicionado


# ========== OBSERVERS ==========

class Observer(ABC):
    """
    Interface dos observadores que reagem a mudanças no catálogo.
    """

    @abstractmethod
    def update(self, subject: CatalogoFilmes) -> None:
        pass


class EmailNotifier(Observer):
    """
    Envia e-mail avisando que um novo filme foi adicionado.
    """

    def update(self, subject: Catalogo) -> None:
        print(f"EmailNotifier: Enviando e-mail sobre '{subject.ultimo_filme}'...")


class LoggerServico(Observer):
    """
    Faz o log do evento de adição de filme.
    """

    def update(self, subject: Catalogo) -> None:
        print(f"LoggerServico: Log registrado -> novo filme: '{subject.ultimo_filme}'.")


class Recomendador(Observer):
    """
    Atualiza recomendações após um novo título ser adicionado.
    """

    def update(self, subject: Catalogo) -> None:
        print(f"Recomendador: Recalculando recomendações incluindo '{subject.ultimo_filme}'...")


# ========== CLIENTE ==========

if __name__ == "__main__":
    catalogo = Catalogo()

    email = EmailNotifier()
    log = LoggerServico()
    rec = Recomendador()

    catalogo.attach(email)
    catalogo.attach(log)
    catalogo.attach(rec)

    catalogo.adicionar_filme("Matrix")
    catalogo.adicionar_filme("Interestelar")

    catalogo.detach(log)

    catalogo.adicionar_filme("O Senhor dos Anéis")
-------------------------------------------------------
Diagrama:

classDiagram
    class CatalogoFilmes {
        <<interface>>
        +attach(observer)
        +detach(observer)
        +notify()
    }

    class Catalogo {
        -filmes
        -observers
        -ultimo_filme_adicionado
        +adicionar_filme(titulo)
        +notify()
        +attach()
        +detach()
        +ultimo_filme
    }

    class Observer {
        <<interface>>
        +update(subject)
    }

    class EmailNotifier {
        +update(subject)
    }

    class LoggerServico {
        +update(subject)
    }

    class Recomendador {
        +update(subject)
    }

    CatalogoFilmes <|-- Catalogo
    Observer <|-- EmailNotifier
    Observer <|-- LoggerServico
    Observer <|-- Recomendador

    Catalogo --> Observer : "notifica"

Esse código aplica o padrão Observer no catálogo de filmes.
Sempre que um filme é adicionado, vários serviços (e-mail, recomendador, logger etc.) são automaticamente notificados.
Isso permite que novos módulos reajam a eventos do sistema sem alterar o código central do catálogo, garantindo baixo acoplamento e escalabilidade.
-----------------------------------------------------------------------------------------------------
*Este arquivo usa como base os padrões apresentados pelo refactoring.guru
*Também conta com o auxílio da LLM Chatgpt
