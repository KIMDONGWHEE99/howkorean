#!/bin/bash
# 모든 bash 명령어 기록
# 훅: PostToolUse (matcher: Bash)
#
# stdin으로 들어오는 JSON에서 실행된 명령어를 읽어 파일에 기록합니다.
#
# 호환: macOS, Linux, Windows(Git Bash)

# stdin에서 JSON 입력 읽기(Claude Code 훅 프로토콜)
INPUT=$(cat)

# tool_input에서 bash 명령어 추출
# 참고: sed의 [^"]*는 JSON 안의 이스케이프된 따옴표에서 멈춥니다. 큰따옴표로 감싼
# 문자열이 들어 있는 명령어는 첫 번째 \"까지만 잡힙니다 — sed 기반 JSON 파싱의
# 알려진 한계이며, 로그 기록 용도로는 받아들일 만합니다.
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$COMMAND" ]; then
  exit 0
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
LOGFILE="$HOME/.claude/bash-commands.log"

# 로그 디렉토리가 없으면 만들기
mkdir -p "$(dirname "$LOGFILE")"

# 명령어 기록
echo "[$TIMESTAMP] $COMMAND" >> "$LOGFILE"

exit 0
