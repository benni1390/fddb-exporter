.PHONY: up down logs test build test-docker

# Run with Docker Compose
up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

# Run unit tests with coverage in docker (no quick curl check)
test:
	@echo "--- running unit tests (docker) ---"
	docker run --rm -v $(CURDIR):/src -w /src -e PYTHONPATH=/src python:3.11-slim \
		bash -lc "pip install -r requirements.txt coverage pytest && coverage run -m pytest && coverage report -m"

# Build (use docker compose so others can use the compose workflow)
# Use: `make build` to build images defined in docker-compose.yml
build:
	docker compose build

# Run unit tests in a disposable Docker container (no local pip installs)
# Usage: `make test-docker` - runs tests and prints coverage report
test-docker:
	docker run --rm -v $(CURDIR):/src -w /src -e PYTHONPATH=/src python:3.11-slim \
		bash -lc "pip install -r requirements.txt coverage pytest && coverage run -m pytest && coverage report -m"

# NOTE: Pushing images should be performed by CI (do not push from local)
