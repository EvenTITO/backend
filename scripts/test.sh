docker compose -f docker-compose-dev.yaml exec backend bash -c "pip install httpx pytest pytest-mock; exec bash"
