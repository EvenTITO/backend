from fastapi import APIRouter
from app.submissions.schemas.work import Work, WorkWithState, BasicWorkInfo
from app.submissions.schemas.work_stages import BeforeDeadline, NoReviewStages
from datetime import datetime
from app.models.work import WorkModel  # noqa
from app.models.submission import SubmissionModel  # noqa
from app.models.review import ReviewModel  # noqa


works_router = APIRouter(prefix="/events/{event_id}/works", tags=["Works"])


@works_router.post("", status_code=201)
async def create_work(work: Work) -> str:
    """
    Creates the Work. This call is made by the work author.
    """
    # TODO
    return 'this-is-a-mocked-answer'


@works_router.put("/{work_id}", status_code=204)
async def update_work(work_update: Work):
    """
    Author updates the work with work_id. This method is used only
    in the first stage before the first submission deadline date.
    """
    # TODO
    pass


@works_router.get("/{work_id}/")
async def get_work_author_information() -> WorkWithState:
    """
    Obtain all the work information that the author is allowed
    to see.
    This method is used by the work author.
    """
    return WorkWithState(
        state=BeforeDeadline(
            deadline_date=datetime(2024, 12, 1)
        )
    )


@works_router.get("/")
async def get_all_works_basic_information() -> list[BasicWorkInfo]:
    """
    Obtain a resumee of all the works in the event.
    This method is used by the event organizer.
    """
    return [
        BasicWorkInfo(
            main_author_name='Martin Sanchez',
            reviewer_name='Juana Gomez',
            title=(
                'Comparación del Rendimiento de Curve25519, '
                'P-256 y Curvas de Edwards en Algoritmos '
                'de Criptografía Cuántica'
            ),
            track='cibersecurity',
            id=3,
            stage=NoReviewStages.BEFORE_DEADLINE,
        ),
        BasicWorkInfo(
            main_author_name='Martina Federer',
            reviewer_name=None,
            title=(
                'Aplicaciones de los Toros de Clifford en '
                'la Teoría de Códigos Correctores de Errores'
            ),
            track='math',
            id=2,
            stage=NoReviewStages.BEFORE_DEADLINE,
        ),
    ]
