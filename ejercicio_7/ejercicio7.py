def clasificar_numero():

    numero = input("Ingresa un número entero: ")

    if numero.lstrip("-").isdigit():

        numero = int(numero)

        if numero > 0:
            print("El número es positivo")

        elif numero < 0:
            print("El número es negativo")

        else:
            print("El número es cero")

        if numero % 2 == 0:
            print("El número es par")

        else:
            print("El número es impar")

    else:
        print("Debes ingresar un número entero")


def categoria_edad():

    print("Categoría de edad y permisos")

    edad = int(input("Ingresa tu edad (0 a 120): "))

    if edad < 0 or edad > 120:
        print("Edad no válida")
        return

    ide = input("¿Cuenta con identificación? (s/n): ").lower()
    lic = input("¿Cuenta con licencia de conducir? (s/n): ").lower()

    if edad <= 12:
        print("Eres un niño")
        print("Necesitas tutor")

    elif edad <= 17:
        print("Eres adolescente")

    elif edad <= 64:
        print("Eres adulto")

        if edad >= 21 and ide == "s":
            print("Puedes acceder al servicio VIP")

    else:
        print("Eres adulto mayor")

        if ide == "s":
            print("Puedes acceder al servicio VIP")

    if lic == "s":
        print("Puedes conducir")

    else:
        print("No puedes conducir")


def calcular_tarifa():

    print("Calcular tarifa final")

    tarifa_base = 200

    edad = int(input("Ingresa tu edad (0 a 120): "))
    dia = int(input("Día de la semana (1=lunes ...7=domingo): "))
    estudiante = input("¿Eres estudiante? (s/n): ").lower()
    miembro = input("¿Eres miembro? (s/n): ").lower()
    metodo = input("Método de pago E(efectivo) T(tarjeta): ").lower()

    descuento = 0
    recargo = 0

    if dia == 6 or dia == 7:
        recargo = 0.10

    if edad <= 12:
        descuento += 0.50

    elif edad <= 17:
        descuento += 0.20

    elif edad >= 65:
        descuento += 0.30

    if estudiante == "s" and edad >= 13:
        descuento += 0.15

    if miembro == "s":
        descuento += 0.10

    if metodo == "e":
        descuento += 0.05

    if descuento > 0.60:
        descuento = 0.60

    tarifa_final = tarifa_base * (1 - descuento) * (1 + recargo)

    print("Tarifa final:", round(tarifa_final,2))


# LOGIN
intentos = 0

while intentos < 3:

    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    if usuario == "":
        print("El usuario no puede estar vacío")
        intentos += 1
        continue

    if not usuario.isalnum():
        print("El usuario debe ser alfanumérico")
        intentos += 1
        continue

    if len(contraseña) < 8:
        print("La contraseña debe tener mínimo 8 caracteres")
        intentos += 1
        continue

    if not any(letra.isalpha() for letra in contraseña):
        print("La contraseña debe tener una letra")
        intentos += 1
        continue

    if not any(numero.isdigit() for numero in contraseña):
        print("La contraseña debe tener un número")
        intentos += 1
        continue

    if usuario == "admin" and contraseña == "Admin2026":

        print("Acceso concedido")

        acceso = 1

        while acceso == 1:

            print("\nMENÚ")
            print("1. Clasificar números")
            print("2. Categoría de edad y permisos")
            print("3. Calcular tarifa final")
            print("4. Cerrar sesión")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")

            match opcion:

                case "1":
                    clasificar_numero()

                case "2":
                    categoria_edad()

                case "3":
                    calcular_tarifa()

                case "4":
                    print("Sesión cerrada")
                    acceso = 0

                case "5":
                    print("Saliendo del sistema")
                    intentos = 4
                    break

                case _:
                    print("Opción no válida")

        break

    else:
        print("Credenciales incorrectas")
        intentos += 1


if intentos == 3:
    print("Se alcanzó el máximo de intentos")

elif intentos == 4:
    print("Programa finalizado")
