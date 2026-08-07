# Status and compatibility

TraceLogica is currently in architecture and protocol design.

Nothing in this repository is a stable compatibility promise unless it carries a
released version and is explicitly marked stable. Proposed endpoints, proof
fields, algorithms, limits, and operational behavior may change before the first
release.

## Planned compatibility policy

- Network, protocol, block, proof, and canonicalization formats are independently
  versioned.
- Finalized history remains verifiable under the rules active when it was created.
- Breaking changes require a new major protocol or format version.
- Deprecations include a published migration path and verification horizon.

Release notes and a support matrix will be added with the first implementation.
