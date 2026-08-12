# System architecture

TraceLogica separates an application's evidence store from a narrow checkpoint
authority.

```text
Source application (currently MeshAI)
  evidence rows -> local hash chain -> transactional delivery outbox
                                      |
                                      | opaque checkpoint + bearer credential
                                      v
TraceLogica authority
  authentication -> validation -> durable SQLite append -> Ed25519 receipt
                                      |                    |
                                      v                    v
                              hash-linked ledger     retained receipt
                                                           |
                                      public-key document  |
                                                 \         /
                                                  v       v
                                                offline verifier
```

## Source boundary

MeshAI computes its evidence-chain head and a secret-keyed HMAC subject ID. Raw
spans, source evidence rows, prompts, customer names, and tenant ULIDs remain in
MeshAI. A transactional outbox lets local evidence processing continue while the
authority is unavailable and makes remote status explicit.

## Authority boundary

The HTTP service authenticates the account, validates the exact v1 checkpoint
shape, and commits before returning success. A single SQLite ledger uses WAL,
foreign keys, `synchronous=FULL`, and database triggers that reject updates or
deletes. Startup audits the complete chain, network metadata, key binding,
digests, and signatures before the service binds.

The sequence is global across authenticated accounts. A receipt binds account,
network, checkpoint, sequence, previous receipt hash, timestamp, key, and
signature profile. Byte-identical retries replay the stored receipt rather than
creating another sequence entry.

## Verification boundary

The customer retains receipts and the corresponding public-key document. The
standalone verifier recomputes canonical bytes and hashes, checks the Ed25519
signature, and can validate an export beginning at sequence 1 for gaps,
duplicates, genesis linkage, and network consistency.

## Availability and trust

There is one writable authority per ledger. This keeps the MVP operationally
small, but the authority can withhold new receipts, lose its database or key, or
misuse a compromised signing key. Backups, key protection, key-history
distribution, and operational separation therefore remain essential.

PostgreSQL, managed key signing, or replicated consensus are expansion options
only when recovery, concurrency, compliance, or independently administered
ordering requirements justify new architecture decisions.

See the [API quickstart](api-quickstart.md) for the implemented HTTP surface and
retry semantics.
