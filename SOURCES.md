# Sources for Design System Examples

Each example in `design-system/examples/` is one of the following:

- A faithful recreation of a diagram that is live on docs.sui.io.
- An anti-example showing a diagram from the live docs that does not
  pass the current standards. (Anti-examples exist as cautionary
  references so Claude Design knows what to avoid.)

Production diagrams from docs.sui.io are licensed under
[CC BY 4.0](https://github.com/MystenLabs/sui/blob/main/docs/site/LICENSE)
and used here with attribution.

## Compliant examples (pattern-match against these)

### `examples/architecture-data-serving.html`

| Field | Value |
|---|---|
| Canonical source | https://docs.sui.io/develop/accessing-data/data-serving |
| Source file | `access-interfaces_accessing-data_v1.svg` |
| Production URL | https://docs.sui.io/assets/images/access-interfaces_accessing-data_v1-ac73a55a4128a0ab18137b0e097cbb95.svg |
| Status | Cited by the standards page as an exemplar architecture diagram. |
| Recreation fidelity | Layout, colors, and shape semantics match. Recreated from the standards page description and the live page; minor pixel-level differences are possible. |

### `examples/sequence-transaction.html`

| Field | Value |
|---|---|
| Canonical source | https://docs.sui.io/guides/developer/transactions/transaction-lifecycle |
| Source file | `transaction-lifecycle_transactions_v1.png` |
| Production URL | https://docs.sui.io/assets/images/transaction-lifecycle_transactions_v1-dd22c5ca774fb65a8e83ce73fc95ef5c.png |
| Status | Cited by the standards page as an exemplar sequence diagram. |
| Recreation fidelity | Swimlanes, fan-out arrows, phase bars, and step-label colors match. The numbered step labels and phase names come from the live page. |

### `examples/context-sui-network.html`

| Field | Value |
|---|---|
| Canonical source | None (synthetic example) |
| Status | Built to the standard. No direct counterpart on docs.sui.io because Sui does not currently publish a Level 1 context diagram of the full network. |
| Use | Reference for what a brand-compliant Level 1 looks like when one needs to be authored. |

## Anti-examples (do NOT pattern-match against these)

### `examples/anti-example-transactions-flowchart.html`

| Field | Value |
|---|---|
| Canonical source | https://docs.sui.io/concepts/transactions |
| Source file | `transactions.mdx` |
| GitHub URL | https://github.com/MystenLabs/sui/blob/main/docs/content/concepts/transactions.mdx |
| Status | Off-palette fills (`fill:#f225` and `fill:#ff43` are 8-digit ARGB hex outside the Sui palette), and the diagram predates the current standard. |
| Use | Cautionary example. The non-compliant panel shows how this diagram appears on the current docs site; the compliant panel shows the corrected version. Claude Design pattern-matches against the compliant panel only. |

## Why the originals are not bundled directly

The egress proxy used to build this package cannot reach `docs.sui.io`
or `raw.githubusercontent.com` directly. To include the original
production SVG and PNG files alongside the recreations, complete the
following.

1. Open each Production URL above in a browser.
2. Right-click and save the image into `design-system/examples/sources/`
   using the filename in the Source file column.
3. The recreations and originals then sit side by side. Either is a
   valid signal for Claude Design.

A one-line script that does the same thing:

```bash
mkdir -p design-system/examples/sources
curl -sL "https://docs.sui.io/assets/images/access-interfaces_accessing-data_v1-ac73a55a4128a0ab18137b0e097cbb95.svg" -o design-system/examples/sources/access-interfaces_accessing-data_v1.svg
curl -sL "https://docs.sui.io/assets/images/transaction-lifecycle_transactions_v1-dd22c5ca774fb65a8e83ce73fc95ef5c.png" -o design-system/examples/sources/transaction-lifecycle_transactions_v1.png
```

The hashes in those URLs are docusaurus build fingerprints and might
shift on re-deploys. If a 404 comes back, open the corresponding page
on docs.sui.io, right-click the diagram, and copy the new image URL.

## Adding more compliant production examples

When other diagrams in the live docs are updated to the current
standard, complete the following.

1. Add a row under "Compliant examples" with the page URL, source file,
   and production URL.
2. Drop the source file into `design-system/examples/sources/`, or use
   the `curl` pattern above.
3. Optionally, build an annotated HTML version in
   `design-system/examples/` that mirrors the format of the existing
   files.

When a diagram in the live docs is non-compliant but flagged for
cleanup, complete the following.

1. Add it under "Anti-examples" with a one-line note about which rule it
   violates.
2. This is high-signal training data. Claude Design needs to know which
   live-doc diagrams to ignore, not only which to imitate.
