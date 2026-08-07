# TraceLogica documentation

TraceLogica collects OpenTelemetry spans and produces independently verifiable,
tamper-evident commitments to that telemetry.

This repository contains customer-safe product and integration documentation.
The product is in its design phase; interfaces described here are proposals until
they are marked stable.

## Start here

- [Product overview](docs/overview.md)
- [Core concepts](docs/concepts.md)
- [System architecture](docs/architecture.md)
- [OpenTelemetry ingestion](docs/otlp-ingestion.md)
- [Proof verification](docs/proof-verification.md)
- [Security and cryptography](docs/security.md)
- [Brand guidelines](docs/brand.md)
- [Glossary](docs/glossary.md)
- [Status and compatibility](docs/status.md)

## Documentation boundary

This public repository intentionally excludes source code, credentials, private
infrastructure, operational runbooks, unreleased security analysis, and customer
data. Report suspected security issues using the process in [SECURITY.md](SECURITY.md).

![TraceLogica mark](assets/brand/tracelogica-mark.svg)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Documentation changes must not disclose
private implementation or infrastructure details.
