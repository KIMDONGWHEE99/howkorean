<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 에이전트 스킬 가이드

에이전트 스킬은 Claude의 기능을 확장하는, 파일 시스템 기반의 재사용 가능한 기능입니다. 특정 분야의 전문 지식, 워크플로우, 모범 사례를 발견 가능한 구성 요소로 패키징하며, Claude는 관련 있을 때 이를 자동으로 사용합니다.

## 개요

**에이전트 스킬**은 범용 에이전트를 전문가로 바꿔 주는 모듈식 기능입니다. 프롬프트(일회성 작업을 위한 대화 수준의 지침)와 달리, 스킬은 필요할 때 로드되므로 여러 대화에서 같은 안내를 반복해서 줄 필요가 없습니다.

### 주요 이점

- **Claude 전문화**: 특정 분야 작업에 맞게 기능을 조정
- **반복 감소**: 한 번 만들면 여러 대화에서 자동으로 사용
- **기능 조합**: 스킬을 조합해 복잡한 워크플로우 구성
- **워크플로우 확장**: 여러 프로젝트와 팀에서 스킬 재사용
- **품질 유지**: 모범 사례를 워크플로우에 바로 녹여 넣기

스킬은 여러 AI 도구에서 동작하는 [Agent Skills](https://agentskills.io) 개방형 표준을 따릅니다. Claude Code는 호출 제어, 서브에이전트 실행, 동적 컨텍스트 주입 같은 추가 기능으로 이 표준을 확장합니다.

> **참고**: 사용자 정의 슬래시 명령어는 스킬로 통합되었습니다. `.claude/commands/` 파일도 여전히 동작하며 같은 frontmatter 필드를 지원합니다. 새로 만들 때는 스킬을 권장합니다. 같은 경로에 둘 다 있으면(예: `.claude/commands/review.md`와 `.claude/skills/review/SKILL.md`) 스킬이 우선합니다.

## 스킬의 동작 방식: 점진적 공개

스킬은 **점진적 공개** 아키텍처를 활용합니다 — Claude는 컨텍스트를 처음부터 소비하지 않고 필요할 때 단계적으로 정보를 로드합니다. 덕분에 확장성에 제한을 두지 않으면서도 컨텍스트를 효율적으로 관리할 수 있습니다.

### 세 단계 로딩

```mermaid
graph TB
    subgraph "레벨 1: 메타데이터 (항상 로드)"
        A["YAML frontmatter"]
        A1["스킬당 약 100토큰"]
        A2["name + description"]
    end

    subgraph "레벨 2: 지침 (트리거될 때)"
        B["SKILL.md 본문"]
        B1["5천 토큰 미만"]
        B2["워크플로우와 안내"]
    end

    subgraph "레벨 3: 리소스 (필요할 때)"
        C["번들 파일"]
        C1["사실상 무제한"]
        C2["스크립트, 템플릿, 문서"]
    end

    A --> B
    B --> C
```

| 레벨 | 로드 시점 | 토큰 비용 | 내용 |
|-------|------------|------------|---------|
| **레벨 1: 메타데이터** | 항상(시작할 때) | 스킬당 약 100토큰 | YAML frontmatter의 `name`과 `description` |
| **레벨 2: 지침** | 스킬이 트리거될 때 | 5천 토큰 미만 | 지침과 안내가 담긴 SKILL.md 본문 |
| **레벨 3+: 리소스** | 필요할 때 | 사실상 무제한 | 내용을 컨텍스트에 로드하지 않고 bash로 실행하는 번들 파일 |

덕분에 스킬은 가볍습니다 — 실제로 트리거되기 전까지 Claude는 각 스킬이 존재한다는 것과 언제 써야 하는지만 압니다. 하지만 공짜는 아닙니다: 목록에 오른 모든 스킬은 매 턴마다 설명을 컨텍스트에 추가합니다.

## 스킬 로딩 과정

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Claude
    participant System as 시스템
    participant SkillInst as 스킬 지침
    participant SkillRes as 스킬 리소스

    User->>Claude: "이 코드에 보안 문제가 있는지 리뷰해 줘"
    Claude->>System: 사용 가능한 스킬 확인(메타데이터)
    System-->>Claude: 시작할 때 로드된 스킬 설명
    Claude->>Claude: 요청과 스킬 설명 대조
    Claude->>SkillInst: code-review-specialist/SKILL.md 읽기
    SkillInst-->>Claude: 레벨 2: 지침 로드됨
    Claude->>Claude: 판단: 템플릿이 필요한가?
    Claude->>SkillRes: templates/checklist.md 읽기
    SkillRes-->>Claude: 레벨 3: 템플릿 로드됨
    Claude->>Claude: 스킬 지침 실행
    Claude->>User: 종합 코드 리뷰
```

## 스킬 유형과 위치

| 유형 | 위치 | 범위 | 공유 | 적합한 용도 |
|------|----------|-------|--------|----------|
| **엔터프라이즈** | 관리형 설정 | 조직의 모든 사용자 | 예 | 조직 전체 표준 |
| **개인** | `~/.claude/skills/<skill-name>/SKILL.md` | 개인 | 아니요 | 개인 워크플로우 |
| **프로젝트** | `.claude/skills/<skill-name>/SKILL.md` | 팀 | 예(git으로) | 팀 표준 |
| **플러그인** | `<plugin>/skills/<skill-name>/SKILL.md` | 활성화된 곳 | 경우에 따라 다름 | 플러그인과 함께 번들 |

여러 단계에 같은 이름의 스킬이 있으면 우선순위가 높은 위치가 이깁니다: **엔터프라이즈 > 개인 > 프로젝트**. `~/.claude/skills/`와 `.claude/skills/`에 같은 이름이 있으면 개인 스킬이 실행됩니다. (우선순위가 아니라) 스킬의 노출 여부를 바꾸려면 `skillOverrides` 설정(v2.1.129+)을 쓰세요 — [스킬 재정의 동작 제어](#스킬-재정의-동작-제어skilloverrides)를 참고하세요. 플러그인 스킬은 `plugin-name:skill-name` 네임스페이스를 쓰므로 충돌하지 않습니다.

> **서브에이전트의 스킬 발견 (v2.1.133+)**: 이제 서브에이전트도 메인 세션과 같은 방식으로 Skill 도구를 통해 프로젝트, 사용자, 플러그인 스킬을 발견합니다. 이전 버전에서는 서브에이전트가 자체에 내장된 스킬만 쓸 수 있어서 스킬과 서브에이전트를 함께 쓰는 워크플로우가 티 나지 않게 제 기능을 못 했지만, v2.1.133부터는 둘 다 같은 스킬 목록을 봅니다.

### 자동 발견

**중첩 디렉토리**: 하위 디렉토리의 파일을 다룰 때 Claude Code는 중첩된 `.claude/skills/` 디렉토리에서 스킬을 자동으로 발견합니다. 예를 들어 `packages/frontend/`의 파일을 편집 중이면 `packages/frontend/.claude/skills/`에서도 스킬을 찾습니다. 패키지마다 자체 스킬을 두는 모노레포 구성을 지원하는 방식입니다. 중첩 스킬이 저장소 루트 스킬과 이름이 같으면 **둘 다 로드됩니다**: 루트와 `apps/web/.claude/skills/`에 모두 `deploy` 스킬이 있으면 `/deploy`는 루트 스킬을, `/apps/web:deploy`는 중첩 스킬을 실행합니다.

**`--add-dir` 디렉토리**: `--add-dir`로 추가한 디렉토리의 스킬은 실시간 변경 감지와 함께 자동으로 로드됩니다. 그 디렉토리의 스킬 파일을 편집하면 Claude Code를 다시 시작하지 않아도 바로 반영됩니다.

**스킬 다시 로드**: `/reload-skills` 명령어(v2.1.152에서 추가)는 세션을 다시 시작하지 않고 모든 스킬 디렉토리를 다시 검색합니다 — 실시간 감지로 반영되지 않는 스킬을 추가하거나 편집한 뒤에 유용합니다. `SessionStart` 훅이 `reloadSkills: true`를 반환해도 같은 재검색이 일어납니다([훅](../06-hooks/README.md) 참고).

**설명 예산**: 스킬 설명(레벨 1 메타데이터)은 **컨텍스트 윈도우의 1%**(대체값: **8,000자**)로 제한됩니다. 설치한 스킬이 많으면 설명이 잘릴 수 있습니다. 모든 스킬 이름은 항상 포함되지만 설명은 한도에 맞게 줄어듭니다. 설명에서는 핵심 활용 사례를 맨 앞에 두세요. 예산은 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 환경 변수로 바꿀 수 있습니다.

## 사용자 정의 스킬 만들기

### 기본 디렉토리 구조

```
my-skill/
├── SKILL.md           # 메인 지침(필수)
├── template.md        # Claude가 채울 템플릿
├── examples/
│   └── sample.md      # 기대하는 형식을 보여 주는 출력 예시
└── scripts/
    └── validate.sh    # Claude가 실행할 수 있는 스크립트
```

### SKILL.md 형식

```yaml
---
name: your-skill-name
description: 이 스킬이 하는 일과 언제 쓰는지에 대한 간단한 설명
---

# 스킬 이름

## 지침
Claude를 위한 명확한 단계별 안내를 제공하세요.

## 예시
이 스킬을 사용하는 구체적인 예시를 보여 주세요.
```

### 권장 필드

- **description**(권장): 스킬이 무엇을 하는지와 언제 써야 하는지를 함께 적습니다. 생략하면 Claude Code는 마크다운 내용에서 처음으로 비어 있지 않은 줄을 사용합니다. `description`과 `when_to_use`를 합친 텍스트는 스킬 목록에서 **1,536자**에서 잘립니다(`skillListingMaxDescChars`로 설정 가능). Claude는 이 텍스트를 보고 스킬을 언제 활성화할지 결정합니다.
- **name**(선택): 기본값은 스킬의 **디렉토리 이름**입니다. 지정하면 표시 이름이 됩니다 — 소문자, 숫자, 하이픈만 쓰는 형식(최대 64자)이 권장되는 호환 형식입니다(claude.ai와 Skills API에서는 필수). Claude Code 자체(v2.1.299+)는 이름에 보이지 않는 문자, 텍스트 방향을 바꾸는 문자, 공백처럼 보이는 문자, `<`나 `>`가 들어 있거나 256자를 넘는 스킬이나 명령어를 이름을 바꿀 때까지 건너뜁니다. Claude Code에서는 `anthropic-skills`와 `synced`가 예약되어 있어 플러그인 밖에서는 로드되지 않으며, "anthropic"이나 "claude"를 금지하는 더 엄격한 규칙은 claude.ai나 Skills API에 올리는 스킬에 적용됩니다. 플러그인 스킬에서는 `name`이 명령어의 마지막 부분도 정합니다.

SKILL.md의 frontmatter 필드는 모두 선택 사항이며, 권장되는 필드는 `description` 하나뿐입니다.

### 선택 frontmatter 필드

```yaml
---
name: my-skill
description: 이 스킬이 하는 일과 언제 쓰는지
argument-hint: "[filename] [format]"        # 자동 완성용 힌트
disable-model-invocation: true              # 사용자만 호출 가능
user-invocable: false                       # 슬래시 메뉴에서 숨김
allowed-tools: Read, Grep, Glob             # 스킬이 실행되는 동안 이 도구들을 사전 승인(권한 프롬프트 없음)
disallowed-tools: Write, Edit               # 활성화된 동안 특정 도구 제거(v2.1.152)
model: opus                                 # 사용할 모델 지정
effort: high                                # 노력 수준 재정의(low, medium, high, xhigh, max)
context: fork                               # 격리된 서브에이전트에서 실행
agent: Explore                              # 에이전트 타입(context: fork와 함께)
background: false                           # 포크 스킬은 백그라운드에서 실행(기본값 true). false = 포그라운드
shell: bash                                 # 명령어용 셸: bash(기본값) 또는 powershell
hooks:                                      # 스킬이 호출될 때 등록되는 훅
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
paths: "src/api/**/*.ts"               # 스킬이 활성화되는 경우를 제한하는 glob 패턴
---
```

| 필드 | 설명 |
|-------|-------------|
| `name` | 권장(호환 형식): 소문자, 숫자, 하이픈만(최대 64자). Claude Code에서는 `anthropic-skills`와 `synced`가 예약되어 있습니다. |
| `description` | 스킬이 무엇을 하는지와 언제 써야 하는지. `description`과 `when_to_use`를 합친 텍스트는 스킬 목록에서 1,536자에서 잘립니다(`skillListingMaxDescChars`로 설정 가능). 자동 호출 매칭에 매우 중요합니다. |
| `when_to_use` | Claude가 스킬을 호출해야 할 때에 대한 추가 컨텍스트. 스킬 목록에서 `description` 뒤에 붙으며 1,536자 한도에 포함됩니다. |
| `argument-hint` | `/` 자동 완성 메뉴에 표시되는 힌트(예: `"[filename] [format]"`). |
| `disable-model-invocation` | `true` = 사용자만 `/name`으로 호출할 수 있습니다. Claude는 절대 자동으로 호출하지 않습니다. |
| `user-invocable` | `false` = `/` 메뉴에서 숨깁니다. Claude만 자동으로 호출할 수 있습니다. |
| `allowed-tools` | 스킬이 권한 프롬프트 없이 쓸 수 있는 도구의 쉼표 구분 목록. |
| `disallowed-tools` | 스킬이 활성화된 동안 제거할 도구의 쉼표 구분 목록(`allowed-tools`를 보완). v2.1.152에서 추가. |
| `model` | 스킬이 활성화된 동안 쓸 모델(예: `opus`, `sonnet`). |
| `effort` | 스킬이 활성화된 동안 쓸 노력 수준: `low`, `medium`, `high`, `xhigh`, `max` — 다섯 가지 모두 Fable 5.1, Fable 5, Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7에서 지원됩니다. 노력 수준을 지원하는 모든 모델의 기본값은 `high`이며, 예외로 Opus 5.5, Sonnet 5.5, Haiku 5.5는 `medium`, Opus 4.7은 `xhigh`가 기본값입니다. |
| `context` | `fork`로 지정하면 자체 컨텍스트 윈도우를 가진 포크된 서브에이전트 컨텍스트에서 스킬을 실행합니다. |
| `agent` | `context: fork`일 때 쓸 서브에이전트 타입(예: `Explore`, `Plan`, `general-purpose`). |
| `background` | `context: fork`와 함께 쓸 때만 의미가 있습니다. `context: fork` 스킬에서는 기본값이 `true`라 백그라운드에서 실행되며, `false`로 설정하면 포그라운드에서 실행됩니다. v2.1.218에서 추가. |
| `shell` | `` !`command` `` 치환과 스크립트에 쓸 셸: `bash`(기본값) 또는 `powershell`. |
| `hooks` | 스킬이 호출될 때 등록되는 훅(설정 파일의 훅과 같은 형식이며 모든 이벤트 가능). 세션이 끝날 때까지 활성 상태로 남습니다. |
| `paths` | 스킬이 자동으로 활성화되는 경우를 제한하는 glob 패턴. 쉼표로 구분한 문자열이나 YAML 목록. 경로별 규칙과 같은 형식입니다. |
| `arguments` | 자동 완성과 인수 치환을 위해 스킬이 받는 인수를 선언합니다. 처음 64개 이름까지만, 이름마다 최대 64자까지 채워집니다(v2.1.301). |
| `metadata` | 자체 관리용 자유 형식 키/값 맵(예: `version`, `author`). Claude Code는 그대로 전달합니다. |
| `license` | 스킬의 라이선스 식별자(예: `MIT`). |
| `compatibility` | 최대 500자의 자유 텍스트 호환성 설명. Claude Code는 받아들이지만 이를 바탕으로 동작하지는 않습니다. |

> **참고**: claude.ai에 올리거나 Skills API로 만드는 스킬에서는 `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`만 유효합니다. 이 표의 나머지 필드는 Claude Code 전용입니다.

v2.1.218부터 불리언 frontmatter 필드는 `true`/`false` 외에 `yes`/`no`, `on`/`off`, `1`/`0`도 받습니다(대소문자 구분 없음).

## 스킬 콘텐츠 유형

스킬에는 두 가지 유형의 콘텐츠를 담을 수 있으며, 각각 쓰임새가 다릅니다:

### 참고 콘텐츠

Claude가 현재 작업에 적용할 지식을 더합니다 — 규칙, 패턴, 스타일 가이드, 분야 지식 등입니다. 대화 컨텍스트 안에서 인라인으로 실행됩니다.

```yaml
---
name: api-conventions
description: 이 코드베이스의 API 설계 패턴
---

API 엔드포인트를 작성할 때:
- RESTful 이름 규칙 사용
- 일관된 오류 형식 반환
- 요청 검증 포함
```

### 작업 콘텐츠

특정 작업을 위한 단계별 지침입니다. 보통 `/skill-name`으로 직접 호출합니다.

```yaml
---
name: deploy
description: 애플리케이션을 프로덕션에 배포
context: fork
disable-model-invocation: true
---

애플리케이션을 배포하세요:
1. 테스트 스위트 실행
2. 애플리케이션 빌드
3. 배포 대상에 푸시
```

## 스킬 호출 제어

기본적으로 사용자와 Claude 모두 어떤 스킬이든 호출할 수 있습니다. frontmatter 필드 두 개로 세 가지 호출 모드를 제어합니다:

| frontmatter | 사용자 호출 | Claude 호출 |
|---|---|---|
| (기본값) | 예 | 예 |
| `disable-model-invocation: true` | 예 | 아니요 |
| `user-invocable: false` | 아니요 | 예 |

**`disable-model-invocation: true`는** 부작용이 있는 워크플로우에 쓰세요: `/commit`, `/deploy`, `/send-slack-message` 등. 코드가 준비된 것처럼 보인다고 해서 Claude가 알아서 배포하기를 바라지는 않을 테니까요.

**`user-invocable: false`는** 명령어로 실행할 만한 동작이 아닌 배경 지식에 쓰세요. 예를 들어 `legacy-system-context` 스킬은 오래된 시스템이 어떻게 동작하는지 설명합니다 — Claude에게는 유용하지만 사용자가 실행할 의미 있는 동작은 아닙니다.

## 문자열 치환

스킬은 내용이 Claude에게 전달되기 전에 해석되는 동적 값을 지원합니다:

| 변수 | 설명 |
|----------|-------------|
| `$ARGUMENTS` | 스킬을 호출할 때 전달한 모든 인수 |
| `$ARGUMENTS[N]` 또는 `$N` | 인덱스로 특정 인수에 접근(0부터 시작) |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |
| `${CLAUDE_SKILL_DIR}` | 스킬의 SKILL.md 파일이 있는 디렉토리 |
| `${CLAUDE_PROJECT_DIR}` | 프로젝트 루트의 절대 경로. 스킬 본문과 `allowed-tools`에서 쓸 수 있음(v2.1.196) |
| `${CLAUDE_EFFORT}` | 현재 노력 수준(`low`, `medium`, `high`, `xhigh`, `max`). 스킬 동작을 분기할 때 유용합니다. 예: `[ "${CLAUDE_EFFORT}" = "max" ] && deep_analysis` (v2.1.120+) |
| `` !`command` `` | 동적 컨텍스트 주입 — 셸 명령어를 실행하고 출력을 인라인으로 넣음 |

**예:**

```yaml
---
name: fix-issue
description: GitHub 이슈 수정
---

우리 코딩 표준에 따라 다음 GitHub 이슈를 수정하세요: $ARGUMENTS
1. 이슈 설명 읽기
2. 수정 구현
3. 테스트 작성
4. 커밋 만들기
```

`/fix-issue 123`을 실행하면 `$ARGUMENTS`가 `123`으로 바뀝니다.

### 스킬 겹쳐 쓰기

터미널 프롬프트에서 `/write-tests /fix-issue 123`처럼 슬래시 스킬 여러 개를 한 번에 겹쳐 호출할 수 있습니다. v2.1.199부터는 앞에 나온 스킬을 모두(첫 번째와 최대 5개 더) 로드하고, 뒤따르는 인수(`123`)를 각 스킬에 전달합니다. 이전에는 첫 번째 스킬만 로드되었습니다. `/code-review`처럼 포크된 서브에이전트로 실행되는 스킬에서는 확장이 멈추며, Agent SDK나 `claude -p`에서는 첫 번째 스킬만 로드됩니다. 같은 스킬을 두 번 이상 호출하면 같은 내용이 두 번 붙지 않고 중복 제거됩니다(v2.1.202).

## 동적 컨텍스트 주입

`` !`command` `` 문법은 스킬 내용이 Claude에게 전달되기 전에 셸 명령어를 실행합니다:

> **참고 (v2.1.299)**: `UserPromptSubmit` 훅은 명령어가 확장되기 전에 실행되므로, 프롬프트를 차단하는 훅은 이 `!` 명령어의 실행도 막습니다.

```yaml
---
name: pr-summary
description: 풀 리퀘스트의 변경 사항 요약
context: fork
agent: Explore
---

## 풀 리퀘스트 컨텍스트
- PR diff: !`gh pr diff`
- PR 댓글: !`gh pr view --comments`
- 변경된 파일: !`gh pr diff --name-only`

## 할 일
이 풀 리퀘스트를 요약하세요...
```

명령어는 즉시 실행되며 Claude는 최종 출력만 봅니다. 기본적으로 명령어는 `bash`에서 실행됩니다. 대신 PowerShell을 쓰려면 frontmatter에 `shell: powershell`을 설정하세요.

## 서브에이전트에서 스킬 실행

`context: fork`를 추가하면 격리된 서브에이전트 컨텍스트에서 스킬을 실행합니다. 스킬 내용이 자체 컨텍스트 윈도우를 가진 전용 서브에이전트의 작업이 되므로 메인 대화가 어수선해지지 않습니다. v2.1.218부터 `context: fork` 스킬의 `background` 기본값이 `true`라 백그라운드에서 실행되며, 포크 스킬을 포그라운드에서 실행하려면 frontmatter에 `background: false`를 설정하세요.

> **v2.1.145 수정 사항**: 이전에는 `context: fork`를 쓰는 스킬이 드물게 무한 재호출 루프를 일으킬 수 있었습니다. 포크 스킬을 만들거나 쓴다면 v2.1.145 이상으로 업그레이드하세요.

`agent` 필드로 사용할 에이전트 타입을 지정합니다:

| 에이전트 타입 | 적합한 용도 |
|---|---|
| `Explore` | 읽기 전용 조사, 코드베이스 분석 |
| `Plan` | 구현 계획 수립 |
| `general-purpose` | 모든 도구가 필요한 폭넓은 작업 |
| 사용자 정의 에이전트 | 설정에서 정의한 전문 에이전트 |

**frontmatter 예:**

```yaml
---
context: fork
agent: Explore
---
```

**전체 스킬 예:**

```yaml
---
name: topic-research
description: 주제를 철저히 조사
context: fork
agent: Explore
---

다음 주제를 철저히 조사하세요: $ARGUMENTS
1. Glob과 Grep으로 관련 파일 찾기
2. 코드를 읽고 분석하기
3. 구체적인 파일을 참조하며 발견한 내용 요약하기
```

## 실전 예제

### 예제 1: 코드 리뷰 스킬

**디렉토리 구조:**

```
~/.claude/skills/code-review-specialist/
├── SKILL.md
├── templates/
│   ├── review-checklist.md
│   └── finding-template.md
└── scripts/
    ├── analyze-metrics.py
    └── compare-complexity.py
```

**파일:** `~/.claude/skills/code-review-specialist/SKILL.md`

```yaml
---
name: code-review-specialist
description: 보안, 성능, 품질 분석을 아우르는 종합 코드 리뷰. 사용자가 코드 리뷰, 코드 품질 분석, 풀 리퀘스트 평가를 요청하거나 코드 리뷰, 보안 분석, 성능 최적화를 언급할 때 사용합니다.
---

# 코드 리뷰 스킬

이 스킬은 다음에 초점을 맞춘 종합 코드 리뷰 기능을 제공합니다:

1. **보안 분석**
   - 인증/인가 문제
   - 데이터 노출 위험
   - 인젝션 취약점
   - 암호화 약점

2. **성능 리뷰**
   - 알고리즘 효율성(Big O 분석)
   - 메모리 최적화
   - 데이터베이스 쿼리 최적화
   - 캐싱 기회

3. **코드 품질**
   - SOLID 원칙
   - 디자인 패턴
   - 이름 규칙
   - 테스트 커버리지

4. **유지 보수성**
   - 코드 가독성
   - 함수 크기(50줄 미만이어야 함)
   - 순환 복잡도
   - 타입 안전성

## 리뷰 템플릿

리뷰한 코드마다 다음을 제공하세요:

### 요약
- 전체 품질 평가(1-5)
- 주요 발견 사항 수
- 우선 개선 권장 영역

### 심각한 문제(있는 경우)
- **문제**: 명확한 설명
- **위치**: 파일과 줄 번호
- **영향**: 왜 중요한지
- **심각도**: Critical/High/Medium
- **수정**: 코드 예시

자세한 체크리스트는 [templates/review-checklist.md](templates/review-checklist.md)를 참고하세요.
```

### 예제 2: 코드베이스 시각화 스킬

대화형 HTML 시각화를 생성하는 스킬입니다:

**디렉토리 구조:**

```
~/.claude/skills/codebase-visualizer/
├── SKILL.md
└── scripts/
    └── visualize.py
```

**파일:** `~/.claude/skills/codebase-visualizer/SKILL.md`

````yaml
---
name: codebase-visualizer
description: 코드베이스를 접고 펼 수 있는 대화형 트리로 시각화합니다. 새 저장소를 살펴보거나, 프로젝트 구조를 파악하거나, 큰 파일을 찾을 때 사용합니다.
allowed-tools: Bash(python *)
---

# 코드베이스 시각화

프로젝트의 파일 구조를 보여 주는 대화형 HTML 트리 뷰를 생성합니다.

## 사용법

프로젝트 루트에서 시각화 스크립트를 실행하세요:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

이 스크립트는 `codebase-map.html`을 만들고 기본 브라우저에서 엽니다.

## 시각화에 표시되는 내용

- **접고 펼 수 있는 디렉토리**: 폴더를 클릭해 펼치거나 접기
- **파일 크기**: 각 파일 옆에 표시
- **색상**: 파일 유형마다 다른 색상
- **디렉토리 합계**: 각 폴더의 전체 크기 표시
````

번들된 Python 스크립트가 무거운 작업을 맡고, Claude는 전체 흐름을 조율합니다.

### 예제 3: 배포 스킬(사용자 호출 전용)

```yaml
---
name: deploy
description: 애플리케이션을 프로덕션에 배포
disable-model-invocation: true
allowed-tools: Bash(npm *), Bash(git *)
---

다음 대상을 프로덕션에 배포하세요: $ARGUMENTS

1. 테스트 스위트 실행: `npm test`
2. 애플리케이션 빌드: `npm run build`
3. 배포 대상에 푸시
4. 배포가 성공했는지 확인
5. 배포 상태 보고
```

### 예제 4: 브랜드 보이스 스킬(배경 지식)

```yaml
---
name: brand-voice
description: 모든 커뮤니케이션이 브랜드 보이스와 어조 가이드라인에 맞도록 합니다. 마케팅 문구, 고객 커뮤니케이션, 외부에 공개되는 콘텐츠를 작성할 때 사용합니다.
user-invocable: false
---

## 어조
- **친근하지만 전문적으로** - 가볍지 않으면서도 다가가기 쉽게
- **명확하고 간결하게** - 전문 용어 피하기
- **자신감 있게** - 우리는 무엇을 하는지 잘 알고 있음
- **공감하며** - 사용자의 필요를 이해하기

## 작성 가이드라인
- 독자에게 직접 말하듯 쓰기("여러분")
- 능동태 사용
- 문장은 20단어 이내로
- 가치 제안으로 시작

템플릿은 [templates/](templates/)를 참고하세요.
```

### 예제 5: CLAUDE.md 생성 스킬

```yaml
---
name: claude-md
description: AI 에이전트가 프로젝트에 가장 잘 적응하도록 모범 사례에 따라 CLAUDE.md 파일을 만들거나 갱신합니다. 사용자가 CLAUDE.md, 프로젝트 문서, AI 온보딩을 언급할 때 사용합니다.
---

## 핵심 원칙

**LLM은 상태가 없습니다**: CLAUDE.md는 모든 대화에 로드되는 메인 프로젝트 파일입니다(자동 메모리, 범위가 지정되지 않은 규칙과 함께).

### 황금률

1. **적을수록 좋다**: CLAUDE.md는 파일마다 200줄 이하로 유지
2. **보편적 적용**: 모든 세션에 공통으로 필요한 정보만 포함
3. **Claude를 린터로 쓰지 말 것**: 대신 결정적인 도구 사용
4. **자동 생성 금지**: 신중하게 고민하며 직접 작성

## 필수 섹션

- **프로젝트 이름**: 한 줄짜리 간단한 설명
- **기술 스택**: 주 언어, 프레임워크, 데이터베이스
- **개발 명령어**: 설치, 테스트, 빌드 명령어
- **핵심 규칙**: 알기 어렵고 영향이 큰 규칙만
- **알려진 문제 / 주의점**: 개발자가 자주 걸려 넘어지는 것들
```

### 예제 6: 스크립트를 갖춘 리팩토링 스킬

**디렉토리 구조:**

```
refactor/
├── SKILL.md
├── references/
│   ├── code-smells.md
│   └── refactoring-catalog.md
├── templates/
│   └── refactoring-plan.md
└── scripts/
    ├── analyze-complexity.py
    └── detect-smells.py
```

**파일:** `refactor/SKILL.md`

```yaml
---
name: refactor
description: 마틴 파울러의 방법론에 기반한 체계적인 코드 리팩토링. 사용자가 코드 리팩토링, 코드 구조 개선, 기술 부채 감소, 코드 스멜 제거를 요청할 때 사용합니다.
---

# 코드 리팩토링 스킬

테스트로 뒷받침되는 안전하고 점진적인 변경을 강조하는 단계별 접근 방식입니다.

## 워크플로우

1단계: 조사와 분석 → 2단계: 테스트 커버리지 평가 →
3단계: 코드 스멜 식별 → 4단계: 리팩토링 계획 수립 →
5단계: 점진적 구현 → 6단계: 리뷰와 반복

## 핵심 원칙

1. **동작 보존**: 외부 동작은 바뀌지 않아야 함
2. **작은 단계**: 테스트할 수 있는 작은 변경
3. **테스트 주도**: 테스트가 안전망
4. **지속적 활동**: 리팩토링은 일회성 이벤트가 아니라 계속되는 활동

코드 스멜 목록은 [references/code-smells.md](references/code-smells.md)를 참고하세요.
리팩토링 기법은 [references/refactoring-catalog.md](references/refactoring-catalog.md)를 참고하세요.
```

## 보조 파일

스킬 디렉토리에는 `SKILL.md` 외에도 여러 파일을 둘 수 있습니다. 이런 보조 파일(템플릿, 예제, 스크립트, 참고 문서)을 쓰면 메인 스킬 파일은 핵심에 집중하게 하면서, Claude가 필요할 때 로드할 수 있는 추가 리소스를 제공할 수 있습니다.

```
my-skill/
├── SKILL.md              # 메인 지침(필수, 500줄 이하로 유지)
├── templates/            # Claude가 채울 템플릿
│   └── output-format.md
├── examples/             # 기대하는 형식을 보여 주는 출력 예시
│   └── sample-output.md
├── references/           # 분야 지식과 명세
│   └── api-spec.md
└── scripts/              # Claude가 실행할 수 있는 스크립트
    └── validate.sh
```

보조 파일 작성 가이드라인:

- `SKILL.md`는 **500줄 이하**로 유지하세요. 자세한 참고 자료, 큰 예제, 명세는 별도 파일로 옮기세요.
- `SKILL.md`에서 추가 파일을 참조할 때는 **상대 경로**를 쓰세요(예: `[API reference](references/api-spec.md)`).
- 보조 파일은 레벨 3(필요할 때)에서 로드되므로, Claude가 실제로 읽기 전까지는 컨텍스트를 소비하지 않습니다.

## 스킬 관리

### 사용 가능한 스킬 보기

Claude에게 직접 물어보세요:
```
어떤 스킬을 쓸 수 있어?
```

또는 파일 시스템을 확인하세요:
```bash
# 개인 스킬 목록
ls ~/.claude/skills/

# 프로젝트 스킬 목록
ls .claude/skills/
```

> **팁 (v2.1.121+):** `/skills` 대화형 메뉴에서 글자를 입력하면 목록을 걸러 볼 수 있습니다 — 스킬을 많이 설치했을 때 유용합니다.

### 스킬 테스트

두 가지 방법으로 테스트할 수 있습니다:

**Claude가 자동으로 호출하게 하기** — 설명과 일치하는 내용을 물어봅니다:
```
이 코드에 보안 문제가 있는지 리뷰해 줄래?
```

**또는 직접 호출하기** — 스킬 이름으로 호출합니다:
```
/code-review-specialist src/auth/login.ts
```

> **참고**: 이 로컬 스킬은 `code-review-specialist`로 설치되므로 번들 스킬 `/code-review`(버그 중심 리뷰, 별칭 `/review`)와 충돌하지 **않습니다**. 대신 `~/.claude/skills/code-review/`에 복사하면 번들 `/code-review`를 대체하게 됩니다(`/review`는 여전히 번들 스킬을 실행합니다) — 이를 피하려면 `-specialist` 접미사를 유지하세요.

### 스킬 업데이트

`SKILL.md` 파일을 직접 편집한 다음 `/reload-skills`(v2.1.152+)를 실행해 스킬 디렉토리를 다시 검색하세요. Claude Code를 다시 시작해도 되지만 꼭 그럴 필요는 없습니다 — `--add-dir` 디렉토리의 스킬은 실시간으로 반영되고, `reloadSkills: true`를 반환하는 `SessionStart` 훅도 같은 재검색을 일으킵니다.

```bash
# 개인 스킬
code ~/.claude/skills/my-skill/SKILL.md

# 프로젝트 스킬
code .claude/skills/my-skill/SKILL.md
```

### Claude의 스킬 접근 제한

Claude가 호출할 수 있는 스킬을 제어하는 방법은 세 가지입니다:

`/permissions`에서 **모든 스킬 끄기**:
```
# 거부 규칙에 추가:
Skill
```

**특정 스킬 허용 또는 거부**:
```
# 특정 스킬만 허용
Skill(commit)
Skill(review-pr *)

# 특정 스킬 거부
Skill(deploy *)
```

frontmatter에 `disable-model-invocation: true`를 추가해 **개별 스킬 숨기기**.

### 스킬 재정의 동작 제어(`skillOverrides`)

`skillOverrides`(v2.1.129+)는 우선순위 스위치가 아니라 스킬별 노출 설정 맵입니다: SKILL.md를 편집하지 않고 설정에서 각 스킬이 어떻게 보일지 정합니다. 각 키는 스킬 이름이며, `/skills` 메뉴에서 바꾸면 자동으로 기록됩니다(`.claude/settings.local.json`에 저장). 우선순위는 바뀌지 않습니다 — 같은 이름이면 여전히 개인 스킬이 프로젝트 스킬보다 우선합니다. `~/.claude/settings.json`이나 프로젝트의 `.claude/settings.json`에 추가하세요:

```json
{
  "skillOverrides": {
    "deploy": "off",
    "legacy-helper": "name-only"
  }
}
```

사용할 수 있는 값:

| 값 | 동작 |
|-------|----------|
| `"on"` (기본값) | 이름과 설명이 Claude에게 제공되고 `/` 메뉴에 표시됩니다. |
| `"name-only"` | 이름만 Claude에게 제공되고 `/` 메뉴에 표시됩니다. |
| `"user-invocable-only"` | Claude에게는 숨기고 `/` 메뉴에는 계속 표시됩니다. |
| `"off"` | Claude와 `/` 메뉴 모두에서 숨깁니다. |

플러그인 스킬은 `skillOverrides`의 영향을 받지 않으니 `/plugin`으로 관리하세요.

## 모범 사례

### 1. 설명을 구체적으로

- **나쁜 예(모호함)**: "문서 작업을 도와줍니다"
- **좋은 예(구체적)**: "PDF 파일에서 텍스트와 표를 추출하고, 양식을 채우고, 문서를 병합합니다. PDF 파일을 다루거나 사용자가 PDF, 양식, 문서 추출을 언급할 때 사용합니다."

### 2. 스킬은 한 가지에 집중

- 스킬 하나 = 기능 하나
- ✅ "PDF 양식 작성"
- ❌ "문서 처리" (너무 넓음)

### 3. 트리거 용어 포함

설명에 사용자 요청과 일치하는 키워드를 넣으세요:
```yaml
description: Excel 스프레드시트를 분석하고, 피벗 테이블을 생성하고, 차트를 만듭니다. Excel 파일, 스프레드시트, .xlsx 파일을 다룰 때 사용합니다.
```

### 4. SKILL.md는 500줄 이하로

자세한 참고 자료는 Claude가 필요할 때 로드하는 별도 파일로 옮기세요.

### 5. 보조 파일 참조

```markdown
## 추가 자료

- 전체 API 세부 정보는 [reference.md](reference.md)를 참고하세요
- 사용 예시는 [examples.md](examples.md)를 참고하세요
```

### 권장

- 명확하고 설명적인 이름 사용
- 빠짐없는 지침 포함
- 구체적인 예제 추가
- 관련 스크립트와 템플릿을 함께 패키징
- 실제 시나리오로 테스트
- 의존성 문서화

### 비권장

- 일회성 작업을 위한 스킬 만들기
- 기존 기능과 중복되는 스킬 만들기
- 범위가 너무 넓은 스킬 만들기
- description 필드 생략하기
- 신뢰할 수 없는 출처의 스킬을 검토 없이 설치하기

## 문제 해결

### 빠른 참조

| 문제 | 해결 방법 |
|-------|----------|
| Claude가 스킬을 쓰지 않음 | 트리거 용어를 넣어 설명을 더 구체적으로 작성 |
| 스킬 파일을 찾을 수 없음 | 경로 확인: `~/.claude/skills/name/SKILL.md` |
| YAML 오류 | `---` 표시와 들여쓰기 확인, 탭 사용 금지 |
| 스킬끼리 충돌 | 설명마다 서로 다른 트리거 용어 사용 |
| 스크립트가 실행되지 않음 | 권한 확인: `chmod +x scripts/*.py` |
| Claude가 일부 스킬을 보지 못함 | 스킬이 너무 많음. `/context`에서 경고를 확인한 뒤 `/skill-doctor`(v2.1.252+)를 실행해 어떤 스킬이 쓰이지 않고 비용이 얼마나 드는지 확인 |

### 스킬이 호출되지 않을 때

예상한 상황에서 Claude가 스킬을 쓰지 않는다면:

1. 설명에 사용자가 자연스럽게 말할 키워드가 들어 있는지 확인하세요
2. "어떤 스킬을 쓸 수 있어?"라고 물었을 때 스킬이 표시되는지 확인하세요
3. 설명과 맞도록 요청을 바꿔 말해 보세요
4. `/skill-name`으로 직접 호출해 테스트하세요

### 스킬이 너무 자주 호출될 때

원하지 않을 때 Claude가 스킬을 쓴다면:

1. 설명을 더 구체적으로 작성하세요
2. 직접 호출할 때만 쓰도록 `disable-model-invocation: true`를 추가하세요

### Claude가 일부 스킬을 보지 못할 때

스킬 설명은 **컨텍스트 윈도우의 1%**(대체값: **8,000자**)까지 로드됩니다. 각 항목의 `description`과 `when_to_use`는 기본적으로 1,536자로 제한됩니다(`skillListingMaxDescChars`). `/context`를 실행해 제외된 스킬에 대한 경고가 있는지 확인하세요. 예산은 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 환경 변수로 바꿀 수 있습니다.

## 보안 고려 사항

**신뢰할 수 있는 출처의 스킬만 사용하세요.** 스킬은 지침과 코드로 Claude에게 기능을 제공합니다 — 악의적인 스킬은 Claude가 해로운 방식으로 도구를 호출하거나 코드를 실행하게 만들 수 있습니다.

**보안 핵심 고려 사항:**

- **철저히 검토**: 스킬 디렉토리의 모든 파일을 검토하세요
- **외부 출처는 위험**: 외부 URL에서 내용을 가져오는 스킬은 오염될 수 있습니다
- **도구 오용**: 악의적인 스킬은 해로운 방식으로 도구를 호출할 수 있습니다
- **소프트웨어 설치처럼 취급**: 신뢰할 수 있는 출처의 스킬만 사용하세요

### 스킬에서 셸 치환 끄기

스킬은 `` !`command` `` 문법으로 셸 명령어의 출력을 Claude가 보기 전에 프롬프트에 넣을 수 있습니다. 보안에 민감한 환경(여럿이 함께 쓰는 엔터프라이즈 배포, 잠긴 CI 러너)에서는 `disableSkillShellExecution` 설정(**v2.1.91**에서 추가)으로 이 치환을 완전히 끌 수 있습니다:

```jsonc
// ~/.claude/settings.json 또는 관리형 정책
{
  "disableSkillShellExecution": true
}
```

`disableSkillShellExecution`이 `true`이면 스킬의 각 `` !`command` `` 표시가 실행되는 대신 `[shell command execution disabled by policy]`로 바뀝니다 — 스킬 자체를 끄지 않고도 스킬 수준의 셸 주입 공격 표면을 없앨 수 있습니다. 심층 방어를 위해 `allowedTools` 허용 목록과 함께 쓰는 것을 고려하세요.

### 번들 스킬 숨기기(`disableBundledSkills`)

`disableBundledSkills` 설정(**v2.1.169**에서 추가)은 Claude Code에 포함된 번들 스킬, 워크플로우, 명령어를 모델에게서 숨깁니다. 기본 제공 스킬이 특정 프로젝트에서 방해만 될 때나, 모델이 다루는 스킬 범위를 줄이고 싶을 때 쓰세요:

```jsonc
// ~/.claude/settings.json 또는 프로젝트의 .claude/settings.json
{
  "disableBundledSkills": true
}
```

같은 효과를 내는 환경 변수 형식은 다음과 같습니다:

```bash
export CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1
```

## 스킬과 다른 기능 비교

| 기능 | 호출 방식 | 적합한 용도 |
|---------|------------|----------|
| **스킬** | 자동 또는 `/name` | 재사용 가능한 전문성, 워크플로우 |
| **슬래시 명령어** | 사용자가 `/name`으로 시작 | 빠른 단축 명령(스킬로 통합됨) |
| **서브에이전트** | 자동 위임 | 격리된 작업 실행 |
| **메모리 (CLAUDE.md)** | 항상 로드 | 지속되는 프로젝트 컨텍스트 |
| **MCP** | 실시간 | 외부 데이터/서비스 접근 |
| **훅** | 이벤트 기반 | 자동화된 부수 효과 |

## 번들 스킬

Claude Code에는 설치 없이 항상 쓸 수 있는 기본 제공 스킬이 들어 있습니다(아래는 가장 유용한 것들이며, 전체 목록은 [명령어 레퍼런스](https://code.claude.com/docs/ko/commands)를 참고하세요):

| 스킬 | 설명 |
|-------|-------------|
| `/batch <instruction>` | git worktree를 써서 코드베이스 전체에 걸친 대규모 병렬 변경을 조율 |
| `/claude-api` | Claude API/SDK 레퍼런스 로드. `anthropic`/`@anthropic-ai/sdk`를 가져오면 자동으로 활성화 |
| `/dataviz` | 실행 가능한 색상 팔레트 검증 도구와 함께 차트·대시보드 디자인 안내 제공(v2.1.198) |
| `/debug [description]` | 디버그 로그를 읽어 현재 세션의 문제 해결 |
| `/deep-research <question>` | 스킬이 아니라 번들 **워크플로우**: 웹 검색을 여러 갈래로 펼친 뒤 출처가 달린 보고서로 종합(v2.1.218부터 직접 호출할 때만 실행 — Claude가 스스로 시작하지 않음) |
| `/fewer-permission-prompts` | 대화 기록을 살펴 자주 쓰는 읽기 전용 도구의 허용 목록을 우선순위대로 제안 |
| `/loop [interval] [prompt]` | 정해진 간격으로 프롬프트를 반복 실행(예: `/loop 5m 배포 상태 확인해 줘`) |
| `/run` *(v2.1.145+)* | 이 프로젝트의 앱을 실행해 변경 사항이 동작하는 모습을 확인 — 프로젝트 스킬을 찾고, 없으면 프로젝트 유형별 기본 제공 패턴을 사용 |
| `/run-skill-generator` *(v2.1.145+)* | 프로젝트별 스킬을 생성해 `/run`/`/verify`에 특정 프로젝트를 다루는 방법을 알려 줌 |
| `/code-review [effort]` | 선택한 노력 수준으로 현재 diff의 정확성 버그를 리뷰(예: `/code-review high`). `--comment`를 넘기면 발견 사항을 PR 인라인 댓글로 게시합니다. v2.1.154에서 다시 분리된 `/simplify`(품질/재사용 정리)와는 별개의 스킬입니다. v2.1.246부터는 어디서든 Claude가 스스로 시작할 수도 있습니다. v2.1.218부터는 백그라운드 서브에이전트로 실행되므로 리뷰 작업이 대화를 채우지 않고, 겹쳐 쓴 슬래시 명령어도 계속 리뷰 대상으로 남습니다. |
| `/simplify` | 정리 전용 리뷰 — 재사용, 단순화, 효율성, 추상화 수준 — 를 하고 수정까지 적용. v2.1.154에서 `/code-review`와 다시 분리됨 |
| `/verify` *(v2.1.145+)* | 앱을 빌드하고 실행하고 관찰해 수정이 실제로 동작하는지 확인(테스트 통과만 보는 것이 아님). v2.1.215부터 직접 호출할 때만 실행 — Claude가 스스로 시작하지 않음 |

GitHub 풀 리퀘스트를 자동으로 리뷰하려면 Team과 Enterprise 조직에서 [관리형 Code Review](https://code.claude.com/docs/ko/code-review)를 켤 수 있습니다.

> **참고**: 프로젝트 스킬이나 사용자 스킬 중에 `verify`라는 이름이 있으면, 문서만 바꾸거나 테스트만 바꾸는 커밋을 제외하고 Claude가 커밋 직전에 그 스킬을 실행합니다(v2.1.286).

이 스킬들은 기본으로 제공되며 설치하거나 설정할 필요가 없습니다. 사용자 정의 스킬과 같은 SKILL.md 형식을 따릅니다.

## 스킬 공유

### 프로젝트 스킬(팀 공유)

1. `.claude/skills/`에 스킬 만들기
2. git에 커밋
3. 팀원이 변경 사항을 받으면(pull) 스킬을 바로 쓸 수 있음

### 개인 스킬

```bash
# 개인 디렉토리에 복사
cp -r my-skill ~/.claude/skills/

# 스크립트에 실행 권한 부여
chmod +x ~/.claude/skills/my-skill/scripts/*.py
```

### 플러그인으로 배포

더 널리 배포하려면 플러그인의 `skills/` 디렉토리에 스킬을 패키징하세요.

## 더 나아가기: 스킬 모음과 스킬 관리자

스킬을 본격적으로 만들기 시작하면 두 가지가 꼭 필요해집니다: 검증된 스킬 라이브러리와 이를 관리할 도구입니다.

**[luongnv89/skills](https://github.com/luongnv89/skills)** — 원저자가 거의 모든 프로젝트에서 매일 쓰는 스킬 모음입니다. 대표적으로 `logo-designer`(프로젝트 로고를 즉석에서 생성)와 `ollama-optimizer`(하드웨어에 맞게 로컬 LLM 성능을 조정)가 있습니다. 바로 쓸 수 있는 스킬이 필요하다면 좋은 출발점입니다.

**[luongnv89/asm](https://github.com/luongnv89/asm)** — Agent Skill Manager. 스킬 개발, 중복 감지, 테스트를 처리합니다. `asm link` 명령어를 쓰면 파일을 복사하지 않고도 어느 프로젝트에서든 스킬을 테스트할 수 있습니다 — 스킬이 몇 개를 넘어가면 꼭 필요해집니다.

## 추가 자료

- [공식 스킬 문서](https://code.claude.com/docs/ko/skills)
- [에이전트 스킬 아키텍처 블로그](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [스킬 저장소](https://github.com/luongnv89/skills) - 바로 쓸 수 있는 스킬 모음
- [슬래시 명령어 가이드](../01-slash-commands/) - 사용자가 시작하는 단축 명령
- [서브에이전트 가이드](../04-subagents/) - 작업을 위임받는 AI 에이전트
- [메모리 가이드](../02-memory/) - 지속되는 컨텍스트
- [MCP (Model Context Protocol)](../05-mcp/) - 실시간 외부 데이터
- [훅 가이드](../06-hooks/) - 이벤트 기반 자동화

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/skills
- https://code.claude.com/docs/en/slash-commands
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/ko/model-config#adjust-effort-level
- https://code.claude.com/docs/en/settings-reference
- https://github.com/anthropics/claude-code/releases/tag/v2.1.286
- https://code.claude.com/docs/ko/hooks#hooks-in-skills-and-agents
- https://code.claude.com/docs/ko/skills#characters-a-skill-name-cant-hold
- https://code.claude.com/docs/ko/hooks#hook-lifecycle
- https://code.claude.com/docs/en/changelog#2-1-299
- https://code.claude.com/docs/ko/skills#pre-approve-tools-for-a-skill
- https://code.claude.com/docs/ko/commands
- https://code.claude.com/docs/ko/memory#write-effective-instructions
- https://code.claude.com/docs/ko/memory
- https://code.claude.com/docs/en/changelog#2-1-301
- https://code.claude.com/docs/ko/code-review
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
