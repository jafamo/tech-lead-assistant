# Copilot Instructions — Tech Lead Assistant (TLA)

## Project context

Read these files before any task:

- `ai/context/architecture.md` — stack, structure, technical decisions.
- `ai/context/business.md` — what the app does and why.
- `ai/context/coding-standards.md` — code conventions.
- `ai/context/glossary.md` — domain terminology.

## Rules by area

- Backend / services: `ai/rules/backend.md`
- UI / pages: `ai/rules/ui.md`
- Security: `ai/rules/security.md`

## Feature specs (SDD)

Specs live in `ai/specs/NNN-name/` with `requirements.md`, `design.md`, `tasks.md`.
Read the full spec before writing code for a feature.

## Full specification

`docs/specifications/tech_lead_assistant_spec.md`

## OpenSpec workflow

Use OpenSpec for any non-trivial feature or change before writing code.

| Command | When to use |
|---|---|
| `/opsx:propose "description"` | Start a new feature — generates proposal, design and tasks |
| `/opsx:apply` | Implement what's in the active spec |
| `/opsx:explore` | Explore the codebase before proposing |
| `/opsx:sync` | Sync specs with the actual state of the code |
| `/opsx:archive` | Archive a completed change |

Active changes live in `.openspec/`. Permanent reference specs go in `ai/specs/NNN-name/`.

## Data root conventions

For agents operating on `data_root`, read `AGENTS.md` at the repo root.
