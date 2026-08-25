# CareLabelGuide

A reusable care-label compiler that converts frozen label language into four canonical operations and then enforces a repeatable wash-bleach-dry-iron state automaton for registered items.

## Why GenLayer

Validators agree on the complete canonical wash, bleach, dry, and iron profile. The item automaton rejects skipped stages and operations outside the compiled profile, then allows a fresh cycle after completion.

## Roles

- label publisher
- item owner
- GenLayer validators

## Lifecycle

register label -> consensus compilation -> register item -> start cycle -> ordered stage records -> repeat or retire

## Contract interface

- Constructor: none
- Write methods: compile_label, record_stage, register_item, register_label, retire_item, retire_label, start_cycle
- View methods: get_item, get_item_count, get_item_id, get_label, get_label_count, get_label_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No external source is fetched. The label text and source reference are public publisher declarations; source_reference is explicitly unverified.

## Verification

```text
genvm-lint check contracts/care_label_guide.py
genvm-lint typecheck contracts/care_label_guide.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

The contract does not inspect fabric, symbols, damage, machines, or manufacturer identity. MANUAL_REVIEW is a hold, not professional advice.

Licensed under MIT. See `LICENSE`.
