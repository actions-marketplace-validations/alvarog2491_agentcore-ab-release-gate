"""Verify release pins in README usage examples."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bump_readme_pin.py"
SPEC = importlib.util.spec_from_file_location("bump_readme_pin", SCRIPT)
bump_readme_pin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bump_readme_pin)


def test_bump_replaces_tags_shas_and_existing_comments(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "- uses: alvarog2491/agentcore-ab-release-gate@v1\n- uses: alvarog2491/agentcore-ab-release-gate@old-sha # v0.9.0\n",
        encoding="utf-8",
    )

    changed = bump_readme_pin.bump_readme(readme, "a" * 40, "v1.2.3")

    assert changed is True
    assert readme.read_text(encoding="utf-8") == (
        f"- uses: alvarog2491/agentcore-ab-release-gate@{'a' * 40} # v1.2.3\n"
        f"- uses: alvarog2491/agentcore-ab-release-gate@{'a' * 40} # v1.2.3\n"
    )


def test_bump_is_idempotent(tmp_path):
    readme = tmp_path / "README.md"
    expected = f"- uses: alvarog2491/agentcore-ab-release-gate@{'b' * 40} # v2.0.0\n"
    readme.write_text(expected, encoding="utf-8")

    changed = bump_readme_pin.bump_readme(readme, "b" * 40, "v2.0.0")

    assert changed is False
    assert readme.read_text(encoding="utf-8") == expected
