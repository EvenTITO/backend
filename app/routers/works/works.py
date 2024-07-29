# flake8: noqa
from fastapi import APIRouter
from app.dependencies.services.works.author_works_dep import AuthorWorksServiceDep
from app.dependencies.services.works.works_dep import WorksServiceDep
from app.schemas.works.work import WorkSchema, WorkWithState
# from app.services.works import works_service
# from app.schemas.works.work_stages import BeforeDeadline, NoReviewStages

works_router = APIRouter(prefix="/events/{event_id}/works", tags=["Works"])


@works_router.post("", status_code=201)
async def create_work(work: WorkSchema, works_service: WorksServiceDep) -> int:
    """
    Creates the Work. This call is made by the work author.
    """
    work_id = await works_service.create_work(work)
    return work_id


@works_router.put("/{work_id}", status_code=204)
async def update_work(work_update: WorkSchema, works_service: AuthorWorksServiceDep) -> None:
    """
    Author updates the work with work_id. This method is used only
    in the first stage before the first submission deadline date.
    """
    await works_service.update(work_update)


@works_router.get("/{work_id}")
async def get_work_author_information(works_service: AuthorWorksServiceDep) -> WorkWithState:
    """
    Obtain all the work information that the author is allowed
    to see.
    This method is used by the work author.
    """
    work = await works_service.get_work()
    return work


# @works_router.get("/")
# async def get_all_works_basic_information() -> list[BasicWorkInfo]:
#     """
#     Obtain a resumee of all the works in the event.
#     This method is used by the event organizer.
#     """
#     return [
#         BasicWorkInfo(
#             main_author_name='Martin Sanchez',
#             reviewer_name='Juana Gomez',
#             title=(
#                 'Comparación del Rendimiento de Curve25519, '
#                 'P-256 y Curvas de Edwards en Algoritmos '
#                 'de Criptografía Cuántica'
#             ),
#             track='cibersecurity',
#             id=3,
#             stage=NoReviewStages.BEFORE_DEADLINE,
#         ),
#         BasicWorkInfo(
#             main_author_name='Martina Federer',
#             reviewer_name=None,
#             title=(
#                 'Aplicaciones de los Toros de Clifford en '
#                 'la Teoría de Códigos Correctores de Errores'
#             ),
#             track='math',
#             id=2,
#             stage=NoReviewStages.BEFORE_DEADLINE,
#         ),
#     ]
