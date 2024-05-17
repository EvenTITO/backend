docker build -f ./Dockerfile -t users:latest .
docker compose -f docker-compose-dev.yaml up --build -d
