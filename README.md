# fddb-exporter

Prometheus exporter for FDDB (daily nutrition diary data).

This repository contains the exporter application, unit tests and deployment artifacts (Helm chart).

Quick start

- Copy environment template and fill values:

```bash
cp .env.dist .env
# edit .env
```

- Run locally with Docker Compose:

```bash
docker compose up --build
```

Important environment variables

- `FDDB_USERNAME` / `FDDB_PASSWORD` – FDDB account credentials
- `EXPORTER_PORT` – HTTP port for Prometheus metrics endpoint
- `DEBUG_OUTPUT_DIR` – optional: store HTML debug dumps

## CI / Releases

### Creating a new release

1. Update `VERSION` file with new version (e.g., `0.2.0`)
2. Commit and push to main (or merge PR)
3. Workflow automatically creates:
   - Git tag `v0.2.0`
   - GitHub release
   - Docker image with tags: `v0.2.0`, `0.2`, `0`, `latest`

### Using specific versions

```bash
# Docker
docker pull ghcr.io/benni1390/fddb-exporter:0.1.0

# Helm with specific image version
helm upgrade --install fddb-exporter benni1390/fddb-exporter \
  --set image.tag=0.1.0
```

Images and Helm charts are built and published by CI. Do not commit credentials.

Running tests

- Run unit tests locally via:

```bash
make test
# or
pytest -q
```

Project layout

- `fddb_exporter/` – package source code
- `exporter.py` – entry point used by Dockerfile
- `fddb-exporter-deployment/` – Helm chart and deployment artifacts
- `tests/` – unit tests

License

See `LICENSE` file.
