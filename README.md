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

CI / Releases

- Images and Helm charts are built and published by CI. Do not commit credentials.
- Configure repository secrets for publishing (e.g. `GITHUB_TOKEN` or `CR_PAT`).

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
