# Reviewer Guide

## Mechanism in one sentence

A reusable care-label compiler that converts frozen label language into four canonical operations and then enforces a repeatable wash-bleach-dry-iron state automaton for registered items.

## What consensus actually decides

Validators agree on the complete canonical wash, bleach, dry, and iron profile.

## What code settles afterward

The item automaton rejects skipped stages and operations outside the compiled profile, then allows a fresh cycle after completion.

## Why this is distinct

Its core reusable mechanism is consensus compilation feeding a deterministic multi-cycle automaton.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

The contract does not inspect fabric, symbols, damage, machines, or manufacturer identity. MANUAL_REVIEW is a hold, not professional advice.
