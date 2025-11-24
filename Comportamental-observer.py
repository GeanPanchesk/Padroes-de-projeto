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
    @abstractmethod
    def update(self, subject: CatalogoFilmes) -> None:
        pass


class EmailNotifier(Observer):

    def update(self, subject: Catalogo) -> None:
        print(f"EmailNotifier: Enviando e-mail sobre '{subject.ultimo_filme}'...")


class LoggerServico(Observer):

    def update(self, subject: Catalogo) -> None:
        print(f"LoggerServico: Log registrado -> novo filme: '{subject.ultimo_filme}'.")


class Recomendador(Observer):

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