jj## Flujo de trabajos

1) se suben trabajos hasta la fecha limite de entrega de trabajos.
durante ese período, el dueño del trabajo puede hacer todas las modificaciones que quiera y al modificar el archivo, lo pisa.

2) cuando llega la fecha límite, se hace un checkpoint de la entrega (el dueño no puede modificar nada).

3) el/los ORGANIZADORES asignan UN SOLO reviewer principal a cada trabajo. En principio no hay segundas opiniones ni nada (de ultima que lo manejen por mail entre ellos).

4) el REVIEWER pasa una correccion con su puntaje estimado y estado: ACEPTADO, REVISAR, RECHAZADO (estado propuesto por el reviewer, pregunta fija para orientar al organizor)

5) los ORGANIZADORES mandan la corrección (nunca lo hace un reviewer). Pueden modificar el ESTADO: ACEPTADO, REVISAR, RECHAZADO y decidir qué campos de la corrección son visibles. Para los REVISADO, definen un DEADLINE.

6) Los "ACEPTADO", cierran ahí el flujo; idem los "RECHAZADO".

7) Los "REVISAR" pueden agregar una SUBMISSION nueva que no va a pisar a la anterior. Pueden modificar siempre que quieran esa submission, hasta llegar al deadline.

8) SE REPITEN PASOS 4 - 7


POST /events/{event_id}/works -> crea el trabajo principal.

PUT /events/{event_id}/works/{work_id} -> guardamos historial de todo. Se modifica el latest.

GET /events/{event_id}/works/{work_id}/submissions/{submission_id}/upload_url -> segun la etapa se devuelve un url a un path nuevo, o a un path a pisar.
El submission_id se obtiene del estado del work.

GET /events/{event_id}/my-works -> un presentador quiere obtener sus trabajos y su estado. No deben verse las revisiones intermedias, solo la de organizer.
Cosas a devolver: titulo, fecha ult modificacion, estado, track.

GET /events/{event_id}/works/{work_id} -> usado por autos, estan en my-works y elegis ver un trabajo de los mios de la lista


GET /events/{event_id}/works/{work_id}/submissions/{submission_id}/download_url

GET /events/{event_id}/my-reviews -> un reviewer quiere obtener sus reviews
GET /events/{event_id}/works/{work_id}/reviews (validado en back que el usuario sea REVIEWER o ORGANIZER de dicho trabajo)


GET /events/{event_id}/works -> ORGANIZER pide lista de trabajos con el fin de ver datos basicos.

---------------------

// organizer

PATCH /events/{event_id}/reviews/assignments (ORGANIZER para poder agregar un reviewer a un work)

{
    assignments: [
        {
            reviewer_id: 'asdasd',
            work_id: 1
        }
    ]
}


-----------------------

// reviewers

POST /events/{event_id}/works/{work_id}/reviews --> llama el reviewer para mandar la correccion y el PUT para actualizar esa misma correccion.

PUT /events/{event_id}/works/{work_id}/reviews/{review_id} //el review por defecto tiene que tener estado y comentario general. 



// organizer

PATCH /events/{event_id}/works/{work_id}/reviews/state --> llama el organizador si quiere modificar lo puesto por el corrector: ACEPTADO, RECHAZADO, REVISAR.
{
    state: 'RECHAZADO',
    commentary: 'Esta mal el abstract'
}

----------------------

POST /events/{event_id}/reviews/publish -> ORGANIZER manda los reviews a los usuarios que el quiere

{
    work_ids: [3, 4, 7, 8, 9] // aca solo esta mandando algunos reviews.
    revision_deadline_date: '2024-10-08' // a los que se los manda a revision, tienen hasta este dia para corregir todo.
}


