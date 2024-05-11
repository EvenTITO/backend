[![codecov](https://codecov.io/gh/EvenTITO/users/graph/badge.svg?token=8HYPP8CZJ6)](https://codecov.io/gh/EvenTITO/users)

# Users

## Config pre-commit for autolint
```
pip install pre-commit
pre-commit install
```

## Tests
```bash
docker run -it -v $(pwd)/app:/code/app -v $(pwd)/tests:/code/tests eventito:latest bash
```

```bash
pip install pytest
pytest
```