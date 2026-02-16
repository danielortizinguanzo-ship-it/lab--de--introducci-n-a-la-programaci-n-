# Calculadora de Conversión de Decimal a Binario, Octal y Hexadecimal

Este documento explica **paso a paso** cómo funciona el siguiente programa en Python. El código convierte un número decimal a:

* Binario (base 2)
* Octal (base 8)
* Hexadecimal (base 16)

---

## Código Completo

```python
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
```

---

# Explicación Paso a Paso

## 1️⃣ Función decimal_a_binario(numero)

Convierte un número decimal a **binario (base 2)**.

### ¿Cómo funciona?

1. Si el número es 0, regresa "0".
2. Crea una variable vacía llamada `binario`.
3. Mientras el número sea mayor que 0:

   * Obtiene el residuo al dividir entre 2 (`numero % 2`).
   * Agrega el residuo al inicio del resultado.
   * Divide el número entre 2 usando división entera (`//`).
4. Devuelve el número convertido.

👉 Se usa el método de **divisiones sucesivas**.

---

## 2️⃣ Función decimal_a_octal(numero)

Convierte un número decimal a **octal (base 8)**.

La lógica es exactamente la misma que la anterior, pero:

* Se divide entre 8
* Se usa `numero % 8`

Esto genera el número en base 8.

---

## 3️⃣ Función decimal_a_hexadecimal(numero)

Convierte un número decimal a **hexadecimal (base 16)**.

Aquí cambia algo importante:

```python
hex_chars = "0123456789ABCDEF"
```

En hexadecimal existen letras:

| Decimal | Hexadecimal |
| ------- | ----------- |
| 10      | A           |
| 11      | B           |
| 12      | C           |
| 13      | D           |
| 14      | E           |
| 15      | F           |

Por eso usamos esa cadena para poder obtener la letra correcta usando:

```python
hex_chars[residuo]
```

---

## 4️⃣ Parte Principal del Programa

```python
numero = int(input("Ingresa un número entero: "))
```

* Pide un número al usuario
* Lo convierte a entero

Después imprime los resultados:

```python
print("Binario:", decimal_a_binario(numero))
print("Octal:", decimal_a_octal(numero))
print("Hexadecimal:", decimal_a_hexadecimal(numero))
```

---

# Ejemplo de Ejecución

Si el usuario ingresa:

```
10
```

El resultado será:

```
Binario: 1010
Octal: 12
Hexadecimal: A
```

---

# Estructura del Método Usado

Todos usan el mismo procedimiento:

1. Dividir entre la base
2. Guardar el residuo
3. Repetir hasta que el número sea 0
4. Leer los residuos de atrás hacia adelante

---

# Conclusión

Este programa demuestra cómo convertir números sin usar:

* `bin()`
* `oct()`
* `hex()`

Usa únicamente lógica matemática y ciclos `while`, lo cual es ideal para aprender cómo funcionan realmente las bases numéricas.

---

📘 Documento listo en formato **Markdown (.md)** para tarea o GitHub.
