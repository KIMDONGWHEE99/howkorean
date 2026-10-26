<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# MCP (Model Context Protocol)

이 폴더에는 Claude Code에서 MCP 서버를 설정하고 사용하는 방법에 대한 종합 문서와 예제가 들어 있습니다.

## 개요

MCP(Model Context Protocol)는 Claude가 외부 도구, API, 실시간 데이터 소스에 접근하는 표준 방식입니다. 메모리와 달리 MCP는 바뀌는 데이터에 실시간으로 접근하게 해 줍니다.

주요 특징:
- 외부 서비스에 실시간 접근
- 실시간 데이터 동기화
- 확장 가능한 아키텍처
- 안전한 인증
- 도구 기반 상호작용

## MCP 아키텍처

```mermaid
graph TB
    A["Claude"]
    B["MCP 서버"]
    C["외부 서비스"]

    A -->|요청: list_issues| B
    B -->|쿼리| C
    C -->|데이터| B
    B -->|응답| A

    A -->|요청: create_issue| B
    B -->|작업| C
    C -->|결과| B
    B -->|응답| A

    style A fill:#e1f5fe,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
    style C fill:#e8f5e9,stroke:#333,color:#333
```

## MCP 생태계

```mermaid
graph TB
    A["Claude"] -->|MCP| B["Filesystem<br/>MCP 서버"]
    A -->|MCP| C["GitHub<br/>MCP 서버"]
    A -->|MCP| D["Database<br/>MCP 서버"]
    A -->|MCP| E["Slack<br/>MCP 서버"]
    A -->|MCP| F["Google Docs<br/>MCP 서버"]

    B -->|파일 I/O| G["로컬 파일"]
    C -->|API| H["GitHub 저장소"]
    D -->|쿼리| I["PostgreSQL/MySQL"]
    E -->|메시지| J["Slack 워크스페이스"]
    F -->|문서| K["Google Drive"]

    style A fill:#e1f5fe,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
    style C fill:#f3e5f5,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#f3e5f5,stroke:#333,color:#333
    style F fill:#f3e5f5,stroke:#333,color:#333
    style G fill:#e8f5e9,stroke:#333,color:#333
    style H fill:#e8f5e9,stroke:#333,color:#333
    style I fill:#e8f5e9,stroke:#333,color:#333
    style J fill:#e8f5e9,stroke:#333,color:#333
    style K fill:#e8f5e9,stroke:#333,color:#333
```

## MCP 설치 방법

Claude Code는 MCP 서버 연결에 여러 전송 프로토콜을 지원합니다:

### HTTP 전송(권장)

```bash
# 기본 HTTP 연결
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 인증 헤더를 붙인 HTTP 연결
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Stdio 전송(로컬)

로컬에서 실행하는 MCP 서버용입니다:

```bash
# 로컬 Node.js 서버
claude mcp add --transport stdio myserver -- npx @myorg/mcp-server

# 환경 변수와 함께
claude mcp add --transport stdio myserver --env KEY=value -- npx server
```

#### stdio 서버용 `CLAUDE_PROJECT_DIR` (v2.1.139+)

모든 MCP stdio 서버는 환경에 `CLAUDE_PROJECT_DIR=<저장소 루트의 절대 경로>`가 이미 설정된 상태로 실행됩니다 — 훅과 같은 규칙입니다. 플러그인과 프로젝트의 `.mcp.json` 파일은 `command`, `args`, `env` 값에서 `${CLAUDE_PROJECT_DIR}`를 참조할 수 있으며, 치환은 `execve()` 전에 일어납니다:

```json
{
  "mcpServers": {
    "repo-tools": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/.claude/mcp/repo-tools.js"],
      "env": {
        "REPO_ROOT": "${CLAUDE_PROJECT_DIR:-.}"
      }
    }
  }
}
```

> **참고**: 프로젝트, 로컬, 사용자 설정에서는 기본값을 넣어 `${CLAUDE_PROJECT_DIR:-.}`로 쓰세요: 이 변수는 Claude Code 자체가 아니라 서버의 환경에 설정되기 때문입니다. `${CLAUDE_PROJECT_DIR}`를 직접 치환하는 것은 플러그인 MCP 설정뿐입니다.

Claude Code를 어디에서 실행했는지와 관계없이 stdio 서버가 프로젝트 루트 기준으로 파일을 읽어야 할 때 쓰세요.

stdio MCP 서버는 `CLAUDE_CODE_SESSION_ID`(훅과 Bash에 전달되는 값과 같음)도 받으며, `--resume`으로 세션을 재개할 때도 마찬가지입니다(v2.1.163+).

### SSE 전송(지원 중단)

Server-Sent Events 전송은 `http`로 대체되어 지원 중단되었지만 아직 쓸 수 있습니다:

```bash
claude mcp add --transport sse legacy-server https://example.com/sse
```

### WebSocket 전송(`ws`)

WebSocket 서버는 지속적인 양방향 연결을 유지하므로, 요청하지 않아도 Claude에게 이벤트를 보내는 원격 MCP 서버에 적합합니다. 서버가 요청에 응답만 한다면 HTTP를 쓰세요. HTTP는 OAuth와 `claude mcp add --transport` 플래그를 지원하지만 WebSocket은 둘 다 지원하지 않습니다.

`--transport`는 `ws`를 받지 않으므로 `.mcp.json`이나 `claude mcp add-json`으로 설정하세요:

```json
{
  "type": "ws",
  "url": "wss://mcp.example.com/socket",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  }
}
```

`type: "ws"` 항목은 `http`와 같은 `url`, `headers`, `headersHelper`, `timeout`, `alwaysLoad` 필드를 받습니다. 인증은 **헤더로만** 할 수 있습니다 — WebSocket 서버에는 OAuth 흐름이 없습니다.

> **참고**: v2.1.285부터 `claude mcp list`가 WebSocket(`ws`) 서버도 URL, 상태와 함께 나열합니다(이전 버전에서는 빠져 있었음). `claude mcp get <name>`이나 `/mcp` 패널로도 확인할 수 있습니다.

HTTP, SSE와 마찬가지로 WebSocket 연결도 5분 유휴 시간을 쓰며, stdio와 WebSocket에는 요청별 타이머가 없습니다. `type` 없이 `url`만 있는 항목은 오류가 나며, 오류 메시지에 유효한 값으로 `"http"`, `"sse"`, `"ws"`가 표시됩니다.

### 세션 작업 디렉토리(roots/list)

MCP 서버는 세션의 작업 디렉토리를 알아낼 수 있습니다: 실행한 디렉토리와 모든 `--add-dir`/`additionalDirectories` 항목이 MCP `roots/list` 요청으로 반환되며, 그 목록이 바뀔 때마다 `notifications/roots/list_changed` 알림이 전송됩니다(v2.1.203). 유휴 시간 제한은 이제 stdio 서버에도 적용되며(30분), 서버별 `timeout`이 유휴 시간의 최솟값 역할을 합니다(v2.1.203).

### Windows 참고 사항

(WSL이 아닌) 네이티브 Windows에서는 npx 명령어에 `cmd /c`를 쓰세요:

```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### OAuth 2.0 인증

Claude Code는 OAuth 2.0이 필요한 MCP 서버를 지원합니다. OAuth를 쓰는 서버에 연결하면 Claude Code가 인증 흐름 전체를 처리합니다:

```bash
# OAuth를 쓰는 MCP 서버에 연결(대화형 흐름)
claude mcp add --transport http my-service https://my-service.example.com/mcp

# 비대화형 설정을 위해 OAuth 자격 증명을 미리 구성
claude mcp add --transport http my-service https://my-service.example.com/mcp \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --callback-port 8080
```

| 기능 | 설명 |
|---------|-------------|
| **대화형 OAuth** | `/mcp`로 브라우저 기반 OAuth 흐름 시작 |
| **미리 구성된 OAuth 클라이언트** | Notion, Stripe 등 자주 쓰는 서비스용 기본 제공 OAuth 클라이언트(v2.1.30+) |
| **미리 구성된 자격 증명** | 자동 설정을 위한 `--client-id`, `--client-secret`, `--callback-port` 플래그 |
| **토큰 저장** | 토큰은 시스템 키체인에 안전하게 저장됨 |
| **단계적 인증(step-up)** | 권한이 필요한 작업에 대한 단계적 인증 지원 |
| **발견 정보 캐싱** | 더 빨리 다시 연결할 수 있도록 OAuth 발견 메타데이터를 캐싱 |
| **메타데이터 재정의** | `.mcp.json`의 `oauth.authServerMetadataUrl`로 기본 OAuth 메타데이터 발견을 재정의 |

#### OAuth 메타데이터 발견 재정의

MCP 서버가 표준 OAuth 메타데이터 엔드포인트(`/.well-known/oauth-authorization-server`)에서는 오류를 내지만 동작하는 OIDC 엔드포인트를 제공한다면, 특정 URL에서 OAuth 메타데이터를 가져오도록 Claude Code에 알려 줄 수 있습니다. 서버 설정의 `oauth` 객체에 `authServerMetadataUrl`을 설정하세요:

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL은 `https://`를 써야 합니다. 이 옵션에는 Claude Code v2.1.64 이상이 필요합니다.

#### 시작 시 인증 알림과 동적 헤더 새로 고침 (v2.1.193)

- **시작 시 인증 알림 (v2.1.193+)**: Claude Code는 시작할 때 아직 인증이 필요한 MCP 서버 목록을 알림으로 보여 주므로, 로그인이 필요한 서버가 말없이 동작하지 않는 채로 남지 않습니다.
- **`headersHelper` 자동 새로 고침 (v2.1.193+)**: `headersHelper`로 사용자 정의 인증을 제공하면, 서버가 HTTP 401이나 403을 반환할 때 헬퍼가 자동으로 다시 호출됩니다. 직접 다시 연결하지 않아도 자격 증명이 즉시 갱신됩니다. [사용자 정의 인증에 동적 헤더 사용하기](https://code.claude.com/docs/ko/mcp)를 참고하세요.

> **경고** (v2.1.238): 이제 프로젝트 `.mcp.json`의 `headersHelper`와, 프로젝트나 `--add-dir` 에이전트 파일의 인라인 MCP 서버는 해당 폴더의 신뢰 대화 상자를 수락해야만 동작합니다 — `claude -p`에서도 마찬가지입니다. 이런 헬퍼는 또한 **상속된 자격 증명 환경 변수 없이** 실행되며, 사용자, 관리형, claude.ai 범위의 헬퍼는 대신 Claude 설정 디렉토리에서 실행됩니다. 상속된 자격 증명에 기대거나 신뢰하지 않은 상태로 실행되던 프로젝트 설정은 신뢰 대화 상자를 수락하고 다른 방법으로 자격 증명을 제공할 때까지 동작하지 않습니다.

### Claude.ai MCP 커넥터

Claude.ai 계정에 설정한 MCP 서버는 Claude Code에서 자동으로 쓸 수 있습니다. 즉 Claude.ai 웹 인터페이스에서 설정한 MCP 연결은 추가 설정 없이 바로 쓸 수 있습니다.

Claude.ai MCP 커넥터는 `--print` 모드(v2.1.83+)에서도 쓸 수 있어 비대화형 사용과 스크립트 사용이 가능합니다.

> **시작 참고 (v2.1.117+):** 로컬 MCP 서버와 claude.ai MCP 서버가 모두 설정되어 있으면 이제 동시에 연결하는 것이 기본값이므로(이전에는 순차 연결), 서버를 여러 개 쓸 때 시작 지연 시간이 줄어듭니다.

Claude Code에서 Claude.ai MCP 서버를 끄려면 `ENABLE_CLAUDEAI_MCP_SERVERS` 환경 변수를 `false`로 설정하세요:

```bash
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

> **참고:** 이 기능은 Claude.ai 계정으로 로그인한 사용자만 쓸 수 있습니다.

## MCP 설정 과정

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Claude as Claude Code
    participant Config as 설정 파일
    participant Service as 외부 서비스

    User->>Claude: /mcp 입력
    Claude->>Claude: 사용 가능한 MCP 서버 나열
    Claude->>User: 옵션 표시
    User->>Claude: GitHub MCP 선택
    Claude->>Config: 설정 갱신
    Config->>Claude: 연결 활성화
    Claude->>Service: 연결 테스트
    Service-->>Claude: 인증 성공
    Claude->>User: ✅ MCP 연결됨!
```

### `/mcp` 명령어

세션 안에서 `/mcp`를 입력하면 연결된 서버 목록을 보고, OAuth 흐름을 시작하고, 연결 상태를 확인할 수 있습니다.

- **v2.1.121**부터 MCP는 일시적인 오류가 나면 첫 연결을 최대 3번까지 다시 시도합니다.
- **v2.1.128**부터 `/mcp`는 연결된 서버마다 **도구 수**를 표시하고, **도구가 0개**라고 보고하는 서버를 눈에 띄게 표시하므로 잘못 설정된 서버를 한눈에 알아볼 수 있습니다.

## MCP 도구 검색

도구 검색은 기본으로 켜져 있습니다: MCP 도구는 지연 로딩되어 필요할 때 발견되므로, 도구 정의가 모델 컨텍스트를 채우지 않습니다. `ANTHROPIC_BASE_URL`이 Anthropic 공식이 아닌 호스트를 가리키면 Claude Code가 이 기능을 끕니다. 대부분의 프록시가 이 기능에 필요한 블록을 전달하지 않기 때문입니다.

| 설정 | 값 | 설명 |
|---------|-------|-------------|
| `ENABLE_TOOL_SEARCH` | (설정 안 함 — 기본값) | 모든 MCP 도구를 지연 로딩하고 필요할 때 로드 |
| `ENABLE_TOOL_SEARCH` | `auto` | 임계값 모드: 도구 정의가 컨텍스트 윈도우의 10%에 이를 때까지는 미리 로드하고, 그 뒤로는 모두 지연 로딩 |
| `ENABLE_TOOL_SEARCH` | `auto:<N>` | 비율을 지정하는 임계값 모드(0-100) — 예: 5%면 `auto:5` |
| `ENABLE_TOOL_SEARCH` | `true` | 모든 MCP 도구를 지연 로딩 |
| `ENABLE_TOOL_SEARCH` | `false` | 꺼짐. 모든 도구 설명을 전체 전송 |

> **참고:** 도구 검색에는 `tool_reference` 블록을 지원하는 모델이 필요합니다: Claude Opus 4, Claude Sonnet 4, Claude Haiku 4.5와 이후 모델(Google Cloud의 Agent Platform에서는 Opus 4.5, Sonnet 4.5, Haiku 4.5와 이후 모델).

### 서버별로 도구 검색 건너뛰기 (v2.1.121+)

특정 MCP 서버의 도구가 매 턴 필요하다면, 그 서버 설정에
`"alwaysLoad": true`를 표시해 도구 검색의 지연 로딩을 건너뛰고
도구를 항상 쓸 수 있게 하세요:

```json
{
  "mcpServers": {
    "always-on-tool": {
      "command": "node",
      "args": ["./tools/always.js"],
      "alwaysLoad": true
    }
  }
}
```

아껴서 쓰세요 — 항상 로드되는 도구는 그만큼 컨텍스트를 차지하며,
그 컨텍스트는 도구 검색으로 더 관련 있는 도구를 찾는 데 쓸 수도 있습니다.

서버의 모든 도구를 도구 검색 뒤에 두려면 그 서버 항목에
`"alwaysLoad": false`를 설정하세요(v2.1.287+). 서버 작성자가 미리 로드하도록
표시한 도구도 여기에 포함됩니다. `alwaysLoad`를 생략하면 그렇게 표시된 도구는
미리 로드됩니다. 서버 작성자는 도구의 `_meta` 객체에 `"anthropic/alwaysLoad"`를
설정해 개별 도구를 표시하며, 사용자 설정의 서버 수준 `alwaysLoad` 설정이
이를 재정의할 수 있습니다.

## 동적 도구 업데이트

Claude Code는 MCP `list_changed` 알림을 지원합니다. MCP 서버가 제공하는 도구를 동적으로 추가, 제거, 수정하면 Claude Code가 업데이트를 받아 도구 목록을 자동으로 조정합니다 -- 다시 연결하거나 다시 시작할 필요가 없습니다.

## MCP Apps

MCP Apps는 최초의 공식 MCP 확장으로, MCP 도구 호출이 채팅 인터페이스 안에서 바로 렌더링되는 대화형 UI 구성 요소를 반환할 수 있게 합니다. MCP 서버는 일반 텍스트 응답 대신 풍부한 대시보드, 양식, 데이터 시각화, 여러 단계의 워크플로우를 제공할 수 있으며 -- 모두 대화를 벗어나지 않고 인라인으로 표시됩니다.

## MCP 입력 요청(Elicitation)

MCP 서버는 대화형 대화 상자로 사용자에게 구조화된 입력을 요청할 수 있습니다(v2.1.49+). 덕분에 MCP 서버가 워크플로우 도중에 추가 정보를 물을 수 있습니다 -- 예를 들어 확인을 요청하거나, 옵션 목록에서 고르게 하거나, 필수 항목을 채우게 하는 식으로 -- MCP 서버와의 상호작용에 대화형 요소를 더합니다.

## 도구 설명과 지침 길이 한도

Claude Code는 장황한 서버가 컨텍스트를 부풀리지 않도록 각 MCP 도구 설명과 각 서버의 지침을 잘라 냅니다. 기본 한도는 서버 지침과 미리 로드되는 도구의 설명이 **4,096자**(v2.1.296. 그 전에는 v2.1.84부터 2,048자), Claude가 도구 검색으로 로드하는 설명이 **16,384자**입니다(v2.1.295). v2.1.280부터 `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH`로 이 한도를 재정의할 수 있으며, 설정한 값이 **두** 한도를 모두 대체합니다(`8192`는 짧은 쪽을 늘리고 긴 쪽을 줄임). v2.1.299부터 `api.anthropic.com`에 있는 Anthropic 공식 MCP 서버의 설명과 지침은 잘리지 않고 그대로 Claude에게 전달됩니다. 중요한 내용은 설명의 앞부분에 두세요.

## 슬래시 명령어로 쓰는 MCP 프롬프트

MCP 서버는 Claude Code에서 슬래시 명령어로 나타나는 프롬프트를 제공할 수 있습니다. 프롬프트는 다음 이름 규칙으로 호출합니다:

```
/mcp__<server>__<prompt>
```

예를 들어 `github`라는 서버가 `review`라는 프롬프트를 제공하면 `/mcp__github__review`로 호출할 수 있습니다.

## 서버 중복 제거

같은 MCP 서버가 여러 범위(로컬, 프로젝트, 사용자)에 정의되어 있으면 로컬 설정이 우선합니다. 덕분에 프로젝트 수준이나 사용자 수준의 MCP 설정을 충돌 없이 로컬 설정으로 재정의할 수 있습니다.

## 최근 수명 주기 수정 (v2.1.136)

오래된 MCP 수명 주기 버그 두 가지가 v2.1.136에서 고쳐졌습니다 — 서버를 여러 개 쓴다면 업그레이드할 만합니다:

- **`/clear` 후에도 MCP 서버 유지**: `.mcp.json`, 플러그인, claude.ai 커넥터로 설정한 서버가 VS Code, JetBrains, Agent SDK에서 `/clear` 후에 더 이상 사라지지 않습니다. 이전 버전에서는 아무 알림 없이 사라져 다시 시작해야 했습니다.
- **OAuth 리프레시 토큰의 동시 갱신 문제 수정**: 여러 서버가 동시에 토큰을 갱신하려고 경쟁해도 더 이상 리프레시 토큰을 잃지 않습니다. OAuth로 보호되는 MCP 서버를 여러 개 쓰는 환경에서 겪던 "매일 아침 다시 인증해야 하는" 문제가 사라졌습니다.

## @ 멘션으로 MCP 리소스 참조

`@` 멘션 문법을 쓰면 프롬프트에서 MCP 리소스를 바로 참조할 수 있습니다:

```
@server-name:protocol://resource/path
```

예를 들어 특정 데이터베이스 리소스를 참조하려면:

```
@database:postgres://mydb/users
```

이렇게 하면 Claude가 MCP 리소스 내용을 가져와 대화 컨텍스트의 일부로 인라인에 포함합니다.

## MCP 범위

MCP 설정은 공유 수준이 다른 여러 범위에 저장할 수 있습니다:

| 범위 | 플래그 | 위치 | 설명 | 공유 대상 | 승인 필요 |
|-------|------|----------|-------------|-------------|------------------|
| **로컬**(기본값) | `--scope local` | `~/.claude.json`(프로젝트 경로 아래) | 현재 사용자의 현재 프로젝트에서만 사용(이전 버전에서는 `project`라고 부름) | 본인만 | 아니요 |
| **프로젝트** | `--scope project` | `.mcp.json` | git 저장소에 커밋 | 팀원 | 예(처음 사용할 때) |
| **사용자** | `--scope user` | `~/.claude.json` | 모든 프로젝트에서 사용 가능(이전 버전에서는 `global`이라고 부름) | 본인만 | 아니요 |

서버를 추가할 때 `--scope`(줄여서 `-s`)로 범위를 고르세요. 생략하면
Claude Code는 `local`을 씁니다:

```bash
# 프로젝트 범위 — 팀이 공유하도록 .mcp.json에 기록
claude mcp add --scope project --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# 사용자 범위 — 모든 프로젝트에서 사용 가능
claude mcp add --scope user --transport stdio memory -- npx @modelcontextprotocol/server-memory
```

### 프로젝트 범위 사용

프로젝트별 MCP 설정은 `.mcp.json`에 저장합니다:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

팀원은 프로젝트 MCP를 처음 쓸 때 승인 프롬프트를 보게 됩니다. 신뢰하지 않은 작업 공간에서는 저장소가 커밋된 `.claude/settings.json`으로 스스로 승인해 둔 서버를 `claude mcp list`/`get`이 자동으로 실행하지 **않습니다** — 신뢰 대화 상자를 수락하기 전까지는 `⏸ Pending approval`(승인 대기)로 표시되며, 신뢰하지 않은 폴더에서는 `enableAllProjectMcpServers`가 무시됩니다(v2.1.196).

## MCP 설정 관리

### MCP 서버 추가

```bash
# HTTP 기반 서버 추가
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# 로컬 stdio 서버 추가
claude mcp add --transport stdio database -- npx @company/db-server

# 모든 MCP 서버 나열
claude mcp list

# 특정 서버의 상세 정보 확인
claude mcp get github

# MCP 서버 제거
claude mcp remove github

# 프로젝트별 승인 선택 초기화
claude mcp reset-project-choices

# CLI에서 MCP 서버 인증(v2.1.186+)
claude mcp login github

# MCP 서버에서 로그아웃(v2.1.186+)
claude mcp logout github

# Claude Desktop에서 가져오기
claude mcp add-from-claude-desktop

# JSON 문자열로 서버 추가(스크립트로 설정할 때 유용)
claude mcp add-json events-server '{"type":"stdio","command":"npx","args":["@modelcontextprotocol/server-events"]}'
```

> **참고**: JSON 설정 — `.mcp.json`, `~/.claude.json`, `claude mcp add-json` — 에서는 `type` 필드에 `http`의 별칭으로 `streamable-http`를 쓸 수 있습니다. MCP 명세에서는 이 전송 방식을 `streamable-http`라고 부르므로, 서버 문서에서 복사한 설정을 그대로 쓸 수 있습니다.

v2.1.238부터 `claude mcp list`와 `claude mcp get`은 꺼진 서버를 상태 확인을 위해 연결하지 않고 `⊘ Disabled`(꺼짐)로 표시합니다.

`claude mcp login <name>` / `claude mcp logout <name>`은 `/mcp` 메뉴의 OAuth 흐름을 비대화형으로 하는 방법입니다 — 메뉴를 열지 않고 인증하거나 로그아웃할 수 있습니다. SSH나 헤드리스 세션에서 OAuth를 마치려면 `login`에 `--no-browser`를 붙이세요(흐름을 stdin으로 돌려받음).

## 사용 가능한 MCP 서버 표

| MCP 서버 | 목적 | 주요 도구 | 인증 | 실시간 |
|------------|---------|--------------|------|-----------|
| **Filesystem** | 파일 작업 | read, write, delete | OS 권한 | ✅ 예 |
| **GitHub** | 저장소 관리 | list_prs, create_issue, push | OAuth | ✅ 예 |
| **Slack** | 팀 커뮤니케이션 | send_message, list_channels | 토큰 | ✅ 예 |
| **Database** | SQL 쿼리 | query, insert, update | 자격 증명 | ✅ 예 |
| **Google Docs** | 문서 접근 | read, write, share | OAuth | ✅ 예 |
| **Asana** | 프로젝트 관리 | create_task, update_status | API 키 | ✅ 예 |
| **Stripe** | 결제 데이터 | list_charges, create_invoice | API 키 | ✅ 예 |
| **Memory** | 지속 메모리 | store, retrieve, delete | 로컬 | ❌ 아니요 |

## 실전 예제

### 예제 1: GitHub MCP 설정

**파일:** `.mcp.json`(프로젝트 루트)

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

**사용 가능한 GitHub MCP 도구:**

#### 풀 리퀘스트 관리
- `list_prs` - 저장소의 모든 PR 나열
- `get_pr` - diff를 포함한 PR 상세 정보 가져오기
- `create_pr` - 새 PR 만들기
- `update_pr` - PR 설명/제목 수정
- `merge_pr` - PR을 main 브랜치에 병합
- `review_pr` - 리뷰 댓글 추가

**요청 예:**
```
/mcp__github__get_pr 456

# 반환 결과:
Title: Add dark mode support
Author: @alice
Description: Implements dark theme using CSS variables
Status: OPEN
Reviewers: @bob, @charlie
```

#### 이슈 관리
- `list_issues` - 모든 이슈 나열
- `get_issue` - 이슈 상세 정보 가져오기
- `create_issue` - 새 이슈 만들기
- `close_issue` - 이슈 닫기
- `add_comment` - 이슈에 댓글 추가

#### 저장소 정보
- `get_repo_info` - 저장소 상세 정보
- `list_files` - 파일 트리 구조
- `get_file_content` - 파일 내용 읽기
- `search_code` - 코드베이스 전체 검색

#### 커밋 작업
- `list_commits` - 커밋 기록
- `get_commit` - 특정 커밋 상세 정보
- `create_commit` - 새 커밋 만들기

**설정**:
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token"
# 또는 CLI로 바로 추가:
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

### 설정의 환경 변수 확장

MCP 설정은 대체 기본값을 지원하는 환경 변수 확장을 지원합니다. `${VAR}`와 `${VAR:-default}` 문법은 `command`, `args`, `env`, `url`, `headers` 필드에서 동작합니다.

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}",
        "X-Custom-Header": "${CUSTOM_HEADER:-default-value}"
      }
    },
    "local-server": {
      "command": "${MCP_BIN_PATH:-npx}",
      "args": ["${MCP_PACKAGE:-@company/mcp-server}"],
      "env": {
        "DB_URL": "${DATABASE_URL:-postgresql://localhost/dev}"
      }
    }
  }
}
```

변수는 실행 시점에 확장됩니다:
- `${VAR}` - 환경 변수를 사용합니다. 설정되어 있지 않고 기본값도 없으면 서버는 `${VAR}` 문자열 그대로 로드되며, `claude mcp list`와 `/mcp`가 빠진 변수에 대해 경고합니다
- `${VAR:-default}` - 환경 변수를 사용하고, 설정되어 있지 않으면 기본값을 씁니다

### 예제 2: 데이터베이스 MCP 설정

**설정:**

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"]
    }
  }
}
```

**사용 예:**

```markdown
사용자: 주문이 10건 넘는 사용자를 모두 가져와 줘

Claude: 데이터베이스를 조회해 해당 정보를 찾아보겠습니다.

# MCP 데이터베이스 도구 사용:
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
HAVING COUNT(o.id) > 10
ORDER BY order_count DESC;

# 결과:
- Alice: 주문 15건
- Bob: 주문 12건
- Charlie: 주문 11건
```

**설정**:
```bash
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
claude mcp add --transport stdio database -- npx -y @bytebase/dbhub \
  --dsn "$DATABASE_URL"
```

> **경고**: 이 설정은 Claude에게 쓰기 권한을 줍니다. DBHub의 `execute_sql` 도구는 읽기 전용 모드를 켜지 않는 한 `UPDATE`, `DELETE`, `DROP`을 포함해 받은 SQL을 모두 실행합니다. 프로덕션이 아니라 로컬 데이터베이스나 버려도 되는 데이터베이스를 쓰세요.

**읽기 전용 설정(권장):**

`SELECT`만 실행할 수 있는 데이터베이스 사용자를 만드세요(PostgreSQL 예):

```sql
CREATE ROLE claude_readonly LOGIN PASSWORD 'change-me';
GRANT CONNECT ON DATABASE mydb TO claude_readonly;
GRANT USAGE ON SCHEMA public TO claude_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_readonly;
```

`dbhub.toml`에서 읽기 전용 모드를 켜세요. 예전의 `--readonly` 플래그는 더 이상 동작하지 않습니다. DBHub가 환경에서 `${DATABASE_URL}`을 채우므로 파일에 자격 증명을 넣지 않아도 됩니다:

```toml
[[sources]]
id = "default"
dsn = "${DATABASE_URL}"

[[tools]]
name = "execute_sql"
source = "default"
readonly = true
```

그런 다음 `--dsn` 대신 이 파일을 DBHub에 지정하세요. Claude Code는 이름이 같은 서버를 두 번 추가하지 않으므로, 먼저 위에서 추가한 쓰기 권한 `database` 서버를 제거하세요:

```bash
# 위에서 추가한 쓰기 권한 서버를 교체
claude mcp remove database
export DATABASE_URL="postgresql://claude_readonly:change-me@localhost/mydb"
claude mcp add --transport stdio database -- npx -y @bytebase/dbhub \
  --config "$PWD/dbhub.toml"
```

읽기 전용 모드는 SQL 텍스트를 걸러 내는 방식이라 과거에 우회 방법이 있었습니다(DBHub 0.22.6에서 수정). 따라서 데이터를 실제로 보호하는 것은 `SELECT` 전용 사용자입니다. [DBHub 읽기 전용 모드](https://dbhub.ai/tools/execute-sql#read-only-mode)를 참고하세요.

### 예제 3: 여러 MCP를 쓰는 워크플로우

**시나리오: 일일 보고서 생성**

```markdown
# 여러 MCP를 쓰는 일일 보고서 워크플로우

## 준비
1. GitHub MCP - PR 지표 가져오기
2. Database MCP - 매출 데이터 조회
3. Slack MCP - 보고서 게시
4. Filesystem MCP - 보고서 저장

## 워크플로우

### 1단계: GitHub 데이터 가져오기
/mcp__github__list_prs completed:true last:7days

출력:
- 전체 PR: 42개
- 평균 병합 시간: 2.3시간
- 리뷰 응답 시간: 1.1시간

### 2단계: 데이터베이스 조회
SELECT COUNT(*) as sales, SUM(amount) as revenue
FROM orders
WHERE created_at > NOW() - INTERVAL '1 day'

출력:
- 판매: 247건
- 매출: $12,450

### 3단계: 보고서 생성
데이터를 HTML 보고서로 합치기

### 4단계: 파일 시스템에 저장
report.html을 /reports/에 쓰기

### 5단계: Slack에 게시
#daily-reports 채널에 요약 보내기

최종 출력:
✅ 보고서 생성 및 게시 완료
📊 이번 주 병합된 PR 47개
💰 일일 매출 $12,450
```

**설정**:
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_BOT_TOKEN="your_slack_bot_token"
export SLACK_TEAM_ID="your_slack_team_id"
# 각 MCP 서버는 CLI로 추가하거나 .mcp.json에서 설정
```

### 예제 4: 파일 시스템 MCP 작업

**설정:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/home/user/projects"]
    }
  }
}
```

**사용 가능한 작업:**

| 작업 | 명령어 | 목적 |
|-----------|---------|---------|
| 파일 목록 | `ls ~/projects` | 디렉토리 내용 표시 |
| 파일 읽기 | `cat src/main.ts` | 파일 내용 읽기 |
| 파일 쓰기 | `create docs/api.md` | 새 파일 만들기 |
| 파일 편집 | `edit src/app.ts` | 파일 수정 |
| 검색 | `grep "async function"` | 파일 안에서 검색 |
| 삭제 | `rm old-file.js` | 파일 삭제 |

**설정**:
```bash
# CLI로 바로 추가:
claude mcp add --transport stdio filesystem -- npx @modelcontextprotocol/server-filesystem /home/user/projects
```

## MCP와 메모리: 결정 매트릭스

```mermaid
graph TD
    A["외부 데이터가 필요한가?"]
    A -->|아니요| B["메모리 사용"]
    A -->|예| C["자주 바뀌는가?"]
    C -->|아니요/드물게| B
    C -->|예/자주| D["MCP 사용"]

    B -->|저장| E["선호 설정<br/>컨텍스트<br/>기록"]
    D -->|접근| F["실시간 API<br/>데이터베이스<br/>서비스"]

    style A fill:#fff3e0,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#fff3e0,stroke:#333,color:#333
    style D fill:#f3e5f5,stroke:#333,color:#333
    style E fill:#e8f5e9,stroke:#333,color:#333
    style F fill:#e8f5e9,stroke:#333,color:#333
```

## 요청/응답 패턴

```mermaid
sequenceDiagram
    participant App as Claude
    participant MCP as MCP 서버
    participant DB as 데이터베이스

    App->>MCP: 요청: "SELECT * FROM users WHERE id=1"
    MCP->>DB: 쿼리 실행
    DB-->>MCP: 결과 집합
    MCP-->>App: 파싱한 데이터 반환
    App->>App: 결과 처리
    App->>App: 작업 계속

    Note over MCP,DB: 실시간 접근<br/>캐싱 없음
```

## 환경 변수

민감한 자격 증명은 환경 변수에 저장하세요:

```bash
# ~/.bashrc 또는 ~/.zshrc
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_xxxxxxxxxxxxx"
export DATABASE_URL="postgresql://user:pass@localhost/mydb"
export SLACK_BOT_TOKEN="your-slack-bot-token"
export SLACK_TEAM_ID="T0000000000"
```

그런 다음 MCP 설정에서 참조하세요:

```json
{
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
  }
}
```

## MCP 서버로 쓰는 Claude (`claude mcp serve`)

Claude Code 자체도 다른 애플리케이션을 위한 MCP 서버로 동작할 수 있습니다. 덕분에 외부 도구, 편집기, 자동화 시스템이 표준 MCP 프로토콜로 Claude의 기능을 활용할 수 있습니다.

```bash
# stdio로 동작하는 MCP 서버로 Claude Code 시작
claude mcp serve
```

그러면 다른 애플리케이션은 일반 stdio 기반 MCP 서버처럼 이 서버에 연결할 수 있습니다. 예를 들어 다른 Claude Code 인스턴스에 Claude Code를 MCP 서버로 추가하려면:

```bash
claude mcp add --transport stdio claude-agent -- claude mcp serve
```

한 Claude 인스턴스가 다른 인스턴스를 조율하는 멀티 에이전트 워크플로우를 만들 때 유용합니다.

## 관리형 MCP 설정(엔터프라이즈)

엔터프라이즈 배포에서는 IT 관리자가 두 가지 메커니즘으로 MCP 서버 정책을 강제합니다: 고정된 서버 목록을 배타적으로 배포하는 `managed-mcp.json` 파일, 그리고 설정된 서버 중 어떤 것을 로드할 수 있는지 걸러 내는 `allowedMcpServers` / `deniedMcpServers` 설정 키입니다.

**위치:**
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux와 WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

`managed-mcp.json`은 프로젝트 `.mcp.json`과 같은 형식, 즉 최상위 `mcpServers` 맵을 씁니다. 이 파일은 서버를 배포할 뿐 걸러 내지는 않습니다:

```json
{
  "mcpServers": {
    "example-remote": {
      "type": "http",
      "url": "https://mcp.example.com/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"]
    }
  }
}
```

이 파일은 컴퓨터의 모든 사용자가 읽을 수 있으므로 `env` 블록에 자격 증명을 절대 넣지 마세요. 대신 `${VAR}` 확장, OAuth, `headersHelper`를 쓰세요.

**걸러 내기: 허용 목록과 거부 목록**

`allowedMcpServers`, `deniedMcpServers`, `allowAllClaudeAiMcps`는 **`managed-mcp.json`의 필드가 아니라 설정 키입니다**. 강제로 적용되게 하려면 관리형 설정 소스 — 서버 관리형 설정, `managed-settings.json`, MDM 프로필, 레지스트리 — 에 넣으세요:

- `allowedMcpServers` -- 허용할 서버의 허용 목록. 같은 관리형 소스에 `allowManagedMcpServersOnly: true`도 함께 설정하세요. 그러지 않으면 모든 범위의 허용 목록이 병합되어 사용자가 관리자의 목록을 넓힐 수 있습니다.
- `deniedMcpServers` -- 차단할 서버의 거부 목록. 어떤 경우든 모든 범위에서 병합됩니다.
- `allowAllClaudeAiMcps` -- 배포된 `managed-mcp.json`과 함께 claude.ai 클라우드 커넥터도 로드합니다(v2.1.149+). 관리자가 제어하는 정책 단계에서만 읽습니다.

각 항목은 키가 **하나**인 객체입니다:

| 키 | 일치 대상 |
|-----|---------|
| `serverUrl` | 원격 서버 URL. 정확히 일치하거나 `*` 와일드카드 사용 |
| `serverCommand` | stdio 서버를 시작하는 정확한 명령어와 인수의 배열 — 모든 인수를 순서대로 |
| `serverName` | 사용자가 붙인 이름. **정확히 일치해야 하며 와일드카드는 확장되지 않음** |

**설정 예:**

```json
{
  "allowedMcpServers": [
    { "serverUrl": "https://mcp.example.com/*" },
    { "serverCommand": ["/usr/local/bin/company-mcp-server", "--config", "/etc/company/mcp-config.json"] }
  ],
  "deniedMcpServers": [
    { "serverName": "untrusted-server" },
    { "serverUrl": "http://*" }
  ],
  "allowManagedMcpServersOnly": true
}
```

세 번째 관리형 설정인 `managedMcpServers`(v2.1.259+)를 쓰면 조직이 모든 사용자에게 HTTP/SSE MCP 서버를 제공할 수 있습니다. 항목은 `.mcp.json`과 같은 형태이며, 실행할 명령어를 지정한 항목은 건너뜁니다.

> **참고:** 한 서버가 `allowedMcpServers`와 `deniedMcpServers`에 모두 일치하면 거부 규칙이 우선합니다.

## 플러그인이 제공하는 MCP 서버

플러그인은 자체 MCP 서버를 묶어 제공할 수 있으며, 플러그인을 설치하면 자동으로 쓸 수 있게 됩니다. 플러그인이 제공하는 MCP 서버는 두 가지 방법으로 정의할 수 있습니다:

1. **별도 `.mcp.json`** -- 플러그인 루트 디렉토리에 `.mcp.json` 파일을 둠
2. **`plugin.json` 안에 인라인** -- 플러그인 매니페스트 안에 MCP 서버를 직접 정의

플러그인 설치 디렉토리 기준 경로를 참조하려면 `${CLAUDE_PLUGIN_ROOT}` 변수를 쓰세요:

```json
{
  "mcpServers": {
    "plugin-tools": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/dist/mcp-server.js"],
      "env": {
        "CONFIG_PATH": "${CLAUDE_PLUGIN_ROOT}/config.json"
      }
    }
  }
}
```

## 서브에이전트 범위 MCP

`mcpServers:` 키를 쓰면 에이전트 frontmatter 안에 MCP 서버를 인라인으로 정의해, 프로젝트 전체가 아니라 특정 서브에이전트로 범위를 한정할 수 있습니다. 워크플로우의 다른 에이전트에게는 필요 없는 특정 MCP 서버에 한 에이전트만 접근해야 할 때 유용합니다.

```yaml
---
name: my-tool-agent
description: 전문 작업에 my-tool을 사용
mcpServers:
  my-tool:
    type: http
    url: https://my-tool.example.com/mcp
---

당신은 전문 작업을 위해 my-tool에 접근할 수 있는 에이전트입니다.
```

서브에이전트 범위 MCP 서버는 그 에이전트의 실행 컨텍스트 안에서만 쓸 수 있으며, 상위 에이전트나 형제 에이전트와 공유되지 않습니다.

## MCP 출력 한도

Claude Code는 컨텍스트가 넘치지 않도록 MCP 도구 출력에 한도를 둡니다:

| 한도 | 임계값 | 동작 |
|-------|-----------|----------|
| **경고** | 10,000 토큰 | 출력이 크다는 경고 표시 |
| **기본 최댓값** | 25,000 토큰 | 더 큰 출력은 파일로 저장되고, 대화에는 그 파일 경로가 대신 들어감 |
| **디스크 저장** | 50,000자 | 5만 자를 넘는 도구 결과는 디스크에 저장 |

최대 출력 한도는 `MAX_MCP_OUTPUT_TOKENS` 환경 변수로 바꿀 수 있습니다:

```bash
# 최대 출력을 50,000 토큰으로 늘리기
export MAX_MCP_OUTPUT_TOKENS=50000
```

## 오래 걸리는 도구 호출의 자동 백그라운드 전환 (v2.1.212)

2분 넘게 실행되는 MCP 도구 호출은 이제 자동으로 백그라운드로 옮겨지므로, 느린 도구 때문에 세션이 멈추지 않고 계속 쓸 수 있습니다. 임계값은 `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`로 바꿀 수 있으며, 같은 변수로 동작을 조정하거나 끌 수도 있습니다:

```bash
# 자동 백그라운드 전환 임계값을 5분(300,000ms)으로 변경
export CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=300000
```

## 코드 실행으로 컨텍스트 비대 문제 해결

MCP 도입이 늘면서, 도구가 수백~수천 개인 서버 수십 개에 연결하면 큰 문제가 생깁니다: 바로 **컨텍스트 비대**입니다. 이는 대규모 MCP 사용에서 가장 큰 문제라 할 만하며, Anthropic 엔지니어링 팀은 직접 도구를 호출하는 대신 코드 실행을 활용하는 깔끔한 해결책을 제안했습니다.

> **출처**: [Code Execution with MCP: Building More Efficient Agents](https://www.anthropic.com/engineering/code-execution-with-mcp) — Anthropic 엔지니어링 블로그

### 문제: 토큰 낭비의 두 가지 원인

**1. 도구 정의가 컨텍스트 윈도우를 가득 채움**

대부분의 MCP 클라이언트는 모든 도구 정의를 미리 로드합니다. 도구 수천 개에 연결되어 있으면 모델은 사용자의 요청을 읽기도 전에 수십만 토큰을 처리해야 합니다.

**2. 중간 결과가 토큰을 추가로 소비함**

모든 중간 도구 결과가 모델의 컨텍스트를 거쳐 갑니다. Google Drive의 회의록을 Salesforce로 옮기는 경우를 생각해 보세요 — 회의록 전체가 컨텍스트를 **두 번** 지나갑니다: 읽을 때 한 번, 대상에 쓸 때 또 한 번. 2시간짜리 회의록이라면 토큰이 5만 개 넘게 더 들 수 있습니다.

```mermaid
graph LR
    A["모델"] -->|"도구 호출: getDocument"| B["MCP 서버"]
    B -->|"회의록 전체 (5만 토큰)"| A
    A -->|"도구 호출: updateRecord<br/>(회의록 전체를 다시 전송)"| B
    B -->|"확인"| A

    style A fill:#ffcdd2,stroke:#333,color:#333
    style B fill:#f3e5f5,stroke:#333,color:#333
```

### 해결책: 코드 API로 쓰는 MCP 도구

도구 정의와 결과를 컨텍스트 윈도우로 주고받는 대신, 에이전트가 MCP 도구를 API처럼 호출하는 **코드를 작성합니다**. 코드는 샌드박스 실행 환경에서 실행되고, 최종 결과만 모델에게 돌아갑니다.

```mermaid
graph LR
    A["모델"] -->|"코드 작성"| B["코드 실행<br/>환경"]
    B -->|"도구를 직접 호출"| C["MCP 서버"]
    C -->|"데이터는 실행 환경에<br/>머묾"| B
    B -->|"최종 결과만<br/>(최소 토큰)"| A

    style A fill:#c8e6c9,stroke:#333,color:#333
    style B fill:#e1f5fe,stroke:#333,color:#333
    style C fill:#f3e5f5,stroke:#333,color:#333
```

#### 동작 방식

MCP 도구는 타입이 지정된 함수의 파일 트리로 제공됩니다:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   └── index.ts
├── salesforce/
│   ├── updateRecord.ts
│   └── index.ts
└── ...
```

각 도구 파일에는 타입이 지정된 래퍼가 들어 있습니다:

```typescript
// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

export async function getDocument(
  input: GetDocumentInput
): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>(
    'google_drive__get_document', input
  );
}
```

그러면 에이전트가 도구를 조율하는 코드를 작성합니다:

```typescript
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

// 데이터는 도구 사이를 직접 오가며 모델을 거치지 않음
const transcript = (
  await gdrive.getDocument({ documentId: 'abc123' })
).content;

await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});
```

**결과: 토큰 사용량이 약 150,000개에서 약 2,000개로 줄어듭니다 — 98.7% 감소.**

### 주요 이점

| 이점 | 설명 |
|---------|-------------|
| **점진적 공개** | 에이전트가 모든 도구를 미리 로드하지 않고, 파일 시스템을 살펴 필요한 도구 정의만 로드 |
| **컨텍스트 효율적인 결과** | 모델에게 돌려주기 전에 실행 환경에서 데이터를 걸러 내거나 변환 |
| **강력한 제어 흐름** | 반복문, 조건문, 오류 처리를 모델을 왕복하지 않고 코드에서 실행 |
| **개인 정보 보호** | 중간 데이터(개인 식별 정보, 민감한 기록)가 실행 환경에 머물고 모델 컨텍스트에 들어가지 않음 |
| **상태 유지** | 에이전트가 중간 결과를 파일에 저장하고 재사용 가능한 스킬 함수를 만들 수 있음 |

#### 예: 큰 데이터 세트 필터링

```typescript
// 코드 실행 없이 — 10,000행이 모두 컨텍스트를 거쳐 감
// TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
//   -> 컨텍스트로 10,000행 반환

// 코드 실행으로 — 실행 환경에서 필터링
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(
  row => row["Status"] === 'pending'
);
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // 모델에는 5행만 전달됨
```

#### 예: 왕복 없는 반복문

```typescript
// 배포 알림을 폴링 — 전부 코드 안에서 실행됨
let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({
    channel: 'C123456'
  });
  found = messages.some(
    m => m.text.includes('deployment complete')
  );
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Deployment notification received');
```

### 고려할 트레이드오프

코드 실행에는 그 나름의 복잡성이 있습니다. 에이전트가 생성한 코드를 실행하려면 다음이 필요합니다:

- 적절한 리소스 제한을 갖춘 **안전한 샌드박스 실행 환경**
- 실행된 코드에 대한 **모니터링과 로깅**
- 직접 도구 호출보다 늘어나는 **인프라 오버헤드**

토큰 비용 감소, 지연 시간 단축, 도구 조합 개선이라는 이점을 이런 구현 비용과 견주어 보세요. MCP 서버가 몇 개뿐인 에이전트라면 직접 도구를 호출하는 편이 더 간단할 수 있습니다. 대규모 에이전트(서버 수십 개, 도구 수백 개)라면 코드 실행이 크게 도움이 됩니다.

### MCPorter: MCP 도구 조합을 위한 런타임

[MCPorter](https://github.com/steipete/mcporter)는 상용구 코드 없이 MCP 서버를 실용적으로 호출하게 해 주는 TypeScript 런타임이자 CLI 도구 모음입니다 — 도구를 골라서 노출하고 타입이 지정된 래퍼를 제공해 컨텍스트 비대를 줄이는 데 도움이 됩니다.

**해결하는 문제:** 모든 MCP 서버의 도구 정의를 미리 로드하는 대신, MCPorter를 쓰면 필요할 때 특정 도구를 찾고 살펴보고 호출할 수 있습니다 — 컨텍스트를 가볍게 유지할 수 있습니다.

**주요 기능:**

| 기능 | 설명 |
|---------|-------------|
| **설정 없는 발견** | Cursor, Claude, Codex, 로컬 설정에서 MCP 서버를 자동으로 발견 |
| **타입이 지정된 도구 클라이언트** | `mcporter emit-ts`가 `.d.ts` 인터페이스와 바로 실행할 수 있는 래퍼를 생성 |
| **조합 가능한 API** | `createServerProxy()`가 `.text()`, `.json()`, `.markdown()` 헬퍼를 갖춘 camelCase 메서드로 도구를 노출 |
| **CLI 생성** | `mcporter generate-cli`가 어떤 MCP 서버든 `--include-tools` / `--exclude-tools` 필터링을 갖춘 독립 CLI로 변환 |
| **매개변수 숨기기** | 선택 매개변수는 기본으로 숨겨져 스키마가 덜 장황해짐 |

**설치:**

```bash
npx mcporter list          # 설치 없이 바로 서버 발견
pnpm add mcporter          # 프로젝트에 추가
brew install steipete/tap/mcporter  # macOS에서 Homebrew로 설치
```

**예 — TypeScript에서 도구 조합하기:**

```typescript
import { createRuntime, createServerProxy } from "mcporter";

const runtime = await createRuntime();
const gdrive = createServerProxy(runtime, "google-drive");
const salesforce = createServerProxy(runtime, "salesforce");

// 데이터가 모델 컨텍스트를 거치지 않고 도구 사이를 오감
const doc = await gdrive.getDocument({ documentId: "abc123" });
await salesforce.updateRecord({
  objectType: "SalesMeeting",
  recordId: "00Q5f000001abcXYZ",
  data: { Notes: doc.text() }
});
```

**예 — CLI로 도구 호출하기:**

```bash
# 특정 도구를 직접 호출
npx mcporter call linear.create_comment issueId:ENG-123 body:'좋아 보여요!'

# 사용 가능한 서버와 도구 나열
npx mcporter list
```

MCPorter는 MCP 도구를 타입이 지정된 API로 호출하는 런타임 인프라를 제공해 위에서 설명한 코드 실행 방식을 보완하며, 중간 데이터를 모델 컨텍스트 밖에 두기 쉽게 해 줍니다.

## 모범 사례

### 보안 고려 사항

#### 권장 ✅
- 모든 자격 증명은 환경 변수에 두기
- 토큰과 API 키를 정기적으로 교체하기(매달 권장)
- 가능하면 읽기 전용 토큰 쓰기
- MCP 서버의 접근 범위를 필요한 최소한으로 제한하기
- MCP 서버 사용 현황과 접근 로그 모니터링하기
- 외부 서비스에 OAuth를 쓸 수 있으면 OAuth 쓰기
- MCP 요청에 속도 제한 적용하기
- 프로덕션에서 쓰기 전에 MCP 연결 테스트하기
- 사용 중인 MCP 연결을 모두 문서화하기
- MCP 서버 패키지를 최신으로 유지하기

#### 비권장 ❌
- 설정 파일에 자격 증명 하드코딩하기
- 토큰이나 비밀 정보를 git에 커밋하기
- 팀 채팅이나 이메일로 토큰 공유하기
- 팀 프로젝트에 개인 토큰 쓰기
- 불필요한 권한 부여하기
- 인증 오류 무시하기
- MCP 엔드포인트를 외부에 공개하기
- root/관리자 권한으로 MCP 서버 실행하기
- 로그에 민감한 데이터 캐싱하기
- 인증 메커니즘 끄기

### 설정 모범 사례

1. **버전 관리**: `.mcp.json`은 git에 두되 비밀 정보는 환경 변수를 쓰세요
2. **최소 권한**: MCP 서버마다 필요한 최소 권한만 주세요
3. **격리**: 가능하면 MCP 서버마다 별도 프로세스로 실행하세요
4. **모니터링**: 감사 추적을 위해 모든 MCP 요청과 오류를 로그로 남기세요
5. **테스트**: 프로덕션에 배포하기 전에 모든 MCP 설정을 테스트하세요

### 성능 팁

- 자주 접근하는 데이터는 애플리케이션 수준에서 캐싱하세요
- 전송되는 데이터를 줄이도록 구체적인 MCP 쿼리를 쓰세요
- MCP 작업의 응답 시간을 모니터링하세요
- 외부 API에는 속도 제한을 고려하세요
- 여러 작업을 할 때는 일괄 처리를 쓰세요

## 설치 방법

### 사전 요구 사항
- Node.js와 npm 설치
- Claude Code CLI 설치
- 외부 서비스용 API 토큰/자격 증명

### 단계별 설정

1. **CLI로 첫 MCP 서버 추가하기**(예: GitHub):
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

   또는 프로젝트 루트에 `.mcp.json` 파일을 만드세요:
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

2. **환경 변수 설정:**
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_personal_access_token"
```

3. **연결 테스트:**
```bash
claude /mcp
```

4. **MCP 도구 사용:**
```bash
/mcp__github__list_prs
/mcp__github__create_issue "제목" "설명"
```

### 서비스별 설치

**GitHub MCP:**
```bash
npm install -g @modelcontextprotocol/server-github
```

**데이터베이스 MCP:**
```bash
npm install -g @bytebase/dbhub
```

**파일 시스템 MCP:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**Slack MCP(지원 중단된 패키지):**
```bash
npm install -g @modelcontextprotocol/server-slack
```

## 문제 해결

### 오류 출력부터 확인하기 (v2.1.219+)

서버가 연결되지 않으면 무엇이든 바꾸기 전에 `claude mcp list`(세션 안에서는 `/mcp`)를 실행하세요. 이제 Claude Code는 실패한 서버 옆에 **HTTP 상태 코드와 서버의 오류 메시지**를 출력하므로, 막연한 "failed to connect" 대신 `401 Unauthorized`나 `404 Not Found` 같은 정보를 볼 수 있습니다:

```bash
# 연결 상태와 함께, 실패한 서버의 HTTP 상태와 오류 메시지를 표시
claude mcp list
```

먼저 상태 코드를 읽으세요 — 어떤 해결책이 맞는지 알려 줍니다:

- `401` / `403` → 잘못되었거나 만료된 자격 증명. `claude mcp login <name>`으로 다시 인증하세요
- `404` → 잘못된 URL(보통 `/mcp`나 `/sse` 경로 접미사가 빠진 것이 원인)
- `5xx` / 시간 초과 → 원격 서버가 다운됨. [연결 시간 초과](#연결-시간-초과)를 참고하세요

### 설정 값의 숨은 공백 (v2.1.219+)

Claude Code는 MCP 설정 값의 **앞뒤에 공백**이 있으면 경고합니다. 이는 흔하지만 찾기 어려운 인증 실패 원인입니다: 브라우저나 채팅 메시지에서 복사해 붙여 넣은 토큰에는 끝에 공백이나 줄바꿈이 따라붙는 경우가 많고, 이것이 `Authorization` 헤더에 그대로 실려 잘못된 자격 증명으로 실패합니다.

이 경고가 보이면 `.mcp.json`의 값(또는 그 값으로 확장되는 환경 변수)을 다시 확인하고 공백을 지우세요:

```bash
# 구분 기호 사이에 숨은 앞뒤 공백을 드러냄
printf '[%s]\n' "$GITHUB_PERSONAL_ACCESS_TOKEN"
```

### 헤드리스 실행에서 건너뛴 서버 (v2.1.219+)

`--mcp-config`로 넘긴 서버 중 설정 검증에 실패한 서버는 실행을 중단시키지 않고 **건너뜁니다**. 그래서 헤드리스 스크립트가 도구의 절반이 빠진 채로 동작하는 것처럼 보일 수 있습니다. 이제 Claude Code는 어떤 서버가 빠졌는지 알려 줍니다:

- **헤드리스 / `-p` 실행**: stream-json의 `init` 이벤트에 건너뛴 항목을 모두 나열하는 `mcp_server_errors` 필드가 들어 있습니다. 실행 결과를 믿기 전에 확인하세요.
- **대화형 터미널 실행**: 같은 문제가 세션을 시작할 때 시작 경고로 출력됩니다.

```bash
# 헤드리스 실행에서 건너뛴 --mcp-config 항목 확인
claude -p "내 도구 목록을 보여 줘" --mcp-config ./servers.json \
  --output-format stream-json --verbose \
  | jq -r 'select(.type == "system" and .subtype == "init") | .mcp_server_errors'
```

### MCP 서버를 찾을 수 없음
```bash
# MCP 서버가 설치되어 있는지 확인
npm list -g @modelcontextprotocol/server-github

# 없으면 설치
npm install -g @modelcontextprotocol/server-github
```

### 인증 실패
```bash
# 환경 변수가 설정되어 있는지 확인
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# 필요하면 다시 export
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"

# 토큰 권한이 올바른지 확인
# GitHub 토큰 범위는 다음에서 확인: https://github.com/settings/tokens
```

### 연결 시간 초과
- 네트워크 연결 확인: `ping api.github.com`
- API 엔드포인트에 접근할 수 있는지 확인
- API의 속도 제한 확인
- 설정에서 시간 제한 늘려 보기
- 방화벽이나 프록시 문제 확인

### MCP 서버 비정상 종료
- MCP 서버 로그 확인: `~/.claude/logs/`
- 모든 환경 변수가 설정되었는지 확인
- 파일 권한이 올바른지 확인
- MCP 서버 패키지 다시 설치해 보기
- 같은 포트를 쓰는 프로세스가 충돌하는지 확인

## 관련 개념

### 메모리와 MCP 비교
- **메모리**: 지속적이고 잘 바뀌지 않는 데이터를 저장(선호 설정, 컨텍스트, 기록)
- **MCP**: 실시간으로 바뀌는 데이터에 접근(API, 데이터베이스, 실시간 서비스)

### 각각을 써야 할 때
- **메모리를 쓸 때**: 사용자 선호 설정, 대화 기록, 학습한 컨텍스트
- **MCP를 쓸 때**: 현재 GitHub 이슈, 실시간 데이터베이스 쿼리, 실시간 데이터

### 다른 Claude 기능과의 통합
- MCP와 메모리를 함께 써서 풍부한 컨텍스트 구성
- 프롬프트에서 MCP 도구를 활용해 더 나은 추론
- 복잡한 워크플로우에 여러 MCP 활용

## 추가 자료

- [공식 MCP 문서](https://code.claude.com/docs/ko/mcp)
- [MCP 프로토콜 명세](https://modelcontextprotocol.io/specification)
- [MCP GitHub 저장소](https://github.com/modelcontextprotocol/servers)
- [사용 가능한 MCP 서버](https://github.com/modelcontextprotocol/servers)
- [MCPorter](https://github.com/steipete/mcporter) — 상용구 코드 없이 MCP 서버를 호출하는 TypeScript 런타임 & CLI
- [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) — 컨텍스트 비대 문제 해결을 다룬 Anthropic 엔지니어링 블로그
- [Claude Code CLI 레퍼런스](https://code.claude.com/docs/ko/cli-reference)
- [Claude API 문서](https://docs.anthropic.com)

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/mcp
- https://code.claude.com/docs/ko/managed-mcp
- https://code.claude.com/docs/en/changelog
- https://github.com/anthropics/claude-code/releases/tag/v2.1.117
- https://github.com/anthropics/claude-code/releases/tag/v2.1.139
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/ko/mcp#configure-tool-search
- https://code.claude.com/docs/ko/env-vars
- https://github.com/anthropics/claude-code/releases/tag/v2.1.285
- https://github.com/anthropics/claude-code/releases/tag/v2.1.296
- https://code.claude.com/docs/ko/mcp#tool-search-for-mcp-server-authors
- https://code.claude.com/docs/ko/mcp#environment-variable-expansion-in-mcp-json
- https://code.claude.com/docs/ko/sub-agents
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
