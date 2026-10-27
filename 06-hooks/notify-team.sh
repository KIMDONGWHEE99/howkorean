#!/bin/bash
# 이벤트가 생기면 알림 보내기
# 훅: PostToolUse (matcher: Bash) — Bash 호출 뒤마다 실행되며, 명령어가 git push가 아니면 스크립트가 바로 종료됨
# 참고: Claude Code에는 PostPush 이벤트가 없습니다. git push에 반응하려면 bash 명령어 문자열에
# "git push"가 있는지 matcher나 이 스크립트 안의 조건 로직으로 확인하세요.

# 훅 입력을 읽고, Bash 명령어가 git push가 아니면 종료
INPUT=$(cat)
# 명령어를 추출하고(\"msg\" 같은 이스케이프된 따옴표는 유지) 그 안 어디에든 명령어 단어로 "git push"가 있는지 확인
COMMAND=$(echo "$INPUT" | sed -nE 's/.*"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/p' | head -1)
printf '%s\n' "$COMMAND" | grep -qE '(^|[^[:alnum:]_-]|\\n)git[[:space:]]+push([^[:alnum:]_-]|$)' || exit 0

REPO_NAME=$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null)
COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null)
AUTHOR=$(git log -1 --pretty=%an 2>/dev/null)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

echo "📢 Sending notification to team..."

# Slack 웹훅 예(웹훅 URL을 자신의 것으로 바꾸세요)
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"

if [ -n "$SLACK_WEBHOOK" ]; then
  curl -X POST "$SLACK_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "{
      \"text\": \"New push to *$REPO_NAME*\",
      \"attachments\": [{
        \"color\": \"good\",
        \"fields\": [
          {\"title\": \"Branch\", \"value\": \"$BRANCH\", \"short\": true},
          {\"title\": \"Author\", \"value\": \"$AUTHOR\", \"short\": true},
          {\"title\": \"Commit\", \"value\": \"$COMMIT_MSG\"}
        ]
      }]
    }" \
    --silent --output /dev/null

  echo "✅ Slack notification sent"
fi

# Discord 웹훅 예(웹훅 URL을 자신의 것으로 바꾸세요)
DISCORD_WEBHOOK="${DISCORD_WEBHOOK_URL:-}"

if [ -n "$DISCORD_WEBHOOK" ]; then
  curl -X POST "$DISCORD_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "{
      \"content\": \"**New push to $REPO_NAME**\",
      \"embeds\": [{
        \"title\": \"$COMMIT_MSG\",
        \"color\": 3066993,
        \"fields\": [
          {\"name\": \"Branch\", \"value\": \"$BRANCH\", \"inline\": true},
          {\"name\": \"Author\", \"value\": \"$AUTHOR\", \"inline\": true}
        ]
      }]
    }" \
    --silent --output /dev/null

  echo "✅ Discord notification sent"
fi

# 이메일 알림 예
EMAIL_TO="${TEAM_EMAIL:-}"

if [ -n "$EMAIL_TO" ]; then
  echo "New push to $REPO_NAME by $AUTHOR" | \
    mail -s "Git Push: $BRANCH" "$EMAIL_TO"

  echo "✅ Email notification sent"
fi

exit 0
