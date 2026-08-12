# API quickstart

The checkpoint API is implemented but pre-release. TraceLogica has not published
a hosted base URL, issued customer credentials, or declared this interface
stable. The examples below describe the current v1 contract for local evaluation
and integration planning; replace the base URL and bearer token only with values
provided through an approved deployment process.

## Authentication

Checkpoint creation and receipt retrieval require:

```http
Authorization: Bearer <credential>
```

Provision bearer credentials from a cryptographically secure random source. The
runtime accepts 32–256 ASCII bytes and maps the SHA-256 digest of a credential to
one account. The account comes only from authentication and is never a request
field. Do not put credentials in source control, example files, URLs, or logs.

For the shell examples, set deployment-specific values without committing them:

```sh
export TRACELOGICA_BASE_URL="http://127.0.0.1:8080"
read -r -s TRACELOGICA_BEARER_TOKEN
export TRACELOGICA_BEARER_TOKEN
```

The loopback URL is an example for a locally operated service, not a hosted
TraceLogica endpoint. Unset the token when finished.

## Create a checkpoint

`POST /api/v1/checkpoints` accepts JSON bodies up to 16 KiB and rejects unknown
fields.

```json
{
  "protocol_version": "tracelogica.checkpoint.v1",
  "submission_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "subject_id": "hmac-sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "stream_id": "meshai.policy_evaluations",
  "source_checkpoint": "2026-08-12",
  "source_chain_version": 1,
  "commitment": {
    "algorithm": "sha256",
    "value": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Constraints:

- `protocol_version` must be exactly `tracelogica.checkpoint.v1`.
- `submission_id` must be `sha256:` followed by 64 lowercase hexadecimal
  characters.
- `subject_id` must be `hmac-sha256:` followed by 64 lowercase hexadecimal
  characters. It is an opaque pseudonym, not a raw tenant identifier.
- `stream_id` must be `meshai.policy_evaluations` or `meshai.audit_events`.
- `source_checkpoint` must contain 1–64 printable ASCII bytes.
- `source_chain_version` must be a nonzero unsigned 32-bit integer.
- `commitment.algorithm` must be `sha256`; `commitment.value` must be exactly 64
  lowercase hexadecimal characters.

Submit the fictional request:

```sh
curl --fail-with-body --silent --show-error \
  --request POST "$TRACELOGICA_BASE_URL/api/v1/checkpoints" \
  --header "Authorization: Bearer $TRACELOGICA_BEARER_TOKEN" \
  --header "Content-Type: application/json" \
  --data @- <<'JSON'
{
  "protocol_version": "tracelogica.checkpoint.v1",
  "submission_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "subject_id": "hmac-sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "stream_id": "meshai.policy_evaluations",
  "source_checkpoint": "2026-08-12",
  "source_chain_version": 1,
  "commitment": {
    "algorithm": "sha256",
    "value": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
  }
}
JSON
```

The first durable append returns `201 Created`, a `Location` header naming the
receipt resource, and a strict `SignedReceiptV1` in the `data` envelope. Success
is returned only after the SQLite transaction commits. This safe example shows
the complete response shape; its placeholder hashes and signature are not
cryptographically valid together:

```json
{
  "data": {
    "receipt_version": "tracelogica.receipt.v1",
    "receipt_id": "tlr_0123456789ABCDEFGHIJKLMNOP",
    "network_id": "tracelogica-dev",
    "account_id": "example-account",
    "global_sequence": 1,
    "accepted_at_unix_ms": 1786492800000,
    "previous_receipt_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "checkpoint_hash": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",
    "checkpoint": {
      "protocol_version": "tracelogica.checkpoint.v1",
      "submission_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "subject_id": "hmac-sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "stream_id": "meshai.policy_evaluations",
      "source_checkpoint": "2026-08-12",
      "source_chain_version": 1,
      "commitment": {
        "algorithm": "sha256",
        "value": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
      }
    },
    "key_id": "ed25519-dev-1",
    "signature_profile": "ed25519-v1",
    "receipt_hash": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "signature": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
  }
}
```

The receipt has exactly these 13 fields:

- `receipt_version` is exactly `tracelogica.receipt.v1`.
- `receipt_id` is `tlr_` followed by 26 uppercase letters or digits and identifies
  the retrieval resource.
- `network_id` identifies the authority ledger and is bound into the signature.
- `account_id` is the authenticated account, not a request-body value.
- `global_sequence` is the nonzero, authority-wide append position as an unsigned
  64-bit integer.
- `accepted_at_unix_ms` is the authority-recorded Unix time in milliseconds as a
  nonzero unsigned 64-bit integer. It is not an external trusted timestamp.
- `previous_receipt_hash` is the preceding receipt's 64-character lowercase
  SHA-256 hex digest. Sequence 1 uses 64 zeroes as the genesis value.
- `checkpoint_hash` is the 64-character lowercase SHA-256 digest of the fixed
  canonical bytes of the embedded checkpoint.
- `checkpoint` is the complete original strict checkpoint object described
  above. Consumers recompute its hash rather than trusting `checkpoint_hash`.
- `key_id` selects the public-key document needed to verify the receipt.
- `signature_profile` is exactly `ed25519-v1` in v1.
- `receipt_hash` is the 64-character lowercase SHA-256 digest of the canonical
  signed receipt core.
- `signature` is the 64-byte Ed25519 signature over that same canonical core,
  encoded as 86 base64url characters without padding.

Consumers should retain the complete receipt and the trusted public-key document
for its `key_id`, including lifecycle metadata. Do not retain only the signature
or hashes: verification also requires the embedded checkpoint and every signed
core field.

An identical retry for the same authenticated account and `submission_id`
returns the exact stored receipt with `200 OK`, the same `Location`, and:

```http
Idempotency-Replayed: true
```

Reusing that account and submission ID with different checkpoint data returns
`409 Conflict`.

## Retrieve a receipt

Receipt retrieval is authenticated and account-scoped. A receipt belonging to a
different account is indistinguishable from a missing receipt.

```sh
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer $TRACELOGICA_BEARER_TOKEN" \
  "$TRACELOGICA_BASE_URL/api/v1/checkpoints/tlr_0123456789ABCDEFGHIJKLMNOP"
```

`GET /api/v1/checkpoints/{receipt_id}` returns the same complete
`SignedReceiptV1` `data` schema shown above or `404`.

## Retrieve signing-key metadata

Signing-key metadata is public. Retrieval of the configured key is intentionally
not subject to the application rate limiter, so remote callers cannot exhaust a
shared allowance and prevent verifiers from fetching it. Requests for unknown
key IDs share a rate limit to bound probing.

```sh
curl --fail-with-body --silent --show-error \
  "$TRACELOGICA_BASE_URL/api/v1/signing-keys/ed25519-dev-1"
```

`GET /api/v1/signing-keys/{key_id}` returns a `data` object containing `key_id`,
`signature_profile`, base64url `public_key`, `activated_at_unix_ms`, and optional
`retired_at_unix_ms` and `compromised_at_unix_ms` values. A verifier must obtain
and trust key material through an authenticated process; this endpoint alone is
not an independent trust anchor.

## Check readiness

`GET /health` is public and reports whether the process is ready to serve.

```sh
curl --fail-with-body --silent --show-error \
  "$TRACELOGICA_BASE_URL/health"
```

A ready service returns `200 OK` with:

```json
{
  "data": {
    "status": "ok"
  }
}
```

## Errors

Errors use one stable envelope shape:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "request is invalid"
  }
}
```

| HTTP status | Code | Meaning |
| --- | --- | --- |
| `401` | `unauthorized` | Bearer authentication is missing, malformed, or unknown. |
| `404` | `not_found` | The route, key, or account-visible receipt was not found. |
| `409` | `idempotency_conflict` | The submission ID already names different checkpoint data. |
| `413` | `payload_too_large` | The request body exceeds 16 KiB. |
| `422` | `invalid_request` | JSON or the v1 checkpoint shape is invalid. |
| `429` | `rate_limited` | Account requests or unknown-key probes exceeded their limits. |
| `500` | `internal_error` | The service encountered an unexpected internal failure. |
| `503` | `service_unavailable` | Readiness, storage, or signing is unavailable. |

Clients should retry timeouts, `429`, and `5xx` responses with bounded backoff
and the same submission ID. Treat authentication, validation, and idempotency
conflicts as configuration or data errors rather than creating a new identity.

Run `unset TRACELOGICA_BEARER_TOKEN` after the example session.
