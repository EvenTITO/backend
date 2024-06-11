from .notifications import (
    send_email,
    FRONTEND_URL,
    message_to_admins,
    create_subject
)

def request_approve_event(user_from, event):
    message = message_to_admins()

    body = f"""
    Se ha solicitado crear un Evento. Ver más información en {FRONTEND_URL}. 
    """

    message['Subject'] = create_subject('Ha llegado una nueva solicitud de Creación de Evento')
    message.set_content(body)
    send_email(message)
