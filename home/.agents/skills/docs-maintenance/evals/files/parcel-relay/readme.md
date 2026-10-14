# Parcel Relay

The current timeout is 60 seconds. There are 3 attempts, with a 2-second backoff between attempts.

Parcel Relay forwards queued webhook deliveries to HTTPS destinations for internal event consumers.
It uses an in-memory queue. Persistent storage is not implemented.

The launch decision was to use one process per destination. The example destination label is `relay-west`.

Audit records are retained for 7 days. Audit records are retained for 7 days.
Exports use JSONL. Read [retention](docs/retention.md) before exporting audit records.

```text
Warning: Clearing the queue permanently deletes undelivered events; export the audit records and confirm the destination before proceeding.
```

Do not shorten the retry budget when rewriting this guide.
Retry budget means 3 attempts total, not 3 retries.

Operators configure delivery settings; consumers receive forwarded events.
No persistent storage is available.
