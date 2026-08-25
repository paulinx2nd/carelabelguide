# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators agree on the complete canonical wash, bleach, dry, and iron profile. The item automaton rejects skipped stages and operations outside the compiled profile, then allows a fresh cycle after completion.
- External world: No external source is fetched. The label text and source reference are public publisher declarations; source_reference is explicitly unverified.

## Event path

register label -> consensus compilation -> register item -> start cycle -> ordered stage records -> repeat or retire

## Actors

- label publisher
- item owner
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

The item automaton rejects skipped stages and operations outside the compiled profile, then allows a fresh cycle after completion. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `75489b79d4177b372950b817f9e9baf27d279af48d9b6998693de903efa02734`.
