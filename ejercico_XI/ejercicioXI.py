import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("📷 Lector de QR y Código de Barras")

img_file = st.camera_input("Toma una foto")

if img_file is not None:
    image = Image.open(img_file)
    img = np.array(image)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if data:
        st.success(f"QR detectado: {data}")
    else:
        st.warning("No se detectó ningún QR")
