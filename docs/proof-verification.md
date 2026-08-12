# Receipt verification

A TraceLogica v1 receipt lets a verifier answer:

> Did the trusted TraceLogica key sign this exact checkpoint and bind it to this
> account, network, sequence, authority-recorded time, and preceding receipt?

The checkpoint-service repository includes `tracelogica-verify`, a standalone
offline verifier. Verification requires the receipt and the corresponding trusted
public-key document; it does not require either MeshAI's query database or a live
TraceLogica service.

## Verify one receipt

```sh
tracelogica-verify receipt \
  --receipt receipt.json \
  --public-key public-key.json
```

The verifier validates the strict JSON shape and version identifiers, recomputes
the embedded checkpoint hash, constructs the fixed canonical receipt bytes,
recomputes the receipt hash, checks key lifecycle metadata, and verifies the
`ed25519-v1` signature.

## Verify a receipt chain

```sh
tracelogica-verify chain \
  --receipts receipts.jsonl \
  --public-key public-key.json
```

Chain verification accepts an ordered JSONL export beginning at global sequence
1. It additionally requires no sequence gaps or duplicates, a zero previous hash
for genesis, correct hash linkage, and one consistent `network_id`.

Exit code `0` means valid, `1` means a local I/O failure, and `2` means malformed
or invalid evidence.

## Trust the key separately

Signature verification is meaningful only if the verifier trusts the public key
and its lifecycle history. Retain the key document with receipt exports and
obtain it through an authenticated process. A compromise timestamp changes the
trust interpretation of historical signatures even though their bytes still
verify.

## What verification does not prove

A valid receipt proves the configured authority's signature and the integrity of
the fields it binds. It does not prove that source evidence is truthful or
complete, that the authority time is externally trusted, that no receipts were
withheld, or that the authority and key were uncompromised.

The v1 frozen compatibility vector fixes the canonical bytes, hashes, public key,
and signature for cross-language implementations. The public interface remains
pre-release until a supported version is published.

The [API quickstart](api-quickstart.md) describes receipt and public-key
retrieval before offline verification.
