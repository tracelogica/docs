# Glossary

**Account** — Customer identity derived from authentication and bound into every
receipt. It is not supplied in checkpoint JSON.

**Authority** — The single TraceLogica operator that durably orders checkpoints
and signs receipts in the MVP.

**Canonicalization** — Deterministic conversion of versioned fields to fixed
binary bytes for hashing and signing.

**Checkpoint** — Versioned, opaque commitment to a source evidence-chain head.

**Commitment** — SHA-256 value supplied by the source application and embedded
in a checkpoint.

**Global sequence** — One-based position of a receipt in the authority-wide
append order across accounts.

**Hash-linked receipt chain** — Ordering in which each receipt binds the hash of
the preceding receipt; genesis binds an all-zero previous hash.

**Idempotent replay** — Return of the exact stored receipt when the same account
retries an identical submission ID and checkpoint.

**Offline verifier** — Standalone program that checks retained receipts using a
trusted public-key document without calling MeshAI or TraceLogica.

**Public-key document** — Ed25519 public key plus its key ID, signature profile,
activation time, and optional retirement or compromise times.

**Receipt** — Timestamped, signed statement binding a checkpoint to an account,
network, sequence, preceding receipt, and signing-key profile.

**Signature profile** — Versioned definition of a signature algorithm and its
encoding. The only v1 profile is `ed25519-v1`.

**Source evidence chain** — Hash-linked evidence maintained by the customer
application. Its contents remain outside TraceLogica.

**Subject ID** — Opaque `hmac-sha256:` pseudonym supplied in a checkpoint instead
of a raw tenant identifier.
