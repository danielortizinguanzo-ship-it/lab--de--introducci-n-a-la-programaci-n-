# Cómo crear un entorno virtual en Python (venv)

Este documento explica **paso a paso** cómo crear y usar un entorno virtual en Python usando `venv`. Está pensado para tareas escolares y proyectos básicos.

---

## ¿Qué es un entorno virtual?

Un **entorno virtual** es un espacio aislado donde puedes instalar librerías de Python sin afectar a otros proyectos ni al Python del sistema.

Ejemplo:

* Proyecto A usa `numpy 1.26`
* Proyecto B usa `numpy 1.22`

👉 Con entornos virtuales, **no hay conflictos**.

---

## Requisitos previos

* Tener **Python 3.8 o superior** instalado
* Tener acceso a la **terminal** o **símbolo del sistema**

Para comprobar Python:

```bash
python --version
```

---

## Paso 1: Crear la carpeta del proyecto

Primero, crea una carpeta para tu proyecto:

```bash
mkdir mi_proyecto
cd mi_proyecto
```

---

## Paso 2: Crear el entorno virtual

Ejecuta el siguiente comando:

### En Windows

```bash
python -m venv env
```

### En macOS o Linux

```bash
python3 -m venv env
```

Esto creará una carpeta llamada `env` con el entorno virtual.

---

## Paso 3: Activar el entorno virtual

### Windows (CMD o PowerShell)

```bash
env\Scripts\activate
```

### macOS / Linux

```bash
source env/bin/activate
```

Cuando esté activo, verás algo así:

```text
(env) C:\mi_proyecto>
```

---

## Paso 4: Instalar librerías dentro del entorno

Ya con el entorno activado, puedes instalar paquetes:

```bash
pip install nombre_del_paquete
```

Ejemplo:

```bash
pip install numpy
```

---

## Paso 5: Ver librerías instaladas

```bash
pip list
```

---

## Paso 6: Desactivar el entorno virtual

Cuando termines de trabajar:

```bash
deactivate
```

---

## Estructura final del proyecto

```text
mi_proyecto/
│── env/
│── main.py
```

---

## Recomendaciones

* ❌ No subas la carpeta `env` a GitHub
* ✔️ Usa un archivo `requirements.txt`

Para crearlo:

```bash
pip freeze > requirements.txt
```

Para instalar dependencias desde el archivo:

```bash
pip install -r requirements.txt
```

---

## Conclusión

El uso de entornos virtuales es una **buena práctica** en Python porque mantiene tus proyectos ordenados, evita errores y facilita el trabajo en equipo.

---

✍️ Documento en formato **Markdown (.md)** listo para entregar o subir a GitHub.
