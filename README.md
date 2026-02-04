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

### Daily Nutrition Metrics

- `fddb_energy_kj` - Energy in kilojoules
- `fddb_energy_kcal` - Energy in kilocalories
- `fddb_fat_grams` - Fat in grams
- `fddb_carbohydrates_grams` - Carbohydrates in grams
- `fddb_sugar_grams` - Sugar in grams
- `fddb_protein_grams` - Protein in grams
- `fddb_alcohol_grams` - Alcohol in grams
- `fddb_water_liters` - Water in liters
- `fddb_fiber_grams` - Fiber in grams
- `fddb_cholesterol_mg` - Cholesterol in milligrams
- `fddb_salt_grams` - Salt in grams

### Vitamin Metrics

- `fddb_vitamin_c_mg` - Vitamin C in milligrams
- `fddb_vitamin_a_mg` - Vitamin A in milligrams
- `fddb_vitamin_d_mg` - Vitamin D in milligrams
- `fddb_vitamin_e_mg` - Vitamin E in milligrams
- `fddb_vitamin_b1_mg` - Vitamin B1 (Thiamine) in milligrams
- `fddb_vitamin_b2_mg` - Vitamin B2 (Riboflavin) in milligrams
- `fddb_vitamin_b6_mg` - Vitamin B6 in milligrams
- `fddb_vitamin_b12_mg` - Vitamin B12 in milligrams

### Mineral Metrics

- `fddb_iron_mg` - Iron in milligrams
- `fddb_zinc_mg` - Zinc in milligrams
- `fddb_magnesium_mg` - Magnesium in milligrams
- `fddb_manganese_mg` - Manganese in milligrams
- `fddb_fluoride_mg` - Fluoride in milligrams
- `fddb_chloride_mg` - Chloride in milligrams
- `fddb_copper_mg` - Copper in milligrams
- `fddb_potassium_mg` - Potassium in milligrams
- `fddb_calcium_mg` - Calcium in milligrams
- `fddb_phosphorus_mg` - Phosphorus in milligrams
- `fddb_sulfur_mg` - Sulfur in milligrams
- `fddb_iodine_mg` - Iodine in milligrams

### Reference Values (D-A-CH Guidelines)

Reference values based on D-A-CH recommendations (German, Austrian, Swiss nutrition societies) for adults:

- `fddb_vitamin_c_reference_mg` - Reference: 100 mg/day
- `fddb_vitamin_a_reference_mg` - Reference: 0.85 mg/day
- `fddb_vitamin_d_reference_mg` - Reference: 0.020 mg/day (20 µg)
- `fddb_vitamin_e_reference_mg` - Reference: 12 mg/day
- `fddb_vitamin_b1_reference_mg` - Reference: 1.2 mg/day
- `fddb_vitamin_b2_reference_mg` - Reference: 1.3 mg/day
- `fddb_vitamin_b6_reference_mg` - Reference: 1.4 mg/day
- `fddb_vitamin_b12_reference_mg` - Reference: 0.004 mg/day (4 µg)
- `fddb_iron_reference_mg` - Reference: 12.5 mg/day
- `fddb_zinc_reference_mg` - Reference: 9 mg/day
- `fddb_magnesium_reference_mg` - Reference: 350 mg/day
- `fddb_calcium_reference_mg` - Reference: 1000 mg/day
- `fddb_potassium_reference_mg` - Reference: 4000 mg/day
- `fddb_phosphorus_reference_mg` - Reference: 700 mg/day
- `fddb_iodine_reference_mg` - Reference: 0.200 mg/day (200 µg)
- `fddb_selenium_reference_mg` - Reference: 0.060 mg/day (60 µg)

**Note**: Reference values are adult averages. Actual requirements vary by age, gender, and individual circumstances. Source: D-A-CH reference values (DGE, ÖGE, SGE/SSN).

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


