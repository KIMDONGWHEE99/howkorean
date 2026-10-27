# 레슨 퀴즈 — 문제 은행

레슨마다 10문항이 있습니다. 각 문항에는 분류, 질문, 보기(3-4개), 정답, 해설, 복습 위치가 있습니다.

---

## 레슨 01: 슬래시 명령어

### Q1
- **분류**: 개념
- **질문**: Claude Code의 슬래시 명령어 네 가지 유형은 무엇인가요?
- **보기**: A) 기본 제공 명령어, 스킬, 플러그인 명령어, MCP 프롬프트 | B) 기본 제공 명령어, 사용자 정의 명령어, 훅 명령어, API 프롬프트 | C) 시스템, 사용자, 플러그인, 터미널 명령어 | D) 코어, 확장, 매크로, 스크립트 명령어
- **정답**: A
- **해설**: Claude Code에는 기본 제공 명령어(/help, /compact 등), 스킬(SKILL.md 파일), 플러그인 명령어(plugin-name:command 형식의 네임스페이스), MCP 프롬프트(/mcp__server__prompt)가 있습니다.
- **복습**: 개요 섹션

### Q2
- **분류**: 실무
- **질문**: 사용자가 넘긴 인수 전체를 스킬에 전달하려면 어떻게 하나요?
- **보기**: A) `${args}` 사용 | B) `$ARGUMENTS` 사용 | C) `$@` 사용 | D) `$INPUT` 사용
- **정답**: B
- **해설**: `$ARGUMENTS`는 명령어 이름 뒤의 텍스트를 모두 담습니다. 위치 인수에는 `$0`, `$1` 등을 씁니다.
- **복습**: 인수

### Q3
- **분류**: 개념
- **질문**: 같은 이름의 스킬(.claude/skills/name/SKILL.md)과 레거시 명령어(.claude/commands/name.md)가 모두 있으면 무엇이 우선하나요?
- **보기**: A) 레거시 명령어 | B) 스킬 | C) 먼저 만들어진 쪽 | D) Claude가 사용자에게 고르라고 묻는다
- **정답**: B
- **해설**: 이름이 같으면 스킬이 레거시 명령어보다 우선합니다. 스킬 시스템이 예전 명령어 시스템을 대체합니다.
- **복습**: 스킬과 명령어가 충돌할 때 섹션

### Q4
- **분류**: 실무
- **질문**: 스킬 프롬프트에 셸 명령어의 실시간 출력을 넣으려면 어떻게 하나요?
- **보기**: A) `$(command)` 문법 사용 | B) `!`command`` 문법(느낌표와 백틱) 사용 | C) `@shell:command` 문법 사용 | D) `{command}` 문법 사용
- **정답**: B
- **해설**: `!`command`` 문법은 셸 명령어를 실행해, Claude가 프롬프트를 보기 전에 그 출력을 스킬 프롬프트에 넣습니다.
- **복습**: 셸 명령어로 동적 컨텍스트 넣기

### Q5
- **분류**: 개념
- **질문**: 스킬 frontmatter의 `disable-model-invocation: true`는 무엇을 하나요?
- **보기**: A) 스킬이 아예 실행되지 않게 한다 | B) 사용자만 호출할 수 있게 한다(Claude가 자동으로 호출할 수 없음) | C) /help 메뉴에서 숨긴다 | D) 스킬의 AI 처리를 끈다
- **정답**: B
- **해설**: `disable-model-invocation: true`이면 사용자만 `/command-name`으로 명령어를 실행할 수 있습니다. Claude는 절대 자동으로 호출하지 않으므로, 배포처럼 부수 효과가 있는 스킬에 유용합니다.
- **복습**: Frontmatter 레퍼런스 섹션

### Q6
- **분류**: 실무
- **질문**: Claude만 자동으로 호출할 수 있는(사용자의 / 메뉴에서는 숨겨진) 스킬을 만들고 싶습니다. 어떤 frontmatter 필드를 설정하나요?
- **보기**: A) `disable-model-invocation: true` | B) `user-invocable: false` | C) `hidden: true` | D) `auto-only: true`
- **정답**: B
- **해설**: `user-invocable: false`는 사용자의 슬래시 메뉴에서 스킬을 숨기지만, Claude는 맥락에 따라 자동으로 호출할 수 있습니다.
- **복습**: Frontmatter 레퍼런스 섹션

### Q7
- **분류**: 실무
- **질문**: "deploy"라는 새 사용자 정의 스킬의 올바른 디렉토리 구조는 무엇인가요?
- **보기**: A) `.claude/commands/deploy.md` | B) `.claude/skills/deploy/SKILL.md` | C) `.claude/skills/deploy.md` | D) `.claude/deploy/SKILL.md`
- **정답**: B
- **해설**: 스킬은 `.claude/skills/` 아래의 디렉토리에 두고 그 안에 `SKILL.md` 파일을 넣습니다. 디렉토리 이름이 명령어 이름이 됩니다.
- **복습**: 사용자 정의 명령어를 스킬로 만들기 섹션

### Q8
- **분류**: 개념
- **질문**: 플러그인 명령어는 사용자 명령어와 이름이 충돌하지 않도록 어떻게 하나요?
- **보기**: A) `plugin-name:command-name` 네임스페이스를 쓴다 | B) 특별한 .plugin 확장자를 쓴다 | C) 앞에 `p/`를 붙인다 | D) 사용자 명령어를 자동으로 재정의한다
- **정답**: A
- **해설**: 플러그인 명령어는 `pr-review:check-security` 같은 네임스페이스를 써서 독립적인 사용자 명령어와 충돌하지 않습니다.
- **복습**: 플러그인 명령어 섹션

### Q9
- **분류**: 실무
- **질문**: 스킬이 특정 도구를 쓸 때마다 권한을 묻지 않게 하고 싶습니다. 어떤 frontmatter 필드를 추가하나요?
- **보기**: A) `tools: [Read, Grep]` | B) `allowed-tools: [Read, Grep]` | C) `permissions: [Read, Grep]` | D) `restrict-tools: [Read, Grep]`
- **정답**: B
- **해설**: `allowed-tools`는 스킬을 호출한 턴 동안 나열한 도구를 미리 승인하므로, Claude가 권한 확인 없이 그 도구를 쓸 수 있습니다. 이 승인은 다음 메시지를 보내면 사라집니다. 쓸 수 있는 도구를 제한하는 기능은 아닙니다 — 스킬이 활성인 동안 도구를 빼려면 `disallowed-tools`를 쓰세요.
- **복습**: Frontmatter 레퍼런스

### Q10
- **분류**: 개념
- **질문**: 스킬에서 `@file` 문법은 무엇에 쓰나요?
- **보기**: A) 다른 스킬 가져오기 | B) 파일을 참조해 그 내용을 프롬프트에 넣기 | C) 심볼릭 링크 만들기 | D) 파일 권한 설정
- **정답**: B
- **해설**: 스킬의 `@path/to/file` 문법은 참조한 파일의 내용을 프롬프트에 넣으므로, 스킬이 템플릿이나 컨텍스트 파일을 불러올 수 있습니다.
- **복습**: 파일 참조 섹션

---

## 레슨 02: 메모리

### Q1
- **분류**: 개념
- **질문**: CLAUDE.md 메모리 파일들은 서로 어떤 관계이며, 가장 큰 권한을 가진 것은 무엇인가요?
- **보기**: A) 상위 계층이 하위 계층을 완전히 재정의한다 | B) 컨텍스트에 이어 붙으며, 관리형 정책(Managed Policy)이 가장 먼저 로드되고 제외할 수 없다 | C) 가장 최근에 수정한 파일이 이긴다 | D) 프로젝트 메모리의 우선순위가 가장 높다
- **정답**: B
- **해설**: CLAUDE.md 파일들은 서로를 재정의하지 않고 컨텍스트에 이어 붙습니다 — 로드 순서는 우선순위가 아니라 컨텍스트 안의 위치를 정합니다. 관리형 정책(관리자가 관리)은 가장 먼저 로드되며 개별 설정으로 제외할 수 없습니다. 자동 메모리는 별개의 메커니즘입니다.
- **복습**: Claude Code의 메모리 계층 섹션

### Q2
- **분류**: 실무
- **질문**: 대화 중에 메모리에 새 규칙을 빠르게 추가하려면 어떻게 하나요?
- **보기**: A) `/memory` 슬래시 명령어를 쓰거나 대화로 요청한다 | B) 메시지 앞에 `#`를 붙인다(예: `# always use TypeScript`) | C) `/rule "rule text"`를 입력한다 | D) `@add-memory "rule text"`를 쓴다
- **정답**: A
- **해설**: `/memory`를 쓰면 CLAUDE.md와 자동 메모리 파일이 편집기에서 열리고, 아니면 Claude에게 대화로 요청하면 됩니다. Claude에게 무언가를 "기억해" 달라고 하면(예: "우리는 항상 TypeScript strict 모드를 쓴다는 걸 기억해 줘") 자동 메모리에 저장됩니다. 대신 CLAUDE.md에 넣으려면 "이걸 CLAUDE.md에 추가해 줘"라고 말하세요. `#` 접두사는 없어져서 더 이상 동작하지 않습니다.
- **복습**: README의 빠른 메모리 갱신 섹션

### Q3
- **분류**: 개념
- **질문**: CLAUDE.md에서 `@path/to/file` 가져오기의 최대 깊이는 얼마인가요?
- **보기**: A) 3단계 | B) 4단계 | C) 10단계 | D) 제한 없음
- **정답**: B
- **해설**: `@path` 가져오기 문법은 무한 반복을 막기 위해 최대 4단계까지 재귀적으로 가져옵니다.
- **복습**: `/memory` 명령어 섹션(가져오기 기능)

### Q4
- **분류**: 실무
- **질문**: 규칙 파일이 `src/api/` 안의 파일에만 적용되게 하려면 어떻게 하나요?
- **보기**: A) 규칙을 `src/api/CLAUDE.md`에 넣는다 | B) `.claude/rules/*.md` 파일에 `paths: src/api/**` YAML frontmatter를 추가한다 | C) 파일 이름을 `.claude/rules/api.md`로 짓는다 | D) 규칙 파일에 `@scope: src/api`를 쓴다
- **정답**: B
- **해설**: `.claude/rules/`의 파일은 `paths:` frontmatter 필드에 glob 패턴을 지정해 규칙을 특정 디렉토리로 한정할 수 있습니다.
- **복습**: YAML frontmatter로 경로별 규칙 지정 섹션

### Q5
- **분류**: 개념
- **질문**: 세션을 시작할 때 자동 메모리의 MEMORY.md에서 몇 줄이 로드되나요?
- **보기**: A) 전부 | B) 처음 100줄 | C) 처음 200줄 | D) 처음 500줄
- **정답**: C
- **해설**: MEMORY.md의 처음 200줄 또는 처음 25KB 중 먼저 닿는 쪽까지가 세션 시작 시 컨텍스트에 자동으로 로드됩니다. MEMORY.md에서 참조하는 주제 파일은 필요할 때 로드됩니다.
- **복습**: 자동 메모리 섹션

### Q6
- **분류**: 실무
- **질문**: git에 커밋하지 않을 개인용 프로젝트 선호 설정을 두고 싶습니다. 어떤 파일을 써야 하나요?
- **보기**: A) `~/.claude/CLAUDE.md` | B) `CLAUDE.local.md` | C) `.claude/rules/personal.md` | D) `.claude/memory/personal.md`
- **정답**: B
- **해설**: 프로젝트 루트의 `CLAUDE.local.md`는 프로젝트별 개인 선호 설정을 위한 파일입니다. git에서 무시하도록 해야 합니다.
- **복습**: 메모리 위치 표

### Q7
- **분류**: 개념
- **질문**: `/init` 명령어는 무엇을 하나요?
- **보기**: A) 새 Claude Code 프로젝트를 처음부터 초기화한다 | B) 프로젝트 구조를 바탕으로 CLAUDE.md 템플릿을 생성한다 | C) 모든 메모리를 기본값으로 초기화한다 | D) 새 세션을 만든다
- **정답**: B
- **해설**: `/init`은 프로젝트를 분석해 규칙과 표준을 제안하는 CLAUDE.md 템플릿을 생성합니다. 이미 CLAUDE.md가 있을 때 다시 실행하면 개선점을 제안합니다.
- **복습**: `/init` 명령어 섹션

### Q8
- **분류**: 실무
- **질문**: 자동 메모리를 완전히 끄려면 어떻게 하나요?
- **보기**: A) ~/.claude/projects 디렉토리를 삭제한다 | B) `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`을 설정한다 | C) CLAUDE.md에 `auto-memory: false`를 추가한다 | D) `/memory disable auto`를 쓴다
- **정답**: B
- **해설**: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`로 설정하면 자동 메모리가 꺼집니다. `0`이면 강제로 켜고, 설정하지 않으면 기본으로 켜집니다.
- **복습**: 자동 메모리 켜고 끄기

### Q9
- **분류**: 개념
- **질문**: 우선순위가 낮은 메모리 계층이 높은 계층의 규칙을 재정의할 수 있나요?
- **보기**: A) 예, 가장 최근 규칙이 항상 이긴다 | B) 아니요 — CLAUDE.md 파일은 재정의되지 않고 컨텍스트에 이어 붙으며, 로드 순서는 우선순위가 아니라 위치를 정한다 | C) 예, 낮은 계층이 `!important` 플래그를 쓰면 가능하다 | D) 규칙 유형에 따라 다르다
- **정답**: B
- **해설**: CLAUDE.md 파일들(사용자, 프로젝트, 로컬, 규칙)은 서로를 재정의하지 않고 컨텍스트에 이어 붙습니다 — 나중 파일은 앞 파일을 "대신"하는 것이 아니라 컨텍스트에서 더 뒤에 나타날 뿐입니다. 관리형 정책만 특별해서, 가장 먼저 로드되고 개별 설정으로 제외할 수 없습니다. 자동 메모리는 이어 붙는 순서에 속하지 않는 별개의 메커니즘입니다.
- **복습**: Claude Code의 메모리 계층 섹션

### Q10
- **분류**: 실무
- **질문**: 저장소 두 개를 오가며 일하는데, Claude가 두 저장소의 CLAUDE.md를 모두 로드하게 하고 싶습니다. 어떻게 하나요?
- **보기**: A) `claude --multi-repo /path/to/other` | B) `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir /path/to/other` | C) `claude --add-dir /path/to/other`만 쓴다 | D) `claude --include /path/to/other`
- **정답**: B
- **해설**: `--add-dir`만 쓰면 추가 디렉토리에 대한 파일 접근 권한만 생기고, 그 디렉토리의 CLAUDE.md는 기본적으로 로드되지 않습니다. `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`을 설정하면 Claude Code가 `--add-dir`로 추가한 디렉토리의 CLAUDE.md도 로드합니다.
- **복습**: `--add-dir`로 디렉토리 추가하기 섹션

---

## 레슨 03: 스킬

### Q1
- **분류**: 개념
- **질문**: 스킬 시스템의 점진적 공개 3단계는 무엇인가요?
- **보기**: A) 메타데이터, 지침, 리소스 | B) 이름, 본문, 첨부 파일 | C) 헤더, 내용, 스크립트 | D) 요약, 세부 사항, 데이터
- **정답**: A
- **해설**: 레벨 1은 메타데이터(약 100 토큰, 항상 로드), 레벨 2는 SKILL.md 본문(5천 토큰 미만, 트리거되면 로드), 레벨 3은 번들 리소스(scripts/references/assets, 필요할 때 로드)입니다.
- **복습**: 스킬의 동작 방식: 점진적 공개

### Q2
- **분류**: 실무
- **질문**: Claude가 스킬을 자동으로 호출하게 만드는 가장 중요한 요소는 무엇인가요?
- **보기**: A) 스킬 파일 이름 | B) 언제 쓰는지를 알려 주는 키워드가 담긴 frontmatter의 `description` 필드 | C) 스킬 디렉토리의 위치 | D) `auto-invoke: true` frontmatter 필드
- **정답**: B
- **해설**: Claude는 스킬의 `description`(그리고 선택 사항인 `when_to_use`)을 보고 자동으로 호출할지 정합니다. 구체적인 트리거 문구와 상황이 들어 있어야 합니다.
- **복습**: 스킬 호출 제어 섹션

### Q3
- **분류**: 개념
- **질문**: SKILL.md 파일의 권장 최대 길이는 얼마인가요?
- **보기**: A) 100줄 | B) 250줄 | C) 500줄 | D) 1000줄
- **정답**: C
- **해설**: SKILL.md는 500줄 이하로 유지해야 합니다. 더 큰 참고 자료는 `references/` 하위 디렉토리의 파일에 둡니다.
- **복습**: 4. SKILL.md는 500줄 이하로 섹션

### Q4
- **분류**: 실무
- **질문**: 스킬이 자체 컨텍스트를 가진 격리된 서브에이전트에서 실행되게 하려면 어떻게 하나요?
- **보기**: A) frontmatter에 `isolation: true` 설정 | B) frontmatter에 `context: fork`와 함께 `agent` 필드 설정 | C) frontmatter에 `subagent: true` 설정 | D) 스킬을 `.claude/agents/`에 둔다
- **정답**: B
- **해설**: `context: fork`는 스킬을 별도의 컨텍스트에서 실행하고, `agent` 필드는 어떤 에이전트 유형(예: `Explore`, `Plan`, 사용자 정의 에이전트)을 쓸지 지정합니다.
- **복습**: 서브에이전트에서 스킬 실행 섹션

### Q5
- **분류**: 개념
- **질문**: 스킬 메타데이터(레벨 1)에 할당되는 컨텍스트 예산은 대략 얼마인가요?
- **보기**: A) 컨텍스트 윈도우의 0.5% | B) 컨텍스트 윈도우의 1% | C) 컨텍스트 윈도우의 5% | D) 컨텍스트 윈도우의 10%
- **정답**: B
- **해설**: 스킬 메타데이터는 컨텍스트 윈도우의 약 1%를 차지합니다(대체값: 8,000자). `SLASH_COMMAND_TOOL_CHAR_BUDGET`이나 `skillListingBudgetFraction` 설정으로 바꿀 수 있습니다.
- **복습**: 자동 발견 섹션의 "설명 예산" 문단

### Q6
- **분류**: 실무
- **질문**: 스킬이 큰 API 명세를 참조해야 합니다. 명세를 어디에 두어야 하나요?
- **보기**: A) SKILL.md 안에 직접 | B) 스킬 디렉토리 안의 `references/api-spec.md` 파일 | C) 프로젝트의 CLAUDE.md | D) 별도의 `.claude/rules/` 파일
- **정답**: B
- **해설**: 큰 참고 자료는 `references/` 하위 디렉토리에 둡니다. Claude는 레벨 3 리소스를 필요할 때 로드하므로 SKILL.md를 가볍게 유지할 수 있습니다.
- **복습**: 보조 파일 섹션

### Q7
- **분류**: 개념
- **질문**: 스킬에서 참고 콘텐츠(Reference Content)와 작업 콘텐츠(Task Content)는 무엇이 다른가요?
- **보기**: A) 참고 콘텐츠는 읽기 전용, 작업 콘텐츠는 읽기/쓰기 | B) 참고 콘텐츠는 컨텍스트에 지식을 더하고, 작업 콘텐츠는 단계별 지침을 제공한다 | C) 참고 콘텐츠는 문서용, 작업 콘텐츠는 코드용 | D) 차이가 없다
- **정답**: B
- **해설**: 참고 콘텐츠는 Claude의 컨텍스트에 분야 지식(예: 브랜드 가이드라인)을 더합니다. 작업 콘텐츠는 워크플로우를 위한 실행 가능한 단계별 지침을 제공합니다.
- **복습**: 스킬 콘텐츠 유형 섹션

### Q8
- **분류**: 실무
- **질문**: claude.ai나 Skills API(Agent Skills 명세)로 공유할 스킬이라면, frontmatter의 `name` 필드에 어떤 문자를 쓸 수 있나요?
- **보기**: A) 아무 문자나 | B) 영문 소문자, 숫자, 하이픈만(최대 64자) | C) 영문자와 밑줄 | D) 영문자와 숫자만
- **정답**: B
- **해설**: 이름은 케밥 케이스(소문자, 하이픈)여야 하고 최대 64자입니다. `name` 자체는 선택 사항이라 생략하면 스킬 디렉토리 이름이 기본값이 되지만, 지정한다면 이 규칙을 따라야 합니다. Claude Code에서는 `anthropic-skills`라는 이름과 네임스페이스가 claude.ai에서 동기화한 스킬용으로 예약되어 있어 그 이름의 스킬은 로드되지 않습니다. "anthropic"이나 "claude"를 더 넓게 금지하는 규칙은 claude.ai 스킬 업로드와 Skills API에 적용됩니다. Claude Code 자체(v2.1.299)는 숨겨진 문자, 방향을 바꾸는 문자, 공백처럼 보이는 문자, `<`나 `>`가 들어 있거나 256자를 넘는 이름만 거부합니다.
- **복습**: SKILL.md 형식 섹션

### Q9
- **분류**: 개념
- **질문**: Claude는 어떤 순서로 스킬을 찾나요?
- **보기**: A) 사용자 > 프로젝트 > 엔터프라이즈 | B) 엔터프라이즈 > 개인 > 프로젝트(플러그인은 네임스페이스 사용) | C) 프로젝트 > 사용자 > 엔터프라이즈 | D) 알파벳순
- **정답**: B
- **해설**: 우선순위는 엔터프라이즈 > 개인 > 프로젝트입니다. 플러그인 스킬은 네임스페이스(plugin-name:skill)를 쓰므로 충돌하지 않습니다.
- **복습**: 스킬 유형과 위치

### Q10
- **분류**: 실무
- **질문**: 사용자가 직접 쓰는 것은 허용하면서 Claude가 스킬을 자동으로 호출하지 못하게 하려면 어떻게 하나요?
- **보기**: A) `user-invocable: false` 설정 | B) `disable-model-invocation: true` 설정 | C) description 필드 제거 | D) `auto-invoke: false` 설정
- **정답**: B
- **해설**: `disable-model-invocation: true`는 Claude의 자동 호출을 막지만, 사용자는 `/` 메뉴에서 스킬을 직접 쓸 수 있습니다.
- **복습**: 스킬 호출 제어

---

## 레슨 04: 서브에이전트

### Q1
- **분류**: 개념
- **질문**: 대화 안에서 바로 처리하는 것과 비교해 서브에이전트의 주된 장점은 무엇인가요?
- **보기**: A) 더 빠르다 | B) 별도의 깨끗한 컨텍스트 윈도우에서 동작해 컨텍스트 오염을 막는다 | C) 더 많은 도구를 쓸 수 있다 | D) 오류 처리가 더 낫다
- **정답**: B
- **해설**: 서브에이전트는 새 컨텍스트 윈도우를 받고, 메인 에이전트가 넘겨준 것만 받습니다. 그래서 메인 대화가 작업별 세부 사항으로 어지러워지지 않습니다.
- **복습**: 개요 섹션

### Q2
- **분류**: 실무
- **질문**: 에이전트 정의의 우선순위는 어떻게 되나요?
- **보기**: A) 프로젝트 > 사용자 > CLI | B) CLI > 프로젝트 > 사용자 | C) 사용자 > 프로젝트 > CLI | D) 모두 우선순위가 같다
- **정답**: B
- **해설**: 전체 순서는 관리형 설정 > `--agents` 플래그 > 프로젝트(`.claude/agents/`) > 사용자(`~/.claude/agents/`) > 플러그인입니다. 보기 중에서는 CLI > 프로젝트 > 사용자가 올바른 상대 순서입니다.
- **복습**: 파일 위치 섹션

### Q3
- **분류**: 개념
- **질문**: 읽기 전용 코드베이스 탐색에 최적화된 기본 제공 서브에이전트는 무엇인가요?
- **보기**: A) general-purpose | B) Plan | C) Explore | D) Bash
- **정답**: C
- **해설**: Explore 서브에이전트는 읽기 전용 코드베이스 검색 에이전트입니다. v2.1.198부터 세션 모델을 상속하며(Claude API에서는 Opus가 상한), `model: haiku`는 기본값이 아니라 직접 지정해야 하는 옵션입니다. quick, medium, very thorough 세 가지 철저함 수준을 지원합니다.
- **복습**: 기본 제공 서브에이전트 섹션

### Q4
- **분류**: 실무
- **질문**: 조율 에이전트가 생성할 수 있는 서브에이전트를 제한하려면 어떻게 하나요?
- **보기**: A) `allowed-agents:` 필드 사용 | B) `tools` 필드에 `Agent(agent_name)` 문법 사용 | C) `spawn-limit: 2` 설정 | D) `restrict-agents: [name1, name2]` 사용
- **정답**: B
- **해설**: `claude --agent`로 메인 스레드에서 실행되는 에이전트라면 `tools: Agent(worker, researcher)`가 허용 목록이 되어, "worker"나 "researcher"라는 서브에이전트만 생성할 수 있습니다. `Task(...)`도 별칭으로 여전히 동작합니다(Task 도구는 v2.1.63에서 Agent로 이름이 바뀌었습니다).
- **복습**: 생성 가능한 서브에이전트 제한 섹션

### Q5
- **분류**: 개념
- **질문**: 서브에이전트의 `isolation: worktree`는 무엇을 하나요?
- **보기**: A) 에이전트를 Docker 컨테이너에서 실행한다 | B) 에이전트에게 자체 git worktree를 주어 변경 사항이 메인 트리에 영향을 주지 않게 한다 | C) 에이전트가 어떤 파일도 읽지 못하게 한다 | D) 에이전트를 샌드박스에서 실행한다
- **정답**: B
- **해설**: worktree 격리는 별도의 git worktree를 만듭니다. 에이전트가 아무것도 바꾸지 않으면 자동으로 정리되고, 바꾼 것이 있으면 worktree 경로와 브랜치를 돌려줍니다.
- **복습**: worktree 격리 섹션

### Q6
- **분류**: 실무
- **질문**: 서브에이전트가 (인라인이 아니라) 항상 백그라운드에서 실행되게 하려면 어떻게 하나요?
- **보기**: A) 에이전트 설정에 `background: true` 설정 | B) 에이전트 설정에 `async: true` 사용 | C) 시작한 뒤 Ctrl+D 누르기 | D) `--background` CLI 플래그 사용
- **정답**: A
- **해설**: 에이전트 설정의 `background: true`는 서브에이전트가 항상 백그라운드 작업으로 실행되게 하고 인라인 실행을 막습니다. 메인 대화에서 Claude가 생성하는 서브에이전트는 이미 기본적으로 백그라운드에서 실행되지만(v2.1.198, 데스크톱 앱과 VS Code에서는 v2.1.302부터 항상), 서브에이전트 안에서 다시 호출하는 Agent는 `claude -p`, Agent SDK, 데스크톱 앱, VS Code에서 기본적으로 포그라운드로 실행됩니다. 사용자는 Ctrl+B를 눌러 실행 중인 포그라운드 작업을 백그라운드로 보낼 수도 있습니다.
- **복습**: 백그라운드 서브에이전트 섹션

### Q7
- **분류**: 개념
- **질문**: 서브에이전트에서 범위를 `project`로 지정한 `memory` 필드는 무엇을 하나요?
- **보기**: A) 프로젝트 CLAUDE.md를 읽을 수 있게 한다 | B) 현재 프로젝트로 범위가 한정된 지속 메모리 디렉토리를 만든다 | C) 메인 에이전트의 대화 기록을 공유한다 | D) 프로젝트의 git 기록을 로드한다
- **정답**: B
- **해설**: `memory` 필드는 서브에이전트를 위한 지속 디렉토리를 만듭니다. 범위가 `project`이면 메모리가 현재 프로젝트에 묶입니다. 에이전트 MEMORY.md의 처음 200줄 또는 25KB 중 먼저 닿는 쪽까지가 자동으로 로드됩니다.
- **복습**: 서브에이전트의 지속 메모리 섹션

### Q8
- **분류**: 실무
- **질문**: Claude가 서브에이전트에게 작업을 자동으로 위임하도록 유도하려면 서브에이전트의 설명에 어떤 문구를 넣나요?
- **보기**: A) "priority: high" 추가 | B) 설명에 "use PROACTIVELY"나 "MUST BE USED" 포함 | C) `auto-delegate: true` 설정 | D) "trigger: always" 추가
- **정답**: B
- **해설**: 설명에 "use PROACTIVELY"나 "MUST BE USED" 같은 문구를 넣으면 Claude가 해당하는 작업을 자동으로 위임하도록 강하게 유도할 수 있습니다.
- **복습**: 자동 위임 섹션

### Q9
- **분류**: 개념
- **질문**: 서브에이전트에 쓸 수 있는 `permissionMode` 값은 무엇인가요?
- **보기**: A) read, write, admin | B) manual, acceptEdits, bypassPermissions, plan, dontAsk, auto | C) safe, normal, dangerous | D) restricted, standard, elevated
- **정답**: B
- **해설**: 서브에이전트는 권한 모드 여섯 가지를 지원합니다: manual(읽기는 묻지 않고 실행하고 나머지는 모두 확인을 요청 — Manual로 표시되며 설정 값은 `default`이고, v2.1.200부터 manual도 별칭으로 받음), acceptEdits(파일 편집 자동 승인), bypassPermissions(모든 확인 건너뜀), plan(읽기 전용), dontAsk(미리 승인한 것이 아니면 자동 거부), auto(백그라운드 분류기가 판단).
- **복습**: 설정 필드 섹션

### Q10
- **분류**: 실무
- **질문**: 이전 실행에서 agentId를 돌려준 서브에이전트를 재개하려면 어떻게 하나요?
- **보기**: A) `/resume agent-id` 사용 | B) Claude에게 재개해 달라고 요청한다 — Claude가 에이전트 ID나 이름으로 SendMessage 도구를 써서 서브에이전트에게 메시지를 보낸다 | C) `claude -r agent-id` 사용 | D) 서브에이전트는 재개할 수 없다
- **정답**: B
- **해설**: 호출할 때마다 새 인스턴스가 시작됩니다. 이전 작업을 이어 가려면 Claude에게 서브에이전트를 재개해 달라고 요청하세요. Claude가 에이전트의 ID나 이름으로 SendMessage 도구를 쓰면 서브에이전트가 전체 대화 기록을 가진 채로 재개합니다. 기본 제공 Explore와 Plan 에이전트는 일회성이라 재개할 수 없습니다.
- **복습**: 재개 가능한 에이전트 섹션

---

## 레슨 05: MCP

### Q1
- **분류**: 개념
- **질문**: MCP 전송 프로토콜 네 가지는 무엇이며, 그중 권장되는 것은 무엇인가요?
- **보기**: A) HTTP(권장), Stdio, SSE(지원 중단), WebSocket(`ws`) | B) REST(권장), GraphQL, gRPC, Thrift | C) TCP, UDP, HTTP | D) Stdio(권장), HTTP, SSE
- **정답**: A
- **해설**: 원격 서버에는 HTTP를 권장합니다. Stdio는 로컬 프로세스용입니다(현재 가장 흔함). SSE는 지원 중단되었지만 아직 지원됩니다. WebSocket(`type: "ws"`)은 서버가 요청 없이 이벤트를 보내는 경우를 위해 양방향 연결을 계속 유지합니다. `--transport`가 아니라 `claude mcp add-json`이나 `.mcp.json`으로 추가하며, 헤더 기반 인증만 지원합니다.
- **복습**: MCP 설치 방법 섹션

### Q2
- **분류**: 실무
- **질문**: CLI로 GitHub MCP 서버를 추가하려면 어떻게 하나요?
- **보기**: A) `claude mcp install github` | B) `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` | C) `claude plugin add github-mcp` | D) `claude connect github`
- **정답**: B
- **해설**: `claude mcp add`에 `--transport` 플래그, 이름, 서버 URL을 넘깁니다. GitHub 원격 서버에는 인증 헤더도 필요합니다: `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"`.
- **복습**: MCP 설정 관리 섹션

### Q3
- **분류**: 개념
- **질문**: `ENABLE_TOOL_SEARCH=auto`일 때 MCP 도구 정의가 컨텍스트 윈도우의 10%에 이르면 어떻게 되나요?
- **보기**: A) 잘린다 | B) 도구 검색이 작동한다: MCP 도구를 미뤄 두었다가 필요할 때 찾는다 | C) Claude가 오류를 보여 준다 | D) 남는 도구가 비활성화된다
- **정답**: B
- **해설**: 기본값(`ENABLE_TOOL_SEARCH`를 설정하지 않음)에서는 도구 검색이 이미 켜져 있어 모든 MCP 도구가 미뤄집니다. `auto`는 임계값 모드로, 도구 정의가 컨텍스트 윈도우의 10%에 이를 때까지는 미리 로드하다가 그 뒤로는 전부 미룹니다(`auto:N`으로 비율을 직접 정할 수 있음). 도구 검색에는 `tool_reference` 블록을 지원하는 모델(Opus 4, Sonnet 4, Haiku 4.5 이상)이 필요합니다.
- **복습**: MCP 도구 검색 섹션

### Q4
- **분류**: 실무
- **질문**: MCP 설정에서 환경 변수의 대체값은 어떻게 지정하나요?
- **보기**: A) `${VAR || "default"}` | B) `${VAR:-default}` | C) `${VAR:default}` | D) `${VAR ? "default"}`
- **정답**: B
- **해설**: `${VAR:-default}`는 환경 변수가 설정되어 있지 않을 때 쓸 대체값을 지정합니다. `VAR`가 설정되어 있지 않고 기본값도 없으면 서버는 `${VAR}`라는 글자 그대로 로드되며, `claude mcp list`와 `/mcp`가 빠진 변수에 대해 경고합니다.
- **복습**: 설정의 환경 변수 확장 섹션

### Q5
- **분류**: 개념
- **질문**: 데이터 접근 측면에서 MCP와 메모리는 무엇이 다른가요?
- **보기**: A) MCP는 빠르고 메모리는 느리다 | B) MCP는 실시간으로 바뀌는 외부 데이터용이고, 메모리는 지속되는 정적 선호 설정용이다 | C) MCP는 코드용, 메모리는 텍스트용이다 | D) 서로 바꿔 쓸 수 있다
- **정답**: B
- **해설**: MCP는 실시간으로 바뀌는 외부 데이터 소스(API, 데이터베이스)에 연결합니다. 메모리는 지속되는 정적 프로젝트 컨텍스트와 선호 설정을 저장합니다.
- **복습**: MCP와 메모리: 결정 매트릭스 섹션

### Q6
- **분류**: 실무
- **질문**: 팀원이 프로젝트 범위의 `.mcp.json`을 처음 만나면 어떻게 되나요?
- **보기**: A) 자동으로 로드된다 | B) 프로젝트의 MCP 서버를 신뢰할지 묻는 승인 확인이 뜬다 | C) 설정에서 직접 켜지 않으면 무시된다 | D) Claude가 관리자에게 승인을 요청한다
- **정답**: B
- **해설**: 프로젝트 범위의 `.mcp.json`은 팀원마다 처음 쓸 때 보안 승인 확인을 띄웁니다. 신뢰할 수 없는 MCP 서버를 막기 위해 의도된 동작입니다.
- **복습**: MCP 범위 섹션

### Q7
- **분류**: 개념
- **질문**: `claude mcp serve`는 무엇을 하나요?
- **보기**: A) MCP 서버 대시보드를 시작한다 | B) Claude Code 자체가 다른 애플리케이션을 위한 MCP 서버로 동작하게 한다 | C) MCP 문서를 제공한다 | D) MCP 서버 연결을 테스트한다
- **정답**: B
- **해설**: `claude mcp serve`는 Claude Code를 MCP 서버로 바꿔, Claude 인스턴스 하나를 다른 인스턴스가 제어하는 멀티 에이전트 오케스트레이션을 가능하게 합니다.
- **복습**: MCP 서버로 쓰는 Claude (`claude mcp serve`) 섹션

### Q8
- **분류**: 실무
- **질문**: MCP 도구 출력의 기본 최대 크기는 얼마인가요?
- **보기**: A) 5,000 토큰 | B) 10,000 토큰 | C) 25,000 토큰 | D) 50,000 토큰
- **정답**: C
- **해설**: 기본 최대값은 25,000 토큰입니다(`MAX_MCP_OUTPUT_TOKENS`). 1만 토큰에서 경고가 나타나며, 50,000자가 넘는 텍스트 결과는 파일로 저장됩니다.
- **복습**: MCP 출력 한도 섹션

### Q9
- **분류**: 개념
- **질문**: 관리형 설정에서 `allowedMcpServers`와 `deniedMcpServers`가 모두 같은 서버에 일치하면 무엇이 이기나요?
- **보기**: A) 허용이 이긴다 | B) 거부가 이긴다 | C) 마지막에 설정한 것이 이긴다 | D) 둘 다 독립적으로 적용된다
- **정답**: B
- **해설**: 관리형 MCP 설정에서는 거부 규칙이 언제나 허용 규칙보다 우선합니다.
- **복습**: 관리형 MCP 설정(엔터프라이즈) 섹션

### Q10
- **분류**: 실무
- **질문**: 대화에서 MCP 리소스를 참조하려면 어떻게 하나요?
- **보기**: A) `/mcp resource-name` 사용 | B) `@server-name:protocol://resource/path` 멘션 문법 사용 | C) `mcp.get("resource")` 사용 | D) 리소스는 자동으로 로드된다
- **정답**: B
- **해설**: MCP 리소스는 대화에서 `@server-name:protocol://resource/path` 멘션 문법으로 접근합니다.
- **복습**: @ 멘션으로 MCP 리소스 참조 섹션

---

## 레슨 06: 훅

### Q1
- **분류**: 개념
- **질문**: Claude Code의 훅 다섯 가지 유형은 무엇인가요?
- **보기**: A) Pre, Post, Error, Filter, Transform 훅 | B) Command, HTTP, MCP Tool, Prompt, Agent 훅 | C) Before, After, Around, Through, Beside 훅 | D) Input, Output, Filter, Transform, Validate 훅
- **정답**: B
- **해설**: Command 훅은 셸 스크립트를 실행하고, HTTP 훅은 웹훅 엔드포인트를 호출하고, MCP Tool 훅은 MCP 도구를 호출하고, Prompt 훅은 단일 턴 LLM 평가를 쓰고, Agent 훅은 서브에이전트 기반 검증을 씁니다. Agent 훅은 실험적 기능이라 바뀔 수 있습니다.
- **복습**: 훅 타입 섹션

### Q2
- **분류**: 실무
- **질문**: 훅 스크립트가 종료 코드 2로 끝나면 어떻게 되나요?
- **보기**: A) 차단하지 않는 경고가 표시된다 | B) 차단 오류 — stderr가 Claude에게 오류로 표시되고 도구 사용이 막힌다 | C) 훅을 다시 시도한다 | D) 세션이 끝난다
- **정답**: B
- **해설**: 종료 코드 0은 성공/계속, 종료 코드 2는 차단 오류(stderr가 오류로 표시됨), 그 밖의 0이 아닌 값은 차단하지 않는 오류입니다(대화 기록에 stderr 첫 줄과 함께 `<hook name> hook error` 알림이 표시되고 작업은 그대로 진행됨). v2.1.295부터는 command 훅이나 HTTP 훅에 `"onFailure": "block"`을 설정하면 이런 실패도 종료 코드 2처럼 차단합니다.
- **복습**: 종료 코드 섹션

### Q3
- **분류**: 개념
- **질문**: PreToolUse 훅은 stdin으로 어떤 JSON 필드를 받나요?
- **보기**: A) `tool_name`과 `tool_output` | B) `session_id`, `tool_name`, `tool_input`, `hook_event_name`, `cwd` 등 | C) `tool_name`만 | D) 전체 대화 기록
- **정답**: B
- **해설**: 훅은 stdin으로 다음을 담은 JSON 객체를 받습니다: session_id, transcript_path, hook_event_name, tool_name, tool_input, tool_use_id, cwd, permission_mode.
- **복습**: JSON 입력(stdin으로)

### Q4
- **분류**: 실무
- **질문**: PreToolUse 훅이 실행 전에 도구의 입력 매개변수를 바꾸려면 어떻게 하나요?
- **보기**: A) 수정한 JSON을 stderr로 돌려준다 | B) `updatedInput` 필드를 담은 JSON을 stdout으로 돌려준다(종료 코드 0) | C) 임시 파일에 쓴다 | D) 훅은 입력을 바꿀 수 없다
- **정답**: B
- **해설**: PreToolUse 훅은 stdout으로 `"updatedInput": {...}`을 담은 JSON을 출력해(종료 코드 0) Claude가 쓰기 전에 도구의 매개변수를 바꿀 수 있습니다. `updatedInput`은 `hookSpecificOutput` 아래에 두며 입력 객체 전체를 교체합니다. v2.1.300부터는 Claude 자신의 입력처럼 검증되므로, 알 수 없는 키는 버려지고 도구가 거부하는 입력이면 호출이 거부됩니다.
- **복습**: PreToolUse 섹션

### Q5
- **분류**: 개념
- **질문**: 세션에 환경 변수를 유지하는 `CLAUDE_ENV_FILE`을 지원하는 훅 이벤트는 무엇인가요?
- **보기**: A) PreToolUse | B) UserPromptSubmit | C) SessionStart | D) 모든 이벤트
- **정답**: C
- **해설**: `CLAUDE_ENV_FILE`은 SessionStart, Setup, CwdChanged, FileChanged 훅에서 쓸 수 있으며, 이 훅들은 이를 이용해 세션에 환경 변수를 유지합니다. 보기 중에서는 SessionStart가 이를 지원합니다 — PreToolUse와 UserPromptSubmit은 지원하지 않으며, 모든 이벤트에서 쓸 수 있는 것도 아닙니다.
- **복습**: SessionStart 섹션

### Q6
- **분류**: 실무
- **질문**: 도구를 호출할 때마다가 아니라 스킬이 처음 로드될 때 한 번만 실행되는 훅을 원합니다. 어떤 필드를 추가하나요?
- **보기**: A) `run-once: true` | B) 스킬 frontmatter의 훅에 `once: true` | C) `single: true` | D) `max-runs: 1`
- **정답**: B
- **해설**: 스킬 frontmatter에 선언한 훅은 `once: true`를 지원합니다 — Claude Code는 훅이 처음 성공적으로 실행되면 그 훅을 제거합니다(실패하거나, 차단하거나, 시간이 초과되면 그대로 남음). `once`는 스킬 frontmatter에서만 적용됩니다.
- **복습**: 구성 요소 범위 훅 섹션

### Q7
- **분류**: 개념
- **질문**: 서브에이전트의 frontmatter에 Stop 훅을 정의하면 자동으로 무엇으로 바뀌나요?
- **보기**: A) PostToolUse 훅 | B) SubagentStop 훅 | C) SessionEnd 훅 | D) Stop 훅 그대로 유지된다
- **정답**: B
- **해설**: 서브에이전트의 frontmatter에 둔 Stop 훅은 자동으로 SubagentStop으로 바뀌어, 그 서브에이전트가 끝날 때 실행됩니다.
- **복습**: 구성 요소 범위 훅 섹션

### Q8
- **분류**: 실무
- **질문**: 특정 서버의 모든 MCP 도구에 훅이 일치하게 하려면 어떻게 하나요?
- **보기**: A) `matcher: "mcp_github"` | B) `matcher: "mcp__github__.*"`(정규식 패턴) | C) `matcher: "mcp:github:*"` | D) `matcher: "github-mcp"`
- **정답**: B
- **해설**: matcher에는 정규식 패턴을 씁니다. MCP 도구는 `mcp__server__tool` 이름 규칙을 따르므로 `mcp__github__.*`는 GitHub MCP 도구 전체와 일치합니다.
- **복습**: 매처 패턴 섹션

### Q9
- **분류**: 개념
- **질문**: Claude Code가 지원하는 훅 이벤트는 모두 몇 개인가요?
- **보기**: A) 16 | B) 25 | C) 33 | D) 40
- **정답**: C
- **해설**: Claude Code는 훅 이벤트 33개를 지원합니다. 네 그룹으로 나뉩니다: 세션 수명 주기(`SessionStart`, `Setup`, `SessionEnd`), 프롬프트와 메시지 처리(`UserPromptSubmit`, `UserPromptExpansion`, `MessageDisplay`), 도구 사용과 권한(`PreToolUse`, `PostToolUse`, `PermissionRequest`, …), 에이전트·작업·환경 조율(`SubagentStart`, `TaskCreated`, `CwdChanged`, `WorktreeCreate`, `PreModelSwitch`, `PostModelSwitch`, …).
- **복습**: 훅 이벤트 표

### Q10
- **분류**: 실무
- **질문**: 훅이 실행되지 않는 이유를 디버깅하고 싶습니다. 가장 좋은 방법은 무엇인가요?
- **보기**: A) 훅 스크립트에 출력문을 추가한다 | B) `--debug` 플래그를 쓰고 `Ctrl+O`로 대화 기록 보기를 연다 | C) 시스템 로그를 확인한다 | D) 훅에는 디버깅 도구가 없다
- **정답**: B
- **해설**: `claude --debug`(또는 `--debug-file <path>`, 세션 중에는 `/debug`)는 어떤 훅이 실행되는지, 그 입력과 출력까지 포함해 훅 실행을 디버그 로그에 기록합니다. `Ctrl+O`로 대화 기록 보기를 열면 훅 결과를 볼 수 있습니다.
- **복습**: 디버깅 섹션

---

## 레슨 07: 플러그인

### Q1
- **분류**: 개념
- **질문**: 플러그인의 핵심 매니페스트 파일은 무엇이며 어디에 있나요?
- **보기**: A) 루트 디렉토리의 `plugin.yaml` | B) `.claude-plugin/plugin.json` | C) "claude" 키가 있는 `package.json` | D) `.claude/plugin.md`
- **정답**: B
- **해설**: 플러그인 매니페스트는 `.claude-plugin/plugin.json`에 있습니다. 매니페스트 자체는 선택 사항이며, 있다면 필수 키는 `name`(케밥 케이스 식별자) 하나뿐입니다. `description`, `version`, `author`, `homepage`, `repository`, `license`는 선택 메타데이터입니다.
- **복습**: 플러그인 정의 구조 섹션

### Q2
- **분류**: 실무
- **질문**: 공개하기 전에 세션에서 시험해 보려고 로컬 디렉토리의 플러그인을 로드하려면 어떻게 하나요?
- **보기**: A) `/plugin test ./my-plugin` 사용 | B) `claude --plugin-dir ./my-plugin` 사용 | C) `claude plugin validate ./my-plugin` 사용 | D) ~/.claude/plugins/에 복사
- **정답**: B
- **해설**: `--plugin-dir` 플래그는 테스트용으로 로컬 디렉토리의 플러그인을 로드합니다. 여러 번 지정해 플러그인 여러 개를 로드할 수 있습니다. `claude plugin validate ./my-plugin`은 매니페스트와 구성 요소를 검사하지만 플러그인을 세션에 로드하지는 않습니다.
- **복습**: 플러그인 테스트 섹션

### Q3
- **분류**: 개념
- **질문**: 플러그인 훅과 MCP 설정 안에서 플러그인 설치 디렉토리를 가리킬 때 쓸 수 있는 환경 변수는 무엇인가요?
- **보기**: A) `$PLUGIN_HOME` | B) `${CLAUDE_PLUGIN_ROOT}` | C) `$PLUGIN_DIR` | D) `${CLAUDE_PLUGIN_PATH}`
- **정답**: B
- **해설**: `${CLAUDE_PLUGIN_ROOT}`는 플러그인이 설치된 디렉토리로 바뀌므로, 훅과 MCP 설정에서 이식성 있게 경로를 참조할 수 있습니다.
- **복습**: 레슨 05(MCP)의 플러그인이 제공하는 MCP 서버 섹션

### Q4
- **분류**: 실무
- **질문**: "pr-review" 플러그인에 "check-security"라는 명령어가 있습니다. 사용자는 이 명령어를 어떻게 실행하나요?
- **보기**: A) `/check-security` | B) `/pr-review:check-security` | C) `/plugin pr-review check-security` | D) `/pr-review/check-security`
- **정답**: B
- **해설**: 플러그인 명령어는 `plugin-name:command-name` 네임스페이스를 써서 사용자 명령어나 다른 플러그인과 충돌하지 않습니다.
- **복습**: 레슨 01(슬래시 명령어)의 플러그인 명령어 섹션

### Q5
- **분류**: 개념
- **질문**: 플러그인에 묶을 수 있는 구성 요소는 무엇인가요?
- **보기**: A) 명령어와 설정만 | B) 스킬, 에이전트, 명령어, 훅, MCP 서버, LSP 설정, 설정, 템플릿, 스크립트 | C) 명령어, 훅, MCP 서버만 | D) 스킬과 에이전트만
- **정답**: B
- **해설**: 플러그인에는 skills/, agents/, commands/, hooks/hooks.json, .mcp.json, .lsp.json, settings.json, templates/, scripts/, docs/, tests/를 묶을 수 있습니다. `commands/`는 레거시이므로, 기존 `commands/` 디렉토리는 계속 동작하지만 새 플러그인에는 `skills/`를 쓰라는 것이 공식 안내입니다.
- **복습**: 플러그인 구조 예 섹션

### Q6
- **분류**: 실무
- **질문**: GitHub에서 플러그인을 설치하려면 어떻게 하나요?
- **보기**: A) `claude plugin add github:username/repo` | B) `/plugin marketplace add username/repo`를 실행한 뒤 `/plugin install plugin-name@marketplace-name` | C) `npm install @claude/username-repo` | D) `git clone`한 뒤 `claude plugin register`
- **정답**: B
- **해설**: `/plugin marketplace add username/repo`로 GitHub 저장소를 마켓플레이스로 추가한 다음 `/plugin install plugin-name@marketplace-name`으로 설치합니다. 세션 안에서 `/plugin install plugin-name --marketplace username/repo`(v2.1.275+)를 쓰거나 셸에서 `claude plugin install plugin-name --marketplace username/repo`(v2.1.292+)를 쓰면 한 번에 할 수도 있습니다. `github:` 형식의 설치 방법은 없습니다.
- **복습**: 설치 방법 섹션

### Q7
- **분류**: 개념
- **질문**: 플러그인의 `settings.json`에서 `agent` 키는 무엇을 하나요?
- **보기**: A) 인증 자격 증명을 지정한다 | B) 플러그인의 메인 스레드 에이전트를 정한다 | C) 쓸 수 있는 서브에이전트를 나열한다 | D) 에이전트 권한을 설정한다
- **정답**: B
- **해설**: 플러그인 settings.json의 `agent` 키는 플러그인이 활성일 때 어떤 에이전트 정의를 메인 스레드 에이전트로 쓸지 지정합니다.
- **복습**: 플러그인 설정 섹션

### Q8
- **분류**: 실무
- **질문**: 플러그인 수명 주기(켜기/끄기/업데이트)는 어떻게 관리하나요?
- **보기**: A) 설정 파일을 직접 편집한다 | B) `/plugin enable`, `/plugin disable`, `claude plugin update <name>` 사용 | C) `claude plugin-manager` 사용 | D) 플러그인을 다시 설치한다
- **정답**: B
- **해설**: `/plugin enable`과 `/plugin disable`은 실제로 있는 슬래시 명령어입니다. 설치한 플러그인의 업데이트에는 플러그인 레퍼런스에 문서화된 `claude plugin update <name>`을 쓰며, 업데이트가 있을 때 Claude Code가 안내하는 것도 이 형식입니다.
- **복습**: 플러그인 CLI 명령어 섹션

### Q9
- **분류**: 개념
- **질문**: 독립적인 스킬/훅/MCP와 비교해 플러그인의 주된 장점은 무엇인가요?
- **보기**: A) 플러그인이 더 빠르다 | B) 명령어 하나로 설치하고, 버전이 관리되며, 마켓플레이스로 배포되고, 모든 것을 함께 묶는다 | C) 플러그인이 더 많은 권한을 가진다 | D) 플러그인은 오프라인에서도 동작한다
- **정답**: B
- **해설**: 플러그인은 여러 구성 요소를 버전 관리, 마켓플레이스 배포, 자동 업데이트가 되는 설치 단위 하나로 묶습니다 — 독립 구성 요소를 하나하나 직접 설정하는 것과 대조됩니다.
- **복습**: 독립 실행형과 플러그인 방식 비교

### Q10
- **분류**: 실무
- **질문**: 플러그인 디렉토리 안에서 플러그인 훅 설정은 어디에 두나요?
- **보기**: A) `.claude-plugin/hooks.json` | B) `hooks/hooks.json` | C) `plugin.json`의 hooks 섹션 | D) `.claude/settings.json`
- **정답**: B
- **해설**: 플러그인 훅은 플러그인 디렉토리 구조 안의 `hooks/hooks.json`에서 설정합니다.
- **복습**: 플러그인 구조 예

---

## 레슨 08: 체크포인트

### Q1
- **분류**: 개념
- **질문**: 체크포인트가 담는 네 가지는 무엇인가요?
- **보기**: A) git 커밋, 브랜치, 태그, stash | B) 메시지, 파일 수정, 도구 사용 기록, 세션 컨텍스트 | C) 코드, 테스트, 로그, 설정 | D) 입력, 출력, 오류, 시간
- **정답**: B
- **해설**: 체크포인트는 대화 메시지, Claude의 도구로 수정한 파일, 도구 사용 기록, 세션 컨텍스트를 담습니다.
- **복습**: 개요 섹션

### Q2
- **분류**: 실무
- **질문**: 체크포인트 브라우저는 어떻게 여나요?
- **보기**: A) `/restore` 명령어 사용 | B) `Esc + Esc`(Esc 두 번)를 누르거나 `/rewind` 사용 | C) `/history` 명령어 사용 | D) `Ctrl+Z` 누르기
- **정답**: B
- **해설**: Esc를 두 번(Esc+Esc) 누르거나 `/rewind` 명령어를 쓰면 체크포인트 브라우저가 열려 복원 지점을 고를 수 있습니다.
- **복습**: 체크포인트 열기 섹션

### Q3
- **분류**: 개념
- **질문**: 되감기 옵션은 몇 개이며, 무엇이 있나요?
- **보기**: A) 3개: 실행 취소, 다시 실행, 초기화 | B) 6개: 코드와 대화 복원, 대화 복원, 코드 복원, 여기부터 요약, 여기까지 요약, 취소(Never mind) | C) 2개: 전체 복원, 부분 복원 | D) 4개: 코드, 메시지, 둘 다, 취소
- **정답**: B
- **해설**: 여섯 가지 옵션은 코드와 대화 복원(전체 롤백), 대화만 복원, 코드만 복원, 여기부터 요약(앞쪽으로 압축), 여기까지 요약(뒤쪽으로 압축), 취소입니다. 두 요약 옵션으로 컨텍스트를 양방향으로 압축할 수 있습니다.
- **복습**: 되감기 옵션 섹션

### Q4
- **분류**: 실무
- **질문**: Claude Code에서 Bash로 `rm -rf temp/`를 실행한 뒤 되감기를 하려고 합니다. 체크포인트가 그 파일들을 복원할까요?
- **보기**: A) 예, 체크포인트는 모든 것을 담는다 | B) 아니요, Bash 파일 시스템 작업(rm, mv, cp)은 체크포인트가 추적하지 않는다 | C) 대신 Edit 도구를 썼을 때만 복원된다 | D) autoCheckpoint를 켰을 때만 복원된다
- **정답**: B
- **해설**: 체크포인트는 메인 스레드에서 Claude 자신의 Write/Edit 도구로 바꾼 파일을 추적합니다. Bash 명령어(rm, mv, cp), 서브에이전트의 편집(포그라운드 `context: fork` 스킬 제외), Claude Code 밖에서 한 편집, 심볼릭 링크/하드 링크 경로는 모두 체크포인트 추적 범위 밖입니다.
- **복습**: 제한 사항 섹션

### Q5
- **분류**: 개념
- **질문**: 체크포인트는 얼마 동안 보관되나요?
- **보기**: A) 세션이 끝날 때까지 | B) 7일 | C) 30일 | D) 무기한
- **정답**: C
- **해설**: 체크포인트는 세션과 함께 저장되므로 세션을 재개한 뒤에도 `/rewind`가 동작합니다. 스냅숏은 세션이 마지막으로 스냅숏을 저장한 뒤 약 30일이 지나면 삭제되며(`cleanupPeriodDays`), 가장 최근 체크포인트 100개만 파일 스냅숏을 유지합니다. 보관 기간은 `cleanupPeriodDays`로 정합니다.
- **복습**: 체크포인트 보존 섹션

### Q6
- **분류**: 실무
- **질문**: 되감을 때 "여기부터 요약(Summarize from here)"은 무엇을 하나요?
- **보기**: A) 그 시점부터의 대화를 삭제한다 | B) 원래 내용은 대화 기록에 보존한 채, 대화를 AI가 만든 요약으로 압축한다 | C) 변경 사항을 글머리 기호 목록으로 만든다 | D) 대화를 파일로 내보낸다
- **정답**: B
- **해설**: 요약은 대화를 AI가 만든 더 짧은 요약으로 압축합니다. 원래 전체 텍스트는 대화 기록 파일에 보존됩니다.
- **복습**: 되감기 옵션 섹션

### Q7
- **분류**: 개념
- **질문**: 체크포인트는 언제 자동으로 만들어지나요?
- **보기**: A) 5분마다 | B) 사용자 프롬프트마다 | C) 직접 저장할 때만 | D) 도구를 쓸 때마다
- **정답**: B
- **해설**: 자동 체크포인트는 사용자 프롬프트마다 만들어지며, Claude가 요청을 처리하기 전의 상태를 담습니다.
- **복습**: 자동 체크포인트 섹션

### Q8
- **분류**: 실무
- **질문**: 자동 체크포인트 생성을 끄려면 어떻게 하나요?
- **보기**: A) `--no-checkpoints` 플래그 사용 | B) 설정에서 `fileCheckpointingEnabled: false` 지정 | C) 체크포인트 디렉토리 삭제 | D) 체크포인트는 끌 수 없다
- **정답**: B
- **해설**: 설정에서 `fileCheckpointingEnabled: false`로 지정하면 자동 체크포인트 생성이 꺼집니다(기본값은 true, v2.1.119+ 필요). 같은 효과의 환경 변수는 `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`입니다.
- **복습**: 설정 섹션

### Q9
- **분류**: 개념
- **질문**: 체크포인트가 git 커밋을 대신할 수 있나요?
- **보기**: A) 예, 더 강력하다 | B) 아니요, 서로 보완 관계다 — 체크포인트는 세션 범위이고 만료되지만, git은 영구적이고 공유할 수 있다 | C) 작은 프로젝트라면 예 | D) 혼자 개발할 때만
- **정답**: B
- **해설**: 체크포인트는 임시(30일 보관)이고 세션 범위이며 공유할 수 없습니다. git 커밋은 영구적이고 감사할 수 있으며 공유할 수 있습니다. 둘을 함께 쓰세요.
- **복습**: Git과의 통합 섹션

### Q10
- **분류**: 실무
- **질문**: 서로 다른 두 접근 방식을 비교하고 싶습니다. 권장되는 체크포인트 워크플로우는 무엇인가요?
- **보기**: A) 별도의 세션 두 개를 만든다 | B) 접근 방식 A 전에 체크포인트를 두고 시도한 뒤, 그 체크포인트로 되감아 접근 방식 B를 시도하고 결과를 비교한다 | C) 대신 git 브랜치를 쓴다 | D) 접근 방식을 비교할 좋은 방법은 없다
- **정답**: B
- **해설**: 분기 전략: 깨끗한 상태에서 체크포인트를 두고, 접근 방식 A를 시도해 결과를 적어 둔 뒤, 같은 체크포인트로 되감아 접근 방식 B를 시도합니다. 두 결과를 비교하세요.
- **복습**: 워크플로우 패턴 섹션

---

## 레슨 09: 고급 기능

### Q1
- **분류**: 개념
- **질문**: Claude Code의 권한 모드 여섯 가지는 무엇인가요?
- **보기**: A) read, write, execute, admin, root, sudo | B) manual, acceptEdits, plan, auto, dontAsk, bypassPermissions | C) safe, normal, elevated, admin, unrestricted, god | D) view, edit, run, deploy, full, bypass
- **정답**: B
- **해설**: 여섯 가지 모드는 manual(읽기는 묻지 않고 실행하고 나머지는 모두 확인을 요청 — Manual로 표시되며 설정 값은 `default`이고, v2.1.200부터 manual도 별칭으로 받음), acceptEdits(파일 편집 자동 승인), plan(읽기 전용 분석), auto(백그라운드 분류기가 판단), dontAsk(미리 승인한 것이 아니면 자동 거부), bypassPermissions(모든 확인 건너뜀)입니다.
- **복습**: 권한 모드 섹션

### Q2
- **분류**: 실무
- **질문**: 계획 모드는 어떻게 켜나요?
- **보기**: A) `/plan` 명령어로만 | B) `/plan`, `Shift+Tab`/`Alt+M`, `--permission-mode plan` 플래그, 또는 기본값 설정으로 | C) `--planning` 플래그로만 | D) 계획 모드는 항상 켜져 있다
- **정답**: B
- **해설**: 계획 모드는 여러 방법으로 켤 수 있습니다: /plan 명령어, Shift+Tab/Alt+M 단축키, --permission-mode plan CLI 플래그, 또는 설정의 기본값.
- **복습**: 계획 모드 섹션

### Q3
- **분류**: 개념
- **질문**: `opusplan` 모델 별칭은 무엇을 하나요?
- **보기**: A) 모든 작업에 Opus만 쓴다 | B) 계획 단계에는 Opus를, 구현에는 Sonnet을 쓴다 | C) 계획에 최적화된 특별한 모델을 쓴다 | D) 계획 모드를 자동으로 켠다
- **정답**: B
- **해설**: `opusplan`은 계획 단계에는 Opus(더 높은 품질의 분석)를, 실행 단계에는 Sonnet(더 빠른 구현)을 쓰는 모델 별칭입니다.
- **복습**: 계획 모드 섹션

### Q4
- **분류**: 실무
- **질문**: 사고를 끌 수 있는 모델(예: Sonnet 5)에서 세션 중에 확장 사고를 켜고 끄려면 어떻게 하나요?
- **보기**: A) `/effort max` 입력 | B) `Option+T`(macOS)나 `Alt+T` 누르기 | C) 프롬프트에 "ultrathink" 넣기 | D) 항상 켜져 있어 끌 수 없다
- **정답**: B
- **해설**: Option+T(macOS)나 Alt+T는 세션의 확장 사고를 켜고 끕니다(`Ctrl+O`는 추론 텍스트를 보여 주거나 숨기는 자세한 모드를 켜고 끔). Opus 5.5(v2.1.280부터 기본 모델), Sonnet 5.5(v2.1.284부터 Anthropic API에서 `sonnet` 별칭이 가리키는 모델), Haiku 5.5(v2.1.293부터 Anthropic API에서 `haiku` 별칭이 가리키는 모델), Fable 모델에서는 사고를 끌 수 없어서, 이 토글과 `alwaysThinkingEnabled`, `MAX_THINKING_TOKENS=0`이 아무 효과가 없습니다. 한 번만 깊이 추론하게 하려면 프롬프트에 "ultrathink"를 넣고, 세션 단위로 제어하려면 `/effort` 명령어를 쓰세요.
- **복습**: 확장 사고 섹션

### Q5
- **분류**: 개념
- **질문**: "ultrathink" 키워드는 깊은 추론을 켜나요?
- **보기**: A) 예, 세션 설정은 바꾸지 않고 응답 하나에 대해 깊은 추론을 켠다 | B) 아니요, 일반 프롬프트 텍스트로 취급된다 | C) 예, 하지만 Opus 4.6에서만 | D) 예, 그리고 노력 수준을 영구적으로 바꾼다
- **정답**: A
- **해설**: 프롬프트에 "ultrathink"를 넣으면 그 턴에서 더 깊이 추론하라는 지시가 컨텍스트에 추가됩니다. API로 보내는 노력 수준은 바꾸지 않으므로, 세션 단위로 깊이 추론하게 하려면 `/effort max`를 쓰세요.
- **복습**: 확장 사고 섹션

### Q6
- **분류**: 실무
- **질문**: CI/CD 파이프라인에서 구조화된 JSON 출력과 턴 제한을 두고 Claude를 실행하려면 어떻게 하나요?
- **보기**: A) `claude --ci --json --limit 3` | B) `claude -p --output-format json --max-turns 3 "review code"` | C) `claude --pipeline --format json` | D) `claude run --json --turns 3`
- **정답**: B
- **해설**: print 모드(`-p`)에 `--output-format json`과 `--max-turns`를 함께 쓰는 것이 표준 CI/CD 통합 패턴입니다.
- **복습**: 헤드리스 모드

### Q7
- **분류**: 개념
- **질문**: 작업 목록 기능(Ctrl+T)은 무엇을 제공하나요?
- **보기**: A) 실행 중인 백그라운드 프로세스 목록 | B) 컨텍스트 컴팩션 후에도 유지되고 `CLAUDE_CODE_TASK_LIST_ID`로 공유할 수 있는 할 일 목록 | C) 지난 세션 기록 | D) 대기 중인 도구 호출 큐
- **정답**: B
- **해설**: 작업 목록(Ctrl+T)은 컨텍스트 컴팩션이 일어나도 유지되며, `CLAUDE_CODE_TASK_LIST_ID`로 이름 붙인 작업 디렉토리를 써서 여러 세션이 공유할 수 있습니다.
- **복습**: 작업 목록 섹션

### Q8
- **분류**: 실무
- **질문**: 계획 모드 중에 계획을 외부에서(원하는 편집기로) 편집하려면 어떻게 하나요?
- **보기**: A) 터미널에서 복사해 붙여 넣는다 | B) `Ctrl+G`를 눌러 외부 편집기에서 계획을 연다 | C) `/export-plan` 명령어 사용 | D) 계획은 외부에서 편집할 수 없다
- **정답**: B
- **해설**: Ctrl+G를 누르면 현재 계획이 설정된 외부 편집기에서 열려 수정할 수 있습니다.
- **복습**: 계획 모드 섹션

### Q9
- **분류**: 개념
- **질문**: `dontAsk` 모드와 `bypassPermissions` 모드는 무엇이 다른가요?
- **보기**: A) 같다 | B) `dontAsk`는 미리 승인한 것이 아니면 자동으로 거부하고, `bypassPermissions`는 모든 확인을 완전히 건너뛴다 | C) `dontAsk`는 파일용, `bypassPermissions`는 명령어용이다 | D) `bypassPermissions`가 더 안전하다
- **정답**: B
- **해설**: dontAsk는 미리 승인한 패턴과 일치하지 않으면 권한 요청을 자동으로 거부합니다. bypassPermissions는 모든 안전 검사를 완전히 건너뛰므로 일상적으로 쓰기에는 위험합니다.
- **복습**: 권한 모드 섹션

### Q10
- **분류**: 실무
- **질문**: CLI 세션을 데스크톱 앱으로 넘기려면 어떻게 하나요?
- **보기**: A) `/export` 명령어 사용 | B) `/desktop` 명령어 사용 | C) 세션 ID를 복사해 앱에 붙여 넣는다 | D) CLI와 데스크톱 사이에서는 세션을 옮길 수 없다
- **정답**: B
- **해설**: `/desktop` 명령어는 현재 CLI 세션을 네이티브 데스크톱 앱으로 넘겨, 시각적 diff 검토와 여러 세션 관리를 할 수 있게 합니다.
- **복습**: 데스크톱 앱 섹션

---

## 레슨 10: CLI 레퍼런스

### Q1
- **분류**: 개념
- **질문**: Claude CLI의 두 가지 주요 모드는 무엇인가요?
- **보기**: A) 온라인 모드와 오프라인 모드 | B) 대화형 REPL(`claude`)과 print 모드(`claude -p`) | C) GUI 모드와 터미널 모드 | D) 단일 모드와 일괄 모드
- **정답**: B
- **해설**: 대화형 REPL은 기본 대화 모드입니다. print 모드(-p)는 비대화형이라 스크립트로 실행하거나 파이프로 연결할 수 있으며, 응답 하나를 마치면 종료합니다.
- **복습**: 아키텍처 섹션

### Q2
- **분류**: 실무
- **질문**: 파일을 Claude에 파이프로 넘기고 JSON 출력을 받으려면 어떻게 하나요?
- **보기**: A) `claude --file error.log --json` | B) `cat error.log | claude -p --output-format json "explain this"` | C) `claude < error.log --format json` | D) `claude -p --input error.log --json`
- **정답**: B
- **해설**: stdin으로 print 모드(-p)에 내용을 파이프로 넘기고, 구조화된 출력에는 --output-format json을 씁니다.
- **복습**: 대화형 모드와 print 모드 비교 섹션

### Q3
- **분류**: 개념
- **질문**: `-c` 플래그와 `-r` 플래그는 무엇이 다른가요?
- **보기**: A) 둘 다 같은 일을 한다 | B) `-c`는 가장 최근 세션을 이어 가고, `-r`은 이름이나 ID로 재개한다 | C) `-c`는 새 세션을 만들고, `-r`은 재개한다 | D) `-c`는 코드용, `-r`은 리뷰용이다
- **정답**: B
- **해설**: `-c/--continue`는 가장 최근 대화를 재개합니다. `-r/--resume "name"`은 이름이나 세션 ID로 특정 세션을 재개합니다.
- **복습**: 세션 관리 섹션

### Q4
- **분류**: 실무
- **질문**: Claude가 스키마에 맞는 JSON을 출력하도록 보장하려면 어떻게 하나요?
- **보기**: A) `--output-format json`만 쓴다 | B) `--output-format json --json-schema '{"type":"object",...}'` 사용 | C) `--strict-json` 플래그 사용 | D) JSON 출력은 항상 스키마에 맞는다
- **정답**: B
- **해설**: `--output-format json`만 쓰면 최대한 맞춘 JSON이 나옵니다. JSON Schema 정의와 함께 `--json-schema`를 추가하면 출력이 스키마와 일치하도록 보장됩니다.
- **복습**: 출력과 형식

### Q5
- **분류**: 개념
- **질문**: print 모드(-p)에서만 동작하고 대화형 모드에서는 효과가 없는 플래그는 무엇인가요?
- **보기**: A) `--model` | B) `--system-prompt-file` | C) `--verbose` | D) `--max-turns`
- **정답**: D
- **해설**: `--max-turns`는 에이전트 턴 수를 제한하며 print 모드(`-p`)에서만 적용됩니다. 한도에 도달하면 오류와 함께 종료합니다. `--system-prompt-file`은 다른 시스템 프롬프트 플래그와 마찬가지로 대화형 모드와 print 모드 모두에서 동작합니다.
- **복습**: 고급 기능

### Q6
- **분류**: 실무
- **질문**: 보안 감사를 위해 Claude가 읽기 전용 도구만 쓰도록 제한하려면 어떻게 하나요?
- **보기**: A) `claude --read-only "audit code"` | B) `claude --permission-mode plan --tools "Read,Grep,Glob" "audit code"` | C) `claude --safe-mode "audit code"` | D) `claude --no-write "audit code"`
- **정답**: B
- **해설**: `--permission-mode plan`(읽기 전용 분석)과 `--tools`(특정 도구의 허용 목록)를 함께 써서 Claude가 읽기 작업만 하도록 제한합니다.
- **복습**: 도구와 권한 관리

### Q7
- **분류**: 개념
- **질문**: 에이전트 정의의 우선순위는 어떻게 되나요?
- **보기**: A) 프로젝트 > 사용자 > CLI | B) CLI > 프로젝트 > 사용자 | C) 사용자 > CLI > 프로젝트 | D) 모두 우선순위가 같다
- **정답**: B
- **해설**: 전체 순서는 관리형 설정 > `--agents` 플래그 > 프로젝트(`.claude/agents/`) > 사용자(`~/.claude/agents/`) > 플러그인입니다. 보기 중에서는 CLI > 프로젝트 > 사용자가 올바른 상대 순서입니다.
- **복습**: 에이전트 설정 섹션

### Q8
- **분류**: 실무
- **질문**: 셸에서, 저장된 세션 `feature-auth`를 바탕으로 원래 세션은 그대로 두고 새 세션을 시작하려면 어떻게 하나요?
- **보기**: A) `claude --clone feature-auth` | B) `claude --resume feature-auth --fork-session` | C) `claude --branch feature-auth` | D) `claude --resume feature-auth`
- **정답**: B
- **해설**: `--fork-session`(`--resume`이나 `--continue`와 함께 사용)은 원래 세션 ID를 재사용하지 않고 새 세션 ID를 만들므로 원래 대화가 보존됩니다. `--resume`만 쓰면 같은 세션을 다시 열어 거기에 이어 씁니다. 실행 중인 세션 안에서는 `/branch`가 같은 일을 하고 복사본으로 전환하며, `/fork`는 대화를 새 백그라운드 세션으로 복사합니다.
- **복습**: 세션 포크 섹션

### Q9
- **분류**: 개념
- **질문**: 사용자가 로그인되어 있을 때 `claude auth status`는 어떤 종료 코드를 돌려주나요?
- **보기**: A) 1 | B) 0 | C) 200 | D) 종료 코드를 돌려주지 않는다
- **정답**: B
- **해설**: `claude auth status`는 로그인되어 있으면 0, 아니면 1로 종료합니다. 그래서 CI/CD에서 인증 상태를 확인하는 스크립트에 쓸 수 있습니다.
- **복습**: CLI 명령어 표

### Q10
- **분류**: 실무
- **질문**: Claude로 여러 파일을 일괄 처리하려면 어떻게 하나요?
- **보기**: A) `claude --batch *.md` | B) for 반복문 사용: `for file in *.md; do claude -p "summarize: $(cat $file)" > ${file%.md}.json; done` | C) `claude -p --files *.md "summarize all"` | D) 일괄 처리는 지원되지 않는다
- **정답**: B
- **해설**: 셸 for 반복문과 print 모드를 함께 써서 파일을 하나씩 처리합니다. 호출마다 독립적이며 구조화된 출력을 만들 수 있습니다.
- **복습**: 5. 일괄 처리 섹션

---
**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/hooks
- https://code.claude.com/docs/ko/skills
- https://code.claude.com/docs/ko/mcp
- https://code.claude.com/docs/ko/memory
- https://code.claude.com/docs/ko/sub-agents
- https://code.claude.com/docs/ko/permission-modes
- https://code.claude.com/docs/ko/checkpointing
- https://code.claude.com/docs/ko/plugins-reference
- https://code.claude.com/docs/ko/cli-reference
- https://code.claude.com/docs/ko/model-config#extended-thinking
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/ko/commands
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/ko/plugins
- https://code.claude.com/docs/ko/hooks#pretooluse-decision-control
- https://code.claude.com/docs/ko/mcp#environment-variable-expansion-in-mcp-json
- https://code.claude.com/docs/ko/mcp#configure-tool-search
- https://code.claude.com/docs/ko/skills#frontmatter-reference
- https://code.claude.com/docs/ko/checkpointing#automatic-tracking
- https://code.claude.com/docs/ko/mcp#example-connect-to-github-for-code-reviews
- https://code.claude.com/docs/en/changelog#2-1-302
- https://code.claude.com/docs/ko/interactive-mode
