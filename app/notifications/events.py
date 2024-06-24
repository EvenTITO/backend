from .notifications import (
    send_email,
    FRONTEND_URL,
    message_to_admins,
    create_subject
)


async def request_approve_event(db, user_from, event):
    message = await message_to_admins(db)

    body = f"""
    {user_from.name} ha solicitado crear un Evento.
    Nombre del evento: {event.title}

    Ver más información en {FRONTEND_URL}.
    """

    message['Subject'] = create_subject(
        'Ha llegado una nueva solicitud de Creación de Evento'
    )
    message.set_content(body)
    send_email(message)


def notify_event_approved(user_from, event):
    raise 'TODO'
    message = 'TODO'
    event_name = event.name

    body = f"""
    Ya puedes configurar tu evento {event_name} y publicarlo!

    Visita nuestra página: {FRONTEND_URL}.
    """

    message['Subject'] = create_subject(
        f'Tu Evento {event_name} ha sido aprobado!'
    )
    message.set_content(body)
    send_email(message)
