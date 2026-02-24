# Explicación del Código -- Kiosco con Control de Acceso

Este programa funciona como un sistema de inicio de sesión con un máximo
de 3 intentos.

## 1) Variable intentos

Se inicializa en 0 y sirve para contar cuántas veces el usuario falla al
ingresar las credenciales.

## 2) Ciclo while

El ciclo se ejecuta mientras `intentos` sea menor que 3. Esto permite un
máximo de tres intentos.

## 3) Entrada de datos

Se solicita al usuario que ingrese su nombre de usuario y contraseña
usando `input()`.

## 4) Variable valido

Se utiliza como bandera lógica (True o False). Si alguna validación
falla, se cambia a False.

## 5) Validaciones del usuario

-   No debe estar vacío.
-   Debe ser alfanumérico (solo letras y números, sin espacios).

## 6) Validaciones de la contraseña

-   Debe tener al menos 8 caracteres.
-   Debe contener al menos una letra.
-   Debe contener al menos un número.

## 7) Verificación de credenciales

Si todas las validaciones son correctas, se comparan con: - Usuario:
`admin` - Contraseña: `Admin2026`

Si coinciden → Acceso concedido.\
Si no coinciden → Se incrementa el contador de intentos.

## 8) Límite de intentos

Si el usuario falla 3 veces, el programa muestra un mensaje indicando
que se alcanzó el máximo de intentos y termina.

------------------------------------------------------------------------

### Resumen

El programa controla acceso validando formato de datos y limitando el
número de intentos para mayor seguridad.
