.PHONY: up down logs test build test-docker

# Run with Docker Compose
up:
	docker compose up --build

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
