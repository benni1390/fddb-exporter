# fddb-exporter

Prometheus exporter for [FDDB](https://fddb.info) (daily nutrition diary data).

Exports your daily nutrition data from FDDB as Prometheus metrics for monitoring and visualization in Grafana.

## Features

- Exports comprehensive nutrition metrics (calories, macros, vitamins, minerals)
- Automatic data fetching from FDDB
- Prometheus-compatible metrics endpoint
- Docker and Kubernetes ready
- Helm chart available

## Installation

### Helm (Kubernetes)

```bash
# Add Helm repository
helm repo add benni1390 https://benni1390.github.io/fddb-exporter-deployment
helm repo update

# Install with your FDDB credentials
helm upgrade --install fddb-exporter benni1390/fddb-exporter \
  --namespace monitoring --create-namespace \
  --set env.FDDB_USERNAME=your-username \
  --set env.FDDB_PASSWORD=your-password \
  --set image.tag=0.0.1
```

See [Helm chart documentation](https://github.com/benni1390/fddb-exporter-deployment) for more options.

### Docker

```bash
# Pull image
docker pull ghcr.io/benni1390/fddb-exporter:0.0.1

# Run with environment variables
docker run -d -p 8000:8000 \
  -e FDDB_USERNAME=your-username \
  -e FDDB_PASSWORD=your-password \
  -e SCRAPE_INTERVAL=3600 \
  ghcr.io/benni1390/fddb-exporter:0.0.1
```

### Docker Compose

```bash
# Copy environment template
cp .env.dist .env
# Edit .env with your credentials

# Start
docker compose up -d
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FDDB_USERNAME` | FDDB account username | *required* |
| `FDDB_PASSWORD` | FDDB account password | *required* |
| `EXPORTER_PORT` | HTTP port for metrics endpoint | `8000` |
| `SCRAPE_INTERVAL` | Data fetch interval in seconds | `3600` |
| `FDDB_DATE_OFFSET` | Days offset from today | `0` |
| `DEBUG_OUTPUT_DIR` | Directory for HTML debug dumps | *(optional)* |

### Empty Diary Handling

If no entries are tracked for the selected day, the exporter returns zero values for all metrics instead of failing. This allows continuous monitoring even on days without data.

## Metrics

Access metrics at `http://localhost:8000/metrics`

Example metrics:
- `fddb_calories_total` - Total calories
- `fddb_protein_g` - Protein in grams
- `fddb_carbs_g` - Carbohydrates in grams
- `fddb_fat_g` - Fat in grams
- `fddb_fiber_g` - Fiber in grams
- Plus vitamins, minerals, and micronutrients

## Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'fddb-exporter'
    static_configs:
      - targets: ['fddb-exporter.monitoring.svc.cluster.local:8000']
    scrape_interval: 5m
```

---

## Development

### Project Structure

```
fddb-exporter/
├── fddb_exporter/          # Python package
│   ├── fetcher.py          # FDDB data fetching
│   ├── parser.py           # HTML parsing
│   ├── metrics.py          # Prometheus metrics definitions
│   ├── updater.py          # Metrics updater
│   └── runner.py           # Main loop
├── exporter.py             # Entry point
├── tests/                  # Unit tests
├── fddb-exporter-deployment/ # Helm chart (symlink)
├── Dockerfile
├── docker-compose.yml
└── VERSION                 # Version file for releases
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
make test

# Run locally
python exporter.py
```

### Running Tests

```bash
# With Docker (recommended)
make test

# With coverage
make test-docker

# Direct
pytest -v
```

### Creating a Release

1. Update `VERSION` file with new version (e.g., `0.2.0`)
2. Commit and push to main (or merge PR)
3. Workflow automatically creates:
   - Git tag `v0.2.0`
   - GitHub release
   - Docker images: `0.2.0`, `0.2`, `0`, `latest`

### CI/CD

- **Tests**: Run on every PR via pytest workflow
- **Docker Build**: Builds and pushes images on tags
- **Release**: Automated via VERSION file changes

Images are published to: `ghcr.io/benni1390/fddb-exporter`

### Contributing

1. Create feature branch: `feature/your-feature`
2. Write tests for new features
3. Run tests: `make test`
4. Create PR to main branch

## License

See `LICENSE` file.


