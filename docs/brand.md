# Brand guidelines

TraceLogica's identity represents telemetry paths converging into independently
verifiable history. The primary mark combines three inputs, a verification point,
and a persistent ledger stroke.

The current identity is a version-one candidate and may be refined before general
availability.

## Name

Write the product name as **TraceLogica**, with a capital `T` and `L`. Do not use
`Tracelogica`, `Trace Logica`, or all capitals in prose.

## Positioning line

Preferred short description:

> Verifiable telemetry, committed to history.

Descriptive alternative:

> Quantum-resistant integrity proofs for OpenTelemetry traces.

Do not claim that TraceLogica proves telemetry is truthful, prevents every form of
tampering, or is absolutely quantum-proof.

## Logo assets

- [`tracelogica-mark.svg`](../assets/brand/tracelogica-mark.svg) — primary
  transparent vector mark for light surfaces.
- [`tracelogica-mark-dark.svg`](../assets/brand/tracelogica-mark-dark.svg) — square
  dark treatment for GitHub and application avatars.
- [`tracelogica-github.png`](../assets/brand/tracelogica-github.png) — 512 px square
  PNG prepared for the GitHub organization avatar.
- [`tracelogica-mark.png`](../assets/brand/tracelogica-mark.png) — transparent
  high-resolution raster concept for compatibility and exploration.

Keep clear space around the mark equal to the width of one input terminal. Do not
rotate it, stretch it, add effects, recolor individual paths, place it on a noisy
image, or combine it with chain links, coins, locks, and quantum-orbit imagery.

## Color

| Token | Hex | Use |
|---|---|---|
| Midnight | `#08131F` | Primary background and text |
| Verification cyan | `#21D4C2` | Mark, links, active state |
| Ice | `#C9FFF7` | Dark-surface highlight |
| Cloud | `#F4F8FA` | Light background |
| Slate | `#52616B` | Secondary text |
| Evidence amber | `#F2B84B` | Warnings and pending finality only |

Cyan must not be the only indication of state. Pair color with text, shape, or an
icon that remains understandable without color perception.

## Typography

Use a neutral sans-serif with strong technical legibility for interfaces and
prose. Until final font licensing is selected, prefer the system font stack:

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", sans-serif;
```

Use a monospace font only for identifiers, hashes, code, and protocol fields.

## Voice

TraceLogica communicates with precision and restraint:

- Say what is verifiable and state what is not.
- Prefer concrete protocol language over blockchain hype.
- Use quantum-resistant instead of quantum-proof.
- Avoid claims of absolute immutability when validators share an operator.
- Explain evidence in terms an auditor or engineer can reproduce.

## GitHub treatment

Use the dark square mark for the organization avatar. Repository social previews
should pair the mark with the repository name and one factual description; do not
place dense architecture diagrams or implementation details in public previews.

## Landing-page direction

Use a dark technical canvas with generous spacing and restrained cyan accents.
The hero should lead with the positioning line, explain OTLP ingestion and proof
verification, and illustrate the path from spans to Merkle commitment to finalized
block. Avoid finance, coin, mining, and science-fiction imagery.
