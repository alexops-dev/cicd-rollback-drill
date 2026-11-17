# cicd-rollback-drill
A reproducible CI/CD lab that detects a broken release, restores the previous version, and verifies recovery. Runs locally with Docker Compose and in GitHub Actions.

Start the stable container
docker run --rm --name catalog-stable \
  -p 127.0.0.1:8080:8000 \
  -e RELEASE_VERSION=v1 \
  catalog-api:dev


Now start a broken candidate from the same image. Keep the stable container running and execute this in another terminal.
docker run --rm --name catalog-candidate \
  -p 127.0.0.1:8081:8000 \
  -e RELEASE_VERSION=v2 \
  -e PRODUCT_LOOKUP_FAILS=true \
  catalog-api:dev