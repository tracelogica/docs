# Contributing

TraceLogica welcomes corrections and improvements to its public documentation.

## Before opening a change

- Keep examples free of real credentials, account identifiers, endpoints, and
  customer data.
- Do not publish internal infrastructure, operational procedures, private
  repository links, or unreleased vulnerabilities.
- Treat the signed single-authority checkpoint service as the current product.
  Clearly label blockchain, validator, OTLP, Merkle-proof, and post-quantum work
  as deferred, not implemented.
- Do not describe an interface as stable until a versioned release explicitly
  makes that promise.
- Preserve the product boundary: TraceLogica receives opaque commitments, not
  raw spans, prompts, names, or tenant identifiers.

## Style

- Use short sentences and descriptive headings.
- Define specialized terms on first use.
- Use `example.com` and obviously fictional identifiers in examples.
- State what a receipt proves and what it cannot prove.
- Describe v1 signatures exactly as Ed25519; do not make post-quantum claims.

Security reports do not belong in public issues. Follow [SECURITY.md](SECURITY.md).
