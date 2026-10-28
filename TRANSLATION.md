# 한국어판 번역 안내

이 문서는 한국어판의 번역 기준입니다. 원본 정보, 번역 범위, 한국어 전용판 정리 내용, 문체, 번역하지 않는 것, 용어집을 정리했습니다. 내용을 고치거나 원본 업데이트를 반영할 때 이 기준을 따르세요.

## 원본 정보

- **원본**: [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto) — MIT License, Copyright (c) 2024 luongnv89
- **한국어판**: [KIMDONGWHEE99/howkorean](https://github.com/KIMDONGWHEE99/howkorean)
- **번역 기준 커밋**: `188f468893231cbe4525f45e657d554746232072` (2026-10-20), 가이드 버전 v2.1.302
- 이 한국어판은 **비공식 번역**이며 원저작자와 관계가 없습니다. 라이선스 조건에 따라 [LICENSE](LICENSE)는 영어 원문 그대로 둡니다.

### 원본 업데이트를 반영하는 방법

이 저장소의 첫 커밋은 번역 기준 커밋의 원본 파일을 그대로 가져온 것이며, 원본의 이전 커밋 기록은 들어 있지 않습니다. 원본이 업데이트되면 다음 순서로 반영합니다.

1. 원본 저장소를 연결하고 최신 내용을 가져옵니다.

   ```bash
   git remote add upstream https://github.com/luongnv89/claude-howto.git
   git fetch upstream
   ```

2. 기준 커밋 이후 바뀐 문서를 확인합니다.

   ```bash
   git diff --stat 188f468 upstream/main -- '*.md' ':!ja' ':!zh' ':!uk' ':!vi'
   ```

   원본의 다른 언어판(`ja/`, `zh/`, `uk/`, `vi/`)은 이 저장소에서 지웠으므로 비교에서 뺍니다.

3. 바뀐 파일만 이 문서의 기준에 맞춰 다시 번역합니다.
4. 위의 **번역 기준 커밋**을 새 커밋으로 갱신합니다.

## 번역 범위

| 구분 | 대상 | 처리 |
|------|------|------|
| 입문 안내서 | `README.md`, `INDEX.md`, `CATALOG.md`, `LEARNING-ROADMAP.md`, `QUICK_REFERENCE.md`, `claude_concepts_guide.md`, `resources.md` | 번역 |
| 강의 10개 장 | `01-`~`10-` 폴더의 `README.md` | 번역 |
| 장별 예제·템플릿 | 명령어·스킬·서브에이전트·플러그인 정의 파일, 예제 스크립트의 주석, `clean-code-rules.md` | 번역 |
| 내장 학습 스킬 | `.claude/skills/` (`/lesson-quiz`, `/self-assessment`) | 번역 |
| 학습 진도 페이지 | `local-progress/index.html` | 화면 문구 번역 |
| EPUB·웹사이트 출력 | `scripts/website_templates/`의 화면 문구와 `roadmap.json`, `build_epub.py`·`build_website.py`의 제목과 장 이름 | 화면에 보이는 문구만 번역(코드와 주석은 영어 유지) |
| 운영 문서 | `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `STYLE_GUIDE.md`, `.github/`, `scripts/`(위의 출력 문구 제외), `docs/`, `prompts/` | 영어 원문 유지 |
| 법적 문서·자료 | `LICENSE`, `slides/`의 PDF, `resources/`의 로고·디자인 자료 문서 | 영어 원문 유지 |

영어 원문을 유지하는 문서로 가는 링크에는 `(영문)`을 붙입니다.

## 한국어 전용판 정리

이 저장소는 한국어 사용자만을 위한 판입니다. 원본과 다른 점은 다음과 같습니다.

- **다른 언어판 제거**: 원본의 일본어(`ja/`), 중국어(`zh/`), 우크라이나어(`uk/`), 베트남어(`vi/`) 번역판과 그 전용 검사 훅, 베트남어 번역 동기화 스크립트를 지웠습니다. 다른 언어판이 필요하면 [원본 저장소](https://github.com/luongnv89/claude-howto)를 참고하세요.
- **EPUB 빌드**: `uv run scripts/build_epub.py`가 저장소 루트의 한국어판을 언어 코드 `ko`, 한국어 제목과 장 이름으로 빌드합니다. 표지는 한글 글꼴(Apple SD Gothic Neo, Noto Sans CJK, 나눔고딕, 맑은 고딕 중 하나)이 있으면 한국어로, 없으면 영어로 만듭니다.
- **웹사이트 빌드**: `uv run scripts/build_website.py`가 한국어 화면 문구로 사이트를 만들고, GitHub 링크는 이 저장소를 가리킵니다. 랜딩 페이지 로드맵(`scripts/website_templates/roadmap.json`)의 `heading`은 각 장 README의 한국어 제목과 글자 그대로 같아야 합니다. 제목을 바꾸면 이 값도 함께 바꾸세요. `pytest scripts/tests/`가 어긋난 곳을 알려 줍니다.
- **GitHub Pages**: 자동 배포를 끄고 Actions 탭에서 수동으로만 실행하도록 바꿨습니다(`.github/workflows/pages.yml`).

## 문체

| 대상 | 규칙 | 예 |
|------|------|-----|
| 본문 서술 | 합니다체 | 스킬은 필요할 때 자동으로 로드됩니다. |
| 지시·권유 | ~하세요 | 설정 파일을 열고 훅을 추가하세요. |
| 질문형 제목 | ~인가요? / ~하나요? | 무료인가요? |
| 제목·표 셀·짧은 목록 | 명사형 | 빠른 시작 / 프로젝트 메모리 설정 |
| 문장형 목록 항목 | 합니다체 | Claude가 관련 있다고 판단하면 스킬을 자동으로 호출합니다. |

- 직역보다 자연스러운 한국어를 우선하되, 기술적 의미는 바꾸지 않습니다.
- 제목의 수와 순서는 원문과 1:1로 맞춥니다. 문서 안 목차 링크가 이 순서를 기준으로 자동 변환됩니다.
- 원문에 없는 내용은 덧붙이지 않습니다. 한국 사용자에게 꼭 필요한 보충만 `> **역주**:` 형식으로 짧게 구분해 씁니다.
- 영어 날짜는 한국식으로 씁니다: October 18, 2026 → 2026년 10월 18일
- 핵심 용어가 문서에 처음 나올 때 필요하면 영어를 괄호로 병기합니다: 서브에이전트(subagent)

### 강조 표시와 조사

굵게(`**`)·기울임(`*`) 표시가 문장 부호나 코드로 끝날 때 조사를 표시 바깥에 바로 붙이면 GitHub에서 강조가 깨집니다. 이럴 때는 조사를 강조 안에 넣습니다.

- ✗ `` **`/clear`**는 `` → 별표가 그대로 보임
- ○ `` **`/clear`는** `` → 정상 표시

### 범위 표기와 물결표

GitHub은 한 문단(표에서는 한 칸) 안에서 짝을 이루는 물결표를 취소선으로 렌더링합니다. 범위를 물결표로 두 번 쓰면 그 사이 글자에 줄이 그어집니다. 코드(백틱) 안의 물결표는 괜찮습니다.

- ✗ `Opus 4~4.7, Sonnet 4~4.6` → "4.7, Sonnet 4"에 취소선
- ○ `Opus 4–4.7, Sonnet 4–4.6` → 범위는 en 대시(`–`)로 쓰거나 "4부터 4.7까지"처럼 풀어 씁니다

## 번역하지 않는 것

- 명령어·플래그·설정 키·환경 변수·파일과 폴더 이름·코드: `/compact`, `--permission-mode`, `allowed-tools`, `CLAUDE_CODE_NEW_INIT`
- 훅 이벤트 이름(`PreToolUse` 등), 도구 이름(`Bash`, `Read`), 모델 이름(Claude Opus 5.5 등), 제품·기능 이름(Claude Code, Claude Desktop, Remote Control, Agent SDK)
- frontmatter의 키와 `name` 값 (`description` 값은 번역합니다)
- 화면(UI)에 영어로 표시되는 문구: 원문 그대로 두고 필요하면 괄호로 뜻을 붙입니다. 예: `Restore code and conversation`(코드와 대화 복원)
- 실제 출력 예시(로그, 오류 메시지, 상태 표시)
- 버전 번호

## 코드블록 안에서 번역하는 것

- 주석: `# 1. 가이드 내려받기`
- 예제 명령의 프롬프트 문장(따옴표 안의 자연어): `claude -p "이 코드를 리뷰해 줘"`. Claude는 한국어 프롬프트를 그대로 이해합니다. 세션 이름·파일명·식별자는 그대로 둡니다.
- 예제 명령어·스킬·서브에이전트 파일의 본문(Claude에게 주는 지침)
- Mermaid 다이어그램의 라벨. 노드 ID와 문법은 그대로 둡니다.

### 한국어 프롬프트 예제를 쓸 때

- `@파일경로` 뒤에 조사를 바로 붙이지 않습니다. 경로 인식이 틀어질 수 있습니다.
  - ✗ `@src/app.js를 검토해 줘`
  - ○ `다음 파일을 검토해 줘: @src/app.js`
- `$ARGUMENTS`, `$0` 같은 변수 바로 뒤에도 조사를 붙이지 않고 문장을 재구성합니다.
  - ✗ `이슈 #$ARGUMENTS를 수정하세요`
  - ○ `다음 이슈를 수정하세요: #$ARGUMENTS`

## 링크 규칙

- 저장소 안 링크: 경로는 그대로 두고, 제목(앵커) 링크만 한국어 제목에 맞게 바꿉니다.
- 공식 문서 링크: 한국어판이 있는 페이지는 `https://code.claude.com/docs/ko/...`로 연결합니다. 한국어판이 없는 페이지와 변경 로그(changelog)·새 소식(whats-new) 페이지는 영어판이 더 최신이므로 영어판을 유지합니다. 특정 섹션을 가리키는 링크는 한국어판 페이지에 그 섹션이 있을 때만 바꿉니다.
- 외부 링크(`https://...`) 바로 뒤에 괄호를 붙이지 않습니다. 저장소의 링크 검사가 괄호까지 주소로 읽어 실패합니다. 저장소 안 문서 링크 뒤의 `(영문)`은 괜찮습니다.
- 저장소 복제 명령: 한국어판 저장소를 받도록 `git clone https://github.com/KIMDONGWHEE99/howkorean.git claude-howto`로 씁니다. 받는 폴더 이름을 `claude-howto`로 지정하므로 문서에 나오는 `cd claude-howto` 같은 경로를 그대로 쓸 수 있습니다.

## 용어집

[Claude Code 공식 한국어 문서](https://code.claude.com/docs/ko/overview)와 [공식 용어집](https://code.claude.com/docs/ko/glossary)을 기준으로 삼았습니다. 공식 문서 안에서도 표기가 엇갈리는 용어는 하나로 정해 통일했습니다.

### 핵심 기능

| 영어 | 한국어 | 비고 |
|------|--------|------|
| Claude Code | Claude Code | 제품명 |
| slash command | 슬래시 명령어 | 공식 문서는 Commands(명령어)로 개칭 |
| built-in command | 기본 제공 명령어 | |
| bundled skill | 번들 스킬 | Claude Code에 포함된 스킬 |
| custom command | 사용자 정의 명령어 | 지금은 스킬로 통합 |
| legacy command | 레거시 명령어 | `.claude/commands/` 방식 |
| skill | 스킬 | |
| subagent | 서브에이전트 | |
| agent team | 에이전트 팀 | |
| agent view | 에이전트 뷰 | |
| memory | 메모리 | |
| auto memory | 자동 메모리 | |
| hook | 훅 | |
| hook event | 훅 이벤트 | 이벤트 이름은 영어 유지 |
| hook type | 훅 타입 | `command`, `http` 등 |
| matcher | 매처 | 설정 키 `matcher`는 그대로 |
| exit code | 종료 코드 | |
| plugin | 플러그인 | |
| marketplace | 마켓플레이스 | |
| MCP server | MCP 서버 | |
| MCP prompt | MCP 프롬프트 | |
| checkpoint / checkpointing | 체크포인트 / 체크포인팅 | |
| rewind | 되감기 | `/rewind` |
| dynamic workflow | 동적 워크플로우 | |
| output style | 출력 스타일 | |
| status line | 상태 표시줄 | |
| artifact | 아티팩트 | |
| side question | 곁가지 질문 | `/btw` |
| scheduled task | 예약 작업 | |

### 세션과 실행

| 영어 | 한국어 | 비고 |
|------|--------|------|
| session | 세션 | |
| conversation | 대화 | |
| turn | 턴 | |
| context | 컨텍스트 | |
| context window | 컨텍스트 윈도우 | |
| compaction / compact | 컴팩션 / 압축 | 명사는 컴팩션, 동사는 "압축하다" |
| prompt cache | 프롬프트 캐시 | |
| resume | 재개 | |
| fork | 포크 | |
| branch (대화) | 분기 | `/branch`. git 브랜치는 "브랜치" |
| background task / session | 백그라운드 작업 / 세션 | |
| interactive mode | 대화형 모드 | |
| headless mode | 헤드리스 모드 | 공식 문서의 "비대화형 모드" |
| print mode (`-p`) | print 모드 | 비대화형 실행 |
| extended thinking | 확장 사고 | |
| effort level | 노력 수준 | 공식 문서 표기 |
| fast mode | 빠른 모드 | |
| fullscreen rendering | 전체 화면 렌더링 | |
| worktree | worktree | git 용어, 번역하지 않음 |

### 권한과 보안

| 영어 | 한국어 | 비고 |
|------|--------|------|
| permission | 권한 | |
| permission mode | 권한 모드 | |
| plan mode / planning mode | 계획 모드 | |
| auto mode | 자동 모드 | |
| manual mode | 수동 모드 | 설정값 `default` |
| permission prompt | 권한 프롬프트 | 승인을 묻는 창 |
| allow / ask / deny rule | 허용 / 요청 / 거부 규칙 | |
| allowlist | 허용 목록 | |
| sandbox / sandboxing | 샌드박스 / 샌드박싱 | |
| protected path | 보호된 경로 | |
| prompt injection | 프롬프트 주입 | |
| credential / secret | 자격 증명 / 비밀 정보 | |

### 설정과 확장

| 영어 | 한국어 | 비고 |
|------|--------|------|
| settings | 설정 | |
| managed settings | 관리형 설정 | |
| scope (user / project / local) | 범위 (사용자 / 프로젝트 / 로컬) | |
| environment variable | 환경 변수 | |
| flag | 플래그 | |
| frontmatter | frontmatter | 파일 맨 위 YAML 설정 블록 |
| argument | 인수 | |
| tool / tool call | 도구 / 도구 호출 | |
| invoke / invocation | 호출 | |
| auto-invoke | 자동 호출 | |
| delegate / delegation | 위임 | |
| orchestrate / orchestration | 조율 / 오케스트레이션 | |
| progressive disclosure | 점진적 공개 | |
| namespace | 네임스페이스 | |
| keybinding | 키 바인딩 | |
| system prompt | 시스템 프롬프트 | |
| agentic loop | 에이전트 루프 | |
| desktop app | 데스크톱 앱 | |

### 학습 가이드

| 영어 | 한국어 | 비고 |
|------|--------|------|
| module | 모듈 | 1~10장 각각 |
| lesson | 레슨 | |
| learning path | 학습 경로 | |
| roadmap | 로드맵 | |
| self-assessment | 자가 진단 | |
| quiz | 퀴즈 | |
| beginner / intermediate / advanced | 입문 / 중급 / 고급 | |
| quick start | 빠른 시작 | |
| quick reference | 빠른 참조 | |
| feature catalog | 기능 카탈로그 | |
| template / example | 템플릿 / 예제 | |
| best practices | 모범 사례 | |
| troubleshooting | 문제 해결 | |
| use case | 활용 사례 | |
| hands-on | 실습 | |

### 일반 개발 용어

| 영어 | 한국어 | 비고 |
|------|--------|------|
| repository | 저장소 | |
| codebase | 코드베이스 | |
| commit | 커밋 | |
| pull request | 풀 리퀘스트(PR) | |
| branch (git) | 브랜치 | |
| merge | 병합 | |
| deploy / deployment | 배포 | |
| production | 프로덕션 | |
| workflow | 워크플로우 | 공식 문서 표기 |
| pipeline | 파이프라인 | |
| directory | 디렉토리 | 공식 문서 표기 |
| working directory | 작업 디렉토리 | |
| refactoring | 리팩토링 | |
| linting | 린팅 | |
| test coverage | 테스트 커버리지 | |
| edge case | 엣지 케이스 | |
| alias | 별칭 | |
| deprecated / removed | 지원 중단 / 제거 | |
| rate limit | 속도 제한 | |
| usage limit | 사용 한도 | 요금제 사용 한도 |
