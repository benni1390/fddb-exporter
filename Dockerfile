FROM python:3.11.14-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3-debian12@sha256:62214ec8dc220b42d244b471c6da1fe8017fdfeb361c8cf8d2ce254cd39def0c

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/venv/lib/python3.11/site-packages:/app"

# copy the application package into the virtualenv site-packages and the thin entrypoint script
COPY --chown=nonroot:nonroot fddb_exporter /opt/venv/lib/python3.11/site-packages/fddb_exporter
COPY --chown=nonroot:nonroot exporter.py /app/

WORKDIR /app
EXPOSE 8000
USER nonroot

ENTRYPOINT ["/usr/bin/python3.11"]
CMD ["/app/exporter.py"]
