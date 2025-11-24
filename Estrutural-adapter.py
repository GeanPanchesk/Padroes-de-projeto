"""
Meu sistema trabalha com um serviço interno que consulta filmes em um formato padrão (ex.: dicionários Python).
Mas quero integrar um serviço externo de filmes que devolve os dados em outro formato (ex.: string invertida, JSON estranho, API antiga etc).

O Adapter converte a interface do serviço externo para a interface interna do sistema.
"""
class CatalogoTarget:

    def buscar_filme(self, titulo: str) -> dict:
        return {"titulo": titulo, "status": "Filme encontrado no catálogo interno"}


class ServicoExternoAdaptee:


    def buscar_especifico(self, titulo: str) -> str:
        return titulo[::-1]  # Devolve o título invertido


class FilmeAdapter(CatalogoTarget):

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