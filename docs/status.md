# Status and compatibility

TraceLogica has an implemented signed-checkpoint MVP and is currently
pre-release. It has not been deployed or published as a supported production
service.

The MVP is a separately operated, single-authority service. It accepts opaque,
versioned checkpoint commitments, appends them durably to a hash-linked SQLite
ledger, and returns timestamped Ed25519-signed receipts. A standalone verifier
can validate individual receipts and exported receipt chains without access to
the application database that created the original evidence.

The current implementation includes:

- authenticated, account-scoped checkpoint submission;
- deterministic, versioned checkpoint and receipt formats;
- durable append-before-success and exact idempotent replay;
- startup ledger and signing-key audits;
- public-key metadata and offline receipt-chain verification; and
- frozen compatibility vectors.

The MVP provides independently verifiable signed receipts from a separate
single authority. It is not a blockchain, decentralized consensus network,
independent-validator system, trusted external timestamp, or proof that source
evidence is true or complete.

Before the first release, the project still needs to finish operational,
retention, key-lifecycle, and separation decisions; exercise backup, restore,
credential-rotation, and incident procedures; complete release quality gates in
the target environment; and publish a supported version and deployment status.

Nothing in this repository is a stable compatibility promise unless it carries a
released version and is explicitly marked stable. Proposed endpoints, proof
fields, algorithms, limits, and operational behavior may change before the first
release.

## Planned compatibility policy

- Protocol, checkpoint, receipt, key, signature-profile, and canonicalization
  formats are independently versioned where applicable.
- Retained receipts remain verifiable under the rules and public-key material
  active when they were created.
- Breaking wire-format changes require a new protocol or format version.
- Deprecations include a published migration path and verification horizon.

Release notes and a support matrix will be added with the first supported
release.
