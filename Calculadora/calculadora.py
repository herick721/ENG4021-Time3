import soma
import subtrai
import multiplica
import divisao


def main():
    print("=== Calculadora ===")
    
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    operador = input("Digite o operador (+, -, *, /): ").strip()

    if operador == "+":
        resultado = soma.somaf(n1, n2)
    elif operador == "-":
        resultado = subtrai.subtraif(n1, n2)
    elif operador == "*":
        resultado = multiplica.multiplicaf(n1, n2)
    elif operador == "/":
        try:
            resultado = divisao.dividef(n1, n2)
        except ValueError as e:
            print(e)
            return
    else:
        print("Operador inválido. Use +, -, * ou /.")
        return

    print(f"Resultado: {n1} {operador} {n2} = {resultado}")


if __name__ == "__main__":
    main()


