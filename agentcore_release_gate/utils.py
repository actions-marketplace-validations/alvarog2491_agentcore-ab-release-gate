"""Shared input validation and AWS readiness helpers."""

import json
import math
import re
import time
from collections.abc import Callable, Collection
from typing import TypeVar, cast

from agentcore_release_gate.constants import (
    AWS_ACCOUNT_ID_LENGTH,
    AWS_POLL_INTERVAL_SECONDS,
    DEFAULT_AWS_WAIT_TIMEOUT_SECONDS,
    EVALUATOR_ID_SUFFIX_LENGTH,
    MAX_EVALUATOR_NAME_PREFIX_LENGTH,
    MAXIMUM_VARIANT_WEIGHT,
    MINIMUM_VARIANT_WEIGHT,
    SHA256_HEX_LENGTH,
    TOTAL_TRAFFIC_WEIGHT,
)
from agentcore_release_gate.types import EcrImageParts, QualityGates

ResultT = TypeVar("ResultT", bound=dict[str, object])
ECR_IMAGE_PATTERN = re.compile(
    rf"(?P<account>\d{{{AWS_ACCOUNT_ID_LENGTH}}})\.dkr\.ecr\."
    r"(?P<region>[a-z0-9-]+)\.amazonaws\.com(?:\.cn)?/"
    rf"(?P<repository>[a-z0-9][a-z0-9/_.-]*)(?::(?P<tag>[\w.-]+)|"
    rf"@(?P<digest>sha256:[a-f0-9]{{{SHA256_HEX_LENGTH}}}))"
)
EVALUATOR_PATTERN = re.compile(
    r"(?:Builtin\.[a-zA-Z0-9._-]+|ThirdParty\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
    rf"|[a-zA-Z][a-zA-Z0-9-_]{{0,{MAX_EVALUATOR_NAME_PREFIX_LENGTH - 1}}}"
    rf"-[a-zA-Z0-9]{{{EVALUATOR_ID_SUFFIX_LENGTH}}})"
)


def _parse_image(image: str) -> EcrImageParts:
    """Validate an ECR image URI and return its registry components."""
    match = ECR_IMAGE_PATTERN.fullmatch(image)
    if not match:
        raise ValueError(
            "AgentCore requires an ECR image URI with a tag or digest. Mirror Docker Hub/GHCR "
            "images to ECR before using this action; it does not publish images."
        )
    return cast(EcrImageParts, match.groupdict())


def parse_weights(control: str | int, treatment: str | int) -> tuple[int, int]:
    """Validate complementary, non-zero A/B test traffic weights.

    Args:
        control: Control traffic percentage, supplied as an integer or input string.
        treatment: Treatment traffic percentage, supplied as an integer or input string.

    Returns:
        Validated control and treatment percentages.

    Raises:
        ValueError: If either value is not an integer from 1 through 99, or the pair
            does not total 100.
    """
    try:
        control_weight, treatment_weight = int(control), int(treatment)
    except (TypeError, ValueError) as error:
        raise ValueError("control-weight and treatment-weight must be integers") from error
    if not (
        MINIMUM_VARIANT_WEIGHT <= control_weight <= MAXIMUM_VARIANT_WEIGHT
        and MINIMUM_VARIANT_WEIGHT <= treatment_weight <= MAXIMUM_VARIANT_WEIGHT
    ):
        raise ValueError("control-weight and treatment-weight must each be between 1 and 99")
    if control_weight + treatment_weight != TOTAL_TRAFFIC_WEIGHT:
        raise ValueError("control-weight and treatment-weight must add up to 100")
    return control_weight, treatment_weight


def parse_quality_gates(value: str) -> QualityGates:
    """Parse finite evaluator thresholds from a JSON object.

    Args:
        value: JSON object mapping supported evaluator IDs to minimum numeric scores.

    Returns:
        Validated evaluator thresholds keyed by evaluator ID.

    Raises:
        ValueError: If the JSON is invalid, empty, or contains unsupported IDs or
            non-finite scores.
    """
    try:
        gates = json.loads(value)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError("quality-gates must map evaluator IDs to minimum scores") from error
    if (
        not isinstance(gates, dict)
        or not gates
        or any(
            not isinstance(name, str)
            or not EVALUATOR_PATTERN.fullmatch(name)
            or isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not math.isfinite(score)
            for name, score in gates.items()
        )
    ):
        raise ValueError(
            "quality-gates must be a non-empty JSON object of evaluator IDs and numeric minimum scores"
        )
    return cast(QualityGates, gates)


def wait_for(
    read: Callable[[], ResultT],
    status: str | Collection[str],
    version: str | None = None,
    timeout: float = DEFAULT_AWS_WAIT_TIMEOUT_SECONDS,
    execution_status: str | None = None,
    on_poll: Callable[[ResultT], None] | None = None,
) -> ResultT:
    """Wait for an AWS resource to reach the requested state.

    Args:
        read: Callable that fetches the latest resource representation.
        status: One acceptable status or a collection of acceptable statuses.
        version: Optional live version that must also match.
        timeout: Maximum number of seconds to wait.
        execution_status: Optional A/B test execution status that must also match.
        on_poll: Optional callable invoked with the latest result on each tick where
            the target state has not been reached and no failure was detected.

    Returns:
        The first resource representation matching all requested conditions.

    Raises:
        RuntimeError: If AWS reports a failed resource status.
        TimeoutError: If the requested state is not reached before ``timeout``.
    """
    statuses = (status,) if isinstance(status, str) else status
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = read()
        if (
            result["status"] in statuses
            and (version is None or result.get("liveVersion") == version)
            and (execution_status is None or result.get("executionStatus") == execution_status)
        ):
            return result
        resource_status = result["status"]
        if isinstance(resource_status, str) and (
            "FAILED" in resource_status or "ERROR" in resource_status.upper()
        ):
            raise RuntimeError("AWS resource failed to become ready")
        if on_poll is not None:
            on_poll(result)
        time.sleep(AWS_POLL_INTERVAL_SECONDS)
    raise TimeoutError("Timed out waiting for AWS readiness")
