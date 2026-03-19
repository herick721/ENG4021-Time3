def multiplicaf(n1: float, n2: float) -> float:
    '''
    Função que retorna a multiplicação de dois números (inteiros ou reais).

    :param n1: número 1 (int ou float)
    :param n2: número 2 (int ou float)
    :return: multiplicação de n1 * n2 (float)

    Exemplo:
    >>> multiplicaf(2, 3)
    6
    >>> multiplicaf(2.5, 4.0)
    10.0
    '''
    return n1 * n2


def main():
    assert multiplicaf(2, 3) == 6, "Erro: 2 * 3 deveria ser 6"
    assert multiplicaf(2.5, 4.0) == 10.0, "Erro: 2.5 * 4.0 deveria ser 10.0"
    assert multiplicaf(-2, 3) == -6, "Erro: -2 * 3 deveria ser -6"
    assert multiplicaf(0, 5) == 0, "Erro: 0 * 5 deveria ser 0"
    assert multiplicaf(5, 0) == 0, "Erro: 5 * 0 deveria ser 0"
    assert multiplicaf(1.5, 1.5) == 2.25, "Erro: 1.5 * 1.5 deveria ser 2.25"
    print("Todos os testes passaram com sucesso!")


if __name__ == "__main__":
    main()