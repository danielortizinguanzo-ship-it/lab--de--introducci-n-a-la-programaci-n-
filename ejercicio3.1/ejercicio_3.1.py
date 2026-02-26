while True:
 intentos = 0
 Acceso = 1
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
            Acceso = 1
            break
         
        else:
            intentos += 1
            print("Credenciales incorrectas ")
            print("Te quedan", 3 - intentos, "intentos")
    else:
        print("Datos inválidos, intenta nuevamente\n")


 if intentos == 3:
    print("Se alcanzó el máximo de intentos. Programa finalizado.")
    
 while Acceso ==1:
    print("Bienvenido.")
    print("1.clasificar numeros")
    print("2.categoria de edad y permisos")
    print("3.calcular tarifa final")
    print("4.cerrar sesion")
    print("5.salir")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        print("Has seleccionado clasificar numeros")
    elif opcion == "2":
        print("Has seleccionado categoria de edad y permisos")
    elif opcion == "3":
        print("Has seleccionado calcular tarifa final")
    elif opcion == "4":
        print("Has seleccionado cerrar sesion")
        Acceso = 0
    elif opcion.lower() == "5":
        print("Saliendo del programa")
    else:
        print("Opción no válida, por favor selecciona una opción del menú.")
