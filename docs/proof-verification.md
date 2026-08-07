# Proof verification

A TraceLogica proof package is intended to let a verifier answer:

> Does this canonical span record belong to the committed batch referenced by a
> finalized TraceLogica block?

## Planned proof package

- Protocol and canonicalization versions
- Hash and signature algorithm identifiers
- Canonical span record or its digest
- Leaf index and total leaf count
- Merkle sibling path
- Batch commitment metadata
- Finalized block header
- Validator signature material
- Network and chain identifiers

## Verification procedure

1. Canonicalize the supplied span using the declared version, if canonical bytes
   are not already provided.
2. Hash the domain-separated leaf representation.
3. Recompute the Merkle root using the leaf index and sibling path.
4. Compare it with the root in the batch commitment.
5. Recompute the commitment and block hashes.
6. Verify the block linkage and validator signatures under the declared protocol
   rules.
7. Confirm that the relevant key was valid for that block height.

## What a valid proof means

A valid proof demonstrates cryptographic inclusion in finalized history. It does
not establish the truth of the operation described by the span, completeness of
the trace, or authorization to disclose the span.

The binary proof format and test vectors remain under design and will be published
before being marked stable.
