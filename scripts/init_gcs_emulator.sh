#!/bin/sh
set -e

# Wait for the emulator to be ready
echo "Waiting for GCS emulator to be ready..."
sleep 5

# Create required buckets
echo "Creating buckets in GCS emulator..."
curl -X POST "http://fake-gcs:4443/storage/v1/b" \
  -H "Content-Type: application/json" \
  -d '{"name": "events-bucket"}'

curl -X POST "http://fake-gcs:4443/storage/v1/b" \
  -H "Content-Type: application/json" \
  -d '{"name": "works-bucket"}'

curl -X POST "http://fake-gcs:4443/storage/v1/b" \
  -H "Content-Type: application/json" \
  -d '{"name": "certificates-bucket"}'

curl -X POST "http://fake-gcs:4443/storage/v1/b" \
  -H "Content-Type: application/json" \
  -d '{"name": "users-bucket"}'

echo "GCS emulator initialization complete."
