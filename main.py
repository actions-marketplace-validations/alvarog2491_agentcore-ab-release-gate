"""Run deployment, recovery, or PR reporting for the standalone action."""

import argparse
import json
import os
import signal
from pathlib import Path

from agentcore_release_gate.deployment import Deployment
from agentcore_release_gate.report import build_report, publish_report
from agentcore_release_gate.utils import parse_quality_gates, parse_weights


def _interrupted(_signal, _frame) -> None:
    raise KeyboardInterrupt("Workflow interrupted; attempting rollback")


def cmd_report() -> None:
    """Publish the optional pull-request report for the completed action run.

    Missing pull-request context is expected for non-PR workflows and skips
    reporting without affecting the deployment outcome.
    """
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pull_request = event.get("pull_request", {}).get("number")
    if not pull_request:
        return
    state_path = os.environ.get("STATE_FILE", "")
    state = {}
    if state_path and Path(state_path).is_file():
        state = json.loads(Path(state_path).read_text(encoding="utf-8"))
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    run_url = (
        f"{server}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
    )
    report = build_report(state, os.environ.get("DEPLOY_OUTCOME", "failure"), run_url)
    publish_report(
        os.environ["GITHUB_TOKEN"],
        os.environ["GITHUB_REPOSITORY"],
        int(pull_request),
        report,
        os.environ.get("GITHUB_API_URL", "https://api.github.com"),
    )


def cmd_rollback(state_file: str) -> None:
    """Recover an unfinished deployment when its state journal exists.

    Args:
        state_file: Path to the deployment recovery journal.
    """
    # Validation failures can reach cleanup without creating deployment state.
    if not Path(state_file).exists():
        return
    Deployment(state_file).rollback()


def cmd_promote(state_file: str) -> None:
    """Promote the candidate recorded as ready in a recovery journal.

    Args:
        state_file: Path to the deployment recovery journal.
    """
    Deployment(state_file).promote_candidate()


def _build_deployment(state_file: str) -> tuple[Deployment, int]:
    gates = parse_quality_gates(os.environ["QUALITY_GATES"])
    timeout = int(os.environ.get("EVALUATION_TIMEOUT_SECONDS", "900"))
    duration = int(os.environ.get("DURATION_SECONDS", "7200"))
    scoring_lag = int(os.environ.get("SCORING_LAG_SECONDS", "120"))
    require_significance = os.environ.get("REQUIRE_SIGNIFICANCE", "true").strip().lower() != "false"
    if timeout <= 0 or duration < 60:
        raise ValueError(
            "Evaluation timeout must be positive and observation must last at least 60 seconds"
        )
    if scoring_lag < 0:
        raise ValueError("Scoring lag seconds must be non-negative")
    evaluation_config_template = os.environ["EVALUATION_CONFIG_ID"].strip()
    ab_test_role_arn = os.environ["AB_TEST_ROLE_ARN"].strip()
    if not evaluation_config_template:
        raise ValueError("evaluation-config-id must not be empty")
    if not ab_test_role_arn:
        raise ValueError("ab-test-role-arn must not be empty")
    control_weight, treatment_weight = parse_weights(
        os.environ.get("CONTROL_WEIGHT", "80"), os.environ.get("TREATMENT_WEIGHT", "20")
    )
    deployment = Deployment(
        state_file,
        quality_gates=gates,
        require_significance=require_significance,
        control_endpoint_name=os.environ.get("CONTROL_ENDPOINT_NAME", "control"),
        evaluation_config_template=evaluation_config_template,
        ab_test_role_arn=ab_test_role_arn,
        control_weight=control_weight,
        treatment_weight=treatment_weight,
        evaluation_timeout=timeout,
        scoring_lag_seconds=scoring_lag,
    )
    return deployment, duration


def cmd_observe(state_file: str) -> None:
    """Deploy and evaluate a candidate without promoting it.

    Args:
        state_file: Path where deployment state is persisted for later promotion.
    """
    deployment, duration = _build_deployment(state_file)
    deployment.observe_candidate(os.environ["IMAGE_URI"], duration)


def cmd_run(state_file: str) -> None:
    """Run the action's complete observe-and-promote deployment workflow.

    Args:
        state_file: Path where deployment state is persisted for recovery.
    """
    deployment, duration = _build_deployment(state_file)
    deployment.run(os.environ["IMAGE_URI"], duration)


def main() -> None:
    """Dispatch the selected action subcommand and install cancellation handling."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["run", "observe", "promote", "rollback", "report"])
    command = parser.parse_args().command

    if command == "report":
        try:
            cmd_report()
        except Exception as error:
            # Reporting is optional and must never change the deployment result.
            print(f"::warning::Unable to publish AgentCore A/B PR report: {error}")
        return

    state_file = os.environ["STATE_FILE"]
    signal.signal(signal.SIGTERM, _interrupted)
    signal.signal(signal.SIGINT, _interrupted)

    if command == "rollback":
        cmd_rollback(state_file)
    elif command == "promote":
        cmd_promote(state_file)
    elif command == "observe":
        cmd_observe(state_file)
    else:
        cmd_run(state_file)


if __name__ == "__main__":
    main()
