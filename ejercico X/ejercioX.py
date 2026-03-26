import streamlit as st

class LoginStreamlitApp:
    def __init__(self) -> None:
        self.usuario_correcto = "admin"
        self.contrasena_correcta = "Admin2026"
        
        if "autenticado" not in st.session_state:
            st.session_state.autenticado = False
        if "intentos" not in st.session_state:
            st.session_state.intentos = 0

    def ejecutar(self) -> None:
        st.set_page_config(page_title="Sistema Seguro", page_icon="🔐", layout="wide")
        st.title("🔐 Sistema de Gestión")

        if st.session_state.autenticado:
            self.mostrar_menu_con_cards()
        else:
            self.mostrar_login()

    def mostrar_login(self) -> None:
        st.subheader("Iniciar Sesión")
        
        with st.form("form_login"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write("👤")
            with col2:
                usuario = st.text_input("Usuario")
                contrasena = st.text_input("Contraseña", type="password")
            
            enviar = st.form_submit_button("🚪 Ingresar", use_container_width=True)

        if enviar:
            if st.session_state.intentos >= 3:
                st.error("🔒 Se alcanzó el máximo de 3 intentos.")
                return

            if not usuario.strip():
                st.error("❌ El usuario no puede estar vacío")
                st.session_state.intentos += 1
                return
            if not usuario.isalnum():
                st.error("❌ El usuario debe ser alfanumérico")
                st.session_state.intentos += 1
                return
            if len(contrasena) < 8:
                st.error("❌ La contraseña debe tener mínimo 8 caracteres")
                st.session_state.intentos += 1
                return
            if not any(c.isalpha() for c in contrasena):
                st.error("❌ La contraseña debe tener al menos una letra")
                st.session_state.intentos += 1
                return
            if not any(c.isdigit() for c in contrasena):
                st.error("❌ La contraseña debe tener al menos un número")
                st.session_state.intentos += 1
                return

            if usuario.strip() == self.usuario_correcto and contrasena.strip() == self.contrasena_correcta:
                st.session_state.autenticado = True
                st.session_state.intentos = 0
                st.success("✅ ¡Bienvenido, Administrador!")
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")
                st.session_state.intentos += 1
                if st.session_state.intentos >= 3:
                    st.error("🔒 Máximo de intentos alcanzado.")

    def mostrar_menu_con_cards(self) -> None:
        st.success("✅ Sesión iniciada correctamente como **admin**")
        st.subheader("Menú Principal")

        # === CARDS ===
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("### 1️⃣ Clasificar Números")
                st.write("Determina si un número es positivo, negativo o cero.")
                if st.button("Abrir Clasificador →", key="btn_clasificar", use_container_width=True):
                    self.clasificar_numero()

            with st.container(border=True):
                st.markdown("### 2️⃣ Categoría de Edad")
                st.write("Muestra la categoría según la edad y sus permisos.")
                if st.button("Ver Categorías →", key="btn_edad", use_container_width=True):
                    self.categoria_edad()

        with col2:
            with st.container(border=True):
                st.markdown("### 3️⃣ Calcular Tarifa Final")
                st.write("Calcula el precio final con descuento según edad.")
                if st.button("Calcular Tarifa →", key="btn_tarifa", use_container_width=True):
                    self.calcular_tarifa()

        # === UN SOLO BOTÓN DE CERRAR SESIÓN ===
        st.divider()
        col_btn = st.columns([3, 1])[1]   # Esto centra un poco el botón
        with col_btn:
            if st.button("🚪 Cerrar Sesión", 
                        use_container_width=True, 
                        type="secondary",
                        key="cerrar_sesion_unico"):
                st.session_state.autenticado = False
                st.success("Sesión cerrada correctamente.")
                st.rerun()

    # ==================== FUNCIONES ====================

    def clasificar_numero(self):
        with st.expander("🔢 Clasificar Números", expanded=True):
            numero = st.number_input("Ingrese un número:", value=0, step=1)
            if st.button("Clasificar", type="primary", use_container_width=True, key="clasificar_action"):
                if numero > 0:
                    st.success(f"✅ **{numero}** es **POSITIVO**")
                elif numero < 0:
                    st.error(f"❌ **{numero}** es **NEGATIVO**")
                else:
                    st.info(f"⚪ **{numero}** es **CERO**")

    def categoria_edad(self):
        with st.expander("👤 Categoría de Edad y Permisos", expanded=True):
            edad = st.number_input("Ingrese su edad:", min_value=0, max_value=120, value=18)
            if st.button("Mostrar Categoría", type="primary", use_container_width=True, key="edad_action"):
                if edad < 13:
                    st.info("👦 **Niño** (0-12 años)\n\n• No puede conducir\n• No puede votar")
                elif edad < 18:
                    st.warning("🧑 **Adolescente** (13-17 años)\n\n• Puede usar redes\n• No puede conducir ni votar")
                elif edad < 65:
                    st.success("🧔 **Adulto** (18-64 años)\n\n• Puede conducir\n• Puede votar\n• Puede trabajar")
                else:
                    st.info("👴 **Adulto Mayor** (65+ años)\n\n• Puede conducir y votar\n• Beneficios disponibles")

    def calcular_tarifa(self):
        with st.expander("💰 Calcular Tarifa Final", expanded=True):
            precio = st.number_input("Precio base ($):", min_value=0.0, value=100.0, step=0.1)
            edad = st.number_input("Edad del cliente:", min_value=0, max_value=120, value=30)
            
            if st.button("Calcular Tarifa", type="primary", use_container_width=True, key="tarifa_action"):
                descuento = 0.0
                if edad < 18:
                    descuento = 0.15
                elif edad >= 65:
                    descuento = 0.20
                
                tarifa_final = precio * (1 - descuento)
                st.success(f"**Tarifa Final: ${tarifa_final:.2f}**")
                if descuento > 0:
                    st.balloons()
                    st.info(f"🎉 Descuento aplicado: **{descuento*100:.0f}%**")

# ====================== EJECUCIÓN ======================
if __name__ == "__main__":
    app = LoginStreamlitApp()
    app.ejecutar()
