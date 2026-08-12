# Core concepts

## Source evidence chain

The customer application maintains its own hash-linked evidence. TraceLogica does
not store or validate the underlying evidence; it receives only a commitment to a
chain head.

## Checkpoint

A checkpoint is a strict, versioned request containing an opaque subject ID,
source stream and chain version, submission ID, source checkpoint label, and a
SHA-256 commitment. In v1, the supported streams are MeshAI policy evaluations
and audit events. The authenticated account is derived from the bearer credential
and is never accepted from request JSON.

## Canonicalization

Checkpoint and receipt fields are converted to fixed binary bytes before
hashing or signing. Domain separation, fixed field order, length-prefixed UTF-8
strings, fixed-width integers, and decoded 32-byte hashes make the result
deterministic across implementations. JSON serialization is not signed directly.

## Receipt

A receipt embeds the submitted checkpoint and binds it to the authenticated
account, authority network, global sequence, authority-recorded time, preceding
receipt hash, signing key, and signature profile. The `ed25519-v1` signature
covers the canonical receipt core.

## Authority log

The MVP has one signing authority and one global append sequence. Each receipt
contains the preceding receipt hash, forming a hash-linked log across accounts.
SQLite provides the authority's durable ordering; it is not a distributed
consensus system or an independent witness.

## Idempotency

Within an account, a repeated submission ID with the identical checkpoint
returns the exact stored receipt. Reusing that ID for different checkpoint data
is rejected.

## Public-key document

A public-key document identifies the Ed25519 key and its activation, retirement,
and compromise metadata. A verifier must obtain and retain trusted key material
through an authenticated channel; fetching a key from the same service at
verification time does not create an independent trust anchor.

## Offline verification

The standalone verifier checks an individual receipt or an ordered JSONL chain
using retained receipts and public-key metadata. Verification proves signature
and binding integrity under the trusted key. It does not prove the truth or
completeness of the source evidence.

See the [API quickstart](api-quickstart.md) for the checkpoint request and HTTP
response contract.
