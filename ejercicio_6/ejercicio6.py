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

            print(f"La tarifa final es: {tarifa_final:.2f}")
