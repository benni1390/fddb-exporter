#!/usr/bin/env python3
import sys
import requests

# keep the stdout unbuffer wrapper for docker logs
if __name__ == '__main__':
    try:
        sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)
    except Exception:
        pass

# Re-export key functions from the modular package for backwards compatibility
from fddb_exporter.updater import extract_number, update_metrics
from fddb_exporter.parser import parse_fddb_data
from fddb_exporter.fetcher import fetch_fddb_data

# Thin wrapper to maintain original entrypoint
from fddb_exporter.runner import main

__all__ = [
    'extract_number', 'parse_fddb_data', 'update_metrics', 'fetch_fddb_data', 'main'
]

if __name__ == '__main__':
    main()
