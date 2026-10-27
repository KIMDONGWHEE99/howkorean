#!/bin/bash
# 파일을 쓸 때 보안 검사
# 훅: PostToolUse (matcher: Write)
#
# 파일에 하드코딩된 비밀 정보, API 키, 자격 증명이 있는지 검사합니다.
# 문제를 찾으면 additionalContext로 차단하지 않는 경고를 출력합니다.
#
# 호환: macOS, Linux, Windows(Git Bash)

# stdin에서 JSON 입력 읽기(Claude Code 훅 프로토콜)
INPUT=$(cat)

# sed로 file_path 추출(Windows Git Bash를 포함한 모든 플랫폼과 호환)
# grep -P(Windows Git Bash에서는 쓸 수 없음)와 python3 의존성을 피함
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# 바이너리 파일, vendor 디렉토리, 빌드 결과물은 건너뛰기
case "$FILE_PATH" in
  *.png|*.jpg|*.jpeg|*.gif|*.svg|*.ico|*.woff|*.woff2|*.ttf|*.eot) exit 0 ;;
  */node_modules/*|*/.git/*|*/dist/*|*/build/*) exit 0 ;;
esac

ISSUES=""

# 하드코딩된 비밀번호 확인
# JSON 형식("password": "value")과 코드 형식(password = 'value')을 모두 처리
# 구분자로 \\n 사용 — JSON에서 유효한 줄바꿈 이스케이프이며 printf도 안전하게 통과함
if grep -qiE '"password"[[:space:]]*:[[:space:]]*"[^"]+"' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- WARNING: Potential hardcoded password detected\\n"
elif grep -qiE '(password|passwd|pwd)[[:space:]]*=[[:space:]]*'"'"'[^'"'"']+'"'"'' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- WARNING: Potential hardcoded password detected\\n"
fi

# 하드코딩된 API 키 확인
if grep -qiE '"(api[_-]?key|apikey|access[_-]?token)"[[:space:]]*:[[:space:]]*"[^"]+"' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- WARNING: Potential hardcoded API key detected\\n"
fi

# 하드코딩된 비밀 값과 토큰 확인
if grep -qiE '(secret|token)[[:space:]]*=[[:space:]]*['"'"'"][^'"'"'"]+['"'"'"]' "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- WARNING: Potential hardcoded secret or token detected\\n"
fi

# 개인 키 확인
if grep -q "BEGIN.*PRIVATE KEY" "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- WARNING: Private key detected\\n"
fi

# AWS 키 확인
if grep -qE "AKIA[0-9A-Z]{16}" "$FILE_PATH" 2>/dev/null; then
  ISSUES="${ISSUES}- WARNING: AWS access key detected\\n"
fi

# semgrep이 있으면 검사(JSON 출력과 섞이지 않도록 stdout은 숨김)
if command -v semgrep &> /dev/null; then
  semgrep --config=auto "$FILE_PATH" --quiet >/dev/null 2>/dev/null
fi

# trufflehog가 있으면 검사(JSON 출력과 섞이지 않도록 stdout은 숨김)
if command -v trufflehog &> /dev/null; then
  trufflehog filesystem "$FILE_PATH" --only-verified --quiet >/dev/null 2>/dev/null
fi

# 문제를 찾으면 additionalContext로 출력(차단하지 않는 경고)
# Claude Code PostToolUse 프로토콜이 요구하는 hookSpecificOutput 형식 사용
if [ -n "$ISSUES" ]; then
  # JSON에 넣을 수 있도록 파일 경로 이스케이프(백슬래시와 큰따옴표)
  # ISSUES는 이미 구분자로 \\n(유효한 JSON 이스케이프)을 쓰므로 큰따옴표만 이스케이프
  SAFE_PATH=$(printf '%s' "$FILE_PATH" | sed 's/\\/\\\\/g; s/"/\\"/g')
  SAFE_ISSUES=$(printf '%s' "$ISSUES" | sed 's/"/\\"/g')
  printf '{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "Security scan found issues in %s:\\n%sPlease review and use environment variables instead."}}' "$SAFE_PATH" "$SAFE_ISSUES"
fi

exit 0
