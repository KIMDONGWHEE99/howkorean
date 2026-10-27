# 심층 진단 — 라운드별 질문

심층 진단의 5라운드입니다. 라운드마다 AskUserQuestion을 한 번 호출하세요(다중 선택, 선택지 최대 4개). 각 라운드는 기능 영역 2개를 다루며 영역마다 선택지가 2개입니다. 라운드별 채점표는 SKILL.md 2B단계에도 똑같이 들어 있으므로, 이 파일을 다시 읽지 않고도 결과를 계산할 수 있습니다.

---

**1라운드 — 슬래시 명령어와 메모리**(header: "명령어")

"다음 중 해 본 것은 무엇인가요? 해당하는 것을 모두 고르세요."
선택지:
1. "사용자 정의 슬래시 명령어나 스킬 만들기" — frontmatter가 있는 SKILL.md 파일을 작성했거나 .claude/commands/ 파일을 만들어 봄
2. "명령어에서 동적 컨텍스트 사용" — 스킬/명령어 파일에서 `$ARGUMENTS`, `$0`/`$1`, 백틱 `!command` 문법, `@file` 참조를 써 봄
3. "프로젝트 + 개인 메모리 설정" — 프로젝트 CLAUDE.md와 개인 ~/.claude/CLAUDE.md(또는 CLAUDE.local.md)를 모두 만들어 봄
4. "메모리 계층 기능 사용" — 메모리 위치 7곳이 컨텍스트에 어떻게 이어 붙는지(루트부터 아래로 로드되고, 각 수준에서 CLAUDE.local.md가 CLAUDE.md 뒤에 붙으며, 하위 디렉토리 파일은 필요할 때 로드됨) 이해하고, .claude/rules/ 디렉토리, 경로별 규칙, @import 문법을 써 봄

**채점:** 선택지 1-2 → **슬래시 명령어**(0-2점), 선택지 3-4 → **메모리**(0-2점)

---

**2라운드 — 스킬과 훅**(header: "자동화")

"다음 중 해 본 것은 무엇인가요? 해당하는 것을 모두 고르세요."
선택지:
1. "자동 호출 스킬 설치와 사용" — /명령어로 직접 호출하지 않아도 description에 따라 자동으로 트리거되는 스킬
2. "스킬 호출 동작 제어" — SKILL.md frontmatter에서 `disable-model-invocation`, `user-invocable`, 또는 agent 필드와 함께 `context: fork`를 써 봄
3. "PreToolUse나 PostToolUse 훅 설정" — 도구 실행 전후에 실행되는 훅을 설정해 봄(예: 명령어 검사기, 자동 포매터)
4. "고급 훅 기능 사용" — prompt 타입 훅, 스킬 frontmatter 훅, HTTP 훅, 또는 사용자 정의 JSON 출력(updatedInput, systemMessage)을 쓰는 훅을 설정해 봄

**채점:** 선택지 1-2 → **스킬**(0-2점), 선택지 3-4 → **훅**(0-2점)

---

**3라운드 — MCP와 서브에이전트**(header: "통합")

"다음 중 해 본 것은 무엇인가요? 해당하는 것을 모두 고르세요."
선택지:
1. "MCP 서버를 연결해 도구 사용" — 예: PR/이슈용 GitHub MCP, 쿼리용 데이터베이스 MCP, 또는 다른 외부 데이터 소스
2. "고급 MCP 기능 사용" — 프로젝트 범위 .mcp.json, OAuth 인증, @멘션을 쓰는 MCP 리소스, 도구 검색(Tool Search), 또는 `claude mcp serve`
3. "사용자 정의 서브에이전트 만들기/설정" — .claude/agents/에 도구, 모델, 권한을 지정한 에이전트를 정의해 봄
4. "고급 서브에이전트 기능 사용" — worktree 격리, 지속 에이전트 메모리, Ctrl+B로 보내는 백그라운드 작업, `claude --agent`로 메인 스레드에서 실행하는 에이전트를 위한 `Agent(agent_type)` 에이전트 허용 목록(`Task(...)` 형식은 하위 호환 별칭), 또는 에이전트 팀

**채점:** 선택지 1-2 → **MCP**(0-2점), 선택지 3-4 → **서브에이전트**(0-2점)

---

**4라운드 — 체크포인트와 고급 기능**(header: "파워 유저")

"다음 중 해 본 것은 무엇인가요? 해당하는 것을 모두 고르세요."
선택지:
1. "체크포인트로 안전하게 실험" — Esc+Esc나 /rewind로 체크포인트까지 되감아 코드나 대화(또는 둘 다)를 복원했거나, 요약 옵션(여기부터 요약 / 여기까지 요약) 중 하나를 써 봄
2. "계획 모드나 확장 사고 사용" — /plan, Shift+Tab, --permission-mode plan으로 계획 모드를 켜 봄. 확장 사고를 끌 수 있는 모델에서 Alt+T/Option+T로 확장 사고를 켜고 꺼 봤거나, `/effort`로 추론 깊이를 정해 봄
3. "권한 모드 설정" — 여섯 가지 모드 — manual(설정 값 `default`, v2.1.200부터 Manual로 표시), acceptEdits, plan, auto, dontAsk, bypassPermissions — 중 하나를 CLI 플래그, 키보드 단축키, 설정으로 써 봄(기본으로 정해진 auto 모드로 시작하기만 한 경우는 해당하지 않음)
4. "원격/데스크톱/웹 기능 사용" — `claude --remote-control`, `claude --cloud`, `/teleport`, `/desktop`, 또는 `claude -w`로 worktree를 써 봄

**채점:** 선택지 1 → **체크포인트**(0-1점), 선택지 2-4 → **고급 기능**(0-3점)

---

**5라운드 — 플러그인과 CLI**(header: "숙달")

"다음 중 해 본 것은 무엇인가요? 해당하는 것을 모두 고르세요."
선택지:
1. "플러그인 설치하거나 만들기" — 마켓플레이스의 묶음 플러그인을 써 봤거나, plugin.json 매니페스트가 있는 .claude-plugin/ 디렉토리를 만들어 봄
2. "플러그인 고급 기능 사용" — 플러그인 스킬(`skills/` — 권장하는 형식이며, 네임스페이스가 붙는 `commands/`는 레거시지만 여전히 동작), 플러그인 훅, 플러그인 MCP 서버, LSP 설정, 또는 테스트용 --plugin-dir 플래그
3. "스크립트나 CI/CD에서 print 모드 사용" — --output-format json, --max-turns, 파이프 입력과 함께 `claude -p`를 썼거나, GitHub Actions / CI 파이프라인에 통합해 봄
4. "고급 CLI 기능 사용" — 세션 재개(-c/-r), --agents 플래그, 구조화된 출력을 위한 --json-schema, --fallback-model, --from-pr, 또는 일괄 처리 반복문

**채점:** 선택지 1-2 → **플러그인**(0-2점), 선택지 3-4 → **CLI**(0-2점)

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/memory
- https://code.claude.com/docs/ko/sub-agents
- https://code.claude.com/docs/ko/permission-modes
- https://code.claude.com/docs/ko/checkpointing
- https://code.claude.com/docs/ko/plugins-reference
- https://code.claude.com/docs/ko/permission-modes#which-mode-a-session-starts-in
- https://code.claude.com/docs/ko/hooks#hooks-in-skills-and-agents
- https://code.claude.com/docs/ko/model-config#extended-thinking
