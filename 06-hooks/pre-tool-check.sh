#!/bin/bash
# Bash 명령어 실행 전 안전 검사
# 훅: PreToolUse (matcher: Bash)
#
# 이 훅은 Bash 도구가 실행되기 전마다 실행되어, 파괴적이거나 위험도가 높을 수 있는
# 셸 명령어를 차단하거나 경고합니다.
#
# 설정:
#   cp 06-hooks/pre-tool-check.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/pre-tool-check.sh
#
# ~/.claude/settings.json에서 설정:
#   {
#     "hooks": {
#       "PreToolUse": [
#         {
#           "matcher": "Bash",
#           "hooks": [
#             {
#               "type": "command",
#               "command": "~/.claude/hooks/pre-tool-check.sh"
#             }
#           ]
#         }
#       ]
#     }
#   }
#
# 입력: 다음 형태의 JSON이 stdin으로 들어옴:
#   { "tool_name": "Bash", "tool_input": { "command": "..." } }
#
# 출력 규칙(Claude Code 훅 프로토콜 기준):
#   - exit 0 → 허용. stdout에는 JSON(hookSpecificOutput)을 담을 수 있음. stderr는
#     아무 알림 없이 버려지므로, stderr로 출력한 경고는 보이지 않음.
#     허용된 명령어를 관찰하려면 감사 로그 파일에 기록하세요.
#   - exit 2 → 차단. stderr가 차단 이유로 Claude에게 전달됨.
#     명령어가 *왜* 차단되었는지 설명하는 echo는 반드시 `>&2`로 stderr에
#     보내야 함. 그렇지 않으면 Claude Code가 "No stderr output"이라고 보고함.
#
# 감사 로그: 모든 호출이 판정 결과(BLOCK/WARN/ALLOW)와 함께
#   $CLAUDE_PROJECT_DIR/.claude/hooks/audit.log
# 에 기록되므로, Claude Code가 stderr 출력을 버리더라도 WARN 단계에
# 걸린 명령어를 확인할 수 있음.

# stdin에서 JSON 입력 전체 읽기
INPUT=$(cat)

# 이식성 있는 sed로 명령어 추출(macOS, Linux와 호환)
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

# 추출에 실패하면 원래 입력을 그대로 사용
if [ -z "$COMMAND" ]; then
  COMMAND="$INPUT"
fi

# ── 감사 로그 ─────────────────────────────────────────────────────────────────
# 모든 호출을 최종 판정과 함께 기록합니다. exit 0일 때 Claude Code가 stderr를
# 아무 알림 없이 버리므로, WARN 단계를 확인할 수 있는 유일하게 확실한 방법입니다.
# 훅을 Claude Code 밖에서(예: 로컬 테스트) 호출하면 $(pwd)를
# 대신 사용합니다.
LOG_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/hooks"
LOG_FILE="$LOG_DIR/audit.log"
mkdir -p "$LOG_DIR" 2>/dev/null
log_decision() {
  echo "$(date -u +%FT%TZ) [$1] $COMMAND" >> "$LOG_FILE"
}

# ── 차단 패턴 ─────────────────────────────────────────────────────────────────
# 이 명령어들은 거의 항상 파괴적이고 자동화된 맥락에서 의도한 경우가 드물기
# 때문에 무조건 차단합니다.

BLOCKED_PATTERNS=(
  # `rm -rf /` 뒤에 공백이나 줄 끝이 와야 하도록 고정합니다. 그렇지 않으면
  # 부분 문자열 매칭 때문에 `rm -rf /tmp/foo` 같은 명령어까지 잘못 걸립니다.
  "rm -rf /([[:space:]]|$)"
  "rm -rf \*"
  "dd if=/dev/zero"
  "dd if=/dev/random"
  ":\(\)\{:\|:&\};:"  # 포크 폭탄(정규식 메타 문자는 이스케이프)
  "mkfs\."           # 파일 시스템 포맷
  "format c:"        # Windows 디스크 포맷
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    log_decision "BLOCK:$pattern"
    # 이 echo들은 반드시 stderr로 보내야 함 — exit 2일 때 Claude Code는 stderr를
    # 차단 이유로 보여 줌. stdout에 쓰면 "No stderr output"이 표시됨.
    echo "❌ Blocked: Potentially destructive command detected: $pattern" >&2
    echo "   Command: $COMMAND" >&2
    exit 2
  fi
done

# ── 경고 패턴 ─────────────────────────────────────────────────────────────────
# 위험하지만 의도한 것일 수도 있는 패턴입니다. 경고를 기록하고 허용합니다.

WARNING_PATTERNS=(
  "rm -rf"
  "git push --force"
  "git reset --hard"
  "git clean -f"
  "chmod -R 777"
  "sudo rm"
  "DROP TABLE"
  "DROP DATABASE"
  "truncate"
)

MATCHED_WARNINGS=""
for pattern in "${WARNING_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qi "$pattern"; then
    MATCHED_WARNINGS="${MATCHED_WARNINGS:+$MATCHED_WARNINGS,}$pattern"
    # 훅을 직접 실행하는 사람을 위해 stderr에도 경고를 출력합니다.
    # exit 0이면 Claude Code는 이 출력을 버리므로, 확실한 기록은 감사 로그입니다
    # (WARN 항목 참고).
    echo "⚠️  Warning: High-risk operation detected: $pattern" >&2
  fi
done

if [ -n "$MATCHED_WARNINGS" ]; then
  log_decision "WARN:$MATCHED_WARNINGS"
  echo "   Command: $COMMAND" >&2
  echo "   Proceeding — review the above warnings before continuing." >&2
else
  log_decision "ALLOW"
fi

# ── 허용 ──────────────────────────────────────────────────────────────────────
exit 0
