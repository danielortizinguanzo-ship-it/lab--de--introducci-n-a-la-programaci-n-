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
        numero=int(input("ingresa un numero "))
        if numero >0:
            print("el numero es poditivo")
        elif numero <0:
            print("el numero es negativo")
        else:
            print("el numero es cero")
        if numero % 2==0:
            print("el numero es par")
        else:
            print("el numero es impar")
    elif opcion == "2":
        print("Has seleccionado categoria de edad y permisos")
        edad=int(input("ingresa tu edad(0 a 120) "))
        if (edad <0 or edad >120):
            print("no pudedes ingresar esa edad")
            continue
        
        ide =str(input("cuenta con identificacion? (s/n)? "))
        if not (ide=="s" or ide=="n"):
                    print("solo puedes ingresar s o n")
                    continue
        lic=str(input("cuenta con licencia de conducir? (s/n)? "))
        if not (ide=="s" or ide=="n"):
                    print("solo puedes ingresar s o n")
                    continue
        if (edad>0 and edad<=12):
            print(f"tu edad es {edad} y eres un niño, nesesitas tutor")
            print("nesesitas ide y mas de 21 para el servisio vip")
            if (lic=="s"):
                print("puedes conducir")
            else:                    
                print("no puedes conducir")
        
        if (edad>12 and edad<=17):
            print(f"tu edad es {edad} eres un dadolescente pudes registrarte con un tutor  tutor")
            print("nesesitas ide y mas de 21 para el servisio vip")
            if (lic=="s"):
                print("puedes conducir")
            else:
                print("no puedes conducir")
                
        if (edad>=18 and edad<=64):
            print(f"tu edad es {edad} eres un adulto puedes registrarte ")
            if (edad >=21):
                if(ide=="s"):
                    print("puedes acceder al servicio vip")
                else:
                    print("Nesetitas ide para un servico vip")
            if (lic=="s"):
                print("puedes conducir")
            else:
                print("no puedes conducir") 
        if (edad>65):
            print(f"tu edad es {edad} eres un adulto mayor puedes registrarte ")
            if (ide=="s"):
                print("puedes acceder al servicio vip")
            else:
                print("Nesetitas ide para un servico vip")
            if (lic=="s"):
                print("pudes conducir")
            else:
                print("no puedes conducir")
                 
        opcion2=int(input("deseas volver a inicir el proceso? 1.si 2.volver menu principal"))
        if opcion2 == 1:
            continue
        elif opcion2 == 2:
            break
    elif opcion == "3":
        print("Has seleccionado calcular tarifa final")
    elif opcion == "4":
        print("Has seleccionado cerrar sesion")
        Acceso = 0
    elif opcion.lower() == "5":
        print("Saliendo del programa")
    else:
        print("Opción no válida, por favor selecciona una opción del menú.")
