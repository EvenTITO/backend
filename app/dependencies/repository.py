from app.dependencies.database.session_dep import SessionDep


def get_repositories(*repositories):
    """
    Returns a list of repository instances.
    Source Code: https://github.com/khalilSaidane/fastapi-project-template
    """

    def _get_repositories(session: SessionDep):
        instantiated_repositories = []
        for repo in repositories:
            instantiated_repositories.append(repo(session))
        return instantiated_repositories

    return _get_repositories


def get_repository(repository):
    async def _get_repository(session: SessionDep):
        return repository(session)

    return _get_repository
