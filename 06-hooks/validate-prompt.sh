#!/bin/bash
# 사용자 프롬프트 검증
# 훅: UserPromptSubmit
#
# stdin으로 들어오는 JSON에서 사용자 프롬프트를 읽어 위험한 작업을 차단합니다.
#
# 호환: macOS, Linux, Windows(Git Bash)

# stdin에서 JSON 입력 읽기(Claude Code 훅 프로토콜)
INPUT=$(cat)

# JSON 입력에서 프롬프트 텍스트 추출
# Claude Code는 UserPromptSubmit 텍스트를 "prompt" 필드에 담아 보냄
PROMPT=$(echo "$INPUT" | sed -n 's/.*"prompt"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$PROMPT" ]; then
  exit 0
fi

# 위험한 작업 확인
DANGEROUS_PATTERNS=(
  "rm -rf /"
  "delete database"
  "drop database"
  "format disk"
  "dd if="
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$PROMPT" | grep -qi "$pattern"; then
    printf '{"decision": "block", "reason": "Dangerous operation detected: %s"}' "$pattern"
    exit 0
  fi
done

# 프로덕션 배포 확인
if echo "$PROMPT" | grep -qiE "(deploy|push).*production"; then
  if [ ! -f ".deployment-approved" ]; then
    echo '{"decision": "block", "reason": "Production deployment requires approval. Create .deployment-approved file to proceed."}'
    exit 0
  fi
fi

# 특정 작업에 필요한 컨텍스트가 있는지 확인
if echo "$PROMPT" | grep -qi "refactor"; then
  if [ ! -d "tests" ] && [ ! -d "test" ]; then
    printf '{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "Warning: Refactoring without tests may be risky. Consider writing tests first."}}'
  fi
fi

exit 0
