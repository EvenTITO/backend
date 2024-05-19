docker build -f ./Dockerfile -t backend:latest .
docker compose -f docker-compose-dev.yaml up --build -d
