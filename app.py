import streamlit as st
from utils.email_service import enviar_correo
import re
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Soporte Técnico",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #6c757d;
        border-top: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="main-header">
    <h1>🛠️ Sistema de Soporte Técnico Cloud</h1>
    <p>Reporte de incidencias - Envío automático al administrador</p>
</div>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
if 'enviado' not in st.session_state:
    st.session_state.enviado = False
if 'datos' not in st.session_state:
    st.session_state.datos = {}

# FORMULARIO
with st.form("formulario_soporte", clear_on_submit=False):
    
    # Información del usuario
    st.subheader("👤 Información del Usuario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input(
            "Nombre Completo *",
            placeholder="Ej: Juan Pérez",
            help="Ingresa tu nombre completo"
        )
        
        telefono = st.text_input(
            "Teléfono",
            placeholder="Ej: 555-123-4567",
            help="Opcional - Solo para contacto rápido"
        )
    
    with col2:
        email = st.text_input(
            "Correo Electrónico *",
            placeholder="ejemplo@correo.com",
            help="Donde recibirás la confirmación"
        )
        
        departamento = st.selectbox(
            "Departamento",
            ["Selecciona...", "IT", "Recursos Humanos", "Finanzas", "Ventas", "Operaciones", "Marketing", "Otro"]
        )
    
    st.divider()
    
    # Detalles del problema
    st.subheader("🔍 Detalles de la Incidencia")
    
    col3, col4 = st.columns(2)
    
    with col3:
        tipo_problema = st.selectbox(
            "Tipo de Problema *",
            [
                "Selecciona...",
                "🔧 Hardware",
                "💻 Software",
                "🌐 Red/Conectividad",
                "📧 Correo Electrónico",
                "🔐 Acceso/Seguridad",
                "📊 Base de Datos",
                "☁️ Servicios Cloud",
                "📱 Aplicación Móvil",
                "🖨️ Impresión",
                "🎥 Videoconferencia",
                "🔒 VPN",
                "Otro"
            ],
            help="Selecciona la categoría del problema"
        )
        
        prioridad = st.select_slider(
            "Prioridad *",
            options=["Muy Baja", "Baja", "Media", "Alta", "Muy Alta"],
            value="Media",
            help="Selecciona la urgencia del problema"
        )
    
    with col4:
        sistema_afectado = st.selectbox(
            "Sistema Afectado",
            [
                "Selecciona...",
                "Windows",
                "macOS",
                "Linux",
                "Sistema Web",
                "Sistema Interno",
                "Aplicación Móvil",
                "Servidor",
                "Red",
                "Impresora",
                "Otro"
            ]
        )
        
        # Indicador visual de prioridad
        if prioridad == "Muy Alta":
            st.error("⚠️ **Prioridad Muy Alta** - Se atenderá de inmediato")
        elif prioridad == "Alta":
            st.warning("⚡ **Prioridad Alta** - Se atenderá en 1 hora")
        elif prioridad == "Media":
            st.info("📌 **Prioridad Media** - Se atenderá en 4 horas")
        else:
            st.success("📋 **Prioridad Baja/Muy Baja** - Se atenderá en 24 horas")
    
    st.divider()
    
    # Descripción del problema
    st.subheader("📝 Descripción del Problema")
    
    descripcion = st.text_area(
        "Descripción detallada *",
        placeholder="Describe el problema en detalle...\n\nEjemplo: Desde esta mañana no puedo acceder al sistema, me sale error de conexión. Ya reinicié el equipo y el router pero el problema persiste.",
        height=150,
        help="Incluye todos los detalles que puedan ayudar a resolver el problema"
    )
    
    # Adjuntar archivo (opcional)
    archivo_adjunto = st.file_uploader(
        "📎 Adjuntar archivo (Opcional)",
        type=['png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx', 'txt', 'zip'],
        help="Puedes adjuntar capturas de pantalla o documentos relevantes"
    )
    
    st.divider()
    
    # Botón de envío
    col5, col6, col7 = st.columns([1, 2, 1])
    with col6:
        enviar = st.form_submit_button(
            "📤 ENVIAR REPORTE",
            use_container_width=True,
            type="primary"
        )

# PROCESAMIENTO DEL FORMULARIO
if enviar:
    # VALIDACIONES
    errores = []
    
    # Validar nombre
    if not nombre or nombre.strip() == "":
        errores.append("El nombre es obligatorio")
    elif len(nombre) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres")
    
    # Validar email
    if not email or email.strip() == "":
        errores.append("El correo electrónico es obligatorio")
    else:
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, email):
            errores.append("El correo electrónico no es válido")
    
    # Validar tipo de problema
    if not tipo_problema or tipo_problema == "Selecciona...":
        errores.append("Debes seleccionar un tipo de problema")
    
    # Validar descripción
    if not descripcion or descripcion.strip() == "":
        errores.append("La descripción del problema es obligatoria")
    elif len(descripcion) < 10:
        errores.append("La descripción debe tener al menos 10 caracteres")
    
    # MOSTRAR ERRORES
    if errores:
        st.markdown("""
        <div class="error-box">
            <strong>❌ Por favor, corrige los siguientes errores:</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for error in errores:
            st.error(f"• {error}")
    
    # SI NO HAY ERRORES, PROCESAR
    else:
        with st.spinner("📨 Enviando reporte al administrador..."):
            try:
                # Guardar datos en sesión
                st.session_state.datos = {
                    "nombre": nombre.strip(),
                    "email": email.strip(),
                    "telefono": telefono.strip() if telefono else "No proporcionado",
                    "departamento": departamento if departamento != "Selecciona..." else "No especificado",
                    "tipo_problema": tipo_problema,
                    "prioridad": prioridad,
                    "sistema_afectado": sistema_afectado if sistema_afectado != "Selecciona..." else "No especificado",
                    "descripcion": descripcion.strip(),
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "tiene_archivo": archivo_adjunto is not None,
                    "nombre_archivo": archivo_adjunto.name if archivo_adjunto else "Sin archivo"
                }
                
                # Enviar correo
                resultado = enviar_correo(st.session_state.datos)
                
                if resultado["exito"]:
                    st.session_state.enviado = True
                    
                    # Mostrar éxito
                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ ¡REPORTE ENVIADO CORRECTAMENTE!</h3>
                        <p>Tu reporte ha sido enviado al administrador del sistema.</p>
                        <p>📧 Recibirás una confirmación en tu correo: <strong>{}</strong></p>
                        <p>🆔 Número de seguimiento: <strong>{}</strong></p>
                    </div>
                    """.format(
                        st.session_state.datos["email"],
                        f"INC-{datetime.now().strftime('%Y%m%d')}-{hash(st.session_state.datos['email']) % 10000:04d}"
                    ), unsafe_allow_html=True)
                    
                    # Mostrar resumen del reporte
                    with st.expander("📋 Ver detalles del reporte enviado"):
                        st.json(st.session_state.datos)
                    
                    # Botón para nuevo reporte
                    if st.button("📝 Crear nuevo reporte"):
                        st.session_state.enviado = False
                        st.rerun()
                
                else:
                    st.markdown("""
                    <div class="error-box">
                        <strong>❌ Error al enviar el reporte</strong>
                        <p>No se pudo enviar el correo al administrador.</p>
                        <p>Detalle técnico: {}</p>
                    </div>
                    """.format(resultado["mensaje"]), unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown("""
                <div class="error-box">
                    <strong>❌ Error inesperado</strong>
                    <p>Ha ocurrido un error al procesar tu solicitud.</p>
                    <p>Detalle: {}</p>
                </div>
                """.format(str(e)), unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <p>🔒 Este reporte se envía de forma segura al administrador</p>
    <p>📧 Sistema de Soporte Técnico Cloud - v1.0.0</p>
    <p style="font-size: 0.8rem;">📌 Los datos no se almacenan en base de datos</p>
</div>
""", unsafe_allow_html=True)

# Información en la barra lateral
with st.sidebar:
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **Proceso de soporte:**
    
    1. 📝 Completa el formulario
    2. ✅ Valida la información
    3. 📨 Envía automáticamente
    4. 📧 Admin recibe el correo
    5. ✅ Confirmación al usuario
    
    **Seguridad:**
    - 🔐 Credenciales en Secrets
    - 📁 No almacenamos datos
    - 🚀 Desplegado en Cloud
    
    **Tiempos de respuesta:**
    - 🔴 Muy Alta: Inmediato
    - 🟠 Alta: 1 hora
    - 🟡 Media: 4 horas
    - 🟢 Baja: 24 horas
    """)