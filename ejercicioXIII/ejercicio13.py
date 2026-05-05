"""
Captura de Productos por Código de Barras
==========================================
Sin pyzbar — usa solo OpenCV (QRCodeDetector + BarcodeDetector).
El código escaneado se inyecta automáticamente en el formulario.

Instalar:
    pip install streamlit opencv-python-headless pillow pandas openpyxl numpy

Ejecutar:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import io

# ─── Página ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Captura de Productos",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main .block-container { padding: 1.5rem 1rem 2rem; max-width: 700px; }
.app-header { text-align:center; padding:1rem 0 .4rem; margin-bottom:1.2rem; }
.app-header h1 { font-size:1.6rem; font-weight:700; color:#1e293b; margin:0; }
.app-header p  { color:#64748b; font-size:.88rem; margin:4px 0 0; }
.barcode-badge {
    display:inline-flex; align-items:center; gap:8px;
    background:#eff6ff; border:1px solid #bfdbfe;
    color:#2563eb; font-size:1rem; font-weight:700;
    border-radius:8px; padding:10px 16px; margin:8px 0 4px;
    word-break:break-all; width:100%; box-sizing:border-box;
}
.alert-ok  { background:#f0fdf4; border:1px solid #bbf7d0;
             border-left:4px solid #16a34a; border-radius:8px;
             padding:9px 14px; color:#16a34a; font-size:.88rem; margin:6px 0; }
.alert-err { background:#fef2f2; border:1px solid #fecaca;
             border-left:4px solid #dc2626; border-radius:8px;
             padding:9px 14px; color:#dc2626; font-size:.88rem; margin:6px 0; }
.mobile-hint {
    background:#fefce8; border:1px solid #fde68a; border-radius:8px;
    padding:8px 12px; font-size:.82rem; color:#92400e;
    margin-bottom:1rem; display:flex; gap:8px; align-items:flex-start;
}
@media(min-width:600px){ .mobile-hint{ display:none; } }
.stButton > button { border-radius:8px !important; font-weight:500 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Estado inicial ───────────────────────────────────────────────────────────
# La clave "codigo_campo" es la que usa el widget de texto del formulario.
# Al escribir en session_state["codigo_campo"] ANTES de renderizar el widget,
# Streamlit lo pre-rellena automáticamente.
defaults = {
    "productos":     [],
    "scan_count":    0,
    "codigo_campo":  "",   # ← vinculado al campo del formulario con key=
    "ultima_imagen": None, # hash de la última imagen procesada (evita re-escaneos)
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Detección de códigos (sin pyzbar) ───────────────────────────────────────

def detectar_codigos(img_pil: Image.Image) -> tuple[list[str], np.ndarray]:
    img_rgb  = np.array(img_pil.convert("RGB"))
    img_bgr  = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    anotada  = img_bgr.copy()
    encontrados: list[str] = []

    def anotar(puntos, texto, color):
        if puntos is not None:
            pts = np.array(puntos).astype(int).reshape((-1, 1, 2))
            cv2.polylines(anotada, [pts], True, color, 3)
            x, y = int(np.array(puntos)[0][0]), int(np.array(puntos)[0][1])
            cv2.putText(anotada, texto[:28], (x, max(y - 10, 14)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # 1. QR Aruco (OpenCV ≥ 4.8)
    try:
        det = cv2.QRCodeDetectorAruco()
        datos, pts_list, _ = det.detectAndDecodeMulti(img_gray)
        if datos:
            for d, pts in zip(datos, pts_list):
                if d and d not in encontrados:
                    encontrados.append(d)
                    anotar(pts, d, (37, 99, 235))
    except Exception:
        pass

    # 2. QR clásico (fallback)
    if not encontrados:
        try:
            det = cv2.QRCodeDetector()
            dato, puntos, _ = det.detectAndDecode(img_gray)
            if dato and dato not in encontrados:
                encontrados.append(dato)
                anotar(puntos[0] if puntos is not None else None, dato, (37, 99, 235))
        except Exception:
            pass

    # 3. Barras 1D con BarcodeDetector (requiere opencv-contrib)
    try:
        det = cv2.barcode.BarcodeDetector()
        ok, datos_bc, _, pts_bc = det.detectAndDecodeMulti(img_gray)
        if ok and datos_bc:
            for d, pts in zip(datos_bc, pts_bc):
                if d and d not in encontrados:
                    encontrados.append(d)
                    anotar(pts, d, (22, 163, 74))
    except AttributeError:
        pass  # módulo no disponible en esta build

    # 4. Reintento con preprocesamiento
    if not encontrados:
        for proc in [
            lambda g: cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            lambda g: cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 11, 2),
            lambda g: cv2.equalizeHist(g),
        ]:
            variante = proc(img_gray)
            try:
                d, _, _ = cv2.QRCodeDetector().detectAndDecode(variante)
                if d:
                    encontrados.append(d)
                    break
            except Exception:
                pass
            try:
                ok2, ds2, _, _ = cv2.barcode.BarcodeDetector().detectAndDecodeMulti(variante)
                if ok2:
                    validos = [x for x in ds2 if x]
                    if validos:
                        encontrados.extend(validos)
                        break
            except AttributeError:
                pass

    return encontrados, cv2.cvtColor(anotada, cv2.COLOR_BGR2RGB)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def procesar_imagen(src) -> bool:
    """
    Escanea la imagen y, si detecta un código, lo escribe directo en
    session_state["codigo_campo"] para que el formulario lo muestre al instante.
    Retorna True si se detectó algo.
    """
    if src is None:
        return False

    # Evitar re-procesar la misma imagen en cada rerun
    img_hash = hash(src.getvalue())
    if img_hash == st.session_state.ultima_imagen:
        return False
    st.session_state.ultima_imagen = img_hash

    img_pil = Image.open(src)
    codigos, anotada = detectar_codigos(img_pil)

    if codigos:
        st.session_state.scan_count += 1
        # ← Aquí está la clave: escribimos en la misma variable que usa el widget
        st.session_state.codigo_campo = codigos[0]

        if len(codigos) > 1:
            st.info(f"Detectados {len(codigos)} códigos — se usará el primero.")

        st.markdown(
            f'<div class="alert-ok">✅ Código detectado y cargado en el formulario</div>'
            f'<div class="barcode-badge">🔖 {codigos[0]}</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Ver imagen anotada"):
            st.image(anotada, use_container_width=True)
        return True
    else:
        st.markdown("""
        <div class="alert-err">
            ❌ No se detectó código.<br>
            • El código debe ocupar al menos ¼ de la imagen<br>
            • Buena iluminación, sin reflejos ni sombras<br>
            • Imagen nítida y enfocada
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Ver imagen recibida"):
            st.image(img_pil, use_container_width=True)
        return False


def agregar_producto(codigo, nombre, cantidad, precio, unidad, notas) -> bool:
    if not codigo.strip():
        return False
    st.session_state.productos.append({
        "Código":       codigo.strip(),
        "Nombre":       nombre.strip() or "—",
        "Cantidad":     cantidad,
        "Unidad":       unidad,
        "Precio Unit.": round(precio, 2),
        "Total":        round(cantidad * precio, 2),
        "Notas":        notas.strip(),
        "Fecha/Hora":   datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    return True


def exportar_excel() -> bytes:
    df  = pd.DataFrame(st.session_state.productos)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Productos")
        ws = w.sheets["Productos"]
        for col in ws.columns:
            ancho = max(len(str(c.value or "")) for c in col) + 4
            ws.column_dimensions[col[0].column_letter].width = min(ancho, 42)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="app-header">
    <h1>📦 Captura de Productos</h1>
    <p>Escanea un código · el formulario se rellena solo</p>
</div>
<div class="mobile-hint">
    📱 <span>En móvil usa <strong>"Tomar foto"</strong> — la cámara trasera escanea el código automáticamente.</span>
</div>
""", unsafe_allow_html=True)

# ─── Métricas ─────────────────────────────────────────────────────────────────
n_prod = len(st.session_state.productos)
valor  = sum(p["Total"] for p in st.session_state.productos)
c1, c2, c3 = st.columns(3)
c1.metric("Productos",   n_prod)
c2.metric("Escaneos",    st.session_state.scan_count)
c3.metric("Valor total", f"${valor:,.2f}")
st.divider()

# ─── Escáner ──────────────────────────────────────────────────────────────────
st.markdown("### 📷 Escanear código")

tab_cam, tab_file, tab_manual = st.tabs([
    "📸 Cámara", "🖼️ Subir imagen", "⌨️ Manual / Pistola"
])

with tab_cam:
    st.caption("Móvil: abre la cámara trasera. PC: usa la webcam.")
    cam_src = st.camera_input("Tomar foto del código")
    if procesar_imagen(cam_src):
        st.rerun()   # refrescar para que el formulario muestre el código al instante

with tab_file:
    st.caption("Sube una foto o captura de pantalla con el código visible.")
    file_src = st.file_uploader("Seleccionar imagen",
                                type=["jpg", "jpeg", "png", "webp", "bmp"])
    if procesar_imagen(file_src):
        st.rerun()

with tab_manual:
    st.caption("Con pistola lectora USB: coloca el cursor en el campo y escanea.")
    cod_m = st.text_input("Código de barras", placeholder="Escribe o escanea con pistola...")
    if st.button("Usar este código", use_container_width=True):
        if cod_m.strip():
            st.session_state.codigo_campo = cod_m.strip()
            st.rerun()
        else:
            st.error("Ingresa un código válido.")

# ─── Formulario ───────────────────────────────────────────────────────────────
st.divider()
st.markdown("### 📝 Datos del producto")

# Indicador visual del código activo
if st.session_state.codigo_campo:
    st.markdown(
        f'<div class="barcode-badge">🔖 {st.session_state.codigo_campo}</div>',
        unsafe_allow_html=True,
    )

with st.form("form_producto", clear_on_submit=True):

    # El campo de código usa key="codigo_campo" → se sincroniza con session_state
    # automáticamente: cuando session_state["codigo_campo"] cambia (al escanear),
    # Streamlit pone ese valor en el input sin que el usuario haga nada.
    codigo_input = st.text_input(
        "Código de barras *",
        key="codigo_campo",          # ← vínculo directo con session_state
        placeholder="Se rellena automáticamente al escanear…",
        help="Puedes editarlo manualmente si lo necesitas.",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        nombre = st.text_input("Nombre del producto *", placeholder="Ej: Leche entera 1L")
    with col2:
        unidad = st.selectbox("Unidad", ["pza", "kg", "lt", "caja", "paq", "par", "mt", "otro"])

    col3, col4 = st.columns(2)
    with col3:
        cantidad = st.number_input("Cantidad *", min_value=1, max_value=99999,
                                   value=1, step=1)
    with col4:
        precio = st.number_input("Precio unitario ($)", min_value=0.0,
                                  value=0.0, step=0.50, format="%.2f")

    notas = st.text_area("Notas / Descripción",
                          placeholder="Lote, caducidad, observaciones…", height=75)

    if st.form_submit_button("➕ Agregar producto", use_container_width=True, type="primary"):
        if not codigo_input.strip():
            st.error("Escanea o ingresa un código primero.")
        elif not nombre.strip():
            st.error("El nombre del producto es obligatorio.")
        else:
            agregar_producto(codigo_input, nombre, int(cantidad),
                             float(precio), unidad, notas)
            # Limpiar el código después de agregar
            st.session_state.codigo_campo  = ""
            st.session_state.ultima_imagen = None
            st.success(f"✅ **{nombre.strip()}** agregado correctamente.")
            st.rerun()

# ─── Lista de productos ───────────────────────────────────────────────────────
if st.session_state.productos:
    st.divider()
    st.markdown(f"### 📋 Productos capturados ({n_prod})")

    df = pd.DataFrame(st.session_state.productos)
    st.dataframe(
        df, use_container_width=True, hide_index=True,
        column_config={
            "Precio Unit.": st.column_config.NumberColumn(format="$%.2f"),
            "Total":        st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    r1, r2, r3 = st.columns(3)
    r1.metric("Unidades totales",  int(df["Cantidad"].sum()))
    r2.metric("Promedio por item", f"${df['Total'].mean():.2f}")
    r3.metric("Valor acumulado",   f"${df['Total'].sum():,.2f}")

    st.markdown("#### Editar lista")
    e1, e2 = st.columns(2)
    with e1:
        idx = st.number_input("Eliminar fila #", min_value=1,
                               max_value=n_prod, value=1, step=1)
        if st.button("🗑️ Eliminar fila seleccionada", use_container_width=True):
            st.session_state.productos.pop(int(idx) - 1)
            st.rerun()
    with e2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧹 Limpiar toda la lista", use_container_width=True):
            st.session_state.productos = []
            st.session_state.scan_count = 0
            st.rerun()

    # ─── Exportar ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### 💾 Exportar")
    ex1, ex2 = st.columns(2)
    with ex1:
        st.download_button(
            "⬇️ Excel (.xlsx)", exportar_excel(),
            file_name=f"productos_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True, type="primary",
        )
    with ex2:
        st.download_button(
            "⬇️ CSV", df.to_csv(index=False).encode("utf-8"),
            file_name=f"productos_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True,
        )

    with st.expander("Ver JSON (para integración con APIs)"):
        st.json(st.session_state.productos)

else:
    st.info("📭 Sin productos aún. Escanea un código para comenzar.")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:.75rem;padding:.4rem 0">
    📦 Captura de Productos · OpenCV sin pyzbar · Móvil y escritorio
</div>
""", unsafe_allow_html=True)
