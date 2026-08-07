# Product overview

Distributed traces help operators explain how a request moved through a system.
Conventional telemetry stores are optimized for search and retention, but their
contents can be edited or deleted by an administrator. TraceLogica adds a separate
cryptographic evidence layer so an authorized verifier can detect later changes.

TraceLogica is designed to:

1. Receive spans using OpenTelemetry protocols.
2. Store telemetry in systems optimized for search and retention.
3. Convert accepted spans into deterministic, content-addressed records.
4. Commit batches of records to a purpose-built evidence blockchain.
5. Return portable proofs that can be verified independently.

TraceLogica does not place complete spans on the blockchain. The chain records
compact commitments to off-chain batches, limiting disclosure and allowing the
telemetry store to scale independently.

## Intended users

- Engineering and site-reliability teams that need trustworthy trace history.
- Auditors who need evidence that a supplied trace matches an earlier commitment.
- Platform teams that need a standard OTLP ingestion path and independent proof
  verification.

## Non-goals

The initial product is not a cryptocurrency, proof-of-work network, general smart
contract platform, or replacement for access control, encryption, backups, and
retention governance.
