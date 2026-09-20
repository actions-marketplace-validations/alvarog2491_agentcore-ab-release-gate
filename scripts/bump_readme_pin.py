#!/usr/bin/env python3
"""Pin README action examples to a released commit SHA and tag."""

import argparse
import re
from pathlib import Path

ACTION_REFERENCE = re.compile(r"alvarog2491/agentcore-ab-release-gate@[^\s`]+(?:\s+#[^\n`]*)?")


def bump_readme(readme: Path, sha: str, tag: str) -> bool:
    """Replace every action reference and report whether the file changed."""
    before = readme.read_text(encoding="utf-8")
    replacement = f"alvarog2491/agentcore-ab-release-gate@{sha} # {tag}"
    after = ACTION_REFERENCE.sub(replacement, before)
    if after == before:
        return False
    readme.write_text(after, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sha", help="Commit SHA referenced by the release tag")
    parser.add_argument("tag", help="Published release tag")
    args = parser.parse_args()

    changed = bump_readme(Path("README.md"), args.sha, args.tag)
    if changed:
        print(f"Bumped README to {args.tag} ({args.sha}).")
    else:
        print(f"README already references {args.tag} ({args.sha}).")


if __name__ == "__main__":
    main()
