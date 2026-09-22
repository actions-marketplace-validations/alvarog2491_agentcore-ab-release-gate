# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (including dev extras)
uv sync --extra dev

# Run the full test suite
pytest

# Run a single test file
pytest tests/test_action.py

# Run a single test by name
pytest tests/test_action.py::test_name

# Lint
ruff check .

# Format
ruff format .
```

Tests use `unittest.mock` to stub AWS API calls — no real AWS credentials needed.

## Architecture

This is a composite GitHub Action that evaluates a new Amazon Bedrock AgentCore Runtime image against the currently live version using a native A/B test, then promotes or rolls back.

**Entry point**: `main.py` dispatches to one of five subcommands (`run`, `observe`, `promote`, `rollback`, `report`) based on the `step` action input. The action.yml composite steps set environment variables and call `main.py`.

**`agentcore_release_gate/` package**:
- `deployment.py` — `Deployment` class orchestrates the full lifecycle: baseline capture, treatment endpoint setup, evaluation config cloning, A/B test creation, observation loop, result collection, and promotion/rollback. Every mutable state change is checkpointed to a JSON recovery journal (`state.json`) before the next AWS API call so failures are recoverable.
- `evaluation.py` — polls `GetABTest` until all configured evaluators have scored results, enforces quality gates (minimum score + no regression + optional statistical significance).
- `aws_client.py` — thin wrapper over `boto3` for AgentCore Control, AgentCore (data-plane), and ECR API calls.
- `report.py` — builds and publishes the optional pull-request comment.
- `utils.py` — `wait_for` poller, input parsers.
- `types.py` — `JsonObject`, `QualityGates`, `VariantResult` type aliases.
- `constants.py` — timeouts, poll intervals, weight defaults.

**Deployment flow**:
1. Resolve ECR image tag → immutable digest.
2. Capture baseline runtime version (`control` endpoint `liveVersion`).
3. Checkpoint baseline to `state.json` (the always() cleanup step reads this).
4. Ensure `treatment` endpoint and Gateway targets exist.
5. Clone the template online-evaluation config into two ephemeral configs (one per variant), patching CloudWatch log/service names.
6. Create and start the A/B test (variants `C` and `T1`).
7. Observe for `duration-seconds`, polling A/B test status.
8. Wait for all quality-gate evaluators to return results.
9. Enforce gates — promote on pass, rollback on failure.
10. Cleanup: stop A/B test, delete ephemeral evaluation configs.

**Recovery journal** (`state.json`): Records `baseline`, `version`, `ab_test_id`, `ephemeral_*_config_id`, `promoting`, `finished`. The `rollback` subcommand reads this file and is safe to call repeatedly (idempotent via `finished` flag).

**Step modes**: `auto` runs observe+promote in one job; `observe`/`promote`/`rollback` split across jobs using a GitHub Actions artifact to pass `state.json` between jobs.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). Every PR title must be prefixed with a Conventional Commits type that determines the version bump:

| Prefix | Bump | When to use |
|---|---|---|
| `feat:` | **minor** | New feature or capability |
| `fix:` | **patch** | Bug fix |
| `feat!:` / `fix!:` / `refactor!:` (or any type with `!`) | **major** | Breaking change |
| `chore:`, `docs:`, `ci:`, `test:`, `refactor:`, `perf:`, `style:` | none | No user-facing change |

Always choose the prefix that matches the actual change. When a PR contains multiple changes, use the highest-impact prefix (major > minor > patch).

## Changing action inputs/outputs

Any change to inputs or outputs in `action.yml` requires updating the README table and bumping the pinned version in the README via `scripts/bump_readme_pin.py`.
