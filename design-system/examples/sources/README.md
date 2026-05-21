# Canonical production diagram sources

This folder holds the original SVG/PNG files from docs.sui.io that the
annotated recreations in the parent folder are based on.

The files are not bundled with the design-system package. They live on
docs.sui.io and are subject to docusaurus build-hash rotation. Pull them
in with the included script:

```bash
./fetch-originals.sh
```

Or grab them by hand from the Production URLs listed in
[`../../../SOURCES.md`](../../../SOURCES.md).

## Why both formats?

| Format | Strength |
|---|---|
| Annotated HTML recreation (parent folder) | Compliance checklist and source code on the same page. Teaches Claude Design why each choice was made |
| Production SVG/PNG (this folder) | Pixel-perfect fidelity. Teaches Claude Design exactly what production-quality output looks like |

Claude Design ingests both during onboarding. Together they're stronger
training signal than either alone.

## License

Production diagrams from docs.sui.io are licensed under
[Creative Commons Attribution 4.0](https://github.com/MystenLabs/sui/blob/main/docs/site/LICENSE).
Recreations are derivative works under the same license.
