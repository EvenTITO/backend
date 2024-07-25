from app.submissions.schemas.work_stages import NoReviewStages
from fastapi import APIRouter
from app.submissions.schemas.work import BasicWorkInfo

my_reviews_router = APIRouter(
    prefix="/events/{event_id}/my-reviews",
    tags=["Reviews"]
)


@my_reviews_router.get("")
async def get_all_works_assigned_for_my_review() -> list[BasicWorkInfo]:
    """
    This method is used by a reviewer to get all his asigned works.
    """
    return [
        BasicWorkInfo(
            main_author_name='Julian Altocapo',
            title=(
                'Aplicaciones de los Toros de Clifford en '
                'la Teoría de Códigos Correctores de Errores'
            ),
            track='math',
            id=2,
            stage=NoReviewStages.BEFORE_DEADLINE,
            reviewer_name='Martina Perez'
        ),
        BasicWorkInfo(
            title=(
                'Comparación del Rendimiento de Curve25519, '
                'P-256 y Curvas de Edwards en Algoritmos '
                'de Criptografía Cuántica'
            ),
            track='cibersecurity',
            id=3,
            stage=NoReviewStages.BEFORE_DEADLINE,
            reviewer_name='Martina Perez'
        )

    ]
