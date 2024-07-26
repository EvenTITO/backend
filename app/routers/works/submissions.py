from fastapi import APIRouter
from app.schemas.works.submission import Submission, SubmissionWithId
from app.schemas.works.author import AuthorInformation

submissions_router = APIRouter(
    prefix="/events/{event_id}/works/submissions",
    tags=["Works Submissions"]
)


@submissions_router.put("/latest", status_code=204)
async def update_latest_submission(submission: Submission):
    """
    Updates the work with work_id. The update is always made to
    the latest version of the work: the latest submission.
    If the work stage changes, it creates a new submission.
    """
    # TODO
    pass


@submissions_router.get("/{submission_id}")
async def get_submission(submission_id: int) -> SubmissionWithId:
    """
    Get the submission with submission_id.
    """
    # TODO
    return SubmissionWithId(
        id=2,
        abstract=(
            "Este trabajo explora los toros de Clifford y su aplicación en la "
            "teoría de códigos correctores de errores. Los toros de Clifford, "
            "con sus propiedades topológicas y geométricas únicas, permiten "
            "el diseño de códigos que mejoran la eficiencia y robustez en la "
            "detección y corrección de errores en sistemas de comunicación "
            "digital. Se presenta un marco teórico que aprovecha la simetría "
            "y periodicidad de estos toros para simplificar la codificación y "
            "decodificación, demostrando mejoras significativas en "
            "comparación con los métodos tradicionales."
        ),
        keywords=['math', 'topology', 'Clifford Torus', 'Complex Spaces'],
        authors=[
            AuthorInformation(
                full_name='Juan Sanchez',
                membership='FIUBA',
                mail='juansanchez@mail.com'
            ),
            AuthorInformation(
                full_name='Julian Altocapo',
                membership='Exactas',
                mail='julianaltocapo@mail.com'
            )
        ]
    )
