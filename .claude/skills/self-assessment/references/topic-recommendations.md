# 주제별 추천

주제가 부족한 부분일 때 다음 추천을 쓰세요. 경로는 이 참조 파일(`.claude/skills/self-assessment/references/`)을 기준으로 한 상대 경로입니다.

**슬래시 명령어(0점)**:
- 튜토리얼: [01-slash-commands/](../../../../01-slash-commands/)
- 집중할 부분: 기본 제공 명령어 레퍼런스, 첫 SKILL.md 만들기, `$ARGUMENTS` 문법
- 핵심 실습: `/optimize` 명령어를 만들어 테스트하기
- 완료 기준: 인수와 동적 컨텍스트를 쓰는 사용자 정의 스킬을 만들 수 있음

**슬래시 명령어(1점 — 복습)**:
- 집중할 부분: ``!`command` `` 문법을 쓰는 동적 컨텍스트, `@file` 참조, `disable-model-invocation`과 `user-invocable`의 제어 차이
- 완료 기준: 실시간 명령어 출력을 주입하고 자신의 호출 동작을 제어하는 스킬을 만들 수 있음

**메모리(0점)**:
- 튜토리얼: [02-memory/](../../../../02-memory/)
- 집중할 부분: CLAUDE.md 만들기, `/init`과 `/memory` 명령어, 그리고 자동 메모리와의 차이(Claude에게 무언가를 기억해 달라고 하면 자동 메모리에 저장됨. CLAUDE.md에 넣으려면 "이걸 CLAUDE.md에 추가해 줘"라고 말하거나 `/memory`로 편집함 — 예전의 `#` 단축키는 제거됨)
- 핵심 실습: 내 코딩 표준을 담은 프로젝트 CLAUDE.md 만들기
- 완료 기준: 세션이 바뀌어도 Claude가 내 선호를 기억함

**메모리(1점 — 복습)**:
- 집중할 부분: 메모리 위치 7곳과 이들이 컨텍스트에 이어 붙는 방식(루트부터 아래로 로드되며, 서로 덮어쓰지 않음), 경로별 규칙을 담는 .claude/rules/ 디렉토리, `@import` 문법(최대 깊이 4), 자동 메모리 MEMORY.md(Claude는 처음 200줄과 25KB 중 먼저 닿는 쪽까지 로드함 — 파일 크기 제한이 아니라 로드 상한)
- 완료 기준: 디렉토리마다 모듈화된 규칙을 두고, 모든 메모리 파일이 컨텍스트에 어떻게 이어 붙는지 이해함

**스킬(0점)**:
- 튜토리얼: [03-skills/](../../../../03-skills/)
- 집중할 부분: SKILL.md 형식, description 필드를 통한 자동 호출, 점진적 공개(로딩 3단계)
- 핵심 실습: `03-skills/code-review-specialist`를 설치하고 자동으로 트리거되는지 확인하기
- 완료 기준: 스킬이 대화 맥락에 따라 자동으로 활성화됨

**스킬(1점 — 복습)**:
- 집중할 부분: 서브에이전트에서 실행하기 위한 `agent` 필드와 `context: fork`, `disable-model-invocation`과 `user-invocable`의 차이, 스킬 목록 예산(컨텍스트 윈도우의 1%, 대체값 8,000자. 각 항목의 `description` + `when_to_use`는 `skillListingMaxDescChars`에 따라 기본 1,536자로 제한됨), 함께 묶는 리소스(scripts/, references/, assets/)
- 완료 기준: 포크한 컨텍스트로 서브에이전트에서 실행되는 스킬을 만들 수 있음

**훅(0점)**:
- 튜토리얼: [06-hooks/](../../../../06-hooks/)
- 집중할 부분: 설정 구조(matcher + hooks 배열), PreToolUse/PostToolUse 이벤트, 종료 코드(0=성공, 2=차단), JSON 입출력 형식
- 핵심 실습: Bash 명령어를 검사하는 PreToolUse 훅 만들기
- 완료 기준: 훅이 위험한 명령어를 실행 전에 차단함

**훅(1점 — 복습)**:
- 집중할 부분: 훅 이벤트 33개 전체(PostToolUseFailure, StopFailure, TaskCreated, CwdChanged, FileChanged, PostCompact, Elicitation, ElicitationResult, Setup, UserPromptExpansion, MessageDisplay, PreModelSwitch, PostModelSwitch 포함 — 마지막 두 개는 v2.1.251에서 추가됨), 훅 타입 5가지(command, http, mcp_tool, prompt, agent — agent 훅은 실험적이며 바뀔 수 있음), SKILL.md frontmatter의 훅(호출된 뒤 세션 내내 유지됨. 서브에이전트 frontmatter의 훅은 서브에이전트가 끝나면 함께 끝남), allowedEnvVars를 쓰는 HTTP 훅, command 훅이나 HTTP 훅이 실패하면 동작을 차단하는 `onFailure: "block"`(v2.1.295+), SessionStart, Setup, CwdChanged, FileChanged에서 쓰는 `CLAUDE_ENV_FILE`
- 완료 기준: 프롬프트 기반 Stop 훅과 스킬 frontmatter의 훅을 만들 수 있음(그리고 그 훅이 남은 세션 동안 계속 등록되어 있다는 것을 앎)

**MCP(0점)**:
- 튜토리얼: [05-mcp/](../../../../05-mcp/)
- 집중할 부분: `claude mcp add` 명령어, 전송 방식(권장하는 `http`, `stdio`, 푸시형 서버용 `ws`, 지원 중단된 `sse` — `--transport`는 `ws`를 받지 않으므로 WebSocket 서버는 `claude mcp add-json`으로 추가함), GitHub MCP 설정, 환경 변수 확장
- 핵심 실습: GitHub MCP 서버를 추가하고 PR 조회하기
- 완료 기준: MCP로 외부 서비스의 실시간 데이터를 조회할 수 있음

**MCP(1점 — 복습)**:
- 집중할 부분: 프로젝트 범위 .mcp.json(사용자마다 처음 쓸 때 승인하며, 작업 공간 신뢰가 적용됨), OAuth 2.0 인증, `@server:resource` 멘션을 쓰는 MCP 리소스, 도구 검색(ENABLE_TOOL_SEARCH), `claude mcp serve`, 출력 한도(10,000토큰에서 경고, `MAX_MCP_OUTPUT_TOKENS`로 정하는 기본 최대값 25,000토큰, 디스크 저장 기준 50,000자)
- 완료 기준: 프로젝트 .mcp.json이 있고, 도구 검색이 기본적으로 MCP 도구를 어떻게 지연 로드하는지와 `ENABLE_TOOL_SEARCH=auto`/`false`가 무엇을 바꾸는지 이해함

**서브에이전트(0점)**:
- 튜토리얼: [04-subagents/](../../../../04-subagents/)
- 집중할 부분: 에이전트 파일 형식(.claude/agents/*.md), 기본 제공 에이전트(Explore, Plan, general-purpose, claude, statusline-setup, claude-code-guide), tools/model/permissionMode 설정, 생성 한도(v2.1.219부터 깊이 기본값 3, 동시 실행 기본값 20, 세션당 200개였던 생성 상한은 v2.1.224에서 제거됨)
- 핵심 실습: code-reviewer 서브에이전트를 만들고 위임을 테스트하기
- 완료 기준: Claude가 코드 리뷰를 내 사용자 정의 에이전트에 위임함

**서브에이전트(1점 — 복습)**:
- 집중할 부분: worktree 격리(`isolation: worktree`), 지속 에이전트 메모리(범위를 지정하는 `memory` 필드), 백그라운드 에이전트(Ctrl+B로 백그라운드로 보내고, Ctrl+X Ctrl+K를 두 번 누르면 모두 중지), `claude --agent`로 시작한 메인 스레드 에이전트를 위한 `Agent(agent_type)` 에이전트 허용 목록(`Task(...)`는 하위 호환 별칭으로 남아 있음. 서브에이전트 자신의 `tools`에서는 유형 목록이 무시됨), 에이전트 팀(`--teammate-mode`)
- 완료 기준: 지속 메모리를 가진 서브에이전트가 worktree 격리 상태로 실행됨

**체크포인트(0점)**:
- 튜토리얼: [08-checkpoints/](../../../../08-checkpoints/)
- 집중할 부분: Esc+Esc와 /rewind로 여는 방법, 되감기 옵션 6가지(코드와 대화 복원, 대화 복원, 코드 복원, 여기부터 요약, 여기까지 요약, 취소), 한계 — bash 파일 시스템 작업, 서브에이전트의 편집(포그라운드 `context: fork` 스킬 제외), Claude Code 밖에서 한 편집은 추적되지 않으며, 심볼릭 링크/하드 링크 경로는 복원할 때 건너뜀
- 핵심 실습: 실험적인 변경을 한 뒤 되감아 복원하기
- 완료 기준: 되감을 수 있다는 것을 알고 자신 있게 실험할 수 있음

**고급 기능(0점)**:
- 튜토리얼: [09-advanced-features/](../../../../09-advanced-features/)
- 집중할 부분: 계획 모드(/plan이나 Shift+Tab), 권한 모드(6가지: manual — 설정 값 `default`, v2.1.200부터 Manual로 표시 — acceptEdits, plan, auto, dontAsk, bypassPermissions), 확장 사고(Alt+T/Option+T 토글 — 사고가 항상 켜져 있는 Opus 5.5(기본 모델), Sonnet 5.5, Haiku 5.5, Fable 모델에서는 효과 없음)
- 핵심 실습: 계획 모드로 기능을 설계한 뒤 구현하기
- 완료 기준: 계획 모드와 구현 모드를 자연스럽게 오갈 수 있음

**고급 기능(1점 — 복습)**:
- 집중할 부분: Remote Control(`claude --remote-control`, 별칭 `--rc`), 웹 세션(`claude --cloud`. `--remote`는 지원 중단된 별칭), 데스크톱으로 넘기기(`/desktop`), worktree(`claude -w`), 작업 목록(Ctrl+T), 엔터프라이즈용 관리형 설정
- 완료 기준: CLI, 웹, 데스크톱 사이에서 세션을 넘길 수 있음

**플러그인(0점)**:
- 튜토리얼: [07-plugins/](../../../../07-plugins/)
- 집중할 부분: 플러그인 구조(.claude-plugin/plugin.json), 플러그인에 묶이는 것(스킬, 에이전트, MCP, 훅, 설정 — 그리고 레거시 `commands/` 디렉토리. 여전히 동작하지만 새 플러그인에는 `skills/`를 권장함), 마켓플레이스에서 설치하기(`/plugin install`, 또는 셸에서 `claude plugin install <plugin> --marketplace <source>`)
- 핵심 실습: 플러그인을 설치하고 구성 요소 살펴보기
- 완료 기준: 플러그인과 독립 구성 요소를 각각 언제 쓰는지 이해함

**플러그인(1점 — 복습)**:
- 집중할 부분: plugin.json 매니페스트 만들기, 플러그인 훅(hooks/hooks.json), LSP 설정(.lsp.json), `${CLAUDE_PLUGIN_ROOT}` 변수, 테스트용 --plugin-dir, 마켓플레이스에 공개하기, mods(플러그인에 담겨 배포되며 창, 명령어, 도구 호출 규칙을 추가하는 훅 모듈 — v2.1.287+)
- 완료 기준: 팀을 위한 플러그인을 만들고 테스트할 수 있음

**CLI(0점)**:
- 튜토리얼: [10-cli/](../../../../10-cli/)
- 집중할 부분: 대화형 모드와 print 모드의 차이, 파이프와 함께 쓰는 `claude -p`, `--output-format json`, 세션 관리(-c/-r)
- 핵심 실습: 파일을 `claude -p`에 파이프로 넘겨 JSON 출력 받기
- 완료 기준: 스크립트에서 Claude를 비대화형으로 쓸 수 있음

**CLI(1점 — 복습)**:
- 집중할 부분: JSON 설정을 쓰는 --agents 플래그, 구조화된 출력을 위한 --json-schema, --fallback-model, --from-pr, --strict-mcp-config, for 반복문을 쓰는 일괄 처리, `claude mcp serve`
- 완료 기준: 구조화된 JSON 출력으로 Claude를 쓰는 CI/CD 스크립트가 있음

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/hooks
- https://code.claude.com/docs/ko/memory
- https://code.claude.com/docs/ko/skills
- https://code.claude.com/docs/ko/mcp
- https://code.claude.com/docs/ko/sub-agents
- https://code.claude.com/docs/ko/checkpointing
- https://code.claude.com/docs/ko/permission-modes
- https://code.claude.com/docs/ko/plugins-reference
- https://code.claude.com/docs/ko/interactive-mode
- https://code.claude.com/docs/ko/model-config#extended-thinking
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/en/plugins/mods/overview
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/ko/mcp#configure-tool-search
- https://code.claude.com/docs/ko/mcp#project-server-approvals-and-workspace-trust
