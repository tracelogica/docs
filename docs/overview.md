# Product overview

Applications often maintain hash-linked evidence inside their own database. That
evidence can detect changes, but an operator that controls both the data and the
database remains inside the trust boundary. TraceLogica adds a separate signing
authority at the evidence-chain boundary.

The current MVP:

1. Accepts an authenticated, opaque SHA-256 checkpoint commitment.
2. Appends it to one durable, globally ordered authority log.
3. Returns a timestamped, hash-linked Ed25519-signed receipt.
4. Publishes signing-key metadata for offline receipt verification.

MeshAI is the first consumer. It submits commitments to its evidence-chain heads,
not the evidence itself. TraceLogica does not receive raw telemetry, spans,
prompts, customer names, or tenant ULIDs.

## What a receipt establishes

A valid receipt establishes that the configured TraceLogica authority signed a
specific versioned checkpoint, recorded it at the stated authority time, and
placed it at the stated position in its receipt sequence. Because the receipt and
public key are portable, verification does not depend on MeshAI's application
database or a live TraceLogica API.

A receipt does not establish:

- that the underlying evidence is accurate or complete;
- that the recorded time came from an external trusted timestamping service;
- that the authority was uncompromised or could not withhold new receipts; or
- that multiple independent parties agreed on the ordering.

## Intended users

- Product and platform teams that need portable evidence-chain checkpoints.
- Auditors who need to validate retained receipts offline.
- Security teams evaluating the boundary between a source application and a
  separate signing authority.

## Current non-goals

The MVP is not a blockchain, cryptocurrency, consensus network, raw telemetry
store, search platform, or post-quantum system. OTLP ingestion, Merkle proofs for
individual spans, validators, and public-chain publication are deferred.

Continue with the [API quickstart](api-quickstart.md) for the current HTTP
contract or [core concepts](concepts.md) for the receipt model.
