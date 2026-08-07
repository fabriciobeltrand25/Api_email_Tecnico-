import requests
import os
import streamlit as st
from datetime import datetime

def enviar_correo(datos_usuario):
    """
    Envía un correo utilizando el servicio EmailJS
    
    Args:
        datos_usuario (dict): Diccionario con los datos del formulario
    
    Returns:
        dict: Resultado del envío con estado y mensaje
    """
    
    # Obtener variables de entorno
    try:
        # Intentar obtener desde Streamlit Secrets (producción)
        SERVICE_ID = st.secrets["EMAILJS_SERVICE_ID"]
        TEMPLATE_ID = st.secrets["EMAILJS_TEMPLATE_ID"]
        PRIVATE_KEY = st.secrets["EMAILJS_PRIVATE_KEY"]  # <--- CAMBIADO
        EMAIL_ADMIN = st.secrets["EMAIL_ADMIN"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        
        SERVICE_ID = os.getenv("EMAILJS_SERVICE_ID")
        TEMPLATE_ID = os.getenv("EMAILJS_TEMPLATE_ID")
        PRIVATE_KEY = os.getenv("EMAILJS_PRIVATE_KEY")  # <--- CAMBIADO
        EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")
    
    # Verificar que todas las variables existen
    if not all([SERVICE_ID, TEMPLATE_ID, PRIVATE_KEY, EMAIL_ADMIN]):
        return {
            "exito": False,
            "mensaje": "Faltan credenciales de EmailJS. Verifica la configuración."
        }
    
    # Preparar datos para EmailJS
    template_params = {
        "to_email": EMAIL_ADMIN,
        "user_name": datos_usuario["nombre"],
        "user_email": datos_usuario["email"],
        "user_phone": datos_usuario["telefono"],
        "department": datos_usuario["departamento"],
        "problem_type": datos_usuario["tipo_problema"],
        "priority": datos_usuario["prioridad"],
        "system": datos_usuario["sistema_afectado"],
        "description": datos_usuario["descripcion"],
        "report_date": datos_usuario["fecha"],
        "has_attachment": "Sí" if datos_usuario["tiene_archivo"] else "No",
        "filename": datos_usuario["nombre_archivo"],
        "priority_emoji": obtener_emoji_prioridad(datos_usuario["prioridad"])
    }
    
    # URL de la API de EmailJS
    url = f"https://api.emailjs.com/api/v1.0/email/send"
    
    # Datos para la solicitud
    payload = {
        "service_id": SERVICE_ID,
        "template_id": TEMPLATE_ID,
        "user_id": PRIVATE_KEY,  # <--- USAR PRIVATE KEY
        "template_params": template_params
    }

    
    try:
        # Enviar solicitud a EmailJS
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return {
                "exito": True,
                "mensaje": "Correo enviado correctamente"
            }
        else:
            return {
                "exito": False,
                "mensaje": f"Error al enviar correo. Código: {response.status_code}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "exito": False,
            "mensaje": f"Error de conexión: {str(e)}"
        }
    except Exception as e:
        return {
            "exito": False,
            "mensaje": f"Error inesperado: {str(e)}"
        }

def obtener_emoji_prioridad(prioridad):
    """
    Retorna un emoji según la prioridad
    
    Args:
        prioridad (str): Nivel de prioridad
    
    Returns:
        str: Emoji correspondiente
    """
    emojis = {
        "Muy Alta": "🔴",
        "Alta": "🟠",
        "Media": "🟡",
        "Baja": "🟢",
        "Muy Baja": "🔵"
    }
    return emojis.get(prioridad, "⚪")