import requests
import json
import streamlit as st
import base64

def enviar_correo(datos):
    """
    Envía el reporte a EmailJS usando credenciales de st.secrets o valores por defecto.
    """
    service_id = st.secrets.get("EMAILJS_SERVICE_ID", "service_844lp4n")
    template_id = st.secrets.get("EMAILJS_TEMPLATE_ID", "template_8zrdioc")
    public_key = st.secrets.get("EMAILJS_PUBLIC_KEY", "1cXVMYweDioV6ajCc")
    private_key = st.secrets.get("EMAILJS_PRIVATE_KEY", None)

    if not service_id or not template_id or not public_key:
        return {
            "exito": False,
            "mensaje": "Faltan credenciales de EmailJS. Verifica la configuración de Secrets."
        }

    url = "https://api.emailjs.com/api/v1.0/email/send"

    emojis_prioridad = {
        "Muy Alta": "🔴",
        "Alta": "🟠",
        "Media": "🟡",
        "Baja": "🟢",
        "Muy Baja": "⚪"
    }
    priority_emoji = emojis_prioridad.get(datos.get("prioridad"), "📌")

    # --- PROCESAMIENTO DEL ARCHIVO ADJUNTO ---
    content_b64 = None
    if datos.get("archivo_objeto") is not None:
        archivo = datos["archivo_objeto"]
        # Convertir los bytes del UploadedFile a string base64
        bytes_data = archivo.getvalue()
        content_b64 = base64.b64encode(bytes_data).decode("utf-8")

    # Construcción de template_params
    template_params = {
        "report_date": datos.get("fecha"),
        "priority_emoji": priority_emoji,
        "priority": datos.get("prioridad"),
        "user_name": datos.get("nombre"),
        "user_email": datos.get("email"),
        "user_phone": datos.get("telefono"),
        "department": datos.get("departamento"),
        "problem_type": datos.get("tipo_problema"),
        "system": datos.get("sistema_afectado"),
        "description": datos.get("descripcion"),
        "has_attachment": "Sí" if datos.get("tiene_archivo") else "No",
        "filename": datos.get("nombre_archivo")
    }

    # Si hay archivo, agregamos la propiedad en template_params
    if content_b64:
        template_params["content"] = content_b64

    payload = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": public_key,
        "template_params": template_params
    }

    if private_key:
        payload["accessToken"] = private_key

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            return {"exito": True, "mensaje": "OK"}
        else:
            return {
                "exito": False,
                "mensaje": f"Error {response.status_code}: {response.text}"
            }

    except Exception as e:
        return {"exito": False, "mensaje": str(e)}
