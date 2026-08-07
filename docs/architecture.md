# System architecture

TraceLogica separates telemetry processing from integrity verification.

```text
Telemetry source
      |
      | OTLP over gRPC or HTTP
      v
Ingestion service -----> searchable span storage
      |
      v
Canonical batch -----> durable batch storage
      |
      v
Merkle commitment
      |
      v
TraceLogica blockchain -----> verification service
```

## Data plane

The data plane accepts, validates, searches, and retains spans. It can scale with
telemetry volume without forcing the blockchain to process every span as an
individual transaction.

## Evidence plane

The evidence plane canonicalizes accepted spans, constructs batch commitments,
orders commitments into blocks, and signs finalized state using versioned
cryptographic algorithms.

## Verification plane

The verification plane supplies the canonical record, inclusion path, commitment,
block header, and signature material needed by a verifier. Verification should be
possible without trusting the current contents of the searchable span database.

## Trust boundary

TraceLogica can prove that supplied data matches a finalized commitment. It cannot
prove that an instrumented application emitted truthful data, that every span was
submitted, or that a tenant configured instrumentation correctly.
