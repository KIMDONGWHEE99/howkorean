#!/usr/bin/env python3
"""
setup-auto-mode-permissions.py

~/.claude/settings.json에 Claude Code용 안전한 권한의 보수적인 기본 세트를
넣어 줍니다. 기본 세트는 읽기 전용과 로컬 검사 위주이며, 선택 플래그로 편집,
테스트 실행, git 쓰기 작업, 패키지 설치, GitHub CLI 쓰기까지 허용 목록을
넓힐 수 있습니다.

사용법:
    python3 setup-auto-mode-permissions.py
    python3 setup-auto-mode-permissions.py --dry-run
    python3 setup-auto-mode-permissions.py --include-edits --include-tests
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Iterable

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

# 핵심 기본 세트: 읽기 전용 검사와 위험이 낮은 로컬 셸 명령어.
CORE_PERMISSIONS = [
    "Read(*)",
    "Grep(*)",
    "Agent(*)",
    "Skill(*)",
    "WebSearch(*)",
    "WebFetch(*)",
    "Bash(ls:*)",
    "Bash(pwd:*)",
    "Bash(which:*)",
    "Bash(echo:*)",
    "Bash(cat:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(wc:*)",
    "Bash(sort:*)",
    "Bash(uniq:*)",
    "Bash(find:*)",
    "Bash(dirname:*)",
    "Bash(basename:*)",
    "Bash(realpath:*)",
    "Bash(file:*)",
    "Bash(stat:*)",
    "Bash(diff:*)",
    "Bash(md5sum:*)",
    "Bash(sha256sum:*)",
    "Bash(date:*)",
    "Bash(env:*)",
    "Bash(printenv:*)",
    "Bash(git status:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git branch:*)",
    "Bash(git show:*)",
    "Bash(git rev-parse:*)",
    "Bash(git remote -v:*)",
    "Bash(git remote get-url:*)",
    "Bash(git stash list:*)",
]

# 선택 사항이지만 여전히 로컬: 파일 편집과 작업 관리.
EDITING_PERMISSIONS = [
    "Edit(*)",
    "TaskCreate(*)",
    "TaskUpdate(*)",
]

# 선택 사항인 개발/테스트 명령어. 이 명령어들은 여전히 임의의 프로젝트 스크립트를
# 실행할 수 있으므로, 기본 세트에 넣지 않고 직접 켜도록 둡니다.
TEST_AND_BUILD_PERMISSIONS = [
    "Bash(npm test:*)",
    "Bash(cargo test:*)",
    "Bash(go test:*)",
    "Bash(pytest:*)",
    "Bash(python3 -m pytest:*)",
    "Bash(make:*)",
    "Bash(cmake:*)",
]

# 선택 사항인 로컬 git 쓰기 작업. 기록을 다시 쓰는 명령어는 잘못 쓰기 쉬우므로
# 기본 세트에서 뺍니다.
GIT_WRITE_PERMISSIONS = [
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git switch:*)",
    "Bash(git stash:*)",
    "Bash(git tag:*)",
]

# 선택 사항인 의존성/패키지 명령어. 프로젝트 훅을 실행하거나 코드를 가져올 수
# 있으므로 일부러 기본 세트에서 뺍니다.
PACKAGE_MANAGER_PERMISSIONS = [
    "Bash(npm ci:*)",
    "Bash(npm install:*)",
    "Bash(pip install:*)",
    "Bash(pip3 install:*)",
]

# 선택 사항인 GitHub CLI 쓰기 권한.
GITHUB_WRITE_PERMISSIONS = [
    "Bash(gh pr create:*)",
]

# 선택 사항인 GitHub CLI 추가 읽기 권한.
GITHUB_READ_PERMISSIONS = [
    "Bash(gh pr view:*)",
    "Bash(gh pr list:*)",
    "Bash(gh issue view:*)",
    "Bash(gh issue list:*)",
    "Bash(gh repo view:*)",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed Claude Code settings with a conservative permission baseline."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the rules that would be added without writing settings.json",
    )
    parser.add_argument(
        "--include-edits",
        action="store_true",
        help="Add file-editing permissions (Edit/TaskCreate/TaskUpdate)",
    )
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Add local build/test commands such as pytest, cargo test, and make",
    )
    parser.add_argument(
        "--include-git-write",
        action="store_true",
        help="Add local git mutation commands such as add, commit, checkout, and stash",
    )
    parser.add_argument(
        "--include-packages",
        action="store_true",
        help="Add package install commands such as npm ci, npm install, and pip install",
    )
    parser.add_argument(
        "--include-gh-write",
        action="store_true",
        help="Add GitHub CLI write permissions such as gh pr create",
    )
    parser.add_argument(
        "--include-gh-read",
        action="store_true",
        help="Add GitHub CLI read permissions such as gh pr view and gh repo view",
    )
    return parser.parse_args()


def load_settings(path: Path) -> dict:
    if not path.exists():
        return {}

    try:
        with path.open() as f:
            settings = json.load(f)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(settings, dict):
        raise SystemExit(f"Expected {path} to contain a JSON object.")

    return settings


def build_permissions(args: argparse.Namespace) -> list[str]:
    permissions = list(CORE_PERMISSIONS)

    if args.include_edits:
        permissions.extend(EDITING_PERMISSIONS)

    if args.include_tests:
        permissions.extend(TEST_AND_BUILD_PERMISSIONS)

    if args.include_git_write:
        permissions.extend(GIT_WRITE_PERMISSIONS)

    if args.include_packages:
        permissions.extend(PACKAGE_MANAGER_PERMISSIONS)

    if args.include_gh_write:
        permissions.extend(GITHUB_WRITE_PERMISSIONS)

    if args.include_gh_read:
        permissions.extend(GITHUB_READ_PERMISSIONS)

    return permissions


def append_unique(existing: list, new_items: Iterable[str]) -> list[str]:
    seen = set(existing)
    added: list[str] = []
    for item in new_items:
        if item not in seen:
            existing.append(item)
            seen.add(item)
            added.append(item)
    return added


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=str(path.parent),
        delete=False,
    ) as tmp:
        json.dump(payload, tmp, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)

    tmp_path.replace(path)


def main() -> None:
    args = parse_args()
    permissions_to_add = build_permissions(args)

    settings = load_settings(SETTINGS_PATH)
    permissions = settings.setdefault("permissions", {})

    if not isinstance(permissions, dict):
        raise SystemExit("Expected permissions to be a JSON object.")

    allow = permissions.setdefault("allow", [])
    if not isinstance(allow, list):
        raise SystemExit("Expected permissions.allow to be a JSON array.")

    added = append_unique(allow, permissions_to_add)

    if not added:
        print("Nothing to add — all selected rules already present.")
        return

    print(f"{'Would add' if args.dry_run else 'Adding'} {len(added)} rule(s):")
    for rule in added:
        print(f"  + {rule}")

    if args.dry_run:
        print("\nDry run — no changes written.")
        return

    atomic_write_json(SETTINGS_PATH, settings)
    print(f"\nDone. {len(added)} rule(s) added to {SETTINGS_PATH}")


if __name__ == "__main__":
    main()
