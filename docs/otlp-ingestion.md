# OpenTelemetry ingestion scope

TraceLogica does not accept OpenTelemetry Protocol (OTLP) traffic in the current
MVP. It has no OTLP/gRPC or OTLP/HTTP endpoint, span store, trace search API,
canonical span format, or per-span Merkle proof.

MeshAI may derive evidence from application activity, but only opaque checkpoint
metadata and SHA-256 commitments cross the TraceLogica boundary. Raw spans,
telemetry attributes, prompts, customer names, and tenant ULIDs are not part of
the checkpoint request.

The implemented HTTP surface is limited to:

- authenticated checkpoint creation at `POST /api/v1/checkpoints`;
- authenticated, account-scoped receipt retrieval at
  `GET /api/v1/checkpoints/{receipt_id}`;
- public signing-key metadata at `GET /api/v1/signing-keys/{key_id}`; and
- readiness at `GET /health`.

See the [API quickstart](api-quickstart.md) for request fields, authentication,
responses, and errors.

Raw OTLP ingestion and span-level proofs are deferred platform ideas, not current
interfaces or roadmap commitments. Adding them would require a new architecture
decision, privacy and threat-model review, versioned formats, and compatibility
tests.
