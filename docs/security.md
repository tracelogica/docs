# Security and cryptography

TraceLogica uses the term **quantum-resistant**, not quantum-proof. Cryptographic
algorithms and implementation guidance can change, so all formats carry explicit
algorithm and version identifiers.

## Planned cryptographic profile

- Post-quantum signatures based on ML-DSA, standardized in
  [NIST FIPS 204](https://doi.org/10.6028/NIST.FIPS.204).
- A SHA-3-family hash with an output length selected by the final protocol profile
  for records, Merkle nodes, commitments, and block linkage.
- Domain separation between every hashed object type.
- Explicit network, chain, tenant, sequence, and version binding in signed data.
- Cryptographic agility so future protocol upgrades can introduce new algorithms
  without reinterpreting old blocks.

The first release may use a hybrid signature profile during migration, subject to
implementation and interoperability testing.

## Security properties

The design targets:

- Detection of changes to committed canonical records
- Authenticated block production
- Deterministic independent proof verification
- Protection against cross-network and cross-object proof substitution
- Auditable key and protocol-version history

## Explicit limitations

- Integrity is not confidentiality. Telemetry still requires encryption in
  transit, encryption at rest, authorization, and data minimization.
- A commitment proves inclusion, not that input was accurate or complete.
- A TraceLogica-operated validator set provides replicated finality, not independent
  organizational decentralization.
- Security depends on correct canonicalization, key protection, node operation,
  and verifier implementation as well as cryptographic primitives.
