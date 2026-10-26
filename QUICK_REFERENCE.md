<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 예제 - 빠른 참조 카드

## 🚀 설치 빠른 명령어

### 슬래시 명령어
```bash
# 전체 설치
cp 01-slash-commands/*.md .claude/commands/

# 특정 명령어만 설치
cp 01-slash-commands/optimize.md .claude/commands/
```

### 메모리
```bash
# 프로젝트 메모리
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 개인 메모리
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### 스킬
```bash
# 개인 스킬
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 프로젝트 스킬
cp -r 03-skills/code-review-specialist .claude/skills/
```

### 서브에이전트
```bash
# 전체 설치
cp 04-subagents/*.md .claude/agents/

# 특정 에이전트만 설치
cp 04-subagents/code-reviewer.md .claude/agents/
```

### MCP
```bash
# 자격 증명 설정
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 설정 설치 (프로젝트 범위)
cp 05-mcp/github-mcp.json .mcp.json

# 또는 사용자 범위: ~/.claude.json에 추가
```

### 훅
```bash
# 훅 설치
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 설정 파일(~/.claude/settings.json)에서 구성
```

### 플러그인
```bash
# 예제에서 설치 (게시된 경우)
claude --plugin-dir ./07-plugins/pr-review
/plugin install devops-automation
/plugin install documentation
```

### 체크포인트
```bash
# 체크포인트는 사용자가 프롬프트를 보낼 때마다 자동으로 만들어집니다
# 되감으려면 Esc를 두 번 누르거나 다음을 입력하세요:
/rewind

# 그런 다음 고르세요: Restore code and conversation(코드와 대화 복원), Restore conversation(대화 복원),
# Restore code(코드 복원), Summarize from here(여기부터 요약), Never mind(취소)
```

### 고급 기능
```bash
# 설정 파일(.claude/settings.json)에서 구성
# 09-advanced-features/config-examples.json 참고

# 계획 모드
/plan 작업 설명

# 권한 모드 (--permission-mode 플래그 사용)
# manual         - 모든 작업마다 승인 요청 (설정값 "default". v2.1.200부터 "manual"이 별칭)
# acceptEdits    - 파일 편집은 자동 승인, 나머지는 확인
# plan           - 읽기 전용 분석, 수정 없음
# auto           - 백그라운드 분류기가 권한을 자동으로 결정
# dontAsk        - 사전 승인된 도구만 실행하고 나머지는 모두 거부
# bypassPermissions - 모든 작업 허용 (--permission-mode bypassPermissions. --dangerously-skip-permissions와 동일)

# 세션 관리
/resume                # 이전 대화 재개 (인수 없이 실행하면 지난 세션 선택기)
/rename "name"         # 현재 세션 이름 지정
/fork [prompt]         # 대화를 새 백그라운드 세션으로 복사하고 지금 세션에서 계속 작업
/subtask <task>        # 대화를 이어받아 작업한 뒤 결과를 보고하는 포크된 서브에이전트 생성
/branch [name]         # 원래 대화는 보존하고 대화 사본으로 전환
claude -c              # 가장 최근 대화 이어 가기
claude -r "session"    # 이름이나 ID로 세션 재개
```

---

## 📋 기능 치트 시트

| 기능 | 설치 경로 | 사용법 |
|---------|-------------|-------|
| **슬래시 명령어 (60개 이상)** | `.claude/commands/*.md` | `/command-name` |
| **메모리** | `./CLAUDE.md` | 자동 로드 |
| **스킬** | `.claude/skills/*/SKILL.md` | 자동 호출 |
| **서브에이전트** | `.claude/agents/*.md` | 자동 위임 |
| **MCP** | `.mcp.json`(프로젝트) 또는 `~/.claude.json`(사용자) | `/mcp__server__action` |
| **훅 (이벤트 33가지)** | `~/.claude/hooks/*.sh` | 이벤트로 실행(타입 5가지) |
| **플러그인** | `/plugin install`로 설치 | 모든 기능을 묶음 |
| **체크포인트** | 기본 제공 | `Esc+Esc` 또는 `/rewind` |
| **계획 모드** | 기본 제공 | `/plan <task>` |
| **권한 모드 (6가지)** | 기본 제공 | `--allowedTools`, `--permission-mode` |
| **세션** | 기본 제공 | `/resume`, `/rename`, `/branch`, `/fork` |
| **백그라운드 작업** | 기본 제공 | 백그라운드에서 실행 |
| **Remote Control** | 기본 제공 | `claude --remote-control` 또는 `/remote-control` |
| **웹 세션** | 기본 제공 | `claude --cloud "task"` |
| **Git worktree** | 기본 제공 | `claude -w <name>` |
| **자동 메모리** | 기본 제공 | `~/.claude/projects/<project>/memory/`에 자동 저장 |
| **작업 목록** | 기본 제공 | `Ctrl+T`(체크리스트), `/tasks`(백그라운드 작업) |
| **번들 스킬** | 기본 제공 | `/batch`, `/claude-api`, `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` *(v2.1.246부터는 어디서든 Claude가 스스로 시작할 수도 있음. 수준을 지정하지 않으면 마지막으로 입력한 수준을 다시 씀, v2.1.223)*, `/simplify` *(정리 전용 리뷰. v2.1.154부터 다시 `/code-review`와 별개)*, `/debug`, `/fewer-permission-prompts`, `/loop`, `/run` *(v2.1.145+)*, `/run-skill-generator` *(v2.1.145+)*, `/verify` *(v2.1.145+. v2.1.215부터는 직접 호출할 때만 실행되며 Claude가 스스로 실행하지 않음)* |

---

## 🎯 자주 쓰는 활용 사례

### 코드 리뷰
```bash
# 방법 1: 슬래시 명령어
cp 01-slash-commands/optimize.md .claude/commands/
# 사용: /optimize

# 방법 2: 서브에이전트
cp 04-subagents/code-reviewer.md .claude/agents/
# 사용: 자동 위임

# 방법 3: 스킬
cp -r 03-skills/code-review-specialist ~/.claude/skills/
# 사용: 자동 호출

# 방법 4: 플러그인 (가장 좋음)
claude --plugin-dir ./07-plugins/pr-review
# 사용: /review-pr
```

### 문서화
```bash
# 슬래시 명령어
cp 01-slash-commands/generate-api-docs.md .claude/commands/

# 서브에이전트
cp 04-subagents/documentation-writer.md .claude/agents/

# 스킬
cp -r 03-skills/doc-generator ~/.claude/skills/

# 플러그인 (완성형 솔루션)
/plugin install documentation
```

### DevOps
```bash
# 완성된 플러그인
/plugin install devops-automation

# 명령어: /deploy, /rollback, /status, /incident
```

### 팀 표준
```bash
# 프로젝트 메모리
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 팀에 맞게 편집
vim CLAUDE.md
```

### 자동화와 훅
```bash
# 훅 설치 (이벤트 33가지, 타입 5가지: command, http, mcp_tool, prompt, agent)
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 예:
# - 커밋 전 테스트: pre-commit.sh
# - 코드 자동 포맷: format-code.sh
# - 보안 검사: security-scan.sh

# 완전 자율 워크플로우를 위한 자동 모드
claude --permission-mode auto -p "auth 모듈을 리팩토링하고 테스트해 줘"
# 또는 대화형으로 Shift+Tab을 눌러 모드 순환
```

### 안전한 리팩토링
```bash
# 체크포인트는 프롬프트마다 그 전에 자동으로 만들어집니다
# 리팩토링 시도
# 잘되면: 계속 진행
# 실패하면: Esc+Esc를 누르거나 /rewind로 되돌아가기
```

### 복잡한 구현
```bash
# 계획 모드 사용
/plan 사용자 인증 시스템 구현

# Claude가 상세한 계획을 만듦
# 검토하고 승인
# Claude가 체계적으로 구현
```

### CI/CD 통합
```bash
# 헤드리스 모드로 실행 (비대화형)
claude -p "모든 테스트를 실행하고 보고서를 만들어 줘"

# CI용 권한 모드와 함께
claude -p "테스트를 실행해 줘" --permission-mode dontAsk

# 완전 자율 CI 작업을 위한 자동 모드와 함께
claude --permission-mode auto -p "테스트를 실행하고 실패를 고쳐 줘"

# 자동화를 위한 훅과 함께
# 09-advanced-features/README.md 참고
```

### 학습과 실험
```bash
# 안전한 분석을 위해 계획 모드 사용
claude --permission-mode plan

# 안전하게 실험하세요 - 체크포인트는 자동으로 만들어집니다
# 되감아야 하면: Esc+Esc를 누르거나 /rewind 사용
```

### 에이전트 팀
```bash
# 에이전트 팀 켜기
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 또는 settings.json에서
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }

# 이렇게 시작하세요: "팀 방식으로 기능 X를 구현해 줘"
```

### 예약 작업
```bash
# 5분마다 명령어 실행
/loop 5m /check-status

# 일회성 알림: 평소 말투로 요청 (/loop는 취소할 때까지 반복)
30분 뒤에 배포 확인하라고 알려 줘
```

---

## 📁 파일 위치 참조

```text
내 프로젝트/
├── .claude/
│   ├── commands/              # 슬래시 명령어 위치
│   ├── agents/                # 서브에이전트 위치
│   ├── skills/                # 프로젝트 스킬 위치
│   └── settings.json          # 프로젝트 설정(훅 등)
├── .mcp.json                  # MCP 설정(프로젝트 범위)
├── CLAUDE.md                  # 프로젝트 메모리
└── src/
    └── api/
        └── CLAUDE.md          # 디렉토리별 메모리

사용자 홈/
├── .claude/
│   ├── commands/              # 개인 명령어
│   ├── agents/                # 개인 에이전트
│   ├── skills/                # 개인 스킬
│   ├── hooks/                 # 훅 스크립트
│   ├── settings.json          # 사용자 설정
│   └── CLAUDE.md              # 개인 메모리
└── .claude.json               # 개인 MCP 설정(사용자 범위)

시스템 디렉토리/               # macOS /Library/Application Support/ClaudeCode/, Linux /etc/claude-code/, Windows C:\Program Files\ClaudeCode\
├── managed-settings.json      # 관리형 설정(엔터프라이즈/조직)
└── managed-settings.d/        # 관리형 설정 드롭인
```

---

## 🔍 예제 찾기

### 분류별
- **슬래시 명령어**: `01-slash-commands/`
- **메모리**: `02-memory/`
- **스킬**: `03-skills/`
- **서브에이전트**: `04-subagents/`
- **MCP**: `05-mcp/`
- **훅**: `06-hooks/`
- **플러그인**: `07-plugins/`
- **체크포인트**: `08-checkpoints/`
- **고급 기능**: `09-advanced-features/`
- **CLI**: `10-cli/`

### 활용 사례별
- **성능**: `01-slash-commands/optimize.md`
- **보안**: `04-subagents/secure-reviewer.md`
- **테스트**: `04-subagents/test-engineer.md`
- **문서**: `03-skills/doc-generator/`
- **DevOps**: `07-plugins/devops-automation/`

### 복잡도별
- **간단**: 슬래시 명령어
- **보통**: 서브에이전트, 메모리
- **고급**: 스킬, 훅
- **완성형**: 플러그인

---

## 🎓 학습 경로

### 1일차
```bash
# 개요 읽기
cat README.md

# 명령어 설치
cp 01-slash-commands/optimize.md .claude/commands/

# 써 보기
/optimize
```

### 2~3일차
```bash
# 메모리 설정
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
vim CLAUDE.md

# 서브에이전트 설치
cp 04-subagents/code-reviewer.md .claude/agents/
```

### 4~5일차
```bash
# MCP 설정
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"
cp 05-mcp/github-mcp.json .mcp.json

# MCP 명령어 써 보기
/mcp__github__list_prs
```

### 2주차
```bash
# 스킬 설치
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 자동으로 호출되게 두기
# 이렇게만 말하세요: "이 코드에 문제가 있는지 리뷰해 줘"
```

### 3주차 이후
```bash
# 완성된 플러그인 설치
claude --plugin-dir ./07-plugins/pr-review

# 번들에 포함된 기능 사용
/review-pr
/check-security
/check-tests
```

---

## 주요 기능 하이라이트

| 기능 | 설명 | 사용법 |
|---------|-------------|-------|
| **자동 모드** | 백그라운드 분류기를 쓰는 완전 자율 동작. v2.1.207부터 Bedrock/Vertex/Foundry에서 기본으로 제공 | `Shift+Tab`으로 모드 순환 또는 `--permission-mode auto` |
| **채널** | Discord와 Telegram 통합 | `--channels` 플래그, Discord/Telegram 봇 |
| **음성 받아쓰기** | Claude에게 명령어와 컨텍스트를 말로 전달 | `/voice` 명령어 |
| **출력 스타일** | Claude의 역할, 톤, 기본 응답 형식 변경 | `/config` → Output style 또는 `outputStyle` 설정. 기본 제공: Default, Proactive, Explanatory, Learning, Concise |
| **상태 표시줄** | 명령어로 만드는 사용자 정의 세션 하단 상태 표시 | `/statusline` 또는 `statusLine` 설정. stdin으로 세션/모델/비용/컨텍스트 JSON을 받음 |
| **훅 (이벤트 33가지)** | 타입 5가지로 확장된 훅 시스템 | command, http, mcp_tool, prompt, agent 훅 타입 |
| **MCP 입력 요청(Elicitation)** | MCP 서버가 실행 중에 사용자 입력을 요청할 수 있음 | 서버에 추가 정보가 필요하면 자동으로 프롬프트 표시 |
| **플러그인 LSP** | 플러그인의 Language Server Protocol 지원 | `userConfig`, `${CLAUDE_PLUGIN_DATA}` 변수 |
| **Remote Control** | claude.ai나 Claude 앱에서 로컬 세션 조작 | `claude --remote-control`(세션 안에서는 `/remote-control`) |
| **웹 세션** | claude.ai/code의 클라우드 세션 | 터미널에서 시작하려면 `claude --cloud "task"` |
| **데스크톱 앱** | 네이티브 데스크톱 애플리케이션 | claude.ai/download에서 다운로드 |
| **작업 목록** | 백그라운드 작업 관리 | `/tasks`(별칭 `/bashes`) |
| **자동 메모리** | 대화에서 자동으로 메모리 저장 | Claude가 `~/.claude/projects/<project>/memory/MEMORY.md`에 메모를 저장하며, `/memory`로 관리 |
| **AGENTS.md** *(v2.1.277)* | 여러 도구가 함께 쓰는 프로젝트 컨텍스트 파일. 작업 디렉토리나 그 상위에 `CLAUDE.md`가 없으면 프로젝트 지침으로 읽힘 | `/config`의 **Project instructions**에서 모드 전환. [AGENTS.md](02-memory/README.md#agentsmd) 참고 |
| **Git worktree** | 병렬 개발을 위한 격리된 작업 공간 | `claude --worktree <name>`(또는 `-w`) |
| **모델 선택** | Fable 5.1, Fable 5, Opus 5.5, Opus 5, Sonnet 5.5, Sonnet 5, Sonnet 4.6, Opus 4.8, Haiku 5.5, Haiku 4.5 사이에서 전환 | `/model`(Anthropic API에서 `sonnet`은 Sonnet 5.5로 해석됨, v2.1.284+) — v2.1.153부터 선택한 모델이 새 세션의 기본값으로 저장되며, 현재 세션에만 적용하려면 `s`를 누름 |
| **에이전트 팀** | 여러 에이전트를 작업에 맞춰 조율 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경 변수로 켬(실험 기능) |
| **동적 워크플로우** *(v2.1.154)* | 결정적 다중 에이전트 조율. v2.1.219부터 기본 크기 지침은 medium(에이전트 10개 미만 목표) | `/workflows`로 실행 보기. Claude에게 만들어 달라고 요청. 크기는 `/config`의 **Dynamic workflow size**에서 변경 |
| **예약 작업** | `/loop`로 반복 작업 | `/loop 5m /command` 또는 CronCreate 도구 |
| **Chrome 통합** | 브라우저 자동화 | `--chrome` 플래그나 `/chrome` 명령어 |
| **키보드 사용자 정의** | 사용자 정의 키 바인딩 | `/keybindings` 명령어 |
| **/usage-credits** | 추가 사용 한도 설정(v2.1.144에서 `/extra-usage`에서 이름이 바뀌었으며 예전 이름도 별칭으로 동작) | `/usage-credits` |
| **/run** *(v2.1.145+)* | 프로젝트의 앱을 실행해 변경 사항이 동작하는 모습 확인 | `/run` |
| **/verify** *(v2.1.145+)* | 앱을 빌드하고 실행하고 관찰해 수정이 동작하는지 확인(v2.1.215부터는 직접 호출할 때만 실행되며 Claude가 스스로 실행하지 않음) | `/verify` |
| **/run-skill-generator** *(v2.1.145+)* | 특정 프로젝트를 다루는 방법을 `/run`/`/verify`에 학습시킴 | `/run-skill-generator` |
| **서브에이전트 출력 검사** *(v2.1.210+)* | 서브에이전트 보고서에서 프롬프트 주입 패턴을 찾아 무력화 | 기본으로 켜져 있으며 끌 수 없음 |
| **WebSearch 한도와 서브에이전트 확장 제한** *(v2.1.212, v2.1.219에서 확장)* | 세션당 WebSearch 200회. v2.1.290부터 대화형 세션에서는 시간당 100회씩 다시 채워짐. 동시 서브에이전트 한도(기본 20)는 v2.1.217에서 추가됨. v2.1.219부터 서브에이전트는 **기본 깊이 3**까지 중첩 서브에이전트를 생성할 수 있음(v2.1.217에서는 중첩이 꺼져 있었음). 세션당 서브에이전트 200개 생성 한도는 **v2.1.224에서 제거됨** — 이제 세션당 전체 서브에이전트 수에는 제한이 없음 | `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`(기본 200, `/clear`로 초기화), `CLAUDE_CODE_WEB_SEARCH_REFILLS_PER_HOUR`(대화형 기본 100, `-p`에서는 0), `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`(기본 20), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`(기본 3, 1로 설정하면 꺼짐) |
| **화면 읽기 모드** *(v2.1.208)* | 화면 읽기 프로그램을 위한 일반 텍스트 렌더링 모드 | `--ax-screen-reader` 플래그, `CLAUDE_AX_SCREEN_READER=1`, 또는 설정의 `"axScreenReader": true` |
| **제한 모드** *(v2.1.248+)* | `--tools`에서 하나씩 지정하지 않는 한(`default` 프리셋으로는 안 됨) 명령어나 코드를 실행하는 기본 제공 도구(Bash, PowerShell 등)와 WebFetch를 뺌. 사용자·프로젝트·로컬 설정을 무시하고(관리형 설정과 `--settings`는 여전히 적용), 파일 도구를 작업 디렉토리로 제한하며, `bypassPermissions`와 클라우드 세션을 거부 | `claude --restricted` 또는 `CLAUDE_CODE_RESTRICTED=1` |
| **서브에이전트 캐시 TTL** *(v2.1.248+)* | 에이전트 frontmatter의 `experimental.cacheTtl` 필드로 서브에이전트의 프롬프트 캐시 유지 시간 설정 | 에이전트 frontmatter에 `experimental:`와 `cacheTtl: "5m"`(또는 `"1h"`) 추가. [서브에이전트](04-subagents/README.md) 참고 |
| **서브에이전트 모델 강제** *(v2.1.257+)* | `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`을 설정하면 `CLAUDE_CODE_SUBAGENT_MODEL`이 에이전트 frontmatter보다 우선함. v2.1.251부터 이 환경 변수는 기본적으로 우선하지 않으며, 이 값을 설정하지 않는 한 frontmatter(`model: inherit` 포함)가 우선 | `CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 claude` |

---

## 팁과 요령

### 사용자 정의
- 처음에는 예제를 그대로 써 보세요
- 필요에 맞게 수정하세요
- 팀과 공유하기 전에 테스트하세요
- 설정은 버전 관리하세요

### 모범 사례
- 팀 표준에는 메모리를 쓰세요
- 완성된 워크플로우에는 플러그인을 쓰세요
- 복잡한 작업에는 서브에이전트를 쓰세요
- 빠른 작업에는 슬래시 명령어를 쓰세요

### 문제 해결
```bash
# 파일 위치 확인
ls -la .claude/commands/
ls -la .claude/agents/

# YAML 문법 확인
head -20 .claude/agents/code-reviewer.md

# MCP 연결 테스트
echo $GITHUB_PERSONAL_ACCESS_TOKEN
```

---

## 📊 기능 매트릭스

| 필요한 것 | 사용할 기능 | 예제 |
|------|----------|---------|
| 빠른 단축 명령 | 슬래시 명령어 (60개 이상) | `01-slash-commands/optimize.md` |
| 팀 표준 | 메모리 | `02-memory/project-CLAUDE.md` |
| 자동 워크플로우 | 스킬 | `03-skills/code-review-specialist/` |
| 전문 작업 | 서브에이전트 | `04-subagents/code-reviewer.md` |
| 외부 데이터 | MCP (+ 입력 요청) | `05-mcp/github-mcp.json` |
| 이벤트 자동화 | 훅 (이벤트 33가지, 타입 5가지) | `06-hooks/pre-commit.sh` |
| 완성형 솔루션 | 플러그인 (+ LSP 지원) | `07-plugins/pr-review/` |
| 안전한 실험 | 체크포인트 | `08-checkpoints/checkpoint-examples.md` |
| 완전 자율 실행 | 자동 모드 | `--permission-mode auto` 또는 `Shift+Tab` |
| 채팅 통합 | 채널 | `--channels`(Discord, Telegram) |
| CI/CD 파이프라인 | CLI | `10-cli/README.md` |

---

## 🔗 바로 가기

- **메인 가이드**: `README.md`
- **전체 색인**: `INDEX.md`
- **원래 가이드**: `claude_concepts_guide.md`

---

## 📞 자주 묻는 질문

**Q: 무엇을 써야 하나요?**
A: 슬래시 명령어로 시작하고 필요할 때 기능을 추가하세요.

**Q: 기능을 섞어 써도 되나요?**
A: 네! 함께 동작합니다. 메모리 + 명령어 + MCP = 강력한 조합입니다.

**Q: 팀과 어떻게 공유하나요?**
A: `.claude/` 디렉토리를 git에 커밋하세요.

**Q: 비밀 정보는 어떻게 하나요?**
A: 환경 변수를 쓰고, 절대 하드코딩하지 마세요.

**Q: 예제를 수정해도 되나요?**
A: 물론입니다! 원하는 대로 고쳐 쓰라고 만든 템플릿입니다.

---

## ✅ 체크리스트

시작하기 체크리스트:

- [ ] `README.md` 읽기
- [ ] 슬래시 명령어 1개 설치
- [ ] 명령어 써 보기
- [ ] 프로젝트 `CLAUDE.md` 만들기
- [ ] 서브에이전트 1개 설치
- [ ] MCP 통합 1개 설정
- [ ] 스킬 1개 설치
- [ ] 완성된 플러그인 써 보기
- [ ] 필요에 맞게 사용자 정의
- [ ] 팀과 공유

---

**빠른 시작**: `cat README.md`

**전체 색인**: `cat INDEX.md`

**이 카드**: 빠르게 참고할 수 있도록 가까이 두세요!

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/workflows#set-a-size-guideline
- https://code.claude.com/docs/ko/memory#agents-md
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/ko/cli-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/ko/sub-agents
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/ko/settings
- https://code.claude.com/docs/ko/hooks
- https://code.claude.com/docs/ko/env-vars
- https://code.claude.com/docs/ko/commands
- https://code.claude.com/docs/ko/remote-control
- https://code.claude.com/docs/ko/agent-teams
- https://code.claude.com/docs/ko/memory#storage-location
- https://code.claude.com/docs/ko/permission-modes
- https://code.claude.com/docs/en/managed-settings
- https://code.claude.com/docs/ko/scheduled-tasks
- https://code.claude.com/docs/en/code-review-local
**호환 모델**: Claude Fable 5.1, Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
