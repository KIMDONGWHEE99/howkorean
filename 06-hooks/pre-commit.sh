#!/bin/bash
# 커밋하기 전에 테스트 실행
# 훅: PreToolUse (matcher: Bash) - 명령어가 git commit인지 확인
# 참고: "PreCommit" 훅 이벤트는 없습니다. Bash matcher와 함께 PreToolUse를 쓰고
# 명령어를 살펴 git commit 작업을 감지하세요.
#
# 종료 코드: 2는 도구 호출을 막고 stderr를 차단 이유로 보여 줍니다.
# 그 밖의 0이 아닌 값은 차단하지 않는 오류이므로 커밋이 그대로 진행됩니다.
# 출처: https://code.claude.com/docs/ko/hooks

# stdin에서 훅 JSON을 읽고, git commit 명령어일 때만 테스트 실행
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
if ! echo "$COMMAND" | grep -q 'git commit'; then
  exit 0
fi

echo "🧪 Running tests before commit..."

# package.json이 있는지 확인(Node.js 프로젝트)
if [ -f "package.json" ]; then
  if grep -q "\"test\":" package.json; then
    npm test
    if [ $? -ne 0 ]; then
      echo "❌ Tests failed! Commit blocked." >&2
      exit 2
    fi
  fi
fi

# pytest를 쓸 수 있는지 확인(Python 프로젝트)
if [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  if command -v pytest &> /dev/null; then
    pytest
    if [ $? -ne 0 ]; then
      echo "❌ Tests failed! Commit blocked." >&2
      exit 2
    fi
  fi
fi

# go.mod가 있는지 확인(Go 프로젝트)
if [ -f "go.mod" ]; then
  go test ./...
  if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Commit blocked." >&2
    exit 2
  fi
fi

# Cargo.toml이 있는지 확인(Rust 프로젝트)
if [ -f "Cargo.toml" ]; then
  cargo test
  if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Commit blocked." >&2
    exit 2
  fi
fi

echo "✅ All tests passed! Proceeding with commit."
exit 0
