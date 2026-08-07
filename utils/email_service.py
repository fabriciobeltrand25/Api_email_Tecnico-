import requests
import json
import streamlit as st

def enviar_correo(datos):
    """
    Envía el reporte a EmailJS usando credenciales de st.secrets o valores por defecto.
    """
    # Intentar obtener credenciales de st.secrets o usar las fijas
    service_id = st.secrets.get("EMAILJS_SERVICE_ID", "service_844lp4n")
    template_id = st.secrets.get("EMAILJS_TEMPLATE_ID", "template_8zrdioc")
    public_key = st.secrets.get("EMAILJS_PUBLIC_KEY", "1cXVMYweDioV6ajCc")
    private_key = st.secrets.get("EMAILJS_PRIVATE_KEY", None)

    # Validar que existan las credenciales mínimas
    if not service_id or not template_id or not public_key:
        return {
            "exito": False,
            "mensaje": "Faltan credenciales de EmailJS. Verifica la configuración de Secrets."
        }

    url = "https://api.emailjs.com/api/v1.0/email/send"

    # Mapeo de emojis para la prioridad
    emojis_prioridad = {
        "Muy Alta": "🔴",
        "Alta": "🟠",
        "Media": "🟡",
        "Baja": "🟢",
        "Muy Baja": "⚪"
    }
    priority_emoji = emojis_prioridad.get(datos.get("prioridad"), "📌")

    # Construcción del Payload
    payload = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": public_key,
        "template_params": {
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
    }

    # Si tienes activada la casilla de "Usa la clave privada" en EmailJS:
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