# Explicación del Código: Lector de QR

Yo realicé este programa utilizando la librería **Streamlit** para crear una página web interactiva en la que se puede usar la cámara del dispositivo y detectar códigos QR.

## Importación de librerías

Primero importé las librerías necesarias:

* **Streamlit** para la interfaz gráfica
* **OpenCV (cv2)** para el procesamiento de imágenes y detección del código QR
* **NumPy** para convertir la imagen a un formato adecuado
* **PIL** para abrir la imagen capturada

## Título de la aplicación

Después coloqué un título en la aplicación utilizando la función `st.title`, con el fin de que el usuario identifique fácilmente la función del programa.

## Uso de la cámara

Posteriormente utilicé la función `st.camera_input` para activar la cámara del dispositivo, permitiendo al usuario tomar una fotografía. Esta imagen se guarda en una variable llamada `img_file`.

## Validación de la imagen

Luego implementé una condición con `if img_file is not None` para verificar si el usuario ya tomó una foto, ya que sin una imagen no se puede continuar con el proceso.

## Procesamiento de la imagen

Una vez que se tiene la imagen:

* La abrí con **PIL** usando `Image.open`
* La convertí a un arreglo de **NumPy**, porque OpenCV trabaja con matrices de píxeles

## Detección del código QR

Después creé un detector de códigos QR utilizando la función `cv2.QRCodeDetector()`. Este objeto se encarga de analizar la imagen.

A continuación utilicé el método `detectAndDecode`, el cual detecta y decodifica el código QR en la imagen. Este método devuelve tres valores, donde el más importante es `data`, que contiene la información del código QR.

## Resultado

Finalmente, agregué una condición para verificar si se detectó un código:

* Si `data` contiene información, se muestra un mensaje de éxito con `st.success` indicando el contenido del QR.
* En caso contrario, se muestra un mensaje de advertencia con `st.warning` indicando que no se detectó ningún código.

## Conclusión

En conclusión, este programa permite capturar una imagen desde la cámara, procesarla y detectar si contiene un código QR, mostrando su contenido en pantalla.
