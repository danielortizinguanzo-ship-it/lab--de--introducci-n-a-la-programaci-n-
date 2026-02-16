def decimal_a_binario(numero):
    if numero == 0:
        return "0"
    binario = ""
    while numero > 0:
        residuo = numero % 2
        binario = str(residuo) + binario
        numero = numero // 2
    return binario


def decimal_a_octal(numero):
    if numero == 0:
        return "0"
    octal = ""
    while numero > 0:
        residuo = numero % 8
        octal = str(residuo) + octal
        numero = numero // 8
    return octal


def decimal_a_hexadecimal(numero):
    if numero == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    while numero > 0:
        residuo = numero % 16
        hexadecimal = hex_chars[residuo] + hexadecimal
        numero = numero // 16
    return hexadecimal

numero = int(input("Ingresa un número entero: "))

print("Binario:", decimal_a_binario(numero))
print("Octal:", decimal_a_octal(numero))
print("Hexadecimal:", decimal_a_hexadecimal(numero))
