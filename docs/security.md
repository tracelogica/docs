# Security and cryptography

TraceLogica v1 uses SHA-256 commitments and hashes plus Ed25519 signatures under
the explicit `ed25519-v1` profile. It makes no post-quantum claim.

## Security properties

- Fixed binary canonicalization prevents JSON representation differences from
  changing what is signed.
- Domain-separated checkpoint and receipt formats bind their exact v1 fields.
- Every receipt binds the authenticated account, network, global sequence,
  preceding receipt hash, checkpoint hash, authority time, key ID, and signature
  profile.
- Commit-before-success and exact idempotent replay prevent an acknowledged
  receipt from representing an uncommitted append.
- Startup audit and database mutation triggers make accidental or unauthorized
  ledger changes detectable at the authority boundary.
- Offline verification removes the live API and source application's query
  database from the verification path.

## Privacy boundary

The checkpoint contains opaque identifiers and SHA-256 commitments, not source
evidence. MeshAI derives the subject ID with a secret-keyed HMAC and does not send
raw spans, prompts, customer names, or tenant ULIDs. TraceLogica still observes
the authenticated account, stream type, submission timing, and commitment
frequency; that metadata is confidential operational data.

Bearer credentials are sent in the `Authorization` header. Provisioning requires
high-entropy values from a cryptographically secure random source; the runtime
itself validates only that a token contains 32–256 ASCII bytes. The authority
configuration stores SHA-256 credential digests rather than raw keys. Transport
security, secret delivery, logging hygiene, and access controls remain deployment
responsibilities. See the [API quickstart](api-quickstart.md) for the request
boundary.

## Explicit limitations

- One authority controls ordering and signing. It can withhold receipts or misuse
  a compromised key.
- The authority-recorded timestamp is not an external trusted timestamp.
- Hash linkage detects modification when receipts or trusted exports are
  available; it does not make the authority database immutable against its
  operator.
- A valid receipt proves a signed commitment, not source accuracy, completeness,
  availability, or authorization to disclose source data.
- The single ledger and filesystem signing key require tested backup, recovery,
  and compromise procedures. The current service does not provide HSM/KMS
  signing or online multi-key rotation.

Algorithm changes, managed-key operation, or independent consensus require new
versioned profiles, interoperability vectors, migration design, and an updated
threat model. They must not reinterpret existing `ed25519-v1` receipts.
