# Core concepts

## Span

An OpenTelemetry span represents one operation in a distributed trace. Related
spans share a trace identifier and form parent-child relationships.

## Canonical record

Equivalent span input must produce the same byte sequence before hashing. This
deterministic representation is called the canonical record. Its version is part
of the proof so verifiers know exactly which rules to apply.

## Batch

A batch is an ordered collection of canonical span records accepted during a
bounded interval or until a configured size is reached.

## Merkle tree

Each canonical record is hashed into a leaf. Hashing pairs of nodes repeatedly
produces one Merkle root that commits to every leaf in the batch. A verifier needs
only the record, its position, and a logarithmic-size path of sibling hashes to
recompute that root.

## Commitment

A commitment binds a Merkle root to context such as tenant, sequence, time range,
record count, canonicalization version, and cryptographic algorithm identifiers.

## Block

A block contains one or more commitments and the hash of the previous finalized
block. Validator signatures attest that the block passed the protocol's validation
rules.

## Inclusion proof

An inclusion proof shows that a particular canonical record contributed to a
Merkle root finalized in a block. It proves inclusion and detects changes; it does
not prove that the original telemetry was factually true.

## Finality

Finality is the point after which the network treats a block as committed. The
initial TraceLogica network is permissioned and operated by TraceLogica.
