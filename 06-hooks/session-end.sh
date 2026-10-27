#!/usr/bin/env bash
# SessionEnd 훅: 작업한 모듈을 기록한 다음, 학습 진도를 계속 추적할 수 있도록
# ~/.claude-howto-progress.json에 세션 기록을 덧붙입니다.
#
# 응답할 때마다가 아니라 Claude Code 세션이 끝날 때 한 번만 실행됩니다.
# 훅은 제어 터미널 없이 실행되므로(/dev/tty를 쓸 수 없음), 모듈과 메모는
# CLAUDE_HOWTO_MODULES / CLAUDE_HOWTO_NOTES 환경 변수에서 가져옵니다.
#
# 설치: .claude/settings.json의 "SessionEnd" 이벤트 아래에 추가하세요(아래 참고).

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# 보호 장치: 이 저장소 안에서만 실행
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

# 진도 파일이 없으면 만들기
if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Claude Code — Learning Session End"
echo " $DATE $TIME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
# 작업한 모듈. 예: CLAUDE_HOWTO_MODULES=06,07 claude 로 시작
# 01=Slash  02=Memory  03=Skills  04=Subagents  05=MCP
# 06=Hooks  07=Plugins 08=Checkpoints 09=Advanced 10=CLI
INPUT="${CLAUDE_HOWTO_MODULES:-}"

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  echo " Skipped — no session logged."
  echo ""
  exit 0
fi

# 짧은 번호를 모듈 이름으로 변환(bash 3.2가 파싱하지 못하는 파이프라인+while 대신 for 반복문 사용)
IFS=',' read -ra PARTS <<< "$INPUT"
MODULES_JSON=""
for m in "${PARTS[@]}"; do
  m="${m// /}"  # 공백 제거
  case "$m" in
    01) label='"01-slash-commands"' ;;
    02) label='"02-memory"' ;;
    03) label='"03-skills"' ;;
    04) label='"04-subagents"' ;;
    05) label='"05-mcp"' ;;
    06) label='"06-hooks"' ;;
    07) label='"07-plugins"' ;;
    08) label='"08-checkpoints"' ;;
    09) label='"09-advanced-features"' ;;
    10) label='"10-cli"' ;;
    *)  label="\"$m\"" ;;
  esac
  MODULES_JSON="${MODULES_JSON:+$MODULES_JSON,}$label"
done

# 선택 사항인 메모. 예: CLAUDE_HOWTO_NOTES="pre-commit 예제를 해 봄"
NOTES="${CLAUDE_HOWTO_NOTES:-}"

# JSON 이스케이프를 Python이 처리하도록 NOTES를 별도 인수로 넘김 —
# 메모에 따옴표나 백슬래시가 들어 있어도 JSON이 깨지지 않음.
python3 - "$PROGRESS_FILE" "$DATE" "$TIME" "$MODULES_JSON" "$NOTES" <<'PYEOF'
import sys, json

path, date, time_str, modules_raw, notes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

new_session = {
    "date": date,
    "time": time_str,
    "modules": json.loads(f"[{modules_raw}]") if modules_raw else [],
    "notes": notes,
}

with open(path, 'r') as f:
    data = json.load(f)

data.setdefault('sessions', []).append(new_session)

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
PYEOF

echo ""
echo " Saved to $PROGRESS_FILE"
[ -n "$NOTES" ] && echo " Notes: $NOTES"
echo ""

exit 0
