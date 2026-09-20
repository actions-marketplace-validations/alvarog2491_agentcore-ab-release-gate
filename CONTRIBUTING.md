# Contributing

## Development setup

```bash
uv sync --extra dev
```

## Useful commands

| Command | What it does |
|---|---|
| `pytest` | Run the full test suite |
| `ruff check .` | Lint `agentcore_release_gate/`, `main.py`, and `tests/` |
| `ruff format .` | Auto-format all Python files |

## Project layout

```
action.yml              # action manifest — inputs, outputs, composite steps
main.py                 # entry point called by action.yml
agentcore_release_gate/
  ab_test.py            # A/B test lifecycle (create, poll, promote/rollback)
  deploy.py             # endpoint deployment and validation
  eval_config.py        # evaluation-config cloning and cleanup
  gateway.py            # Gateway traffic routing
  report.py             # structured result logging
  runtime.py            # AgentCore Runtime helpers
tests/
  test_action.py        # integration-level tests for the full action flow
  test_bump_readme_pin.py
  test_report.py
scripts/
  bump_readme_pin.py    # utility for pinning the README version badge
```

## Running tests

```bash
pytest
```

Tests use `unittest.mock` to stub AWS API calls — no real AWS credentials or resources are needed.

## Making changes

1. Edit source under `agentcore_release_gate/` or `main.py`.
2. Add or update tests in `tests/`.
3. Run `pytest` and `ruff check .` before opening a PR.
4. If you changed any action inputs or outputs in `action.yml`, update the README table and bump the version with `scripts/bump_readme_pin.py`.

## Contract changes

The public contract is:

- Inputs and outputs declared in `action.yml`
- The promotion/rollback decision logic documented in the README

Any change to these warrants a major version bump and a clear description in the PR.

## Reporting bugs and feature requests

Open an issue in this repository. Please include:

- The action version and the inputs you passed to it
- The error output or relevant excerpt from your GitHub Actions job log
- What you expected to happen and what actually happened
