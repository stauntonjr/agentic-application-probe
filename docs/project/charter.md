# Project charter

Status: active

## Purpose

A small deterministic CSV summary CLI used to measure greenfield delivery through the agentic project template.

Primary users:

- maintainer
- data analyst

## Outcomes and success measures

Desired outcomes:

- Summarize a local CSV file as deterministic JSON

Success measures:

- Normal and malformed CSV behavior is tested
- The repository authoritative check passes

## Scope

### In

- UTF-8 CSV input
- Row count
- Column names
- Missing-value counts
- JSON stdout

### Out

- Network access
- CSV dialect inference
- Streaming-scale files
- Data cleaning
- Deployment

## Constraints

- Security: No secrets in the repository
- Data classification: public
- Deployment: local CLI only
- Budget: TBD
- Licensing: MIT

## Engineering and release contract

- Primary check: make smoke
- Dependency lock: uv.lock
- Coverage policy: branch-coverage-baseline-required-before-release
- Product versioning: semver at 0.1.0
- Version source: harness/project.yaml:engineering.versioning.current
- Public contract: csv-summary command-line JSON output
- Harness version: 0.5.0

## Authority

- Autonomy level: supervised
- Network writes: explicit-human-approval
- Destructive actions: explicit-human-approval
- Release: human-only
- Policy changes: human-review

Generated from `harness/project.yaml` and `harness/intake.json`.
