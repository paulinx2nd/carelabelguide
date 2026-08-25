# Source Provenance

## Collection behavior

No external source is fetched. The label text and source reference are public publisher declarations; source_reference is explicitly unverified.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `75489b79d4177b372950b817f9e9baf27d279af48d9b6998693de903efa02734`
- ABI SHA-256: `312599ac1552685d64a803ae2010c41e61605b1a4f4dfd40a40bb462cf5125e8`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
