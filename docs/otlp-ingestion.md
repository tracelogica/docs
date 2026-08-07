# OpenTelemetry ingestion

TraceLogica plans to accept spans using the OpenTelemetry Protocol (OTLP) over
gRPC and HTTP. Exact endpoints, authentication headers, limits, and retry behavior
will be published with the first supported release.

## Expected client behavior

- Use an OpenTelemetry SDK or Collector with bounded queues and retry behavior.
- Send trace data only to the tenant endpoint and credentials assigned to it.
- Avoid placing secrets or unnecessary personal data in span attributes.
- Treat successful ingestion as acceptance for processing, not immediate
  blockchain finality.

## Processing states

An accepted span progresses through these conceptual states:

1. `accepted` — input passed transport and tenant validation.
2. `stored` — the searchable representation was persisted.
3. `batched` — a canonical record was assigned to a commitment batch.
4. `finalized` — the batch commitment was finalized in a block.

The future API will expose enough information to distinguish ingestion acceptance
from cryptographic finality.

## Compatibility

OpenTelemetry permits arbitrary attributes and evolving semantic conventions.
TraceLogica therefore versions its canonicalization rules and preserves the
distinction between absent values, empty values, numeric types, byte values, and
repeated values.
