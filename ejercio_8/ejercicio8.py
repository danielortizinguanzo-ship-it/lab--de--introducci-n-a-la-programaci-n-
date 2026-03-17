def palabras():
   palabrasa = input( "escribe una palbra ") 
   for i in range(10):
      print (palabrasa )

def edad():
    edad = int(input("Ingresa tu edad: "))
    for i in range(1, edad +1):
       print(i)

def enteros_positivos():
    numero = int(input("ingresa un numero entero positovo:"))
    for i in range(1, numero +1):
        if i % 2 != 0:
            print(i, end=",")

def cuenta_atras():
    numero = int(input("ingresa un numero entero que sea positivo: "))
    for i in range(numero,0 , -1):
        print(i, end=",")

def intereses ():
    capital = float(input("ingresa el capital: "))
    tasa = float(input("ingresa la tasa de interes anual (en porcentaje): "))
    años = int(input("ingresa el numero de años: "))

    for i in range(1, años + 1):
        capital += capital * (tasa / 100)
        print(f"Capital al final del año {i}: {capital:.2f}")

def triangulo():
    for i in range(1, 6):
        print("*" * i)

def tabla_multiplicar():
    for i in range(1,11):
        resultado = 1 * i 
        print(f"1 x {i} = {resultado}")

def trinagulo_de_numeros():
    numero = int(input("ingresa un numero entero positivo:"))
    for i in range(1, numero +1 ):
        for j in range(2*i -1, 0, -2):
            print(j, end="")
        print()

def contraseña():
    while True:
        contraseña = input("ingresa la contraseña: ")
        if contraseña == "el dani":
            print("contraseña correcta")
            break
        else:
            print("contraseña incorrecta, intenta de nuevo")

def numeros_primos():
    numero = int(input("ingresa un numero entero"))
    es_primo = True
    for i in range(2 ,numero):
        if numero % i == 0:
            es_primo = False
            break
    if es_primo:
        print(f"{numero} es un numero primo")
    else:
        print(f"{numero} no es un numero primo")

def palabra_separadas():
    palabra = input("ingresa una palabra:")
    for i in range(len(palabra)-1, -1, -1):
        print(palabra[i])

def frases_separadas_por_letras():
    frase = input("ingresa unaletra:")
    letra = input("ingresa una letra:")
    contador = 0
    for i in frase:
        if i == letra:
            contador = contador + 1 
    print(f"La letra '{letra}' aparece {contador} veces en la frase.")

def escrito_por_el_usuario():
    print ("ecribe algo , para salir escribe 'salir'")
    while True:
        texto = input("ingresa un texto: ")
        if texto.lower() == "salir":
            print("Programa finalizado.")
            break
        else:
            print(f"Has ingresado: {texto}")

while True: 
    print("\n menu peron")
    print("1 . rango de palabras")
    print("2 . edad")
    print("3 . enteros positivos")
    print("4 . cuenta atras")
    print("5 . intereses")
    print("6 . triangulo")
    print("7 . tabla de multiplicar")
    print("8 . triangulo de numeros")
    print("9 . contraseña")
    print("10 . numeros primos")
    print("11 . palabra separadas")
    print("12 . frases separadas por letras")
    print("13 . escrito por el usuario")
    print("14 . salir")
    opcion = int(input("selecciona una opcion: "))
    
    match opcion:
        case 1:
            palabras()
        case 2:
            edad()
        case 3:
            enteros_positivos()
        case 4:
            cuenta_atras()
        case 5:
            intereses()
        case 6:
            triangulo()
        case 7:
            tabla_multiplicar()
        case 8:
            trinagulo_de_numeros()
        case 9:
            contraseña()
        case 10:
            numeros_primos()
        case 11:
            palabra_separadas()
        case 12:
            frases_separadas_por_letras()
        case 13:
            escrito_por_el_usuario()
        case 14:
            print("Programa finalizado.")
            break
