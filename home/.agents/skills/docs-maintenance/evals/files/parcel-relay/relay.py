"""Delivery configuration for Parcel Relay; no network access."""

DEFAULT_TIMEOUT_SECONDS = 30
MAX_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = 2
AUDIT_RETENTION_DAYS = 7
EXPORT_FORMAT = "JSONL"
QUEUE_STORAGE = "memory"
