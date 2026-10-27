<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 기능 카탈로그

> 명령어, 에이전트, 스킬, 플러그인, 훅까지 Claude Code의 모든 기능을 한눈에 보는 빠른 참조 가이드입니다.

**바로 가기**: [명령어](#슬래시-명령어) | [권한 모드](#권한-모드) | [서브에이전트](#서브에이전트) | [스킬](#스킬) | [플러그인](#플러그인) | [MCP 서버](#mcp-서버) | [훅](#훅) | [메모리](#메모리-파일) | [새 기능](#새-기능)

---

## 요약

| 기능 | 기본 제공 | 예제 | 합계 | 참고 |
|---------|----------|----------|-------|-----------|
| **슬래시 명령어** | 60개 이상 | 8 | 68개 이상 | [01-slash-commands/](01-slash-commands/) |
| **서브에이전트** | 6 | 9 | 15 | [04-subagents/](04-subagents/) |
| **스킬** | 번들 20개 | 6 | 26 | [03-skills/](03-skills/) |
| **플러그인** | - | 3 | 3 | [07-plugins/](07-plugins/) |
| **MCP 서버** | - | 4 | 4 | [05-mcp/](05-mcp/) |
| **훅** | 이벤트 33개 | 11 | 44 | [06-hooks/](06-hooks/) |
| **메모리** | 유형 7개 | 3 | 10 | [02-memory/](02-memory/) |
| **합계** | **126** | **44** | **170** | |

---

## 슬래시 명령어

명령어는 사용자가 직접 호출해 특정 작업을 실행하는 단축 명령입니다.

### 기본 제공 명령어

| 명령어 | 설명 | 사용 시점 |
|---------|-------------|-------------|
| `/help` | 도움말 보기 | 처음 시작할 때, 명령어를 익힐 때 |
| `/btw` | 일회성 곁가지 질문 — 주 컨텍스트를 어지럽히지 않음 | 잠깐 다른 질문을 할 때 |
| `/chrome` | Chrome 통합 설정 | 브라우저 자동화 |
| `/clear` | 대화 기록 지우기 | 새로 시작할 때, 컨텍스트를 줄일 때 |
| `/diff` | 대화형 diff 뷰어. 전체 화면 TUI(v2.1.260+)에서는 대화 옆에 diff 패널을 열어 계속 띄워 두며, Claude가 파일을 편집하거나 명령어를 실행할 때마다 새로 고칩니다. 기존 렌더러에서는 프롬프트 자리에 뷰어가 열립니다 | 변경 사항 검토 |
| `/config` | 설정 보기/편집 | 동작 사용자 정의 |
| `/status` | 세션 상태 보기 | 현재 상태 확인 |
| `/agents` | 제거됨: 마법사는 v2.1.198에서 빠졌고, v2.1.281에서는 명령어도 `/` 메뉴와 `/help`에서 빠졌습니다 — 서브에이전트를 만들거나 관리하려면 Claude에게 요청하거나 `.claude/agents/`를 편집하세요 | Claude에게 요청해 서브에이전트 관리 |
| `/skills` | 사용 가능한 스킬 목록 | 자동 호출 기능 확인 |
| `/hooks` | 설정된 훅 목록 | 자동화 디버깅 |
| `/insights` | 세션 패턴 분석 | 세션 최적화 |
| `/install-slack-app` | Claude Slack 앱 설치 | Slack 통합 |
| `/keybindings` | 키보드 단축키 사용자 정의 | 키 설정 변경 |
| `/mcp` | MCP 서버 목록 | 외부 통합 확인 |
| `/memory` | 로드된 메모리 파일 보기 | 컨텍스트 로딩 디버깅 |
| `/mobile` | 모바일용 QR 코드 생성 | 모바일 접속 |
| `/passes` | 친구에게 Claude Code 무료 1주일 이용권 공유(대상 계정만) | 추천 |
| `/plugin` | 플러그인 관리 | 확장 기능 설치/제거 |
| `/plan` | 계획 모드 진입 | 복잡한 구현 |
| `/proactive` | `/loop`의 별칭(v2.1.105) | `/loop`와 같음 |
| `/recap` | 세션으로 돌아왔을 때 세션 요약 보기 | 자리를 비운 뒤 그동안 한 일 파악 |
| `/rewind` | 체크포인트로 되감기 | 변경 취소, 다른 방법 탐색 |
| `/checkpoint` | `/rewind`의 별칭 | `/rewind`와 같음 |
| `/cost` | `/usage`의 비용 탭을 여는 단축 별칭(v2.1.118+) | 지출 모니터링 |
| `/context` | 컨텍스트 윈도우 사용량 보기 | 대화 길이 관리 |
| `/export` | 대화 내보내기 | 참고용으로 저장 |
| `/usage-credits` | 추가 사용 한도 설정(v2.1.144에서 `/extra-usage`에서 이름이 바뀌었으며 예전 이름도 별칭으로 동작) | 속도 제한 관리 |
| `/feedback` | 피드백이나 버그 신고 제출 | 문제 신고 |
| `/login` | Anthropic 인증 | 기능 이용 |
| `/logout` | 로그아웃 | 계정 전환 |
| `/sandbox` | 샌드박스 모드 켜기/끄기 | 안전한 명령어 실행 |
| `/doctor` | 진단 실행 | 문제 해결 |
| `/reload-plugins` | 설치된 플러그인 다시 로드. v2.1.221부터는 대부분의 설치가 바로 활성화되므로 설치 요약에 `Run /reload-plugins to activate.`가 표시될 때만 필요합니다. v2.1.260+부터 헤드리스 세션에서도 쓸 수 있어 Claude Code 데스크톱과 SDK의 명령어 목록에도 나타납니다 | 플러그인 관리 |
| `/reload-skills` | 다시 시작하지 않고 스킬 디렉토리 다시 검색(v2.1.152) | 스킬 관리 |
| `/workflows` | 실행 중이거나 완료된 동적 워크플로우 실행 보기(v2.1.154) | 다중 에이전트 조율 |
| `/release-notes` | 릴리스 노트 보기 | 새 기능 확인 |
| `/remote-control` | 원격 제어 켜기 | 원격 접속 |
| `/permissions` | 권한 관리 | 접근 제어 |
| `/rename` | 현재 세션 이름 변경 | 세션 정리 |
| `/resume` | 이전 세션 재개 | 작업 이어 가기 |
| `/tui [default\|fullscreen]` | 터미널 UI 렌더러 설정(`fullscreen` = 깜빡임 없는 대체 화면). 인수 없이 `/tui`를 입력하면 현재 렌더러 출력 | 전체 화면/tmux에서 깜빡임 없는 렌더링 |
| `/tasks` | 백그라운드 작업 보기 | 비동기 작업 모니터링 |
| `/copy` | 마지막 응답을 클립보드에 복사 | 출력을 빠르게 공유 |
| `/teleport` (별칭 `/tp`) | 웹용 Claude Code 세션을 이 터미널에서 재개. 선택기가 열립니다. claude.ai 구독 필요 | 원격으로 작업 이어 가기 |
| `/desktop` | Claude 데스크톱 앱 열기 | 데스크톱 인터페이스로 전환 |
| `/theme` | 색상 테마 변경. v2.1.118에서 `~/.claude/themes/<name>.json`으로 이름 붙인 사용자 정의 테마가 추가됨(플러그인도 `themes/` 디렉토리를 포함할 수 있음) | 화면 꾸미기 |
| `/usage` | 사용량/비용/통계를 위한 대표 명령어 — `/cost`와 `/stats`를 탭으로 구분된 화면 하나로 통합(v2.1.118). v2.1.149부터 비용 보기에서 지출을 분류별(스킬, 서브에이전트, 플러그인, MCP 서버별)로 나눠 보여 줍니다. **VSCode 확장 프로그램**(v2.1.174)에서는 `/usage`(Account & usage) 대화 상자에 기여도 분석이 추가되어 캐시 미스, 긴 컨텍스트 비용, 서브에이전트, 스킬·에이전트·플러그인·MCP별 사용량을 24시간과 7일 단위로 보여 줍니다 | 할당량과 비용 모니터링 |
| `/focus` | 포커스 보기 전환(산만하지 않은 출력 표시) | 오래 걸리는 작업 중 시각적 소음 줄이기 |
| `/fork` | 대화를 독립된 새 백그라운드 세션으로 복사(v2.1.212+) | 다른 방법을 병렬로 탐색 |
| `/subtask` | 대화를 이어받아 작업한 뒤 결과를 보고하는 포크된 서브에이전트 생성(v2.1.212+) | 하던 일을 놓치지 않고 곁다리 작업 위임 |
| `/stats` | `/usage`의 통계 탭을 여는 단축 별칭(v2.1.118+) | 세션 지표 검토 |
| `/statusline` | 상태 표시줄 설정 | 상태 표시 사용자 정의 |
| `/stickers` | Claude Code 스티커 주문 | 재미 요소 |
| `/fast` | 빠른 출력 모드 켜기/끄기. **Opus 5.5**(v2.1.280부터 기본값), **Opus 5, Opus 4.8**에 적용 | 응답 속도 높이기 |
| `/terminal-setup` | 터미널 통합 설정 | 터미널 기능 설정 |
| `/undo` | `/rewind`의 별칭(v2.1.108) | `/rewind`와 같음 |
| `/upgrade` | 상위 요금제로 바꾸는 업그레이드 페이지 열기 | 요금제 업그레이드 |
| `/team-onboarding` | 이 프로젝트의 Claude Code 사용 기록으로 팀원 적응 가이드 생성 | 새 팀원 온보딩(v2.1.101) |
| `/code-review ultra` | 현재 변경 사항에 대해 클라우드 다중 에이전트 코드 리뷰 실행. `/ultrareview`는 별칭으로 남아 있고 `/code-review ultra`가 권장 방식입니다. Pro와 Max에서는 3회 무료이고, 그 이후에는 사용 크레딧이 필요합니다 | 병합 전 여러 에이전트로 심층 리뷰(v2.1.112) |
| `/fewer-permission-prompts` | 대화 기록을 살펴 자주 쓰는 읽기 전용 도구의 허용 목록을 우선순위대로 제안 | 프로젝트에서 반복되는 권한 프롬프트 줄이기(v2.1.112) |
| `/skill-doctor` | 로드된 스킬 중 쓰이지 않는 것과 컨텍스트 비용을 표시. `/plugin` 관리자의 **Stats** 탭에서 열리며 `-p`에서는 텍스트로 출력 | 더 필요 없는 스킬 정리(v2.1.252+) |

### 사용자 정의 명령어(예제)

| 명령어 | 설명 | 사용 시점 | 범위 | 설치 |
|---------|-------------|-------------|-------|--------------|
| `/optimize` | 코드 최적화 분석 | 성능 개선 | 프로젝트 | `cp 01-slash-commands/optimize.md .claude/commands/` |
| `/pr` | 풀 리퀘스트 준비 | PR 제출 전 | 프로젝트 | `cp 01-slash-commands/pr.md .claude/commands/` |
| `/generate-api-docs` | API 문서 생성 | API 문서화 | 프로젝트 | `cp 01-slash-commands/generate-api-docs.md .claude/commands/` |
| `/commit` | 컨텍스트를 반영한 git 커밋 생성 | 변경 사항 커밋 | 사용자 | `cp 01-slash-commands/commit.md .claude/commands/` |
| `/push-all` | 스테이징, 커밋, 푸시 | 빠른 배포 | 사용자 | `cp 01-slash-commands/push-all.md .claude/commands/` |
| `/doc-refactor` | 문서 구조 개선 | 문서 개선 | 프로젝트 | `cp 01-slash-commands/doc-refactor.md .claude/commands/` |
| `/setup-ci-cd` | CI/CD 파이프라인 설정 | 새 프로젝트 | 프로젝트 | `cp 01-slash-commands/setup-ci-cd.md .claude/commands/` |
| `/unit-test-expand` | 테스트 커버리지 확장 | 테스트 개선 | 프로젝트 | `cp 01-slash-commands/unit-test-expand.md .claude/commands/` |

> **범위**: **사용자** = 개인 워크플로우(`~/.claude/commands/`), **프로젝트** = 팀 공유(`.claude/commands/`)

**참고**: [01-slash-commands/](01-slash-commands/) | [공식 문서](https://code.claude.com/docs/ko/interactive-mode)

**한 번에 설치(모든 사용자 정의 명령어)**:
```bash
cp 01-slash-commands/*.md .claude/commands/
```

---

## 권한 모드

Claude Code는 도구 사용을 어떻게 승인할지 정하는 6가지 권한 모드를 지원합니다.

| 모드 | 설명 | 사용 시점 |
|------|-------------|-------------|
| `manual` | 도구를 호출할 때마다 확인 요청 | 모든 작업을 직접 검토할 때(v2.1.200부터 Manual로 표시되며 설정값은 여전히 `default`, `manual`은 별칭). v2.1.283부터는 대화형 터미널과 VS Code 세션의 기본 시작 모드가 auto입니다 |
| `acceptEdits` | 파일 편집은 자동 승인, 나머지는 확인 | 신뢰하는 편집 워크플로우 |
| `plan` | 조사해서 계획을 제안하며, 승인할 때까지 소스를 편집하지 않음 | 계획과 탐색 |
| `auto` | 백그라운드 안전 분류기 검사를 거쳐 모든 작업 허용 | 오래 걸리는 작업, 프롬프트 피로 줄이기 |
| `bypassPermissions` | 모든 권한 확인 건너뛰기 | CI/CD, 헤드리스 환경 |
| `dontAsk` | 권한이 필요한 도구는 건너뛰기 | 비대화형 스크립팅 |

> **참고**: `auto` 모드는 대상 요금제, 모델, 제공자 조건을 갖춰야 쓸 수 있습니다 — [09-advanced-features/](09-advanced-features/#auto-mode)를 참고하세요. `bypassPermissions`는 신뢰할 수 있는 샌드박스 환경에서만 쓰세요.

**참고**: [공식 문서](https://code.claude.com/docs/ko/permissions)

---

## 서브에이전트

특정 작업을 위해 격리된 컨텍스트를 가진 전문 AI 어시스턴트입니다.

> **중첩 생성은 기본으로 켜져 있으며 깊이는 3(v2.1.219)**: 서브에이전트는 메인 대화 아래 세 단계까지 자신의 서브에이전트를 생성할 수 있습니다. 한도를 바꾸려면 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`를 설정하고, 중첩을 끄려면 `1`로 설정하세요. (이력: v2.1.172~v2.1.216에서는 바꿀 방법 없이 기본으로 5단계까지 중첩됐고, v2.1.217에서 깊이 1의 선택 기능이 되었다가, v2.1.219에서 기본값이 3이 되었습니다.) 특정 서브에이전트가 생성할 수 있는 서브에이전트를 제한하는 `Agent(agent_type)` 문법은 [04-subagents/README.md](04-subagents/README.md#생성-가능한-서브에이전트-제한)를 참고하세요.

### 기본 제공 서브에이전트

| 에이전트 | 설명 | 도구 | 모델 | 사용 시점 |
|-------|-------------|-------|-------|-------------|
| **general-purpose** | 여러 단계 작업, 조사 | 모든 도구 | 모델 상속 | 복잡한 조사, 여러 파일에 걸친 작업 |
| **Plan** | 구현 계획 | Read, Glob, Grep, Bash | 모델 상속 | 아키텍처 설계, 계획 |
| **Explore** | 코드베이스 탐색 | Read, Glob, Grep | 상속(최대 Opus) | 빠른 검색, 코드 이해 |
| **claude** | 더 전문화된 에이전트가 맞지 않는 작업을 모두 처리 | 모든 도구 | 모델 상속 | 전문 에이전트가 없는 작업, 디스패치된 백그라운드 세션의 기본 에이전트 |
| **statusline-setup** | 상태 표시줄 설정 | Bash, Read, Write | Sonnet | 상태 표시줄 구성 |
| **claude-code-guide** | 도움말과 문서 | Read, Glob, Grep | Haiku | 도움 받기, 기능 익히기 |

### 서브에이전트 설정 필드

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| `name` | string | 에이전트 식별자 |
| `description` | string | 에이전트가 하는 일 |
| `model` | string | 모델 재정의(`sonnet`, `opus`, `haiku`, `fable`, 전체 모델 ID, 또는 `inherit`) |
| `tools` | array | 허용할 도구 목록 |
| `effort` | string | 노력 수준(`low`, `medium`, `high`, `xhigh`, `max`. 모델에 따라 다름) |
| `initialPrompt` | string | 에이전트가 메인 세션 에이전트(`--agent`)로 실행될 때 자동으로 보내는 첫 사용자 턴 |
| `disallowedTools` | array | 이 에이전트에게 명시적으로 금지할 도구 |

### 사용자 정의 서브에이전트(예제)

| 에이전트 | 설명 | 사용 시점 | 범위 | 설치 |
|-------|-------------|-------------|-------|--------------|
| `code-reviewer` | 종합 코드 품질 | 코드 리뷰 세션 | 프로젝트 | `cp 04-subagents/code-reviewer.md .claude/agents/` |
| `clean-code-reviewer` | 클린 코드 원칙 리뷰 | 유지보수성 리뷰 | 프로젝트 | `cp 04-subagents/clean-code-reviewer.md .claude/agents/` |
| `test-engineer` | 테스트 전략과 커버리지 | 테스트 계획 | 프로젝트 | `cp 04-subagents/test-engineer.md .claude/agents/` |
| `documentation-writer` | 기술 문서 | API 문서, 가이드 | 프로젝트 | `cp 04-subagents/documentation-writer.md .claude/agents/` |
| `secure-reviewer` | 보안 중심 리뷰 | 보안 감사 | 프로젝트 | `cp 04-subagents/secure-reviewer.md .claude/agents/` |
| `implementation-agent` | 기능 전체 구현 | 기능 개발 | 프로젝트 | `cp 04-subagents/implementation-agent.md .claude/agents/` |
| `debugger` | 근본 원인 분석 | 버그 조사 | 사용자 | `cp 04-subagents/debugger.md .claude/agents/` |
| `data-scientist` | SQL 쿼리, 데이터 분석 | 데이터 작업 | 사용자 | `cp 04-subagents/data-scientist.md .claude/agents/` |
| `performance-optimizer` | 프로파일링과 성능 튜닝 | 병목 조사 | 프로젝트 | `cp 04-subagents/performance-optimizer.md .claude/agents/` |

> **범위**: **사용자** = 개인(`~/.claude/agents/`), **프로젝트** = 팀 공유(`.claude/agents/`)

**참고**: [04-subagents/](04-subagents/) | [공식 문서](https://code.claude.com/docs/ko/sub-agents)

**한 번에 설치(모든 사용자 정의 에이전트)**:
```bash
cp 04-subagents/*.md .claude/agents/
```

---

## 스킬

지침, 스크립트, 템플릿을 갖추고 자동으로 호출되는 기능입니다.

### 예제 스킬

| 스킬 | 설명 | 자동 호출 시점 | 범위 | 설치 |
|-------|-------------|-------------------|-------|--------------|
| `code-review-specialist` | 종합 코드 리뷰 | "이 코드 리뷰해 줘", "품질 확인해 줘" | 프로젝트 | `cp -r 03-skills/code-review-specialist .claude/skills/` |
| `brand-voice` | 브랜드 일관성 검사기 | 마케팅 문구를 쓸 때 | 프로젝트 | `cp -r 03-skills/brand-voice .claude/skills/` |
| `doc-generator` | API 문서 생성기 | "문서 만들어 줘", "API 문서화해 줘" | 프로젝트 | `cp -r 03-skills/doc-generator .claude/skills/` |
| `refactor` | 체계적인 코드 리팩토링(Martin Fowler) | "이거 리팩토링해 줘", "코드 정리해 줘" | 사용자 | `cp -r 03-skills/refactor ~/.claude/skills/` |
| `claude-md` | CLAUDE.md 파일 생성·갱신 | "CLAUDE.md 만들어 줘", "CLAUDE.md 점검해 줘" | 프로젝트 | `cp -r 03-skills/claude-md .claude/skills/` |
| `blog-draft` | 아이디어와 자료로 블로그 글 초안 작성 | "블로그 글 써 줘", "기사 초안 잡아 줘" | 사용자 | `cp -r 03-skills/blog-draft ~/.claude/skills/` |

> **범위**: **사용자** = 개인(`~/.claude/skills/`), **프로젝트** = 팀 공유(`.claude/skills/`)

### 스킬 구조

```
~/.claude/skills/skill-name/
├── SKILL.md          # 스킬 정의와 지침
├── scripts/          # 보조 스크립트
└── templates/        # 출력 템플릿
```

### 스킬 frontmatter 필드

스킬은 `SKILL.md`의 YAML frontmatter로 설정합니다:

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| `name` | string | 스킬 표시 이름 |
| `description` | string | 스킬이 하는 일 |
| `when_to_use` | string | `description` 뒤에 덧붙는 트리거 문구나 요청 예시 |
| `effort` | string | 노력 수준(`low`, `medium`, `high`, `xhigh`, `max`. 모델에 따라 다름) |
| `shell` | string | 인라인 `` !`command` `` 블록에 쓸 셸(기본값 `bash`, 또는 `powershell`) |

**참고**: [03-skills/](03-skills/) | [공식 문서](https://code.claude.com/docs/ko/skills)

**한 번에 설치(모든 스킬)**:
```bash
cp -r 03-skills/* ~/.claude/skills/
```

### 번들 스킬

| 스킬 | 설명 | 자동 호출 시점 |
|-------|-------------|-------------------|
| `/artifact-capabilities` | 게시된 아티팩트가 쓸 수 있는 런타임 기능(커넥터, 파일 다운로드) 레퍼런스 로드 | 이런 기능을 쓰는 아티팩트 페이지를 만들기 전 |
| `/artifact-diagramming` *(v2.1.221+)* | 아티팩트용 다이어그램 가이드 로드: 다이어그램이 도움이 되는 경우, 무엇을 그릴지, 밝은 테마와 어두운 테마 모두에서 잘 보이는 인라인 SVG | 아티팩트에 다이어그램을 그릴 때 |
| `/batch` | 큰 변경을 독립적인 단위 5~30개로 나누고, 단위마다 자체 worktree에서 백그라운드 서브에이전트가 실행 | 대규모 병렬 리팩토링 |
| `/claude-api` | Claude API로 앱 만들기 | API 개발 |
| `/claude-in-chrome [task]` | Claude in Chrome으로 브라우저에서 작업 수행(페이지 테스트, 양식 작성, 콘솔 로그 읽기). Chrome 통합이 켜져 있을 때 사용 가능 | 브라우저 작업 |
| `/dataviz [request]` | 차트, 그래프, 대시보드 디자인 가이드: 차트 형태, 역할별 색상, 색각 이상 안전성과 대비를 위한 팔레트 검증 | 차트나 대시보드를 만들 때 |
| `/debug [description]` | 세션의 디버그 로깅을 켜고 세션 디버그 로그로 문제 해결 | Claude Code 자체를 디버깅할 때 |
| `/design` *(v2.1.265+)* | 여러 아트보드로 구성된 디자인 캔버스 생성 — UI 목업, 화면 흐름, 랜딩 페이지, 포스터를 코드가 아니라 시각적으로 다듬습니다. Pro/Max/Team/Enterprise | HTML보다 직접 손으로 다듬고 싶은 화면이나 페이지를 디자인할 때 |
| `/design-sync [hint]` | 저장소의 React 디자인 시스템을 변환해 Claude Design에 올려, 디자인이 실제 컴포넌트를 쓰게 함. Anthropic API 전용. 독립형 Claude Design(claude.ai/design)은 2026년 12월 14일에 종료됩니다. | 디자인 시스템을 Claude Design과 동기화할 때 |
| `/design-login` | `/design-sync`의 디자인 시스템 접근 권한 부여 | `/design-sync`를 실행하기 전 |
| `/doctor [prompt-audit [path]]` | 설치, 설정, 확장 프로그램, `CLAUDE.md` 문제를 진단하고 수정 방법을 제안하는 설정 점검. 별칭: `/checkup` | 설정 문제를 해결할 때 |
| `/fewer-permission-prompts` | 대화 기록을 살펴 우선순위가 매겨진 허용 목록 제안 | 반복되는 권한 프롬프트 줄이기 |
| `/loop` | 지정한 간격으로 프롬프트 실행 | 반복 작업 |
| `/run` *(v2.1.145+)* | 프로젝트의 앱을 실행해 변경 사항이 동작하는 모습 확인 | 실제 앱에서 변경 사항 검증 |
| `/run-skill-generator` *(v2.1.145+)* | 특정 프로젝트를 다루는 방법을 `/run`/`/verify`에 학습시킴 | `/run`을 처음 쓰는 프로젝트 설정 |
| `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` | 현재 diff — 또는 PR, 브랜치, 경로 — 에서 정확성 버그를 리뷰합니다. `--fix`는 발견 사항을 적용하고, `--comment`는 PR 인라인 댓글로 게시합니다. 수준을 지정하지 않으면 마지막으로 입력한 수준을 다시 씁니다(v2.1.223). 낮은 노력 수준은 v2.1.218에서 **백그라운드 서브에이전트**로 옮겨졌고, `high`, `xhigh`, `max`도 v2.1.232에서 뒤따랐으므로 리뷰 출력이 더 이상 대화를 채우지 않습니다 | 코드를 작성한 뒤, PR을 병합하기 전 |
| `/slides [brief]` *(v2.1.265+)* | 요청 내용으로 Claude Slides 아티팩트 형태의 새 프레젠테이션 만들기. 아티팩트와 Slides 템플릿 필요 | 슬라이드 덱을 만들 때 |
| `/simplify` *(v2.1.154부터 다시 별도 명령어)* | 정리 전용 리뷰(재사용 / 단순화 / 효율 / 추상화 수준)를 실행하고 수정 사항 적용. 버그는 찾지 않음 | 버그 찾기 없이 코드만 정리할 때 |
| `/update-config [request]` | 설정 변경(명령어 허용, 환경 변수 설정, 훅 추가)을 설명하면 Claude가 해당 `settings.json`을 편집 | JSON을 직접 편집하지 않고 설정을 바꿀 때 |
| `/verify` *(v2.1.145+)* | 앱을 빌드하고 실행하고 관찰해 수정이 동작하는지 확인 | 수정 사항을 처음부터 끝까지 검증할 때 |
| `/workflow-authoring` *(v2.1.248+)* | 동적 워크플로우 스크립트 작성 레퍼런스(스크립트 API, 재개, 품질 패턴) 로드. 동적 워크플로우가 켜져 있을 때 사용 가능 | 워크플로우 스크립트를 쓰거나 고칠 때 |

---

## 플러그인

명령어, 에이전트, MCP 서버, 훅을 하나로 묶은 모음입니다.

### 예제 플러그인

| 플러그인 | 설명 | 구성 요소 | 사용 시점 | 범위 | 설치 |
|--------|-------------|------------|-------------|-------|--------------|
| `pr-review` | PR 리뷰 워크플로우 | 명령어 3개, 에이전트 3개, GitHub MCP | 코드 리뷰 | 프로젝트 | `claude --plugin-dir ./07-plugins/pr-review` |
| `devops-automation` | 배포와 모니터링 | 명령어 4개, 에이전트 3개, K8s MCP | DevOps 작업 | 프로젝트 | `/plugin install devops-automation` |
| `documentation` | 문서 생성 도구 모음 | 명령어 4개, 에이전트 3개, 템플릿 | 문서화 | 프로젝트 | `/plugin install documentation` |

> **범위**: **프로젝트** = 팀 공유, **사용자** = 개인 워크플로우

### 플러그인 구조

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json   # 매니페스트 파일(.claude-plugin/ 안에는 이 파일만 둠)
├── commands/         # 슬래시 명령어
├── agents/           # 서브에이전트
├── skills/           # 스킬(<name>/SKILL.md)
├── hooks/
│   └── hooks.json    # 훅 설정
├── .mcp.json         # MCP 설정
├── bin/              # 실행 파일
└── scripts/          # 유틸리티 스크립트
```

**참고**: [07-plugins/](07-plugins/) | [공식 문서](https://code.claude.com/docs/ko/plugins)

**플러그인 관리 명령어**:
```bash
/plugin list              # 설치된 플러그인 목록
/plugin install <name>    # 플러그인 설치
/plugin uninstall <name>  # 플러그인 제거
claude plugin update <name>   # 플러그인 업데이트 (CLI. /plugin update 형태는 본문에 언급되지만 명령어 레퍼런스에는 없음)
```

---

## MCP 서버

외부 도구와 API에 접근하기 위한 Model Context Protocol 서버입니다.

### 자주 쓰는 MCP 서버

| 서버 | 설명 | 사용 시점 | 범위 | 설치 |
|--------|-------------|-------------|-------|--------------|
| **GitHub** | PR 관리, 이슈, 코드 | GitHub 워크플로우 | 로컬 | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| **Database** | SQL 쿼리, 데이터 접근 | 데이터베이스 작업 | 로컬 | `claude mcp add db -- npx -y @modelcontextprotocol/server-postgres` |
| **Filesystem** | 고급 파일 작업 | 복잡한 파일 작업 | 로컬 | `claude mcp add fs -- npx -y @modelcontextprotocol/server-filesystem` |
| **Slack** | 팀 커뮤니케이션 | 알림, 업데이트 | 프로젝트 | 설정에서 구성 |
| **Google Docs** | 문서 접근 | 문서 편집, 검토 | 프로젝트 | 설정에서 구성 |
| **Asana** | 프로젝트 관리 | 작업 추적 | 프로젝트 | 설정에서 구성 |
| **Stripe** | 결제 데이터 | 재무 분석 | 프로젝트 | 설정에서 구성 |
| **Memory** | 지속 메모리 | 세션 간 기억 | 사용자 | 설정에서 구성 |
| **Context7** | 라이브러리 문서 | 최신 문서 조회 | 사용자 | 설정에서 구성(서드파티 서버) |

> **범위**: **로컬** = `--scope` 없이 `claude mcp add`를 실행했을 때의 기본값(나만, 이 프로젝트에서만. `~/.claude.json`), **프로젝트** = 팀(`.mcp.json`, `--scope project`), **사용자** = 개인(`~/.claude.json`, `--scope user`), **기본 제공** = 미리 설치됨

### MCP 설정 예시

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**참고**: [05-mcp/](05-mcp/) | [MCP 프로토콜 문서](https://modelcontextprotocol.io)

**한 번에 설치(GitHub MCP)**:
```bash
export GITHUB_TOKEN="your_token" && claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

---

## 훅

Claude Code 이벤트가 발생하면 셸 명령어를 실행하는 이벤트 기반 자동화입니다.

### 훅 이벤트

| 이벤트 | 설명 | 발생 시점 | 활용 사례 |
|-------|-------------|----------------|-----------|
| `SessionStart` | 세션 시작/재개 | 세션 초기화 | 준비 작업 |
| `Setup` | 저장소 설정이나 유지 보수 실행 | `--init-only`를 쓸 때, 또는 `-p`와 함께 `--init`/`--maintenance`를 쓸 때만 | 도구 준비, 의존성 설치 |
| `InstructionsLoaded` | 지침 로드됨 | CLAUDE.md나 규칙 파일이 로드될 때 | 사용자 정의 지침 처리 |
| `UserPromptSubmit` | 프롬프트 처리 전(v2.1.299부터는 스킬이나 사용자 정의 명령어가 확장되기 전에도) | 사용자가 메시지를 보낼 때 | 입력 검증 |
| `UserPromptExpansion` | 입력한 슬래시 명령어(스킬, 사용자 정의 명령어, MCP 프롬프트)가 프롬프트로 확장됨 | `UserPromptSubmit` 다음, 확장된 프롬프트가 Claude에 전달되기 전 | `/command` 직접 사용 차단, 스킬별 컨텍스트 추가, 명령어 기록 |
| `PreToolUse` | 도구 실행 전 | 어떤 도구든 실행되기 전 | 검증, 로깅 |
| `PermissionRequest` | 권한 대화 상자 표시 | 민감한 작업 전 | 사용자 정의 승인 흐름 |
| `PermissionDenied` | 사용자가 권한 프롬프트를 거부 | 권한 거부 후 | 로깅, 분석, 정책 적용 |
| `PostToolUse` | 도구 성공 후 | 어떤 도구든 완료된 후 | 포맷팅, 알림 |
| `PostToolUseFailure` | 도구 실행 실패 | 도구 오류 후 | 오류 처리, 로깅 |
| `PostToolBatch` | 여러 도구 사용이 한 묶음으로 끝난 후 | 도구 묶음이 끝날 때 | 종합 보고, 일괄 검증 |
| `Notification` | 알림 전송 | Claude가 알림을 보낼 때 | 외부 알림 |
| `MessageDisplay` | 어시스턴트 메시지 텍스트 표시 | 메시지가 렌더링되는 동안 | 표시 텍스트 변환이나 숨기기 |
| `SubagentStart` | 서브에이전트 생성 | 서브에이전트 작업 시작 | 서브에이전트 컨텍스트 초기화 |
| `SubagentStop` | 서브에이전트 종료 | 서브에이전트 작업 완료 | 후속 작업 연결 |
| `Stop` | Claude 응답 완료 | 응답이 끝났을 때 | 정리, 보고 |
| `StopFailure` | API 오류로 턴 종료 | API 오류 발생 | 오류 복구, 로깅 |
| `TeammateIdle` | 팀원 에이전트 유휴 | 에이전트 팀 조율 | 작업 분배 |
| `TaskCompleted` | 작업 완료 표시(할 일 도구가 켜져 있을 때만 발생 — [훅](06-hooks/README.md#훅-이벤트) 참고) | 작업 완료 | 작업 후 처리 |
| `TaskCreated` | TaskCreate로 작업 생성(할 일 도구가 켜져 있을 때만 발생 — [훅](06-hooks/README.md#훅-이벤트) 참고) | 새 작업 생성 | 작업 추적, 로깅 |
| `ConfigChange` | 설정 갱신 | 설정이 바뀔 때 | 설정 변경에 대응 |
| `CwdChanged` | 작업 디렉토리 변경 | 디렉토리가 바뀔 때 | 디렉토리별 준비 작업 |
| `DirectoryAdded` | 세션 도중 새 작업 디렉토리 등록 | `/add-dir`이나 SDK `register_repo_root` | 새 디렉토리용 도구 준비 |
| `FileChanged` | 감시 중인 파일 변경 | 파일이 수정될 때 | 파일 모니터링, 다시 빌드 |
| `PreCompact` | 압축 작업 전 | 컨텍스트 압축 | 상태 보존 |
| `PostCompact` | 컴팩션 완료 후 | 컴팩션이 끝났을 때 | 압축 후 작업 |
| `PreModelSwitch` | 요청된 모델 전환이 적용되기 전 | 모델 전환 요청 | 모델 변경 허용이나 거부 |
| `PostModelSwitch` | 세션의 모델이 바뀐 후 | 모델 전환 완료 | 모델 변경 기록이나 대응 |
| `WorktreeCreate` | worktree 생성 중 | git worktree 생성 | worktree 환경 준비 |
| `WorktreeRemove` | worktree 제거 중 | git worktree 제거 | worktree 리소스 정리 |
| `Elicitation` | MCP 서버가 입력 요청 | MCP 입력 요청(elicitation) | 입력 검증 |
| `ElicitationResult` | 사용자가 입력 요청에 응답 | 사용자가 응답할 때 | 응답 처리 |
| `SessionEnd` | 세션 종료 | 세션 종료 시 | 정리, 상태 저장 |

### 예제 훅

| 훅 | 설명 | 이벤트 | 범위 | 설치 |
|------|-------------|-------|-------|--------------|
| `pre-tool-check.sh` | 위험한 Bash 명령어를 차단하거나 경고 | PreToolUse:Bash | 사용자 | `cp 06-hooks/pre-tool-check.sh ~/.claude/hooks/` |
| `security-scan.sh` | 보안 검사 | PostToolUse:Write | 프로젝트 | `cp 06-hooks/security-scan.sh .claude/hooks/` |
| `format-code.sh` | 자동 포맷팅 | PostToolUse:Write | 사용자 | `cp 06-hooks/format-code.sh ~/.claude/hooks/` |
| `validate-prompt.sh` | 프롬프트 검증 | UserPromptSubmit | 프로젝트 | `cp 06-hooks/validate-prompt.sh .claude/hooks/` |
| `context-tracker.py` | 토큰 사용량 추적 | UserPromptSubmit, Stop | 사용자 | `cp 06-hooks/context-tracker.py ~/.claude/hooks/` |
| `context-tracker-tiktoken.py` | 토큰 사용량 추적(tiktoken, 정확도 약 90~95%) | UserPromptSubmit, Stop | 사용자 | `cp 06-hooks/context-tracker-tiktoken.py ~/.claude/hooks/` |
| `pre-commit.sh` | 커밋 전 검증 | PreToolUse:Bash | 프로젝트 | `cp 06-hooks/pre-commit.sh .claude/hooks/` |
| `log-bash.sh` | 명령어 로깅 | PostToolUse:Bash | 사용자 | `cp 06-hooks/log-bash.sh ~/.claude/hooks/` |
| `dependency-check.sh` | 매니페스트가 바뀌면 취약점 검사 | PostToolUse:Write | 프로젝트 | `cp 06-hooks/dependency-check.sh .claude/hooks/` |
| `notify-team.sh` | git push 시 팀 알림 | PostToolUse:Bash | 프로젝트 | `cp 06-hooks/notify-team.sh .claude/hooks/` |
| `session-end.sh` | 세션이 끝날 때 진행 상황 기록 | SessionEnd | 사용자 | `cp 06-hooks/session-end.sh ~/.claude/hooks/` |

> **범위**: **프로젝트** = 팀(`.claude/settings.json`), **사용자** = 개인(`~/.claude/settings.json`)

### 훅 설정

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/pre-tool-check.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/format-code.sh" }
        ]
      }
    ]
  }
}
```

**참고**: [06-hooks/](06-hooks/) | [공식 문서](https://code.claude.com/docs/ko/hooks)

**한 번에 설치(모든 훅)**:
```bash
mkdir -p ~/.claude/hooks && cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh
```

---

## 메모리 파일

세션이 바뀌어도 자동으로 로드되는 지속 컨텍스트입니다.

### 메모리 유형

| 유형 | 위치 | 범위 | 사용 시점 |
|------|----------|-------|-------------|
| **관리형 정책** | 조직에서 관리하는 정책 | 조직 | 조직 전체 표준 강제 |
| **프로젝트** | `./CLAUDE.md` | 프로젝트(팀) | 팀 표준, 프로젝트 컨텍스트 |
| **프로젝트 규칙** | `.claude/rules/` | 프로젝트(팀) | 모듈식 프로젝트 규칙 |
| **사용자** | `~/.claude/CLAUDE.md` | 사용자(개인) | 개인 선호 설정 |
| **사용자 규칙** | `~/.claude/rules/` | 사용자(개인) | 모듈식 개인 규칙 |
| **로컬** | `./CLAUDE.local.md` | 로컬(git에서 제외) | 컴퓨터별 로컬 재정의(gitignore 대상). https://code.claude.com/docs/ko/memory 에 개발자별 재정의 파일로 공식 지원된다고 나와 있습니다. |
| **자동 메모리** | 자동 | 세션 | 자동으로 기록되는 인사이트와 수정 사항 |

> **범위**: **조직** = 관리자가 관리, **프로젝트** = git으로 팀과 공유, **사용자** = 개인 선호 설정, **로컬** = 커밋하지 않음, **세션** = 자동 관리

**참고**: [02-memory/](02-memory/) | [공식 문서](https://code.claude.com/docs/ko/memory)

**한 번에 설치**:
```bash
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 새 기능

| 기능 | 설명 | 사용법 |
|---------|-------------|------------|
| **/focus** | 산만하지 않은 출력 표시를 위한 포커스 보기 전환(v2.1.110) | 오래 걸리는 작업 중 시각적 소음을 줄이려면 `/focus` 실행 |
| **/proactive** | `/loop`의 별칭 — 같은 반복 작업 동작(v2.1.105) | `/loop` 대신 `/proactive`를 써도 됨 |
| **/recap** | 기존 세션으로 돌아왔을 때 세션 요약 보기(v2.1.108) | 자리를 비운 뒤 `/recap`을 실행해 그동안 한 일 파악 |
| **/tui** | 터미널 UI 렌더러 설정: 깜빡임 없는 렌더링은 `/tui fullscreen`, 되돌리려면 `/tui default`. 인수 없이 `/tui`를 입력하면 현재 렌더러 출력(v2.1.110) | 전체 화면 터미널이나 tmux에서 `/tui fullscreen` 사용 |
| **/undo** | `/rewind`의 별칭(v2.1.108) | `/undo`, `/checkpoint`, `/rewind`를 같은 용도로 사용 |
| **Monitor 도구** | 폴링하는 대신 백그라운드 명령어의 stdout 스트림을 지켜보다가 이벤트에 반응(v2.1.98+) | [고급 기능](09-advanced-features/)에서 Monitor 도구 사용법 참고 |
| **출력 스타일** | 시스템 프롬프트로 Claude의 역할, 톤, 기본 응답 형식을 변경. 기본 제공: Default, Proactive, Explanatory, Learning, Concise | `/config` → Output style, `outputStyle` 설정, 또는 `/output-style` 실행(v2.1.91에서 제거됐다가 v2.1.269에서 다시 추가). [고급 기능](09-advanced-features/#output-styles) 참고 |
| **상태 표시줄** | 세션, 모델, 비용, 컨텍스트 JSON을 stdin으로 받는 명령어로 사용자 정의 상태 표시줄 렌더링 | `/statusline` 또는 `statusLine` 설정. [고급 기능](09-advanced-features/#status-line) 참고 |
| **커뮤니티 마켓플레이스** | Anthropic의 자동 검증을 통과한 서드파티 플러그인. 각 플러그인은 커밋 SHA로 고정됨 | `/plugin marketplace add anthropics/claude-plugins-community` 실행 후 `/plugin install <name>@claude-community` |
| **/team-onboarding** | 프로젝트의 Claude Code 설정으로 팀원 적응 가이드 자동 생성(v2.1.101) | 프로젝트에서 `/team-onboarding` 실행 |
| **Remote Control** | API로 Claude Code 세션을 원격 제어. **더 이상 연구 미리보기가 아닙니다** — `claude remote-control`을 실행 중인 컴퓨터는 모두 Claude 앱의 Code 탭에 기기 카드로 나타나므로 휴대폰에서 그 컴퓨터로 세션을 시작할 수 있습니다 | 컴퓨터에서 `claude remote-control`을 실행한 뒤 Claude 앱에서 기기 카드 선택. [고급 기능](09-advanced-features/README.md) 참고 |
| **웹 세션** | 클라우드 세션에서 Claude Code 실행 | `claude --cloud "task"`나 claude.ai/code에서 시작 |
| **데스크톱 앱** | Claude Code용 네이티브 데스크톱 애플리케이션 | `/desktop`을 쓰거나 Anthropic 웹사이트에서 다운로드 |
| **세션 간 메시징** | 세션끼리 메시지를 주고받음 — 내 다른 컴퓨터와 클라우드 세션 포함, `ListAgents`로 찾음(macOS/Linux v2.1.224+, 네이티브 Windows v2.1.234+) | [고급 기능](09-advanced-features/README.md#cross-session-messaging) 참고. 받는 메시지는 `crossSessionInbound`로 제어 |
| **자체 호스팅 러너** | Claude Code 웹, 모바일, 데스크톱 세션을 내 컴퓨터나 컨테이너에서 실행(v2.1.224+, Team/Enterprise) | `claude self-hosted-runner setup`. [CLI](10-cli/README.md) 참고 |
| **`archive` 플러그인 소스** | HTTPS zip에서 플러그인 설치. 선택적으로 `sha256`으로 고정(v2.1.224+) | [플러그인](07-plugins/README.md#archive-소스-v21224) 참고 |
| **`command` 플러그인 소스** | 로컬에 설치된 도구가 플러그인 디렉토리 경로를 출력(v2.1.229+) | [플러그인](07-plugins/README.md#command-소스-v21229) 참고 |
| **마켓플레이스 소유자 와일드카드** | `"owner/*"`로 GitHub 소유자 아래의 모든 마켓플레이스 저장소를 허용하거나 차단 — `strictKnownMarketplaces`와 `blockedMarketplaces`에서만(v2.1.223+) | [플러그인](07-plugins/README.md#마켓플레이스-설정) 참고 |
| **샌드박스 자격 증명 마스킹** | 샌드박스 안의 명령어는 대리 값(sentinel)을 읽고, 프록시가 외부로 나가는 요청에서 실제 비밀 정보로 바꿔 넣음(v2.1.221+, Linux/WSL) | [고급 기능](09-advanced-features/README.md#credential-masking-v21221-v21224) 참고 |
| **에이전트 팀** | 관련된 작업을 하는 여러 에이전트를 조율 | 협업하며 컨텍스트를 공유하는 팀원 에이전트 구성 |
| **작업 목록** | 백그라운드 작업 관리와 모니터링 | `/tasks`로 백그라운드 작업 보기와 관리 |
| **프롬프트 제안** | 컨텍스트를 반영한 명령어 제안 | 현재 컨텍스트에 따라 제안이 자동으로 나타남 |
| **Git worktree** | 병렬 개발을 위한 격리된 git worktree | worktree 명령어로 안전하게 브랜치를 병렬 작업 |
| **샌드박싱** | 안전을 위한 격리된 실행 환경 | `/sandbox`로 켜고 끔. 제한된 환경에서 명령어 실행 |
| **MCP OAuth** | MCP 서버용 OAuth 인증 | 안전한 접근을 위해 MCP 서버 설정에 OAuth 자격 증명 구성 |
| **MCP Tool Search** | MCP 도구를 동적으로 검색하고 발견 | 도구 검색으로 연결된 서버 전체에서 사용 가능한 MCP 도구 찾기 |
| **예약 작업** | `/loop`와 cron 도구로 반복 작업 설정 | `/loop 5m /command`나 CronCreate 도구 사용 |
| **Chrome 통합** | Claude in Chrome 확장 프로그램으로 내 Chrome/Edge를 조작(창이 보이고 내 로그인 사용) | `--chrome` 플래그나 `/chrome` 명령어 사용 |
| **키보드 사용자 정의** | 연속 키 조합(chord)을 포함한 키 바인딩 사용자 정의 | `/keybindings`를 쓰거나 `~/.claude/keybindings.json` 편집 |
| **자동 모드** | 백그라운드 안전 분류기 검사를 거치는 완전 자율 동작 | `Shift+Tab`으로 순환해 선택하거나 `--permission-mode auto` |
| **채널** | 여러 채널을 통한 커뮤니케이션(Telegram, Slack 등)(연구 미리보기) | 채널 플러그인 설정. 2026년 3월 |
| **음성 받아쓰기** | 프롬프트를 음성으로 입력 | 마이크 아이콘이나 음성 키 바인딩 사용 |
| **에이전트 훅 타입** | 셸 명령어 대신 서브에이전트를 생성하는 훅 | 훅 설정에서 `"type": "agent"` 지정 |
| **프롬프트 훅 타입** | Claude 모델에 프롬프트를 보내 한 번 평가받는 훅. 모델은 결정을 JSON으로 반환 | 훅 설정에서 `"type": "prompt"` 지정 |
| **MCP 입력 요청(Elicitation)** | MCP 서버가 도구 실행 중에 사용자 입력을 요청할 수 있음 | `Elicitation`과 `ElicitationResult` 훅 이벤트로 처리 |
| **플러그인 LSP 지원** | 플러그인을 통한 Language Server Protocol 통합 | 편집기 기능을 위해 `plugin.json`에 LSP 서버 구성 |
| **관리형 드롭인** | 조직이 관리하는 드롭인 설정(v2.1.83) | 관리형 정책으로 관리자가 구성하며 모든 사용자에게 자동 적용 |
| **`claude plugin init`** | `.claude/skills`에 새 플러그인 뼈대를 만들며, 이런 플러그인은 마켓플레이스 없이 자동 로드됨(v2.1.157) | `claude plugin init <name>` 실행 |
| **서드파티 제공자의 자동 모드** | Amazon Bedrock, Google Cloud의 Agent Platform, Microsoft Foundry, 로그인한 Claude 앱 게이트웨이 세션에서 기본으로 제공되며, 지원 모델은 Claude Sonnet 5 이상, Opus 4.7 이상, Haiku 5.5(v2.1.293+), Fable 모델입니다(v2.1.158~v2.1.206에서는 별도로 켜야 했으나 v2.1.207에서 이 요구 사항이 사라짐 — `CLAUDE_CODE_ENABLE_AUTO_MODE`는 여전히 허용되지만 효과 없음) | `Shift+Tab`으로 순환해 선택하거나 `--permission-mode auto` |
| **즉시 열리는 대화 상자 명령어** | Claude가 작업 중일 때도 `/permissions`를 열 수 있고(규칙 변경은 현재 턴의 나머지에 적용), `/add-dir`, `/autocompact`, `/theme`, `/help`, `/config`, `/advisor` 대화 상자는 Claude가 응답을 마칠 때까지 기다리지 않고 **전체 화면 TUI에서** 턴 도중에 열립니다(`/bug`는 v2.1.232부터 이미 그랬음)(v2.1.234) | Claude가 작업하는 동안 이 명령어 중 하나 실행. [슬래시 명령어](01-slash-commands/README.md) 참고 |
| **`CLAUDE_CODE_PROJECT_DIR_NAME`** | 프로젝트별 대화 기록 디렉토리 이름을 정하는 환경 변수(v2.1.234) | Claude Code를 실행하기 전에 셸/환경에서 설정. `CLAUDE_CONFIG_DIR`도 설정되어 있어야 적용됨. [CLI](10-cli/README.md) 참고 |
| **목표 점검 기준 시간** | `/goal`이 활성화된 동안 백그라운드 작업이 30분 넘게 진척이 없으면, Claude가 말없이 계속하는 대신 상태를 알려 줌. `CLAUDE_CODE_GOAL_CHECKIN_MINUTES`로 조정하고, `0`으로 설정하면 꺼짐(v2.1.234) | 활성 `/goal`과 함께 `CLAUDE_CODE_GOAL_CHECKIN_MINUTES=<n>` 설정. [슬래시 명령어](01-slash-commands/README.md) 참고 |
| **사용 한도 자동 이어 하기** | claude.ai 사용 한도에 막혀 있던 세션은 한도가 초기화되면 Claude Code가 자동으로 이어 감(v2.1.234) | 기본으로 켜져 있음. `/config` → "Continue automatically at usage limit"에서 끌 수 있음. [고급 기능](09-advanced-features/) 참고 |
| **`spellcheck` 설정** | `PATH`에 있는 aspell, hunspell, ispell 중 하나로 프롬프트 입력의 맞춤법 오류에 밑줄 표시. 기본값은 꺼짐(v2.1.235) | 검사기를 설치한 뒤 `~/.claude/settings.json`에 `"spellcheck": { "enabled": true }` 설정. 사용자 설정, `--settings`, 관리형 설정에서만 읽고 프로젝트 설정에서는 무시됨. [고급 기능](09-advanced-features/) 참고 |
| **에이전트 팀 기본 모델** | `/config`의 "Default teammate model" 설정이 제거됨. 이제 생성 호출에서 따로 지정하지 않는 한 팀원은 기본으로 팀 리더의 모델을 상속(v2.1.234) | [서브에이전트 — 에이전트 팀](04-subagents/README.md#에이전트-팀실험적-기능) 참고 |
| **`/design`** | 디자인 캔버스 — 아티팩트를 바탕으로 만들고 코드가 아니라 시각적으로 다듬는, 여러 아트보드로 구성된 시각 디자인(UI 목업, 화면 흐름, 랜딩 페이지, 포스터). v2.1.265+ 필요, Pro/Max/Team/Enterprise | CLI나 데스크톱 앱에서 `/design` 실행. [슬래시 명령어](01-slash-commands/README.md) 참고 |
| **`notify_when_idle`** | 같은 컴퓨터의 다른 세션에 다음에 유휴 상태가 될 때 알림을 한 번 보내 달라고 요청하는 세션 간 `SendMessage` 입력 — 선택 기능, 일회성, 폴링 없음(v2.1.236). 관련 변경: `ListAgents`가 세션 자신의 이름을 알려 주고 실행 중인 팀원을 나열하며, Windows에서도 세션 간 메시징을 쓸 수 있게 됨(v2.1.239) | `SendMessage`에 `notify_when_idle` 전달. [고급 기능](09-advanced-features/README.md#cross-session-messaging) 참고 |
| **플러그인 매니페스트 필드** | `plugin.json`이 `workflows`, `channels`, `dependencies`(semver), `outputStyles`, `keywords`, `metadata`, `lspServers`, `experimental.themes` / `experimental.monitors`를 받음. CLI에 `claude plugin new`, `remove`/`rm`, `prune`/`autoremove`와 플래그 `--with`, `-f`/`--force`, `--available`, `--push`, `--dry-run`이 추가됨 | [플러그인](07-plugins/README.md) 참고 |
| **제한 모드** | `--tools`에서 하나씩 지정하지 않는 한(`default` 프리셋으로는 안 됨) 명령어나 코드를 실행하는 기본 제공 도구(Bash, PowerShell 등)와 WebFetch를 제거합니다. 사용자·프로젝트·로컬 설정을 무시하고(관리형 설정과 `--settings`는 여전히 적용), 파일 도구를 작업 디렉토리로 제한하며, `bypassPermissions`를 거부하고, 클라우드 세션 생성도 거부합니다(v2.1.248+) | `claude --restricted` 또는 `CLAUDE_CODE_RESTRICTED=1`. [CLI](10-cli/README.md) 참고 |
| **`/advisor` 텍스트 형식** | `/advisor`, `/advisor <model>`, `/advisor off`가 대화 상자뿐 아니라 데스크톱 앱, Remote Control, 기타 헤드리스(`-p` / Agent SDK) 세션에서 텍스트 명령어로도 동작(v2.1.260+) | 헤드리스 세션에서 `/advisor off` 입력. [슬래시 명령어](01-slash-commands/README.md) 참고 |

---

## 빠른 참조 매트릭스

### 기능 선택 가이드

| 필요한 것 | 권장 기능 | 이유 |
|------|---------------------|-----|
| 빠른 단축 명령 | 슬래시 명령어 | 수동, 즉시 실행 |
| 계속 유지되는 컨텍스트 | 메모리 | 자동 로드 |
| 복잡한 자동화 | 스킬 | 자동 호출 |
| 전문 작업 | 서브에이전트 | 격리된 컨텍스트 |
| 외부 데이터 | MCP 서버 | 실시간 접근 |
| 이벤트 자동화 | 훅 | 이벤트로 실행 |
| 완성형 솔루션 | 플러그인 | 올인원 번들 |

### 설치 우선순위

| 우선순위 | 기능 | 명령어 |
|----------|---------|---------|
| 1. 필수 | 메모리 | `cp 02-memory/project-CLAUDE.md ./CLAUDE.md` |
| 2. 매일 사용 | 슬래시 명령어 | `cp 01-slash-commands/*.md .claude/commands/` |
| 3. 품질 | 서브에이전트 | `cp 04-subagents/*.md .claude/agents/` |
| 4. 자동화 | 훅 | `cp 06-hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh` |
| 5. 외부 연동 | MCP | `claude mcp add github -- npx -y @modelcontextprotocol/server-github` |
| 6. 고급 | 스킬 | `cp -r 03-skills/* ~/.claude/skills/` |
| 7. 완성 | 플러그인 | `claude --plugin-dir ./07-plugins/pr-review` |

---

## 명령어 하나로 전체 설치

이 저장소의 모든 예제를 설치합니다:

```bash
# 디렉토리 만들기
mkdir -p .claude/{commands,agents,skills} ~/.claude/{hooks,skills}

# 모든 기능 설치
cp 01-slash-commands/*.md .claude/commands/ && \
cp 02-memory/project-CLAUDE.md ./CLAUDE.md && \
cp -r 03-skills/* ~/.claude/skills/ && \
cp 04-subagents/*.md .claude/agents/ && \
cp 06-hooks/*.sh ~/.claude/hooks/ && \
chmod +x ~/.claude/hooks/*.sh
```

---

## 추가 자료

- [Claude Code 공식 문서](https://code.claude.com/docs/ko/overview)
- [MCP 프로토콜 명세](https://modelcontextprotocol.io)
- [학습 로드맵](LEARNING-ROADMAP.md)
- [메인 README](README.md)

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/sub-agents
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/ko/overview
- https://code.claude.com/docs/ko/commands
- https://code.claude.com/docs/ko/hooks
- https://code.claude.com/docs/ko/permission-modes
- https://code.claude.com/docs/en/changelog#2-1-172
- https://code.claude.com/docs/en/changelog#2-1-174
- https://github.com/anthropics/claude-code/releases/tag/v2.1.145
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://code.claude.com/docs/ko/plugins
- https://code.claude.com/docs/ko/cli-reference
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/ko/skills
- https://code.claude.com/docs/ko/plugin-marketplaces
- https://code.claude.com/docs/ko/discover-plugins
- https://code.claude.com/docs/ko/settings
- https://code.claude.com/docs/ko/plugins-reference
- https://code.claude.com/docs/en/slash-commands
- https://code.claude.com/docs/ko/fast-mode
- https://code.claude.com/docs/ko/permission-modes#eliminate-prompts-with-auto-mode
- https://code.claude.com/docs/ko/mcp
- https://code.claude.com/docs/ko/chrome
- https://code.claude.com/docs/ko/skills#bundled-skills
- https://code.claude.com/docs/en/plugins/manifest-reference
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/ko/env-vars
- https://code.claude.com/docs/en/cross-session-messaging
- https://support.claude.com/en/articles/17440474-migrate-from-standalone-claude-design-to-claude
**호환 모델**: Claude Fable 5.1, Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
