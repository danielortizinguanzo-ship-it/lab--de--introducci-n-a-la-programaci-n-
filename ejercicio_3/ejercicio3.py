intentos = 0

while intentos < 3:

    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    valido = True   
    if usuario == "":
        print("El usuario no debe estar vacío")
        valido = False

    elif not usuario.isalnum():
        print("El usuario debe ser alfanumérico y sin espacios")
        valido = False
    if len(contraseña) < 8:
        print("La contraseña debe tener mínimo 8 caracteres")
        valido = False

    if not any(letra.isalpha() for letra in contraseña):
        print("La contraseña debe tener al menos una letra")
        valido = False

    if not any(numero.isdigit() for numero in contraseña):
        print("La contraseña debe tener al menos un número")
        valido = False

    if valido:
        if usuario == "admin" and contraseña == "Admin2026":
            print("Acceso concedido ")
            break
        else:
            intentos += 1
            print("Credenciales incorrectas ")
            print("Te quedan", 3 - intentos, "intentos")
    else:
        print("Datos inválidos, intenta nuevamente\n")


if intentos == 3:
    print("Se alcanzó el máximo de intentos. Programa finalizado.")
