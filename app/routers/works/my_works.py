from app.schemas.works.work_stages import NoReviewStages
from fastapi import APIRouter
from app.schemas.works.work import BasicWorkInfoForAuthor

my_works_router = APIRouter(
    prefix="/events/{event_id}/my-works",
    tags=["My Works"]
)


@my_works_router.get("")
async def get_my_works() -> list[BasicWorkInfoForAuthor]:
    """
    Get all my works for which I am the main author in the event.
    """
    return [
        BasicWorkInfoForAuthor(
            title=(
                'Aplicaciones de los Toros de Clifford en '
                'la Teoría de Códigos Correctores de Errores'
            ),
            track='math',
            id=2,
            stage=NoReviewStages.BEFORE_DEADLINE
        ),
        BasicWorkInfoForAuthor(
            title=(
                'Comparación del Rendimiento de Curve25519, '
                'P-256 y Curvas de Edwards en Algoritmos '
                'de Criptografía Cuántica'
            ),
            track='cibersecurity',
            id=2,
            stage=NoReviewStages.BEFORE_DEADLINE
        )

    ]
