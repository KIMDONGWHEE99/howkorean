<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 훅

훅은 Claude Code 세션 중에 특정 이벤트가 일어나면 자동으로 실행되는 스크립트입니다. 자동화, 검증, 권한 관리, 사용자 정의 워크플로우를 가능하게 합니다.

## 개요

훅은 Claude Code에서 특정 이벤트가 일어날 때 자동으로 실행되는 동작(셸 명령어, HTTP 웹훅, LLM 프롬프트, MCP 도구 호출, 서브에이전트 평가)입니다. JSON 입력을 받고, 종료 코드와 JSON 출력으로 결과를 전달합니다.

**주요 특징:**
- 이벤트 기반 자동화
- JSON 기반 입출력
- `command`, `http`, `mcp_tool`, `prompt`, `agent` 훅 타입 지원
- 도구별 훅을 위한 패턴 매칭

## 설정

훅은 정해진 구조로 설정 파일에서 구성합니다:

- `~/.claude/settings.json` - 사용자 설정(모든 프로젝트)
- `.claude/settings.json` - 프로젝트 설정(공유 가능, 커밋함)
- `.claude/settings.local.json` - 로컬 프로젝트 설정(커밋하지 않음)
- 관리형 정책 - 조직 전체 설정
- 플러그인 `hooks/hooks.json` - 플러그인 범위 훅
- 스킬/에이전트 frontmatter - 구성 요소의 수명 동안 유지되는 훅

### 기본 설정 구조

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**주요 필드:**

| 필드 | 설명 | 예 |
|-------|-------------|---------|
| `matcher` | 도구 이름과 일치시킬 패턴(대소문자 구분) | `"Write"`, `"Edit\|Write"`, `"*"` |
| `hooks` | 훅 정의 배열 | `[{ "type": "command", ... }]` |
| `type` | 훅 타입: `"command"`(bash), `"prompt"`(LLM), `"http"`(웹훅), `"mcp_tool"`(MCP 도구 호출, v2.1.118+), `"agent"`(서브에이전트) | `"command"` |
| `command` | 실행할 셸 명령어 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"` |
| `timeout` | 선택 사항인 시간 제한(초). 기본값: command/http/mcp_tool은 600, prompt는 30, agent는 60. | `30` |
| `once` | `true`이면 처음으로 성공한 뒤 훅이 제거됩니다(실패, 차단, 시간 초과된 실행은 훅을 유지). 스킬 frontmatter 전용이며 설정 파일과 에이전트 frontmatter에서는 무시됩니다 | `true` |
| `async` | `true`이면 막지 않고 백그라운드에서 실행 | `true` |
| `asyncRewake` | `true`이면 백그라운드에서 실행하다가 종료 코드 2로 끝나면 Claude를 깨웁니다. `async`를 포함합니다. | `true` |
| `shell` | `"bash"` 또는 `"powershell"`. 기본값은 `"bash"`이며, Git Bash가 설치되지 않은 Windows에서는 `"powershell"`. | `"bash"` |
| `statusMessage` | 훅이 실행되는 동안 표시할 사용자 정의 스피너 메시지 | `"Formatting…"` |
| `onFailure` | command 훅이나 HTTP 훅이 실패할 때(시작하지 못하거나, 시간이 초과되거나, 예상하지 못한 코드로 종료) 동작을 어떻게 할지: `"continue"`(기본값) 또는 `"block"`(v2.1.295+) | `"block"` |

> **참고**: 일부 이벤트는 기본 시간 제한을 낮춥니다. `UserPromptSubmit`은 `command`, `http`, `mcp_tool`의 기본값을 30초로, `MessageDisplay`는 10초로 낮춥니다. `SessionEnd` 훅은 1.5초 예산을 함께 쓰며, 설정에서 훅별 `timeout`을 더 길게 지정하면 Claude Code가 최대 60초까지 그에 맞춰 예산을 늘립니다.

### 매처 패턴

| 패턴 | 설명 | 예 |
|---------|-------------|---------|
| 정확한 문자열 | 특정 도구와 일치 | `"Write"` |
| 정규식 패턴 | 여러 도구와 일치 | `"Edit\|Write"` |
| 쉼표 구분 | 나열된 도구 중 아무것과 일치(v2.1.191+) | `"Write,Edit"` |
| 와일드카드 | 모든 도구와 일치 | `"*"` 또는 `""` |
| MCP 도구 | 서버와 도구 패턴 | `"mcp__memory__.*"` |

> **매처는 정확하게 일치시킵니다(v2.1.195+).** 하이픈이 들어간 식별자(예: 하이픈이 포함된 MCP 도구 이름)가 더 이상 실수로 다른 도구의 부분 문자열과 일치하지 않습니다. `"Write,Edit"` 같은 쉼표 구분 매처는 목록의 어느 도구에서든 실행됩니다 — 이전 빌드에서는 아무 알림 없이 한 번도 실행되지 않았습니다.

**InstructionsLoaded 매처 값:**

| 매처 값 | 설명 |
|---------------|-------------|
| `session_start` | 세션 시작 시 로드된 지침 |
| `nested_traversal` | 중첩 디렉토리를 탐색하면서 로드된 지침 |
| `path_glob_match` | 경로 glob 패턴 매칭으로 로드된 지침 |

### `if` 조건으로 범위 좁히기(도구 인수 경로)

`matcher` 필드는 **도구 이름**(`"Write"`, `"Edit|Write"`, `"*"`)으로 훅을 고릅니다. 도구의 **인수**로 더 좁게 거르려면 — 예를 들어 편집이 `src/`를 건드릴 때만 훅을 실행하거나, 비밀 파일 읽기를 막으려면 — 개별 훅 핸들러에 `if` 조건을 추가하세요. 이는 도구 이름 매처와 다릅니다: `matcher`는 *어떤 도구*인지, `if`는 *어떤 호출*인지를 정합니다.

`if`는 [권한 규칙 문법](https://code.claude.com/docs/ko/permissions)인 `ToolName(pattern)` 형식을 쓰며, 도구 이름과 인수를 **함께** 평가합니다. `Read`/`Edit`/`Write`의 경로 패턴은 gitignore 규칙을 따르고 권한 규칙과 같은 기준점을 씁니다: `.env` 같은 이름만 쓰면 어느 깊이에서든 일치하고, `src/**`는 현재 디렉토리 기준, `/src/**`는 프로젝트 루트 기준, `~/...`는 홈 디렉토리 기준이며, `//...`는 파일 시스템의 절대 경로입니다.

`if` 필드는 `matcher`가 아니라 **훅 핸들러 수준**에 둡니다 — `hooks` 배열 안에서 `type`, `command`와 나란히:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "if": "Edit(src/**)",
            "command": "./hooks/lint-src.sh"
          }
        ]
      },
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "if": "Read(.env)",
            "command": "./hooks/block-secret-read.sh"
          }
        ]
      }
    ]
  }
}
```

유효한 `if` 패턴의 예: `Edit(src/**)`(`src/` 아래의 편집), `Read(~/.ssh/**)`(모든 SSH 키 읽기), `Read(.env)`(현재 디렉토리와 그 아래의 모든 `.env`), `Bash(git push *)`(`git push` 하위 명령어만).

> **v2.1.214 변경 사항**: 이제 훅 `if` 조건의 한 단계짜리 `dir/**` 패턴(`Edit(src/**)` 등)은 트리의 어느 깊이에 있는 디렉토리가 아니라 `<cwd>/dir`에만 일치합니다. 이전에는 `src/**`가 `foo/src/**`에도 일치했습니다. 어느 깊이에서든 일치시키려면 `**/dir/**`를 쓰세요. **중요**: 이렇게 좁아지는 것은 훅의 `if:` 조건과 허용 규칙 자동 승인에만 해당합니다 — 거부/요청 권한 규칙은 여전히 어느 깊이에서든 `dir/**`와 일치합니다.

## 훅 타입

Claude Code는 다섯 가지 훅 타입을 지원합니다:

### 명령어 훅

기본 훅 타입입니다. 셸 명령어를 실행하고 JSON stdin/stdout과 종료 코드로 소통합니다.

```json
{
  "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py\"",
  "timeout": 60
}
```

#### exec 형식(`args`)

> v2.1.139에서 추가되었습니다.

명령어 훅은 셸 형식의 `"command": "..."` 대신 `args` 배열로 `execve()`를 통해 바이너리를 직접 실행할 수 있습니다. 셸 파싱이 없으므로 경로 자리 표시자를 따옴표로 감쌀 필요가 없고, 설정이 셸 주입 버그에 영향을 받지 않습니다.

```json
{
  "type": "command",
  "command": "python3",
  "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate.py", "--strict"],
  "timeout": 60
}
```

`command`는 항상 필요합니다: `args`를 설정하면 `command`는 실행할 실행 파일(`PATH`에서 찾음)이고 `args`는 그 인수 벡터입니다. 파이프, 리디렉션, `&&` 연결, 셸 확장이 필요하면 `args`를 생략하고(셸 형식), 바이너리 하나를 인수와 함께 호출할 때는 `args`를 쓰세요.

### HTTP 훅

> v2.1.63에서 추가되었습니다.

명령어 훅과 같은 JSON 입력을 받는 원격 웹훅 엔드포인트입니다. HTTP 훅은 URL로 JSON을 POST하고 JSON 응답을 받습니다. 샌드박싱이 켜져 있으면 HTTP 훅은 샌드박스를 거쳐 전송됩니다. 보안을 위해 헤더 값에 환경 변수를 넣으려면 명시적인 `allowedEnvVars` 목록이 필요합니다.

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "http",
        "url": "https://my-webhook.example.com/hook"
      }]
    }]
  }
}
```

**주요 속성:**
- `"type": "http"` -- HTTP 훅임을 나타냄
- `"url"` -- 웹훅 엔드포인트 URL
- 샌드박스가 켜져 있으면 샌드박스를 거쳐 전송
- `headers` 값에 환경 변수를 넣으려면 명시적인 `allowedEnvVars` 목록이 필요

### 프롬프트 훅

훅 내용이 Claude가 평가하는 프롬프트인, LLM이 평가하는 훅입니다. 주로 `Stop`과 `SubagentStop` 이벤트에서 작업 완료를 지능적으로 확인하는 데 씁니다.

```json
{
  "type": "prompt",
  "prompt": "Claude가 요청받은 작업을 모두 끝냈는지 평가하세요.",
  "timeout": 30
}
```

LLM이 프롬프트를 평가하고 구조화된 결정을 반환합니다(자세한 내용은 [프롬프트 기반 훅](#프롬프트-기반-훅) 참고).

### MCP 도구 훅

> v2.1.118에서 추가되었습니다.

`mcp_tool` 타입은 설정된 MCP 도구를 직접 호출합니다. 설정에서는 셸 명령어나 URL 대신 MCP 서버와 도구 이름을 참조합니다. 검증이나 대응 로직이 이미 설정해 둔 MCP 서버에 있을 때 유용합니다.

```json
{
  "matcher": "Edit",
  "hooks": [{
    "type": "mcp_tool",
    "server": "my-mcp-server",
    "tool": "validate_edit",
    "input": { "file_path": "${tool_input.file_path}" }
  }]
}
```

**주요 속성:**
- `"type": "mcp_tool"` -- MCP 도구 훅임을 나타냄
- `"server"` -- 설정된 MCP 서버의 이름
- `"tool"` -- 그 서버에서 호출할 도구 이름
- `"input"` -- 도구에 넘길 선택 인수. 문자열 값에서는 훅의 JSON 입력을 가져오는 `${path}` 치환을 지원합니다(예: `"${tool_input.file_path}"`)

도구의 인수는 훅 입력에서 바로 오는 것이 아니라 (`${path}` 치환을 거친) `input`에서 옵니다. MCP 서버 설정은 [MCP 서버 설정](../05-mcp/README.md)을 참고하세요.

### 에이전트 훅

전용 에이전트를 생성해 조건을 평가하거나 복잡한 확인을 수행하는, 서브에이전트 기반 검증 훅입니다. (한 턴짜리 LLM 평가인) 프롬프트 훅과 달리 에이전트 훅은 도구를 쓰고 여러 단계로 추론할 수 있습니다.

> **참고**: 에이전트 훅은 실험적 기능이며 바뀔 수 있습니다.

> **참고**: v2.1.280부터 에이전트 훅은 `PermissionRequest`에서 실행되지 않습니다 — 에이전트 훅의 답은 요청을 허용하거나 거부할 수 없었기 때문입니다. 그 이벤트에는 결정 객체를 반환하는 명령어 훅이나 HTTP 훅을 쓰세요(프롬프트 훅의 `ok: false`는 `PermissionRequest`에 아무 효과가 없습니다).

```json
{
  "type": "agent",
  "prompt": "코드 변경이 우리 아키텍처 가이드라인을 따르는지 검증하세요. 관련 설계 문서를 확인하고 비교하세요.",
  "timeout": 120
}
```

**주요 속성:**
- `"type": "agent"` -- 에이전트 훅임을 나타냄
- `"prompt"` -- 서브에이전트에게 줄 작업 설명
- 에이전트는 평가를 위해 도구(Read, Grep, Bash 등)를 쓸 수 있음
- 프롬프트 훅과 비슷한 구조화된 결정을 반환

## 훅 이벤트

Claude Code는 **33가지 훅 이벤트를** 지원합니다:

| 이벤트 | 발생 시점 | 매처 입력 | 차단 가능 | 주요 용도 |
|-------|---------------|---------------|-----------|------------|
| **SessionStart** | 세션 시작/재개/clear/compact | startup/resume/clear/compact/fork | 아니요 | 환경 준비 |
| **Setup** | `--init-only`, 또는 `-p`와 함께 쓴 `--init`/`--maintenance`(CI/스크립트 준비) | `init`/`maintenance` | 아니요 | 도구 준비, 의존성 설치 |
| **InstructionsLoaded** | CLAUDE.md나 규칙 파일이 로드된 뒤 | 로드 이유(`session_start`/`nested_traversal`/`path_glob_match`/`include`/`compact`) | 아니요 | 감사/관측용 로깅 |
| **UserPromptSubmit** | 사용자가 프롬프트를 제출 | (없음) | 예 | 프롬프트 검증 |
| **UserPromptExpansion** | 사용자가 입력한 슬래시 명령어나 MCP 프롬프트가 프롬프트로 확장됨 | 명령어 이름 | 예 | 확장된 프롬프트 변환이나 검사 |
| **PreToolUse** | 도구 실행 전 | 도구 이름 | 예(allow/deny/ask/defer) | 검증, 입력 수정 |
| **PermissionRequest** | 권한 대화 상자 표시 | 도구 이름 | 예 | 자동 승인/거부 |
| **PermissionDenied** | 자동 모드가 도구 호출을 거부 | 도구 이름 | 아니요 | 로깅, 분석, 정책 적용 |
| **PostToolUse** | 도구가 성공한 뒤 | 도구 이름 | 아니요 | 컨텍스트 추가, 피드백 |
| **PostToolUseFailure** | 도구 실행 실패 | 도구 이름 | 아니요 | 오류 처리, 로깅 |
| **PostToolBatch** | 여러 도구 사용이 한 묶음으로 끝난 뒤 | (없음) | 예 | 종합 보고, 일괄 검증 |
| **Notification** | 알림 전송 | 알림 유형 | 아니요 | 사용자 정의 알림 |
| **MessageDisplay** | 어시스턴트 메시지 텍스트가 표시되는 동안 | (없음) | 아니요 | 표시되는 메시지 텍스트 변환이나 숨기기(v2.1.152) |
| **SubagentStart** | 서브에이전트 생성 | 에이전트 타입 이름 | 아니요 | 서브에이전트 준비 |
| **SubagentStop** | 서브에이전트 종료 | 에이전트 타입 이름 | 예 | 서브에이전트 결과 검증 |
| **Stop** | Claude가 응답을 마침 | (없음) | 예 | 작업 완료 확인 |
| **StopFailure** | API 오류로 턴이 끝남 | 오류 유형(`rate_limit`, `overloaded`, `server_error`, …) | 아니요 | 오류 복구, 로깅 |
| **TeammateIdle** | 에이전트 팀의 팀원이 유휴 상태 | (없음) | 예 | 팀원 조율 |
| **TaskCompleted** | 작업이 완료로 표시됨 | (없음) | 예 | 작업 후 처리 |
| **TaskCreated** | TaskCreate로 작업 생성 | (없음) | 예 | 작업 추적, 로깅 |
| **ConfigChange** | 설정 파일 변경 | 설정 출처(`user_settings`/`project_settings`/`local_settings`/`policy_settings`/`skills`) | 예(정책 제외) | 설정 변경에 대응 |
| **CwdChanged** | 작업 디렉토리 변경 | (없음) | 아니요 | 디렉토리별 준비 작업 |
| **DirectoryAdded** | `/add-dir`이나 SDK의 `register_repo_root` 제어 요청으로 세션 도중 새 작업 디렉토리 등록(v2.1.219) | `slash_command`/`register_repo_root` | 아니요 | 새로 추가된 디렉토리용 도구 준비 |
| **FileChanged** | 감시 중인 파일 변경 | 감시할 파일 이름(예: `.envrc\|.env`) | 아니요 | 파일 모니터링, 다시 빌드 |
| **PreCompact** | 컨텍스트 컴팩션 전 | manual/auto | 예 | 컴팩션 전 작업 |
| **PostCompact** | 컴팩션 완료 후 | (없음) | 아니요 | 컴팩션 후 작업 |
| **PreModelSwitch** | 요청된 모델 전환을 Claude Code가 적용하기 전 | 전환될 모델의 정식 이름(`to_model`에서 가져옴) | 예 | 모델 변경 허용 여부 결정이나 거부 |
| **PostModelSwitch** | 세션의 모델이 바뀐 뒤. Claude Code가 스스로 바꾸는 경우(재개할 때 모델을 복원하는 경우 등)도 포함 | 전환된 모델의 정식 이름(`to_model`에서 가져옴) | 아니요 | 모델 변경 기록이나 대응 |
| **WorktreeCreate** | worktree 생성 중 | (없음) | 예(경로 반환) | worktree 초기화 |
| **WorktreeRemove** | worktree 제거 중 | (없음) | 예(0이 아닌 종료 코드면 제거 실패) | worktree 정리 |
| **Elicitation** | MCP 서버가 사용자 입력을 요청 | MCP 서버 이름 | 예 | 입력 검증 |
| **ElicitationResult** | 사용자가 입력 요청에 응답 | MCP 서버 이름 | 예 | 응답 처리 |
| **SessionEnd** | 세션 종료 | 종료 이유(`clear`/`resume`/`logout`/`prompt_input_exit`/`other`) | 아니요 | 정리, 마지막 로깅 |

`PreModelSwitch`와 `PostModelSwitch`에는 v2.1.251 이상이 필요합니다. 둘 다 `from_model`과 `to_model`을 받으며, 매처는 `to_model`에서 가져온 정식 이름(예: `claude-opus-5`, `.*opus.*`)으로 평가됩니다. 이 이벤트에서는 `command`, `http`, `mcp_tool`의 기본 시간 제한이 30초로 낮아집니다.

> **`TaskCreated`와 `TaskCompleted`에는 할 일 도구가 켜져 있어야 합니다(v2.1.233).** 이 두
> 이벤트는 할 일/작업 추적 도구(`TaskCreate`/`Get`/`Update`/`List`,
> `TodoWrite`)에서 발생하는데, 이 도구들은
> **Claude 3.x 모델, Opus 4–4.7, Sonnet 4–4.6, Haiku 4.5에서만 기본으로 제공됩니다**.
> 다른 모델에서는 훅 설정이 유효하더라도 이벤트가 전혀 발생하지 않으며, 출력도 오류도 없습니다.
> `CLAUDE_CODE_ENABLE_TODO_TOOLS=1`을 설정하면 도구와 함께 이벤트도 다시 켜집니다.

> **PostToolUse 실행 시간 (v2.1.119):** 이제 `PostToolUse`와 `PostToolUseFailure` 훅 입력에 `duration_ms`가 들어 있습니다 — 자세한 내용은 [PostToolUse](#posttooluse) 섹션을 참고하세요.

### PreToolUse

Claude가 도구 매개변수를 만든 뒤, 처리하기 전에 실행됩니다. 도구 입력을 검증하거나 수정할 때 쓰세요.

**설정:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

**자주 쓰는 매처:** `Agent`, `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `Write`, `WebFetch`, `WebSearch`

**출력 제어:**
- `permissionDecision`: `"allow"`, `"deny"`, `"ask"`, `"defer"`
  - `"allow"`는 권한 프롬프트를 건너뜁니다(사용자 상호작용이 필요한 도구와, 조직에서 `ask`로 설정한 커넥터 도구는 예외)
  - `"deny"`는 도구 호출을 막습니다
  - `"ask"`는 사용자에게 확인을 요청하며, 프롬프트에 훅을 제공한 플러그인이나 스킬의 이름이 표시됩니다(v2.1.301)
  - `"defer"`는 나중에 도구를 재개할 수 있도록 깔끔하게 종료하며, 이 값에서는 `permissionDecisionReason`, `updatedInput`, `additionalContext`가 모두 무시됩니다
  - 훅이 무엇을 반환하든 거부 규칙과 요청 규칙은 여전히 평가됩니다. 여러 `PreToolUse` 훅의 결정이 다르면 우선순위는 `deny` > `defer` > `ask` > `allow`입니다
- `permissionDecisionReason`: 결정에 대한 설명. `"ask"`일 때는 (Claude가 아니라) 사용자에게, `"deny"`일 때는 Claude에게 표시되며, `"allow"`와 `"defer"`일 때는 디버그 로그에만 기록됩니다
- `updatedInput`: 대체할 도구 입력(입력 객체 전체를 대체). v2.1.300부터는 Claude 자신의 입력처럼 검증됩니다 — 알 수 없는 키는 버려지고, 도구가 거부하는 입력이면 호출이 거부됩니다.

### PostToolUse

도구가 끝난 직후에 실행됩니다. 검증, 로깅, Claude에게 컨텍스트를 돌려줄 때 쓰세요.

**설정:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py"
          }
        ]
      }
    ]
  }
}
```

**출력 제어:**
- `"block"` 결정은 피드백과 함께 Claude에게 알립니다
- `additionalContext`: Claude에게 추가할 컨텍스트

**추가 입력 필드 (v2.1.119):**

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| `duration_ms` | number | 도구 실행 시간(밀리초). 권한 프롬프트와 PreToolUse 훅 실행에 걸린 시간은 제외됩니다. `PostToolUse`와 `PostToolUseFailure` 훅 모두에서 제공됩니다. |

#### 복구 가능한 차단(`continueOnBlock`, v2.1.139)

`PostToolUse`에서 `"decision": "block"`을 반환하는 명령어 훅은 도구 결과 옆에 `reason`을 덧붙이며, Claude는 원래 출력도 그대로 봅니다. `continueOnBlock`은 **프롬프트** 훅의 필드입니다(명령어 훅과 에이전트 훅에는 없음): 기본적으로 `PostToolUse`에서 `ok: false`를 반환하는 프롬프트 훅은 턴을 끝내고 이유를 경고 줄로 표시합니다. 프롬프트 훅에 `"continueOnBlock": true`를 설정하면 대신 이유를 Claude에게 돌려주고 턴을 계속하므로, 모델이 피드백을 읽고 다시 시도하거나 방향을 조정할 수 있습니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "이 편집이 우리 쓰기 정책(예: 읽기 전용 경로)에 맞는지 확인하세요. 훅 입력: $ARGUMENTS",
            "continueOnBlock": true
          }
        ]
      }
    ]
  }
}
```

훅의 `reason`이 Claude가 대응할 수 있는 내용일 때(예: "이 파일은 읽기 전용이니 다른 곳에 쓰세요") 쓰세요. 차단하면 턴을 완전히 멈춰야 하는 경우에는 끄세요.

### UserPromptSubmit

사용자가 프롬프트를 제출하면, Claude가 처리하기 전에 실행됩니다. v2.1.299부터는 스킬이나 사용자 정의 명령어가 확장되기 전에 실행되므로, 프롬프트를 차단하면 그 명령어의 `!` 셸 줄도 실행되지 않습니다. `UserPromptExpansion`은 그 뒤에 발생합니다.

**설정:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py"
          }
        ]
      }
    ]
  }
}
```

**출력 제어:**
- `decision`: 처리를 막으려면 `"block"`
- `reason`: 차단할 때의 설명
- `additionalContext`: 프롬프트에 추가할 컨텍스트

### Stop과 SubagentStop

Claude가 응답을 마칠 때(Stop)나 서브에이전트가 끝날 때(SubagentStop) 실행됩니다. 작업 완료를 지능적으로 확인하는 프롬프트 기반 평가를 지원합니다.

**추가 입력 필드:** `Stop`과 `SubagentStop` 훅은 모두 JSON 입력에서 `last_assistant_message` 필드를 받습니다. 멈추기 직전 Claude나 서브에이전트의 마지막 메시지가 담겨 있어 작업 완료를 평가할 때 유용합니다.

**설정:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Claude가 요청받은 작업을 모두 끝냈는지 평가하세요.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

> **연속 차단 안전 한도 (v2.1.143)**: `Stop` 훅이 같은 턴에서 **8번 연속으로** `"decision": "block"`을 반환하면(또는 `continue: false`를 설정하면) Claude Code가 다음 차단을 무시하고 턴을 끝냅니다. 임계값은 환경 변수 `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP=<정수>`로 바꿀 수 있습니다(`0`이면 한도를 완전히 끔). 버그가 있는 Stop 훅이 턴을 끝없이 반복시키는 것을 막아 줍니다.

**반환 필드 (v2.1.163):** `Stop`이나 `SubagentStop` 훅은 `hookSpecificOutput.additionalContext`를 반환해 Claude에게 피드백을 주고 **오류 표시 없이 턴을 계속할** 수 있습니다. 이전에는 Stop 훅으로 모델에 영향을 주기가 번거로웠지만, 이제는 오래된 피드백 방식(`"decision": "block"` 등)의 오류 표시 동작 없이 컨텍스트를 깔끔하게 넣을 수 있습니다.

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "리마인더: 완료라고 하기 전에 테스트 스위트를 실행하세요."
  }
}
```

### SubagentStart

서브에이전트가 실행을 시작할 때 실행됩니다. 매처 입력은 에이전트 타입 이름이므로 특정 서브에이전트 타입만 대상으로 삼을 수 있습니다.

**설정:**
```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "code-review",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-init.sh"
          }
        ]
      }
    ]
  }
}
```

### SessionStart

세션이 시작되거나 재개될 때 실행됩니다. 환경 변수를 유지할 수 있습니다.

**매처:** `startup`, `resume`, `clear`, `compact`, `fork`

> **v2.1.214 변경 사항**: 이제 포크된 세션은 출처를 `"fork"`로 보고합니다 — 이전에는 `"resume"`으로 보고했습니다.

**특별 기능:** `CLAUDE_ENV_FILE`로 환경 변수를 유지할 수 있습니다(`CwdChanged`와 `FileChanged` 훅에서도 사용 가능):

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

**세션 범위 출력 (v2.1.152):** `SessionStart` 훅은 JSON을 반환해 스킬을 다시 검색하고 세션 제목을 정할 수 있습니다:

```json
{
  "reloadSkills": true,
  "hookSpecificOutput": {
    "sessionTitle": "결제 마이그레이션"
  }
}
```

최상위 `reloadSkills: true`는 같은 세션에서 스킬 재검색을 일으키므로(`/reload-skills` 명령어와 같은 동작), 훅이 방금 설치한 스킬을 바로 쓸 수 있습니다. `hookSpecificOutput.sessionTitle`은 시작하거나 재개할 때 세션의 표시 제목을 정합니다.

### SessionEnd

세션이 끝날 때 정리나 마지막 로깅을 위해 실행됩니다. 종료를 막을 수는 없습니다.

**reason 필드 값:**
- `clear` - 사용자가 세션을 지움
- `resume` - 대화형 `/resume`으로 세션 전환
- `logout` - 사용자가 로그아웃함
- `prompt_input_exit` - 사용자가 프롬프트 입력으로 종료함
- `other` - 기타 이유

**설정:**
```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-cleanup.sh\""
          }
        ]
      }
    ]
  }
}
```

### Notification 이벤트

알림 이벤트에서 쓸 수 있는 매처입니다:
- `permission_prompt` - 권한 요청 알림
- `idle_prompt` - 유휴 상태 알림
- `auth_success` - 인증 성공
- `elicitation_dialog` - MCP 서버가 입력 요청 양식을 엶
- `elicitation_url_dialog` - MCP 서버가 브라우저 URL을 열어 달라고 요청함
- `elicitation_complete` - URL 방식의 입력 요청이 완료되었다고 보고됨
- `elicitation_response` - 입력 요청 응답을 서버로 돌려보냄
- `agent_needs_input` - 백그라운드 에이전트에 입력이 필요함(v2.1.198)
- `agent_completed` - 백그라운드 에이전트가 끝남(v2.1.198)
- `quota_auto_resume_fired` / `quota_auto_resume_stale` / `quota_auto_resume_disabled` - 사용 한도 자동 이어 하기의 결과(v2.1.234)

### PreModelSwitch

요청된 모델 전환을 Claude Code가 적용하기 **전에** 실행됩니다 — 예를 들어 `/model`을 실행하거나, 어떤 구성 요소가 다른 모델을 요청할 때입니다. v2.1.251 이상이 필요합니다.

**매처:** `to_model`에서 가져온, 전환될 모델의 정식 이름. 정확한 모델(`claude-opus-5`)이나 정규식으로 모델 계열(`.*opus.*`)과 일치시킵니다.

**입력 필드:** 공통 필드에 더해 `from_model`(전환 전에 쓰던 모델)과 `to_model`(요청된 모델)을 받습니다.

**차단 가능:** 예. 종료 코드 `2`는 전환을 막고 stderr를 오류로 표시하므로 세션은 현재 모델을 유지합니다. 모델 변경을 허용할지 정하거나 거부할 때 쓰세요 — 예를 들어 비용에 민감한 프로젝트가 가장 비싼 모델을 쓰지 않게 할 수 있습니다.

**시간 제한:** 이 이벤트에서는 `command`, `http`, `mcp_tool`의 기본 시간 제한이 30초로 낮아집니다.

**설정:**
```json
{
  "hooks": {
    "PreModelSwitch": [
      {
        "matcher": ".*opus.*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/gate-model-switch.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
#!/bin/bash
# gate-model-switch.sh - 이 프로젝트에서는 Opus로의 전환을 거부
input=$(cat)
to_model=$(echo "$input" | jq -r '.to_model')

if [[ "$to_model" == *opus* ]]; then
  echo "This project is budgeted for Sonnet; staying on the current model." >&2
  exit 2
fi

exit 0
```

### PostModelSwitch

세션의 모델이 바뀐 **뒤에** 실행됩니다. 사용자가 요청한 전환뿐 아니라 Claude Code가 스스로 바꾸는 경우 — 세션을 재개할 때 이전에 고른 모델을 복원하는 경우 등 — 에도 발생합니다. v2.1.251 이상이 필요합니다.

**매처:** `PreModelSwitch`와 같음 — `to_model`에서 가져온 정식 이름.

**입력 필드:** 공통 필드와 함께 `from_model`, `to_model`.

**차단 가능:** 아니요. 전환은 이미 일어났으므로 훅은 관찰하고 대응할 수만 있습니다.

**시간 제한:** 이 이벤트에서는 `command`, `http`, `mcp_tool`의 기본 시간 제한이 30초로 낮아집니다.

**설정:**
```json
{
  "hooks": {
    "PostModelSwitch": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/log-model-switch.sh"
          }
        ]
      }
    ]
  }
}
```

```bash
#!/bin/bash
# log-model-switch.sh - 모든 모델 변경을 세션 로그에 추가
input=$(cat)
from=$(echo "$input" | jq -r '.from_model')
to=$(echo "$input" | jq -r '.to_model')

echo "$(date -Iseconds) $from -> $to" >> ~/.claude/model-switches.log
exit 0
```

## 구성 요소 범위 훅

훅은 특정 구성 요소(스킬, 에이전트, 명령어)의 frontmatter에 붙일 수 있습니다:

**SKILL.md, agent.md, command.md에서:**

```yaml
---
name: secure-operations
description: 보안 검사와 함께 작업 수행
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true  # 스킬 frontmatter 전용: 처음 성공한 뒤 제거됨
---
```

**지원 이벤트:** 모든 훅 이벤트. 서브에이전트 훅은 서브에이전트가 활성화된 동안에만 실행되며(`Stop` → `SubagentStop`), 스킬 훅은 스킬이 호출될 때 등록되어 세션이 끝날 때까지 활성 상태로 남습니다.

덕분에 훅을 쓰는 구성 요소 안에 훅을 바로 정의해 관련 코드를 한곳에 모을 수 있습니다.

### 서브에이전트 frontmatter의 훅

서브에이전트의 frontmatter에 `Stop` 훅을 정의하면 그 서브에이전트 범위의 `SubagentStop` 훅으로 자동 변환됩니다. 따라서 이 훅은 메인 세션이 멈출 때가 아니라 해당 서브에이전트가 끝날 때만 실행됩니다.

```yaml
---
name: code-review-agent
description: 자동 코드 리뷰 서브에이전트
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "코드 리뷰가 철저하고 빠짐없는지 검증하세요."
  # 위의 Stop 훅은 이 서브에이전트에서 SubagentStop으로 자동 변환됨
---
```

**작업 공간 신뢰 필요 (v2.1.218):** 이제 **프로젝트** 서브에이전트의 frontmatter 훅은 에이전트 파일이 있는 폴더의 작업 공간 신뢰를 수락해야 실행됩니다. v2.1.218 이전에는 신뢰하지 않은 폴더에서도 이 훅이 실행될 수 있었습니다. 어떤 범위가 예외인지는 [서브에이전트 문서](https://code.claude.com/docs/ko/sub-agents#hooks-in-subagent-frontmatter)를 참고하세요.

## PermissionRequest 이벤트

사용자 정의 출력 형식으로 권한 요청을 처리합니다:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": {},
      "message": "사용자 정의 메시지",
      "interrupt": false
    }
  }
}
```

## 훅 입력과 출력

### JSON 입력(stdin으로)

모든 훅은 stdin으로 JSON 입력을 받습니다:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.js",
    "content": "..."
  },
  "tool_use_id": "toolu_01ABC123...",
  "agent_id": "agent-abc123",
  "agent_type": "security-reviewer",
  "worktree": "/path/to/worktree",
  "effort": { "level": "medium" }
}
```

**공통 필드:**

| 필드 | 설명 |
|-------|-------------|
| `session_id` | 고유한 세션 식별자 |
| `transcript_path` | 대화 기록 파일의 경로 |
| `cwd` | 현재 작업 디렉토리 |
| `prompt_id` | 처리 중인 프롬프트의 UUID. OpenTelemetry의 `prompt.id` 속성과 대응합니다(v2.1.196) |
| `hook_event_name` | 훅을 일으킨 이벤트의 이름 |
| `agent_id` | 이 훅을 실행하는 에이전트의 식별자 |
| `agent_type` | 에이전트 이름(예: `"Explore"`, `"security-reviewer"`). 세션이 `--agent`를 쓰거나 서브에이전트 안에서 훅이 실행될 때만 있음 |
| `worktree` | 에이전트가 git worktree에서 실행 중이면 그 worktree의 경로 |
| `effort.level` | (v2.1.133+) 현재 노력 수준: `low`, `medium`, `high`, `xhigh`, `max` |

### 종료 코드

| 종료 코드 | 의미 | 동작 |
|-----------|---------|----------|
| **0** | 성공 | 계속 진행하고 stdout의 JSON을 파싱 |
| **2** | 차단 오류 | 작업을 막고 stderr를 오류로 표시 |
| **그 밖의 값** | 차단하지 않는 오류 | 계속 진행. 대화 기록에 stderr 첫 줄을 담은 `<hook name> hook error` 알림이 표시됨 |

### JSON 출력(stdout, 종료 코드 0)

```json
{
  "continue": true,
  "stopReason": "중단할 때 표시할 메시지(선택)",
  "suppressOutput": false,
  "systemMessage": "경고 메시지(선택)",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "허용된 디렉토리에 있는 파일",
    "updatedInput": {
      "file_path": "/modified/path.js"
    }
  }
}
```

> **범위 (v2.1.121+):** 이제 `hookSpecificOutput.updatedToolOutput`은 MCP 도구만이 아니라 **모든** 도구에 적용됩니다. `Bash`, `Edit`, `Read` 등에 대한 `PostToolUse` 훅이 Claude가 보기 전에 도구의 출력을 다시 쓸 수 있습니다 — 비밀 정보를 가리거나, diff를 정규화하거나, 시끄러운 명령어 출력을 걸러 낼 때 유용합니다. 값은 도구 출력의 형태와 맞아야 합니다 — `Bash`는 `stdout`, `stderr`, `interrupted`, `isImage`를 가진 객체를 반환하며, 기본 제공 도구에서 형태가 맞지 않는 값은 무시되고 원래 출력이 쓰입니다. 예(`Bash` 출력에서 ANSI 색상 코드 제거):
>
> ```json
> {
>   "hookSpecificOutput": {
>     "hookEventName": "PostToolUse",
>     "updatedToolOutput": {
>       "stdout": "<output with ANSI escapes removed>",
>       "stderr": "",
>       "interrupted": false,
>       "isImage": false
>     }
>   }
> }
> ```

> **`retry` (PermissionDenied)**: JSON의 `hookSpecificOutput.retry: true`로 거부된 도구 호출을 다시 시도해도 된다고 모델에게 알릴 수 있습니다.

> **지원 중단된 `PreToolUse` 결정 형식**: `PreToolUse`에서 최상위 `decision`과 `reason` 필드는 **지원 중단되었습니다** — 대신 `hookSpecificOutput.permissionDecision`(`allow` / `deny` / `ask` / `defer`)과 `permissionDecisionReason`을 쓰세요. 결정 사이의 우선순위는 `deny` > `defer` > `ask` > `allow`입니다. 또한 `suppressOutput`은 받아들여지지만 **아무 효과가 없습니다**.

#### `terminalSequence` (v2.1.141)

훅은 JSON 출력에 `terminalSequence`를 설정해 OSC(운영 체제 명령) 이스케이프 시퀀스를 그대로 내보낼 수 있습니다. 훅이 반환되면 호스트가 이 시퀀스를 자신을 제어하는 터미널에 씁니다 — 따로 TTY가 없어도 데스크톱 알림, 창 제목 변경, 터미널 벨에 활용할 수 있습니다.

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| `terminalSequence` | string | 원시 이스케이프 시퀀스(보통 OSC 9 / OSC 0 / OSC 777). 호스트 터미널에 그대로 씁니다. |

예 — 오래 걸리는 작업이 끝나면 OSC 9 데스크톱 알림 보내기. ESC와 BEL은 JSON 이스케이프(`\u001b`, `\u0007`)로 쓰거나 `printf`와 `jq`로 값을 만드세요. JSON 문자열 안에 원시 제어 바이트가 들어가면 파싱에 실패합니다:

```json
{
  "terminalSequence": "\u001b]9;Task complete\u0007"
}
```

Claude가 턴을 마칠 때 알림이 가도록 `Stop` 훅에 설정하세요. 시퀀스 지원 여부는 터미널마다 다릅니다. iTerm2, Windows Terminal, WezTerm은 OSC 9를 지원하고, Kitty는 OSC 99를 씁니다.

## 환경 변수

| 변수 | 사용 가능한 곳 | 설명 |
|----------|-------------|-------------|
| `CLAUDE_PROJECT_DIR` | 모든 훅 | 프로젝트 루트의 절대 경로 |
| `CLAUDE_ENV_FILE` | SessionStart, CwdChanged, FileChanged | 환경 변수를 유지할 파일 경로 |
| `CLAUDE_CODE_REMOTE` | 모든 훅 | 원격 환경에서 실행 중이면 `"true"` |
| `${CLAUDE_PLUGIN_ROOT}` | 플러그인 훅 | 플러그인 디렉토리 경로 |
| `${CLAUDE_PLUGIN_DATA}` | 플러그인 훅 | 플러그인 데이터 디렉토리 경로 |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd 훅 | SessionEnd 훅의 시간 제한(밀리초, 기본값 재정의) |
| `CLAUDE_CODE_SESSION_ID` | Bash 도구 하위 프로세스(v2.1.132+) | 세션 UUID. 훅 입력 JSON의 `session_id` 필드와 같습니다. bash 로그와 훅 텔레메트리를 연결할 때 쓰세요. |
| `CLAUDE_EFFORT` | Bash 도구 하위 프로세스(v2.1.133+) | 현재 노력 수준(`low`/`medium`/`high`/`xhigh`/`max`). 훅 입력 JSON의 `effort.level`과 같습니다. |
| `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` | 프로세스 전체(v2.1.143+) | Claude Code가 다음 차단을 무시하고 턴을 끝내기 전까지 허용되는 Stop 훅의 최대 연속 차단 횟수(기본값 `8`). `0`이면 한도를 끕니다. |

## 프롬프트 기반 훅

`Stop`과 `SubagentStop` 이벤트에서는 LLM 기반 평가를 쓸 수 있습니다:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "모든 작업이 끝났는지 검토하고 결정을 반환하세요.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**LLM 응답 스키마:**
```json
{
  "ok": false,
  "reason": "마지막 편집 이후 테스트를 실행하지 않았음"
}
```

`ok: true`는 동작을 허용하며, `ok`가 `false`이면 `reason`이 필수입니다.

## 예제

### 예제 1: Bash 명령어 검증기(PreToolUse)

**파일:** `.claude/hooks/validate-bash.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\s+/", "Blocking dangerous rm -rf / command"),
    (r"\bsudo\s+rm", "Blocking sudo rm command"),
]

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool_input", {}).get("command", "")

    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            print(message, file=sys.stderr)
            sys.exit(2)  # 종료 코드 2 = 차단 오류

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**설정:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\""
          }
        ]
      }
    ]
  }
}
```

### 예제 2: 보안 스캐너(PostToolUse)

**파일:** `.claude/hooks/security-scan.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

SECRET_PATTERNS = [
    (r"password\s*=\s*['\"][^'\"]+['\"]", "Potential hardcoded password"),
    (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"]", "Potential hardcoded API key"),
]

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    content = tool_input.get("content", "") or tool_input.get("new_string", "")
    file_path = tool_input.get("file_path", "")

    warnings = []
    for pattern, message in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(message)

    if warnings:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Security warnings for {file_path}: " + "; ".join(warnings)
            }
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 예제 3: 코드 자동 포맷(PostToolUse)

**파일:** `.claude/hooks/format-code.sh`

```bash
#!/bin/bash

# stdin에서 JSON 읽기
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))")
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))")

if [ "$TOOL_NAME" != "Write" ] && [ "$TOOL_NAME" != "Edit" ]; then
    exit 0
fi

# 파일 확장자에 따라 포맷
case "$FILE_PATH" in
    *.js|*.jsx|*.ts|*.tsx|*.json)
        command -v prettier &>/dev/null && prettier --write "$FILE_PATH" 2>/dev/null
        ;;
    *.py)
        command -v black &>/dev/null && black "$FILE_PATH" 2>/dev/null
        ;;
    *.go)
        command -v gofmt &>/dev/null && gofmt -w "$FILE_PATH" 2>/dev/null
        ;;
esac

exit 0
```

### 예제 4: 프롬프트 검증기(UserPromptSubmit)

**파일:** `.claude/hooks/validate-prompt.py`

```python
#!/usr/bin/env python3
import json
import sys
import re

BLOCKED_PATTERNS = [
    (r"delete\s+(all\s+)?database", "Dangerous: database deletion"),
    # 한국어 요청도 막음(예: "데이터베이스를 전부 삭제해 줘")
    (r"데이터베이스\S*\s*(전부\s*|모두\s*|다\s*)?(삭제|지워|지우)", "Dangerous: database deletion"),
    (r"rm\s+-rf\s+/", "Dangerous: root deletion"),
]

def main():
    input_data = json.load(sys.stdin)
    prompt = input_data.get("prompt", "")

    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            output = {
                "decision": "block",
                "reason": f"Blocked: {message}"
            }
            print(json.dumps(output))
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 예제 5: 지능형 Stop 훅(프롬프트 기반)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Claude가 요청받은 작업을 모두 끝냈는지 검토하세요. 확인할 것: 1) 모든 파일을 만들거나 수정했는가? 2) 해결되지 않은 오류가 있는가? 끝나지 않았다면 무엇이 빠졌는지 설명하세요.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 예제 6: 컨텍스트 사용량 추적기(훅 쌍)

`UserPromptSubmit`(메시지 전)과 `Stop`(응답 후) 훅을 함께 써서 요청마다 토큰 소비량을 추적합니다.

**파일:** `.claude/hooks/context-tracker.py`

```python
#!/usr/bin/env python3
"""
컨텍스트 사용량 추적기 - 요청마다 토큰 소비량을 추적합니다.

UserPromptSubmit을 "메시지 전" 훅으로, Stop을 "응답 후" 훅으로 써서
요청마다 토큰 사용량의 차이를 계산합니다.

토큰 계산 방법:
1. 글자 수 추정(기본값): 토큰당 약 4글자, 의존성 없음
2. tiktoken(선택): 더 정확함(약 90-95%), 필요: pip install tiktoken
"""
import json
import os
import sys
import tempfile

# 설정
CONTEXT_LIMIT = 1000000  # Opus 5, Sonnet 5, Opus 4.8, Sonnet 4.6은 1M, Haiku 4.5는 200000(사용하는 모델에 맞게 조정)
USE_TIKTOKEN = False    # 더 정확하게 계산하려면 tiktoken을 설치한 뒤 True로 설정


def get_state_file(session_id: str) -> str:
    """메시지 전 토큰 수를 저장할, 세션별로 분리된 임시 파일 경로를 가져옵니다."""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens(text: str) -> int:
    """
    텍스트의 토큰 수를 셉니다.

    tiktoken이 있으면 p50k_base 인코딩을 쓰고(약 90-95% 정확도),
    없으면 글자 수 추정으로 대신합니다(약 80-90% 정확도).
    """
    if USE_TIKTOKEN:
        try:
            import tiktoken
            enc = tiktoken.get_encoding("p50k_base")
            return len(enc.encode(text))
        except ImportError:
            pass  # 추정 방식으로 대체

    # 글자 수 기반 추정: 영어는 토큰당 약 4글자
    return len(text) // 4


def read_transcript(transcript_path: str) -> str:
    """대화 기록 파일의 내용을 모두 읽어 하나로 합칩니다."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                # 여러 메시지 형식에서 텍스트 내용 추출
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)


def handle_user_prompt_submit(data: dict) -> None:
    """메시지 전 훅: 요청 전에 현재 토큰 수를 저장합니다."""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 나중에 비교하도록 임시 파일에 저장
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)


def handle_stop(data: dict) -> None:
    """응답 후 훅: 토큰 차이를 계산하고 보고합니다."""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens(transcript_content)

    # 메시지 전 토큰 수 불러오기
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # 차이 계산
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # 사용량 보고
    method = "tiktoken" if USE_TIKTOKEN else "estimated"
    print(f"Context ({method}): ~{current_tokens:,} tokens ({percentage:.1f}% used, ~{remaining:,} remaining)", file=sys.stderr)
    if delta_tokens > 0:
        print(f"This request: ~{delta_tokens:,} tokens", file=sys.stderr)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

**설정:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/context-tracker.py\""
          }
        ]
      }
    ]
  }
}
```

**동작 방식:**
1. `UserPromptSubmit`은 프롬프트가 처리되기 전에 실행되어 현재 토큰 수를 저장합니다
2. `Stop`은 Claude가 응답한 뒤 실행되어 차이를 계산하고 사용량을 보고합니다
3. 임시 파일 이름의 `session_id`로 세션마다 분리됩니다

**토큰 계산 방법:**

| 방법 | 정확도 | 의존성 | 속도 |
|--------|----------|--------------|-------|
| 글자 수 추정 | 약 80-90% | 없음 | 1ms 미만 |
| tiktoken (p50k_base) | 약 90-95% | `pip install tiktoken` | 10ms 미만 |

> **참고:** Anthropic은 공식 오프라인 토크나이저를 공개하지 않았습니다. 두 방법 모두 근삿값입니다. 대화 기록에는 사용자 프롬프트, Claude의 응답, 도구 출력이 들어 있으며, v2.1.300부터는 각 API 요청의 시스템 프롬프트, 도구, 매개변수도 기록됩니다.

### 예제 7: 자동 모드 권한 미리 채우기(일회성 설정 스크립트)

Claude Code의 자동 모드 기본 허용 범위에 해당하는 안전한 권한 규칙 — 기본 37개, 모든 분류 플래그를 켜면 최대 63개 — 을 `~/.claude/settings.json`에 미리 채워 넣는 일회성 설정 스크립트입니다. 훅을 쓰지 않으며 앞으로의 선택을 기억하지도 않습니다. 한 번만 실행하면 되고, 다시 실행해도 안전합니다(이미 있는 규칙은 건너뜀).

**파일:** `09-advanced-features/setup-auto-mode-permissions.py`

```bash
# 추가될 내용 미리 보기
python3 09-advanced-features/setup-auto-mode-permissions.py --dry-run

# 적용
python3 09-advanced-features/setup-auto-mode-permissions.py
```

**추가되는 내용:**

| 분류 | 예 |
|----------|---------|
| 기본 제공 도구 | `Read(*)`, `Grep(*)`, `Agent(*)`, `WebSearch(*)` |
| 선택적 편집(--include-edits) | `Edit(*)` |
| Git 읽기 | `Bash(git status:*)`, `Bash(git log:*)`, `Bash(git diff:*)` |
| Git 쓰기(로컬) | `Bash(git add:*)`, `Bash(git commit:*)`, `Bash(git checkout:*)` |
| 패키지 관리자 | `Bash(npm ci:*)`, `Bash(npm install:*)`, `Bash(pip install:*)`, `Bash(pip3 install:*)` |
| 빌드와 테스트 | `Bash(make:*)`, `Bash(pytest:*)`, `Bash(go test:*)` |
| 자주 쓰는 셸 명령어 | `Bash(ls:*)`, `Bash(cat:*)`, `Bash(find:*)` |
| GitHub CLI | `Bash(gh pr view:*)`, `Bash(gh pr create:*)`, `Bash(gh issue list:*)` |

**일부러 제외한 것**(이 스크립트는 절대 추가하지 않음):
- `rm -rf`, `sudo`, 강제 푸시, `git reset --hard`
- `DROP TABLE`, `kubectl delete`, `terraform destroy`
- `npm publish`, `curl | bash`, 프로덕션 배포

### 예제 8: 학습 진도 기록기(SessionEnd)

Claude Code 세션이 끝날 때마다 어떤 모듈을 공부했는지 기록합니다. 진도는
저장소 밖의 `~/.claude-howto-progress.json`에 저장되므로 `git pull`을 해도
덮어써지지 않습니다.

**왜 `Stop`이 아니라 `SessionEnd`인가요?**
`Stop`은 Claude가 응답할 *때마다* 실행됩니다. `SessionEnd`는 세션이 끝날 때
한 번만 실행되므로 — 세션 마무리 일지에 딱 맞습니다.

**왜 대화형 입력을 받지 않나요?**
훅은 제어 터미널 없이 실행되므로 `/dev/tty`를 쓸 수 없고, 훅이 사용자에게
입력을 요청할 수 없습니다. Claude Code를 실행할 때 모듈(과 선택적인 메모)을 환경 변수로 넘기세요.
예: `CLAUDE_HOWTO_MODULES=06,07 claude`

**파일:** `06-hooks/session-end.sh`

```bash
#!/usr/bin/env bash
# SessionEnd 훅: 작업한 모듈을 기록하고, 학습 진도를 계속 추적할 수 있도록
# ~/.claude-howto-progress.json에 세션 기록을 추가합니다.

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# 보호 조건: 이 저장소 안에서만 실행
if [[ "$CLAUDE_PROJECT_DIR" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

if [ ! -f "$PROGRESS_FILE" ]; then
  echo '{"sessions":[]}' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

# 작업한 모듈. 예: CLAUDE_HOWTO_MODULES=06,07 claude 로 실행
# 01=슬래시 명령어  02=메모리  03=스킬  04=서브에이전트  05=MCP
# 06=훅  07=플러그인  08=체크포인트  09=고급 기능  10=CLI
INPUT="${CLAUDE_HOWTO_MODULES:-}"

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  exit 0
fi

MODULES_JSON=$(echo "$INPUT" | tr ',' '\n' | tr -d ' ' | while read -r m; do
  case "$m" in
    01) echo '"01-slash-commands"' ;;
    02) echo '"02-memory"' ;;
    03) echo '"03-skills"' ;;
    04) echo '"04-subagents"' ;;
    05) echo '"05-mcp"' ;;
    06) echo '"06-hooks"' ;;
    07) echo '"07-plugins"' ;;
    08) echo '"08-checkpoints"' ;;
    09) echo '"09-advanced-features"' ;;
    10) echo '"10-cli"' ;;
    *)  echo "\"$m\"" ;;
  esac
done | paste -sd ',' -)

# 선택적인 메모. 예: CLAUDE_HOWTO_NOTES="pre-commit 예제를 써 봄"
NOTES="${CLAUDE_HOWTO_NOTES:-}"

# NOTES를 별도 인수로 넘겨 JSON 이스케이프를 Python이 처리하게 함 —
# 메모에 따옴표나 백슬래시가 있어도 JSON이 깨지지 않음.
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

echo " Saved to $PROGRESS_FILE"
```

**설치** — `settings.json`의 경로가 맞도록 스크립트를 프로젝트의 훅 디렉토리에 복사하세요:

```bash
mkdir -p .claude/hooks
cp 06-hooks/session-end.sh .claude/hooks/
chmod +x .claude/hooks/session-end.sh
```

**설정**(`.claude/settings.json`에서):

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-end.sh\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

SessionEnd 훅의 기본 예산은 1.5초입니다. 훅별 `"timeout"`(초)을 설정하면 최대 60초까지 그에 맞춰 예산이 늘어나며, 자체 `timeout`이 없는 훅은 1.5초 뒤에 취소됩니다.

**출력 — `~/.claude-howto-progress.json`:**

```json
{
  "sessions": [
    {
      "date": "2026-04-18",
      "time": "14:32",
      "modules": ["06-hooks", "07-plugins"],
      "notes": "첫 훅을 설치하고 pre-commit 예제를 써 봄"
    }
  ]
}
```

**보여 주는 핵심 패턴:**

| 패턴 | 중요한 이유 |
|---------|----------------|
| `SessionEnd` 이벤트 | `Stop`처럼 응답마다가 아니라 종료할 때 한 번만 실행 |
| `INPUT="${CLAUDE_HOWTO_MODULES:-}"` | 훅에는 터미널이 없으므로(`/dev/tty` 사용 불가) 입력을 환경 변수로 받음 |
| `"timeout": 10` | SessionEnd 훅은 자체 `timeout`을 설정하지 않으면 1.5초 뒤에 취소됨 |
| `$CLAUDE_PROJECT_DIR` | 이식 가능한 경로 — `/Users/yourname/...`을 하드코딩하지 않음 |
| 맨 위의 보호 조건 | 전역으로 설치해도 관계없는 프로젝트에서는 훅이 실행되지 않게 막음 |
| 저장소 밖에 저장 | `~/` 경로는 `git pull` 후에도 데이터가 덮어써지지 않음 |

**함께 쓰기: 시각적 진도 추적기**

10개 모듈 전체를 체크박스로 관리하는 UI가 필요하면, 포함된 추적기를 브라우저에서 여세요:

```bash
open local-progress/index.html
```

진도는 브라우저의 `localStorage`에 저장됩니다(저장소 안의 디스크에는 절대 쓰지 않음).
**Export**(내보내기) 버튼으로 스냅샷을 JSON으로 저장하고, **Import**(가져오기)로 복원하세요.

## 플러그인 훅

플러그인은 `hooks/hooks.json` 파일에 훅을 포함할 수 있습니다:

**파일:** `plugins/hooks/hooks.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

**플러그인 훅의 환경 변수:**
- `${CLAUDE_PLUGIN_ROOT}` - 플러그인 디렉토리 경로
- `${CLAUDE_PLUGIN_DATA}` - 플러그인 데이터 디렉토리 경로

덕분에 플러그인에 사용자 정의 검증과 자동화 훅을 넣을 수 있습니다.

## MCP 도구 훅

MCP 도구는 `mcp__<server>__<tool>` 패턴을 따릅니다:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"systemMessage\": \"Memory operation logged\"}'"
          }
        ]
      }
    ]
  }
}
```

## 보안 고려 사항

### 면책 조항

**사용에 따른 책임은 사용자에게 있습니다**: 훅은 임의의 셸 명령어를 실행합니다. 다음에 대한 책임은 전적으로 사용자에게 있습니다:
- 설정한 명령어
- 파일 접근/수정 권한
- 데이터 손실이나 시스템 손상 가능성
- 프로덕션에서 쓰기 전에 안전한 환경에서 훅 테스트

### 보안 참고 사항

- **작업 공간 신뢰 필요:** 이제 `statusLine`과 `fileSuggestion` 훅 출력 명령어는 작업 공간 신뢰를 수락해야 적용됩니다.
- **상태 표시줄의 터미널 크기 (v2.1.153):** 이제 상태 표시줄 명령어 스크립트가 `COLUMNS`와 `LINES` 환경 변수를 받으므로, 터미널의 너비/높이에 맞춰 출력을 조정할 수 있습니다(예: `[ "$COLUMNS" -lt 80 ] && short_output`).
- **HTTP 훅과 환경 변수:** HTTP 훅이 헤더 값에 환경 변수를 넣으려면 명시적인 `allowedEnvVars` 목록이 필요합니다. 민감한 환경 변수가 원격 엔드포인트로 실수로 유출되는 것을 막습니다.
- **관리형 설정 계층:** 이제 `disableAllHooks` 설정은 관리형 설정 계층을 따르므로, 조직 수준 설정으로 개인 사용자가 재정의할 수 없는 훅 비활성화를 강제할 수 있습니다.
- **PowerShell 자동 승인 (v2.1.119):** Bash와 마찬가지로 PowerShell 도구 명령어도 권한 모드에서 자동 승인될 수 있습니다. PowerShell 기반 셸 도구로 Claude Code를 쓰는 Windows 사용자도 같은 경험을 하게 됩니다.
- **Bash의 단독 환경 변수 자동 승인 허점 수정 (v2.1.145):** v2.1.145 이전에는 `FOO=bar somecommand` 형태의 Bash 명령어(허용 목록에 없는 명령어 앞에 변수 할당을 붙인 형태)가, 허용 목록에 `FOO=bar`만 있어도 자동 승인될 수 있었습니다. v2.1.145에서 이 허점이 막혀 이런 명령어는 이제 권한 프롬프트를 거칩니다. 암묵적인 허용에 기대던 스크립트는 프롬프트를 띄우기 시작하므로, 변수 할당만이 아니라 명령어 전체를 포함하는 `Bash(...)` 권한 규칙으로 명시적으로 다시 허용하세요.

### 모범 사례

| 권장 | 비권장 |
|-----|-------|
| 모든 입력을 검증하고 정제하기 | 입력 데이터를 무작정 믿기 |
| 셸 변수를 따옴표로 감싸기: `"$VAR"` | 따옴표 없이 쓰기: `$VAR` |
| 경로 탐색(`..`) 차단하기 | 임의의 경로 허용하기 |
| `$CLAUDE_PROJECT_DIR`로 절대 경로 쓰기 | 경로 하드코딩하기 |
| 민감한 파일(`.env`, `.git/`, 키) 건너뛰기 | 모든 파일 처리하기 |
| 먼저 훅을 따로 테스트하기 | 테스트하지 않은 훅 배포하기 |
| HTTP 훅에는 명시적인 `allowedEnvVars` 쓰기 | 웹훅에 모든 환경 변수 노출하기 |

## 디버깅

### 디버그 모드 켜기

자세한 훅 로그를 보려면 디버그 플래그와 함께 Claude를 실행하세요:

```bash
claude --debug
```

### 상세 모드

Claude Code에서 `Ctrl+O`를 누르면 상세 모드가 켜져 훅 실행 과정을 볼 수 있습니다.

### 훅을 독립적으로 테스트

```bash
# 샘플 JSON 입력으로 테스트
echo '{"tool_name": "Bash", "tool_input": {"command": "ls -la"}}' | python3 .claude/hooks/validate-bash.py

# 종료 코드 확인
echo $?
```

## 전체 설정 예

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh\"",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/security-scan.py\"",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-prompt.py\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-init.sh\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "멈추기 전에 모든 작업이 끝났는지 검증하세요.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 훅 실행 세부 사항

| 측면 | 동작 |
|--------|----------|
| **시간 제한** | command/http/mcp_tool은 기본 600초(prompt는 30초, agent는 60초). 훅마다 설정 가능 |
| **병렬 실행** | 일치하는 훅은 모두 병렬로 실행됩니다. v2.1.302부터는 한 이벤트의 prompt 훅이나 agent 훅이 한 번에 최대 12개까지 실행되고 나머지는 차례를 기다립니다. |
| **중복 제거** | 똑같은 훅 명령어는 중복 제거됨 |
| **환경** | Claude Code의 환경으로 현재 디렉토리에서 실행 |

## 문제 해결

### 훅이 실행되지 않을 때
- JSON 설정 문법이 올바른지 확인
- 매처 패턴이 도구 이름과 일치하는지 확인
- 스크립트가 있고 실행 가능한지 확인: `chmod +x script.sh`
- `claude --debug`를 실행해 훅 실행 로그 확인
- 훅이 (명령어 인수가 아니라) stdin에서 JSON을 읽는지 확인

### 훅이 예상치 않게 차단할 때
- 샘플 JSON으로 훅 테스트: `echo '{"tool_name": "Write", ...}' | ./hook.py`
- 종료 코드 확인: 허용이면 0, 차단이면 2여야 함
- stderr 출력 확인(종료 코드 2일 때 표시됨)

### JSON 파싱 오류
- 명령어 인수가 아니라 항상 stdin에서 읽기
- (문자열 조작이 아니라) 제대로 된 JSON 파싱 쓰기
- 없는 필드를 부드럽게 처리하기

## 설치

### 1단계: 훅 디렉토리 만들기
```bash
mkdir -p ~/.claude/hooks
```

### 2단계: 예제 훅 복사
```bash
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

### 3단계: 설정 파일에서 구성
위에서 보여 준 훅 설정으로 `~/.claude/settings.json`이나 `.claude/settings.json`을 편집하세요.

## 관련 개념

- **[체크포인트와 되감기](../08-checkpoints/)** - 대화 상태 저장과 복원
- **[슬래시 명령어](../01-slash-commands/)** - 사용자 정의 슬래시 명령어 만들기
- **[스킬](../03-skills/)** - 재사용 가능한 자율 기능
- **[서브에이전트](../04-subagents/)** - 작업 위임 실행
- **[플러그인](../07-plugins/)** - 묶음으로 제공되는 확장 패키지
- **[고급 기능](../09-advanced-features/)** - Claude Code의 고급 기능 살펴보기

## 추가 자료

- **[공식 훅 문서](https://code.claude.com/docs/ko/hooks)** - 훅 전체 레퍼런스
- **[CLI 레퍼런스](https://code.claude.com/docs/ko/cli-reference)** - 명령줄 인터페이스 문서
- **[메모리 가이드](../02-memory/)** - 지속 컨텍스트 설정

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/hooks
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/ko/sub-agents
- https://code.claude.com/docs/ko/permissions
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
- https://code.claude.com/docs/en/plugins/manifest-reference#quoting-and-path-separators
- https://github.com/anthropics/claude-code/releases/tag/v2.1.295
- https://code.claude.com/docs/ko/hooks#pretooluse
- https://code.claude.com/docs/ko/hooks#pretooluse-decision-control
- https://code.claude.com/docs/ko/hooks#hook-lifecycle
- https://code.claude.com/docs/ko/hooks#userpromptsubmit-input
- https://code.claude.com/docs/en/changelog#2-1-299
- https://code.claude.com/docs/en/changelog#2-1-300
- https://code.claude.com/docs/en/changelog#2-1-301
- https://code.claude.com/docs/en/changelog#2-1-302
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
