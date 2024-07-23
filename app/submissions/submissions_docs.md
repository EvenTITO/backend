## Flujo de trabajos

1) se suben trabajos hasta la fecha limite de entrega de trabajos.
durante ese período, el dueño del trabajo puede hacer todas las modificaciones que quiera y al modificar el archivo, lo pisa.

2) cuando llega la fecha límite, se hace un checkpoint de la entrega (el dueño no puede modificar nada).

3) el/los ORGANIZADORES asignan UN SOLO reviewer principal a cada trabajo. En principio no hay segundas opiniones ni nada (de ultima que lo manejen por mail entre ellos).

4) el REVIEWER pasa una correccion con su puntaje estimado y estado: ACEPTADO, REVISAR, RECHAZADO

5) los ORGANIZADORES mandan la corrección (nunca lo hace un reviewer). Pueden modificar el ESTADO: ACEPTADO, REVISAR, RECHAZADO y decidir qué campos de la corrección son visibles. Para los REVISADO, definen un DEADLINE.

6) Los "ACEPTADO", cierran ahí el flujo; idem los "RECHAZADO".

7) Los "REVISAR" pueden agregar una SUBMISSION nueva que no va a pisar a la anterior. Pueden modificar siempre que quieran esa submission, hasta llegar al deadline.

8) SE REPITEN PASOS 4 - 7


POST /events/{event_id}/works -> crea el trabajo principal

PUT /events/{event_id}/works/{work_id} -> no guardamos historial de abstract, etc. Pisamos el valor. Lo unico que guardamos con versionado es el archivo.

GET /events/{event_id}/works/{work_id}/upload_url/submission_file -> segun la etapa se devuelve un url a un path nuevo, o a un path a pisar.


---------------------

PUT /events/{event_id}/review-assignments

{
    assignments: [
        {
            user_id: 'asdasd',
            work_id: 1
        }
    ]

}


-----------------------

POST /events/{event_id}/works/{work_id}/reviews --> llama el reviewer para mandar la correccion y el PUT para actualizar esa misma correccion.

PUT /events/{event_id}/works/{work_id}/reviews/{review_id}


PATCH /events/{event_id}/works/{work_id}/reviews/state --> llama el organizador si quiere modificar lo puesto por el corrector: ACEPTADO, RECHAZADO, REVISAR.

----------------------

POST /events/{event_id}/reviews -> organizador manda los reviews a los usuarios que el quiere

{
    reviews_to_send: [3, 4, 7, 8, 9] // aca solo esta mandando algunos reviews.
    revision_deadline_date: '2024-10-08' // a los que se los manda a revision, tienen hasta este dia para corregir todo.
}


