import requests
import json

def enviar_correo(datos):
    """
    Envía la información del reporte a EmailJS mapeando las variables de la plantilla HTML.
    """
    url = "https://api.emailjs.com/api/v1.0/email/send"
    
    # Mapeo de emojis según la prioridad seleccionada
    emojis_prioridad = {
        "Muy Alta": "🔴",
        "Alta": "🟠",
        "Media": "🟡",
        "Baja": "🟢",
        "Muy Baja": "⚪"
    }
    
    priority_emoji = emojis_prioridad.get(datos.get("prioridad"), "📌")

    # Mapeo exacto con los {{nombres_de_variables}} de tu plantilla de EmailJS
    payload = {
        "service_id": "service_844lp4n",
        "template_id": "template_8zrdioc",
        "user_id": "1cXVMYweDioV6ajCc",  # Tu Public Key
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