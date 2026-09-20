"""Verify PR report rendering and optional GitHub publication."""

import json
import sys
from pathlib import Path

import pytest

ACTION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ACTION))

from agentcore_release_gate.report import COMMENT_MARKER, build_report, publish_report


@pytest.fixture
def stub_urlopen(monkeypatch):
    requests = []

    def install(*payloads):
        responses = iter(payloads)

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(next(responses)).encode()

        def open_request(request, timeout):
            requests.append((request, timeout))
            return Response()

        monkeypatch.setattr("agentcore_release_gate.report.urlopen", open_request)
        return requests

    return install


def test_report_includes_decision_scores_and_thresholds():
    state = {
        "finished": "promoted",
        "version": "2",
        "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/agent@sha256:" + "a" * 64,
        "quality_gates": {"Builtin.Helpfulness": 0.7, "custom-tone-abcdefghij": 3.5},
        "variant_results": {
            "Builtin.Helpfulness": {
                "mean": 0.82,
                "isSignificant": True,
                "absoluteChange": 0.1,
                "pValue": 0.02,
                "controlSampleSize": 40,
                "treatmentSampleSize": 42,
            },
            "custom-tone-abcdefghij": {
                "mean": 4.0,
                "isSignificant": True,
                "absoluteChange": 0.5,
                "pValue": 0.01,
                "controlSampleSize": 40,
                "treatmentSampleSize": 42,
            },
        },
    }

    report = build_report(state, "success")

    assert COMMENT_MARKER in report
    assert "Promoted" in report
    assert "Builtin.Helpfulness" in report
    assert "0.82" in report
    assert "3.5" in report
    assert "`2`" in report
    assert "40/42" in report
    assert "Yes" in report


def test_report_handles_failure_before_deployment_state_exists():
    report = build_report({}, "failure")

    assert "Failed" in report
    assert "No deployment state was recorded" in report


def test_publish_updates_existing_bot_comment(stub_urlopen):
    requests = stub_urlopen(
        [{"id": 42, "body": COMMENT_MARKER, "user": {"type": "Bot"}}],
        {"id": 42},
    )

    publish_report("token", "owner/repository", 7, "report")

    assert [request.get_method() for request, _timeout in requests] == ["GET", "PATCH"]
    assert requests[1][0].full_url.endswith("/repos/owner/repository/issues/comments/42")
    assert json.loads(requests[1][0].data) == {"body": "report"}


def test_publish_creates_comment_when_no_owned_comment_exists(stub_urlopen):
    requests = stub_urlopen(
        [{"id": 9, "body": COMMENT_MARKER, "user": {"type": "User"}}],
        {"id": 10},
    )

    publish_report("token", "owner/repository", 7, "report")

    assert [request.get_method() for request, _timeout in requests] == ["GET", "POST"]
    assert requests[1][0].full_url.endswith("/repos/owner/repository/issues/7/comments")


@pytest.mark.parametrize("repository", ["invalid", "/repository", "owner/"])
def test_publish_rejects_invalid_repository(repository):
    with pytest.raises(ValueError, match="repository"):
        publish_report("token", repository, 7, "report")
