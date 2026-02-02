# FDDB Prometheus Exporter

![pytest](https://github.com/benni1390/fddb-exporter/actions/workflows/pytest.yml/badge.svg) ![docker-publish](https://github.com/benni1390/fddb-exporter/actions/workflows/docker-publish.yml/badge.svg) ![docker-build](https://github.com/benni1390/fddb-exporter/actions/workflows/docker-build.yml/badge.svg) ![docker](https://github.com/benni1390/fddb-exporter/actions/workflows/docker.yml/badge.svg)

Prometheus-Exporter für FDDB (Tagebuch‑Nährwertdaten).

Image: `ghcr.io/benni1390/fddb-exporter`

Kurz (Quick Start)

```bash
cp .env.dist .env     # .env ausfüllen
make build             # baut Image (docker compose build)
docker compose up -d   # startet den Container
# Test
curl http://localhost:8000/metrics | grep '^fddb_'
```

Wichtige Umgebungsvariablen (Kurz)

- `FDDB_USERNAME` – FDDB Login‑Email (required)
- `FDDB_PASSWORD` – FDDB Passwort (required)
- `EXPORTER_PORT` – Default: 8000
- `SCRAPE_INTERVAL` – Default: 300
- `FDDB_DATE_OFFSET` – 0 = heute, -1 = gestern
- `DEBUG_OUTPUT_DIR` – optional: HTML‑Dumps für Debug

Build & Release

- Lokales Build: `make build`
- Push/Publish: über CI (nicht lokal). Setze im Repo Secrets: `GITHUB_TOKEN` (standard) oder `CR_PAT` für alternative PAT.

Kubernetes

Manifeste werden in einem separaten Repo verwaltet:
`benni1390/fddb-exporter-deployment`

License

MIT

Author & Maintainer

- Benjamin Drews — Maintainer
- GitHub: https://github.com/benni1390
- Contact: via GitHub profile
