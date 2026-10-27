<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# 고급 기능

Claude Code의 고급 기능을 종합적으로 다루는 가이드입니다. 계획 모드, 확장 사고, 자동 모드, 백그라운드 작업, 권한 모드, print 모드(비대화형), 세션 관리, 대화형 기능, 채널, 음성 받아쓰기, Remote Control, 웹 세션, 데스크톱 앱, 작업 목록, 프롬프트 제안, git worktree, 샌드박싱, 관리형 설정, 설정 전반을 살펴봅니다.

## 목차

1. [개요](#개요)
2. [계획 모드](#계획-모드)
3. [확장 사고](#확장-사고)
4. [자동 모드](#자동-모드)
5. [백그라운드 작업](#백그라운드-작업)
6. [Monitor 도구(이벤트 기반 스트림)](#monitor-도구이벤트-기반-스트림)
7. [동적 워크플로우](#동적-워크플로우)
8. [예약 작업](#예약-작업)
9. [권한 모드](#권한-모드)
10. [헤드리스 모드](#헤드리스-모드)
11. [세션 관리](#세션-관리)
12. [세션 간 메시지](#세션-간-메시지)
13. [대화형 기능](#대화형-기능)
14. [출력 스타일](#출력-스타일)
15. [상태 표시줄](#상태-표시줄)
16. [TUI 모드(전체 화면)](#tui-모드전체-화면)
17. [음성 받아쓰기](#음성-받아쓰기)
18. [채널](#채널)
19. [Chrome 통합](#chrome-통합)
20. [Remote Control](#remote-control)
21. [웹 세션](#웹-세션)
22. [데스크톱 앱](#데스크톱-앱)
23. [작업 목록](#작업-목록)
24. [프롬프트 제안](#프롬프트-제안)
25. [Git worktree](#git-worktree)
26. [샌드박싱](#샌드박싱)
27. [관리형 설정(엔터프라이즈)](#관리형-설정엔터프라이즈)
28. [설정과 구성](#설정과-구성)
29. [신뢰와 권한 범위](#신뢰와-권한-범위)
30. [에이전트 팀](#에이전트-팀)
31. [모범 사례](#모범-사례)
32. [추가 자료](#추가-자료)

---

## 개요

Claude Code의 고급 기능은 계획, 추론, 자동화, 제어 메커니즘으로 핵심 기능을 확장합니다. 복잡한 개발 작업, 코드 리뷰, 자동화, 여러 세션 관리를 위한 정교한 워크플로우를 가능하게 합니다.

**주요 고급 기능:**
- **계획 모드**: 코딩 전에 상세한 구현 계획 세우기
- **확장 사고**: 복잡한 문제를 위한 깊은 추론
- **자동 모드**: 백그라운드 안전 분류기가 실행 전에 각 작업을 검토
- **백그라운드 작업**: 대화를 막지 않고 오래 걸리는 작업 실행
- **권한 모드**: Claude가 할 수 있는 일 제어(`manual` — 이전 이름 `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`)
- **print 모드**: 자동화와 CI/CD를 위해 Claude Code를 비대화형으로 실행(`claude -p`)
- **세션 관리**: 여러 작업 세션 관리
- **대화형 기능**: 키보드 단축키, 여러 줄 입력, 명령어 기록
- **음성 받아쓰기**: 20개 언어 음성 인식을 지원하는 눌러서 말하기 음성 입력
- **채널**: MCP 서버가 실행 중인 세션에 메시지를 보냄(연구 미리 보기)
- **Remote Control**: Claude.ai나 Claude 앱에서 Claude Code 제어
- **웹 세션**: claude.ai/code에서 브라우저로 Claude Code 실행
- **데스크톱 앱**: 시각적 diff 검토와 여러 세션을 위한 독립 앱
- **작업 목록**: 컨텍스트 컴팩션 후에도 유지되는 작업 추적
- **프롬프트 제안**: 컨텍스트에 맞춘 똑똑한 명령어 제안
- **Git worktree**: 병렬 작업을 위한 격리된 worktree 브랜치
- **샌드박싱**: OS 수준의 파일 시스템과 네트워크 격리
- **관리형 설정**: plist, 레지스트리, 관리형 파일을 통한 엔터프라이즈 배포
- **설정**: JSON 설정 파일로 동작 사용자 지정

---

## 계획 모드

계획 모드를 쓰면 Claude가 복잡한 작업을 구현하기 전에 충분히 생각해, 사용자가 검토하고 승인할 수 있는 상세한 계획을 세웁니다.

### 계획 모드란?

계획 모드는 두 단계로 진행됩니다:
1. **계획 단계**: Claude가 작업을 분석하고 상세한 구현 계획을 세웁니다
2. **구현 단계**: 승인을 받은 뒤 Claude가 계획을 실행합니다

### 계획 모드를 써야 할 때

✅ 계획 모드를 쓰기 좋은 경우:
- 여러 파일에 걸친 복잡한 리팩토링
- 새 기능 구현
- 아키텍처 변경
- 데이터베이스 마이그레이션
- 대규모 API 재설계

❌ 계획 모드가 필요 없는 경우:
- 간단한 버그 수정
- 포맷팅 변경
- 파일 하나만 편집
- 간단한 질문

### 계획 모드 켜기

**슬래시 명령어**:
```bash
/plan 사용자 인증 시스템 구현
```

**CLI 플래그**:
```bash
claude --permission-mode plan
```

**기본값으로 설정**:
```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

**키보드 단축키**:
- `Shift + Tab` - 권한 모드 순환(plan 포함)
- `Alt + M` - 권한 모드 순환(Windows 전용. 런타임이 VT 입력 모드를 켜지 않은 경우)

### 계획 모드의 이점

- **구조화된 구현 방식**: 구현 단계를 자세히 나눔
- **검토와 승인**: 실행 전에 계획을 승인하거나 조정
- **위험 식별**: 구현 전에 잠재적인 문제 파악
- **명확한 단계**: 체계적으로 정리된 구현 단계와 마일스톤

### 예: 기능 구현

```
사용자: /plan 실시간 알림 시스템 추가

Claude: 실시간 알림 구현 계획을 세우겠습니다.

## 구현 계획

### 1단계: 인프라 설정
1. WebSocket 라이브러리 설치(socket.io)
2. WebSocket 서버 설정
3. 연결 관리 구성

### 2단계: 백엔드 구현
4. 알림 서비스 만들기
5. 알림 대기열 구현
6. 알림용 데이터베이스 스키마 추가
7. API 엔드포인트 만들기

### 3단계: 프런트엔드 통합
8. WebSocket 클라이언트 설정
9. 알림 UI 컴포넌트 만들기
10. 알림 상태 관리 구현
11. 알림 권한 추가

### 4단계: 테스트와 배포
12. 단위 테스트 작성
13. 통합 테스트 작성
14. 문서 업데이트
15. 스테이징에 배포

예상 소요 시간: 3-4시간
수정할 파일: 12개
새로 만들 파일: 8개

진행할까요? (예/아니요/계획 수정)

사용자: 예

Claude: [계획에 따라 구현 시작]
```

### 계획 수정

```
사용자: 계획을 수정해 줘 - 대기열은 일단 빼고 나중에 추가하자

Claude: 수정한 계획:
[대기열을 뺀 수정 계획 표시]

사용자: 좋아, 진행해

Claude: [수정한 계획 구현]
```

### 계획 모드 설정

계획 모드는 CLI 플래그나 슬래시 명령어로 켭니다:

```bash
# CLI로 계획 모드 켜기
claude --permission-mode plan

# 또는 REPL 안에서 /plan 슬래시 명령어 사용
/plan 사용자 인증 시스템 구현
```

**계획용 모델 별칭**: 계획에는 Opus를, 실행에는 Sonnet을 쓰려면 모델 별칭 `opusplan`을 쓰세요:

```bash
claude --model opusplan "새 API를 설계하고 구현해 줘"
```

**외부에서 계획 편집**: `Ctrl+G`를 누르면 현재 계획이 외부 편집기에서 열려 자세히 수정할 수 있습니다.

> **v2.1.112 변경 사항**: 이제 계획 파일 이름은 (무작위 단어 대신) 그 계획을 만든 프롬프트를 따라 지어지므로, 둘러보고 재사용하기 쉽습니다.

> **v2.1.136 변경 사항 — 계획 모드의 쓰기 차단은 무조건 적용**: 이제 계획 모드는 `permissions.allow`에 일치하는 `Edit(...)` 규칙이 있어도 모든 파일 쓰기를 막습니다. 이전에는 허용적인 `Edit(...)` 규칙 때문에 계획 모드에서도 쓰기가 통과할 수 있었지만, 그 우회 경로가 막혔습니다. 예전 동작에 기대던 워크플로우라면 편집하기 전에 계획 모드에서 나오세요(`Shift+Tab`).

---

## 확장 사고

확장 사고를 쓰면 Claude가 해결책을 내놓기 전에 복잡한 문제를 더 오래 추론합니다.

### 확장 사고란?

확장 사고는 Claude가 신중하게 단계별로 추론하는 과정으로, Claude는 다음을 합니다:
- 복잡한 문제를 나누어 분석
- 여러 접근 방식 고려
- 트레이드오프 평가
- 엣지 케이스까지 따져 보기

### 확장 사고 켜기

**키보드 단축키**:
- `Option + T`(macOS) / `Alt + T`(Windows/Linux) - 확장 사고 켜고 끄기. Opus 5.5(v2.1.280부터 기본 모델), Sonnet 5.5, Haiku 5.5, Fable 모델에서는 사고를 끌 수 없습니다 — 이 단축키, `alwaysThinkingEnabled`, `MAX_THINKING_TOKENS=0` 모두 효과가 없습니다.

**자동 활성화**:
- 모든 모델에서 기본으로 켜져 있음(Opus 5, Opus 4.8, Opus 4.7, Sonnet 4.6, Haiku 4.5)
- Opus 5 / Opus 4.8: 노력 수준을 쓰는 적응형 추론: `low`(○), `medium`(◐), `high`(●), `xhigh`, `max`. 기본값은 Opus 5.5(v2.1.280부터 기본 모델), Sonnet 5.5, Haiku 5.5에서 `medium`, Opus 5(v2.1.219), Sonnet 5, Opus 4.8(v2.1.154), Opus 4.6, Sonnet 4.6에서 `high`, Opus 4.7에서 `xhigh`입니다. `xhigh`는 Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7에서 쓸 수 있습니다(Opus 4.6 / Sonnet 4.6에서는 `high`로 대체). `max`는 Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8/4.7/4.6, Sonnet 4.6에서 동작합니다(세션 한정). Haiku 4.5에는 노력 수준이 없습니다. Opus 5, Opus 4.8, Opus 4.7은 네이티브 100만 토큰 컨텍스트 윈도우를 가집니다(100만 컨텍스트 수정은 v2.1.117에 반영 — 그 전에는 `/context`가 Opus 4.7을 20만 윈도우 기준으로 잘못 계산해 자동 컴팩션이 너무 일찍 일어났음). v2.1.129부터 `/context`는 시각화를 UI에만 표시하며, ASCII 시각화가 더 이상 대화 컨텍스트로 새어 들어가지 않으므로(호출마다 약 1.6천 토큰 절약) `/context`를 마음 놓고 써도 됩니다.
- Opus 4.6 / Sonnet 4.6의 Pro/Max 구독자: v2.1.117에서 기본 노력 수준이 `medium`에서 `high`로 올라갔습니다.
- 그 밖의 모델: 최대 31,999 토큰의 고정 예산

**설정 방법**:
- 켜고 끄기: `Alt+T` / `Option+T`, 또는 `/config`에서
- 추론 보기: `Ctrl+O`(상세 모드)
- 노력 수준 설정: `/effort` 명령어나 `--effort` 플래그

**사용자 지정 예산**:
```bash
export MAX_THINKING_TOKENS=1024
```

**노력 수준**(Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6에서 지원 — Haiku 4.5는 미지원):
```bash
export CLAUDE_CODE_EFFORT_LEVEL=high   # low(○), medium(◐), high(●), xhigh(Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8/4.7), max 중 하나 — Opus 5와 Opus 4.8의 기본값은 high
```

**CLI 플래그**:
```bash
claude --effort high "복잡한 아키텍처를 리뷰해 줘"
```

**슬래시 명령어**:
```
/effort high
```

> **참고:** 프롬프트에 "ultrathink"라는 키워드를 넣으면 깊은 추론 모드가 켜집니다. 노력 수준 `low`, `medium`, `high`, `max`는 Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6에서 지원됩니다(Haiku 4.5에는 없음). `xhigh`는 Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7에서 쓸 수 있습니다. 기본 노력 수준은 Opus 5.5, Sonnet 5.5, Haiku 5.5에서 `medium`, Opus 5, Sonnet 5, Opus 4.8(그리고 Opus 4.6 / Sonnet 4.6)에서 `high`, Opus 4.7에서 `xhigh`입니다. 처음 실행할 때 기본 노력 수준을 고정하는 Opus 4.8, Opus 4.7과 달리 Opus 5에는 그런 고정이 없어, 이전에 설정한 수준이 그대로 이어집니다. `/effort` 슬라이더에는 **Ultracode** 토글(Tab 또는 `/effort ultracode [on|off]`)도 있는데, 이는 모델의 노력 수준이 **아닙니다** — 세션이 어떤 노력 수준으로 실행되든 Claude가 동적 워크플로우를 조율하게 합니다. v2.1.284부터는 더 이상 `xhigh`를 강제하지 않으며 수준을 바꿔도 켜진 채로 유지됩니다. `--effort ultracode`와 Agent SDK의 `effortLevel: "ultracode"`는 여전히 `xhigh`로 설정합니다.

### Opus 5의 안전 분류기 대체 동작

(과부하와 사용 불가 상황을 다루는) [`fallbackModel` 설정](#대체-모델-fallbackmodel)과 별개로, Claude Code는 안전 분류기가 요청을 표시하면 **분류별 대체 동작**을 적용합니다. Claude Code v2.1.219 이상이 필요합니다.

- **Opus 5**: 사이버 보안으로 표시된 요청은 Opus 4.8에서 다시 실행됩니다. 생물학으로 표시된 요청은 대신 거부로 끝나는데, Opus 5는 대체 모델 없이 자체 생물학 분류기를 쓰기 때문입니다. 이런 거부는 처음 표시된 요청부터 나타납니다.
- 공격 보안이나 생물학 관련 작업 — 침투 테스트, CTF(Capture the Flag) 실습, 생물학과 관련된 코드베이스 — 은 대체 동작을 자주, 흔히 첫 요청부터 일으킵니다.

여기서 이것이 중요한 이유: Opus 5에서 [보안 리뷰 서브에이전트](../04-subagents/README.md)나 CTF/침투 테스트 작업을 실행하면, 사이버 보안 프롬프트는 (노력 수준 상한과 컨텍스트 윈도우가 다른) Opus 4.8에서 말없이 다시 실행되고, 생물학 관련 프롬프트는 바로 거부될 수 있습니다. 이 동작이 방해가 되면 다른 모델을 명시적으로 고정하세요.

**전환 제어** — `switchModelsOnFlag` 설정(v2.1.170+, 기본값 `true`)은 대체가 말없이 일어날지를 정합니다. `false`로 설정하면 Claude Code가 대신 멈추고, 모델을 바꿀지 프롬프트를 고칠지 고르게 합니다. `/config`에서는 **Switch models when a message is flagged**(메시지가 표시되면 모델 전환)로 나타납니다.

```json
{
  "switchModelsOnFlag": false
}
```

### 확장 사고의 이점

- **깊은 추론**: 복잡한 문제를 더 오래 생각
- **더 나은 아키텍처 결정**: 종합적인 평가를 바탕으로 정보에 근거한 선택
- **엣지 케이스 고려**: 잠재적인 문제와 시나리오까지 따져 봄
- **철저한 분석**: 복잡한 문제 해결에 대한 구조적인 접근

### 예: 아키텍처 결정

```
사용자: ultrathink 우리 전자상거래 플랫폼에는 마이크로서비스와 모놀리스 중 무엇을 써야 할까?

Claude: 이 아키텍처 결정을 신중하게 따져 보겠습니다...

<extended_thinking>
## 상황 분석
- 팀 규모: 개발자 5명
- 예상 트래픽: 처음에는 일일 사용자 1만 명
- 10만 명 이상으로 확장해야 함
- DevOps 인력이 제한적
- MVP까지 6개월

## 접근 방식 1: 마이크로서비스
장점:
+ 독립적인 확장
+ 기술 선택의 유연성
+ 팀의 독립성
+ 장애 격리

단점:
- 운영 복잡도
- 네트워크 오버헤드
- 분산 추적 필요
- DevOps 전문성 필요
- 초기 개발이 느림

## 접근 방식 2: 모놀리스
장점:
+ 더 단순한 배포
+ 더 빠른 초기 개발
+ 더 쉬운 디버깅
+ 더 낮은 운영 부담
+ 단일 코드베이스

단점:
- 나중에 확장이 어려움
- 전부 아니면 전무인 배포
- 기술 종속
- 강한 결합이 생길 가능성

## 결정 요인
1. 팀 규모(개발자 5명) → 모놀리스가 유리
2. DevOps 인력(제한적) → 모놀리스가 유리
3. 일정(6개월) → 모놀리스가 유리
4. 미래 규모(사용자 10만 명) → 모놀리스 + 캐싱으로 충분히 가능
5. 감당할 수 있는 복잡도 → 제한적

## 권장 사항
**모듈형 모놀리스**로 시작하세요:
- 단일 배포 단위
- 명확한 모듈 경계
- 모듈 사이의 깔끔한 인터페이스
- 필요하면 나중에 마이크로서비스로 분리할 수 있도록 준비

이렇게 하면 얻는 것:
✓ 빠른 초기 개발
✓ 낮은 운영 복잡도
✓ 나중에 서비스를 분리할 수 있는 선택지
✓ 명확한 아키텍처

이전 경로: 사용자가 5만 명을 넘거나 특정 모듈을 독립적으로 확장해야 할 때, 그 모듈을 마이크로서비스로 분리하세요.
</extended_thinking>

**권장 사항**: 모듈 경계가 깔끔한 모듈형 모놀리스를 구현하세요.

이 방식은 현재의 제약(팀 규모, 일정, DevOps 인력)과 미래의 확장 요구 사이에서 균형을 잡습니다. 비즈니스상 분명한 필요가 생기면 나중에 특정 모듈을 마이크로서비스로 옮길 수 있습니다.
```

### 확장 사고 설정

확장 사고는 환경 변수, 키보드 단축키, CLI 플래그로 제어합니다:

```bash
# 사고 토큰 예산 설정
export MAX_THINKING_TOKENS=16000

# 노력 수준 설정(Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6): low(○), medium(◐), high(●), xhigh(Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8/4.7), max 중 하나 — Opus 5와 Opus 4.8의 기본값은 high
export CLAUDE_CODE_EFFORT_LEVEL=high
```

세션 중에는 `Alt+T` / `Option+T`로 켜고 끄고, `/effort`로 노력 수준을 정하거나, `/config`에서 설정하세요.

> **간결한 시스템 프롬프트 (v2.1.154):** 이제 Haiku 4.5, Sonnet 5, Opus 4.7과 그 계열의 이전 모델을 제외한 모든 모델에서 간결한 시스템 프롬프트가 **기본값**입니다(Haiku 5.5와 Sonnet 5.5도 사용). 덕분에 Opus 5와 Opus 4.8의 기본 토큰 오버헤드가 줄었습니다.

---

## 자동 모드

자동 모드는 백그라운드 안전 분류기가 실행 전에 각 작업을 검토하는 권한 모드입니다. Claude가 자율적으로 작업하면서도 위험한 작업은 막을 수 있습니다. 모든 요금제에서 쓸 수 있지만 지원되는 모델이 필요합니다(Anthropic API와 AWS의 Claude Platform에서는 Claude Opus 4.6 이상, Sonnet 4.6 이상, Haiku 5.5, Fable 모델. Bedrock, Vertex, Foundry, 로그인한 Claude 앱 게이트웨이 세션에서는 Sonnet 5 이상, Opus 4.7 이상, Haiku 5.5, Fable 모델). Team과 Enterprise에서는 기본으로 켜져 있으며, 관리자가 관리형 설정에서 조직 전체에 대해 끌 수 있습니다.

### 요구 사항

자동 모드는 계정이 다음 요구 사항을 모두 충족할 때만 쓸 수 있습니다:

- **요금제**: 모든 요금제.
- **조직**: Team과 Enterprise에서는 자동 모드를 기본으로 쓸 수 있습니다. 관리자는 관리형 설정에서 `permissions.disableAutoMode`를 `"disable"`로 설정해 조직 전체에 대해 끌 수 있습니다.
- **모델**: Anthropic API와 AWS의 Claude Platform에서는 Claude Opus 4.6 이상, Sonnet 4.6 이상, Haiku 5.5, Fable 모델. Amazon Bedrock, Google Cloud의 Agent Platform(Vertex AI), Microsoft Foundry, 로그인한 Claude 앱 게이트웨이 세션에서는 Claude Sonnet 5 이상, Opus 4.7 이상, Haiku 5.5(v2.1.293+), Fable 모델만. 이전 모델 — Sonnet 4.5, Opus 4.5, Haiku 4.5, claude-3 모델 — 은 어떤 제공업체에서도 지원되지 않습니다.
- **제공업체**: Anthropic API, AWS의 Claude Platform, Amazon Bedrock, Google Cloud의 Agent Platform(Vertex AI), Microsoft Foundry, 로그인한 Claude 앱 게이트웨이 세션에서 기본으로 쓸 수 있습니다. v2.1.158부터 v2.1.206까지는 Anthropic API와 AWS의 Claude Platform을 제외한 모든 곳에서 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`을 설정해야 자동 모드가 켜졌지만, v2.1.207에서 이 요구 사항이 없어졌습니다. 이 변수는 호환성을 위해 여전히 받아들여지지만 v2.1.207부터는 효과가 없습니다.
- **분류기**: 토큰 비용이 추가로 듭니다. 단, Enterprise 요금제와 Claude API 계정에서는 v2.1.278+가 서버에서 무료로 검사합니다

### 자동 모드 켜기

```bash
# 권한 모드가 설정되어 있지 않으면 대화형 세션은 자동 모드로 시작(v2.1.284+)
# 명시적으로 고르려면(예: 설정의 기본값이 다른 모드일 때):
claude --permission-mode auto

# 또는 REPL에서 Shift+Tab으로 순환해 선택
```

> **v2.1.112 변경 사항**: 이제 자동 모드에 `--enable-auto-mode` 플래그가 필요 없습니다. Max 구독자는 Opus 4.7에서 바로 쓸 수 있습니다.

> **v2.1.158 변경 사항**: Bedrock, Vertex, Foundry의 Opus 4.7/4.8에서 자동 모드를 쓸 수 있게 되었으며, `CLAUDE_CODE_ENABLE_AUTO_MODE=1`이 필요했습니다.
>
> **v2.1.207 변경 사항**: 그 선택 요구 사항이 없어졌습니다. 이제 Bedrock, Vertex AI, Microsoft Foundry, 로그인한 Claude 앱 게이트웨이 세션에서 Claude Sonnet 5, Opus 4.7, Opus 4.8, Fable 5(그리고 v2.1.219부터 Opus 5)의 자동 모드를 기본으로 쓸 수 있으며, 플래그나 환경 변수가 필요 없습니다. 관리자는 관리형 설정의 `disableAutoMode`로 끌 수 있습니다. `CLAUDE_CODE_ENABLE_AUTO_MODE`는 호환성을 위해 여전히 받아들여지지만 v2.1.207부터는 효과가 없습니다.

또는 기본 권한 모드로 설정하세요:

```bash
claude --permission-mode auto
```

설정 파일로 지정:
```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

### 분류기의 동작 방식

백그라운드 분류기는 다음 순서로 각 작업을 평가합니다:

1. **허용/거부 규칙** -- 명시적인 권한 규칙을 먼저 확인
2. **읽기/편집 자동 승인** -- 파일 읽기와 편집은 자동으로 통과
3. **분류기** -- 백그라운드 분류기가 작업을 검토
4. **대체 동작** -- 연속 3번 또는 총 20번 차단되면 확인 요청으로 돌아감

### 기본으로 차단되는 작업

자동 모드는 기본적으로 다음을 차단합니다:

| 차단되는 작업 | 예 |
|----------------|---------|
| 셸로 파이프하는 설치 | `curl \| bash` |
| 민감한 데이터를 외부로 전송 | 네트워크로 API 키나 자격 증명 전송 |
| 프로덕션 배포 | 프로덕션을 대상으로 하는 배포 명령어 |
| 대량 삭제 | 큰 디렉토리에 `rm -rf` |
| IAM 변경 | 권한과 역할 수정 |
| main에 강제 푸시 | `git push --force origin main` |

> **분류기가 결정하는 범위가 넓어졌습니다(v2.1.218)**: 분류기는 `rm -rf /`나 `rm -rf ~`처럼 파일 시스템 루트나 홈 디렉토리를 대상으로 하는 삭제도 판단하며, 그 삭제가 명령어 치환이나 프로세스 치환 안에 있어도 마찬가지입니다. v2.1.218 이전에는 단순한 형태는 대신 승인을 요청했고, 치환 형태는 v2.1.208부터 v2.1.217까지 승인을 요청했습니다. 백그라운드 `&` 검사와 의심스러운 Windows 경로 검사도 더 이상 권한 대화 상자를 열지 않고 분류기가 판단합니다.

### 기본으로 허용되는 작업

| 허용되는 작업 | 예 |
|----------------|---------|
| 로컬 파일 작업 | 프로젝트 파일 읽기, 쓰기, 편집 |
| 선언된 의존성 설치 | 매니페스트에 있는 `npm install`, `pip install` |
| 읽기 전용 HTTP | 문서를 가져오는 `curl` |
| 현재 브랜치에 푸시 | `git push origin feature-branch` |

### 자동 모드 설정

**기본 규칙을 JSON으로 출력**:
```bash
claude auto-mode defaults
```

**기본 자동 모드 설정으로 복원**(v2.1.212). 확인 프롬프트가 표시되며 `--yes`로 건너뛸 수 있습니다:
```bash
claude auto-mode reset
claude auto-mode reset --yes
```

엔터프라이즈 배포에서는 `autoMode.environment` 관리형 설정으로 **신뢰하는 인프라를 설정**하세요. 관리자가 신뢰하는 CI/CD 환경, 배포 대상, 인프라 패턴을 정의할 수 있습니다.

#### `"$defaults"`로 기본값 확장하기 (v2.1.118)

v2.1.118부터 `autoMode.allow`, `autoMode.soft_deny`, `autoMode.environment`는 `"$defaults"` 토큰을 받으며, 이 토큰을 쓰면 기본 제공 목록을 대체하지 않고 그 뒤에 사용자 규칙을 **덧붙입니다**. v2.1.118 이전에는 사용자가 정의한 배열이 아무 알림 없이 기본 제공 목록을 덮어썼습니다.

#### `autoMode.hard_deny`로 무조건 차단하기 (v2.1.136)

`autoMode.hard_deny`(v2.1.136+)는 **추론된 사용자 의도와 관계없이** 특정 종류의 작업을 막는 분류기 규칙 배열입니다. 자동 모드에서 절대 실행되면 안 되는 작업에 쓰세요 — 예를 들어 루트 경로에 대한 `rm -rf`나 보호된 브랜치에 대한 `git push --force`. `soft_deny`와 달리 hard-deny 규칙은 분류기가 융통성 있게 판단하지 않습니다.

```json
{
  "autoMode": {
    "hard_deny": ["Bash(rm -rf /:*)", "Bash(git push --force*)"]
  }
}
```

**이전(기본 제공 목록을 대체 — v2.1.118 이전 동작):**

```json
{
  "autoMode": {
    "allow": ["Bash(gh pr list:*)"]
  }
}
```

**이후(기본 제공 목록을 확장 — v2.1.118+):**

```json
{
  "autoMode": {
    "allow": ["$defaults", "Bash(gh pr list:*)"],
    "soft_deny": ["$defaults", "Bash(kubectl delete:*)"],
    "environment": ["$defaults", "trusted-ci.internal"]
  }
}
```

`"$defaults"`를 쓰면 기본으로 제공되는 규칙을 유지하면서 그 위에 조직이나 프로젝트별 규칙을 더할 수 있습니다.

#### `autoMode.classifyAllShell`로 모든 셸 명령어 분류하기 (v2.1.193)

`autoMode.classifyAllShell`(불리언, v2.1.193+)은 **모든** Bash/PowerShell 명령어를 자동 모드 분류기로 보냅니다. 세션의 모든 셸 명령어를 분류기가 검사하게 하고 싶을 때 켜세요.

```json
{
  "autoMode": {
    "classifyAllShell": true
  }
}
```

같은 릴리스에서, 자동 모드가 작업을 막으면 **거부 이유**가 표시됩니다 — 대화 기록, 거부 알림, `/permissions` 아래의 최근 거부 목록에서 볼 수 있습니다(v2.1.193+).

#### 의도 기반 기본 보호 (v2.1.183)

사용자가 설정하는 `hard_deny`와 별개로, 자동 모드는 이번 세션에서 사용자가 명시적으로 요청하지 않는 한 다음 파괴적인 명령어를 기본으로 막습니다:

- `git reset --hard`, `git checkout -- .`, `git clean -fd`, `git stash drop`
- `git commit --amend`(이번 세션에서 에이전트가 만든 커밋이 아닐 때)
- `terraform destroy`, `pulumi destroy`, `cdk destroy`(특정 스택을 요청하지 않은 경우)

이는 추론된 의도를 바탕으로 한 기본 보호이므로, 직접 `hard_deny`에 추가할 필요가 없습니다.

### 대체 동작

분류기가 확신하지 못하면 자동 모드는 사용자에게 확인을 요청하는 방식으로 돌아갑니다:
- 분류기 차단이 **연속 3번** 일어난 뒤
- 한 세션에서 분류기 차단이 **총 20번** 일어난 뒤

덕분에 분류기가 작업을 자신 있게 승인하지 못할 때도 사용자가 항상 통제권을 갖습니다.

### 자동 모드에 해당하는 권한 미리 채우기

백그라운드 분류기 없이 더 간단한 방법을 원한다면, `~/.claude/settings.json`에 안전한 권한 규칙의 보수적인 기본 세트를 미리 채워 넣을 수 있습니다. 스크립트는 읽기 전용과 로컬 점검 규칙부터 시작하며, 편집, 테스트, 로컬 git 쓰기, 패키지 설치, GitHub 쓰기 작업은 원할 때만 선택해서 추가할 수 있습니다.

**파일:** `09-advanced-features/setup-auto-mode-permissions.py`

```bash
# 추가될 내용 미리 보기(변경 사항은 기록하지 않음)
python3 09-advanced-features/setup-auto-mode-permissions.py --dry-run

# 보수적인 기본 세트 적용
python3 09-advanced-features/setup-auto-mode-permissions.py

# 필요할 때만 기능을 더 추가
python3 09-advanced-features/setup-auto-mode-permissions.py --include-edits --include-tests
python3 09-advanced-features/setup-auto-mode-permissions.py --include-git-write --include-packages
```

스크립트는 다음 분류에 걸쳐 규칙을 추가합니다:

| 분류 | 예 |
|----------|---------|
| 핵심 읽기 전용 도구 | `Read(*)`, `Grep(*)`, `Agent(*)`, `WebSearch(*)`, `WebFetch(*)` |
| 로컬 점검 | `Bash(git status:*)`, `Bash(git log:*)`, `Bash(git diff:*)`, `Bash(cat:*)` |
| 선택적 편집 | `Edit(*)` |
| 선택적 테스트/빌드 | `Bash(pytest:*)`, `Bash(python3 -m pytest:*)`, `Bash(cargo test:*)` |
| 선택적 git 쓰기 | `Bash(git add:*)`, `Bash(git commit:*)`, `Bash(git checkout:*)`, `Bash(git switch:*)`, `Bash(git stash:*)`, `Bash(git tag:*)` |
| 패키지 관리자 | `Bash(npm ci:*)`, `Bash(npm install:*)`, `Bash(pip install:*)`, `Bash(pip3 install:*)` |
| 빌드와 테스트 | `Bash(make:*)`, `Bash(pytest:*)`, `Bash(go test:*)` |
| 자주 쓰는 셸 명령어 | `Bash(ls:*)`, `Bash(cat:*)`, `Bash(find:*)` |
| GitHub CLI | `Bash(gh pr view:*)`, `Bash(gh pr create:*)`, `Bash(gh issue list:*)` |

위험한 작업(`rm -rf`, `sudo`, 강제 푸시, `DROP TABLE`, `terraform destroy` 등)은 일부러 제외했습니다. 스크립트는 멱등적이라 두 번 실행해도 규칙이 중복되지 않습니다.

---

## 백그라운드 작업

백그라운드 작업을 쓰면 오래 걸리는 작업을 대화를 막지 않고 실행할 수 있습니다.

### 백그라운드 작업이란?

백그라운드 작업은 사용자가 작업을 계속하는 동안 비동기로 실행됩니다:
- 오래 걸리는 테스트 스위트
- 빌드 과정
- 데이터베이스 마이그레이션
- 배포 스크립트
- 분석 도구

**기본 사용법:**
```bash
사용자: 백그라운드에서 테스트를 실행해 줘

Claude: bg-1234 작업을 시작했습니다

/tasks    # 백그라운드 작업(셸과 서브에이전트) 확인과 관리. 여기서 작업을 중지할 수도 있음
Ctrl+B    # 실행 중인 Bash 명령어나 에이전트를 백그라운드로 보내기
```

### 백그라운드 작업 시작하기

```
사용자: 전체 테스트 스위트를 백그라운드에서 실행해 줘

Claude: 백그라운드에서 테스트를 시작합니다(task-id: bg-1234)
테스트가 실행되는 동안 계속 작업하셔도 됩니다.

[대화를 계속할 수 있음]

사용자: 그동안 auth 모듈을 리팩토링하자

Claude: [백그라운드에서 테스트가 실행되는 동안 auth 모듈 작업]

[나중에 테스트가 끝나면]

Claude: 📢 백그라운드 작업 bg-1234 완료:
✅ 테스트 245개 통과
❌ 테스트 3개 실패
결과 보기: /tasks
```

### 백그라운드 작업 관리

`/tasks`(별칭 `/bashes`)를 실행하면 실행 중인 셸과 서브에이전트를 나열하고, 하나를 열어 출력을 보거나 중지할 수 있습니다. `/task` 하위 명령어는 없습니다.

```text
사용자: /tasks

[백그라운드 작업 보기가 열림: 실행 중인 셸과 서브에이전트,
 이미 끝난 서브에이전트도 포함. 하나를 골라 출력을 보거나
 여기서 중지할 수 있음.]
```

### 예: 병렬 개발

```
사용자: 백그라운드에서 빌드를 실행해 줘

Claude: 빌드를 시작합니다... (task-id: bg-5001)

사용자: 린터도 백그라운드에서 실행해 줘

Claude: 린터를 시작합니다... (task-id: bg-5002)

사용자: 그동안 새 API 엔드포인트를 구현하자

Claude: [빌드와 린터가 실행되는 동안 API 엔드포인트 구현]

[10분 뒤]

Claude: 📢 빌드가 성공적으로 끝났습니다(bg-5001)
📢 린터가 문제 12개를 찾았습니다(bg-5002)

사용자: 린터가 찾은 문제를 보여 줘

Claude: [bg-5002의 린터 출력 표시]
```

### 설정

백그라운드 작업을 위한 `settings.json` 블록은 없습니다. 이 기능은 환경 변수로 제어합니다:

```bash
# 백그라운드 작업을 완전히 끄기
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=true
```

동시 실행 수도 백그라운드 작업 설정이 아닙니다 — 한 번에 실행되는 에이전트 수는 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`(기본값 `20`)로 정해집니다.

백그라운드 Bash와 PowerShell 명령어에는 무인 세션에서만 시간 제한이 있습니다(v2.1.288): `-p` 실행, Agent SDK 세션, CI, 클라우드 세션에서는 `run_in_background`로 시작한 명령어가 `timeout`(기본 30분, 최대 2시간)이 지나면 중지되며, 중지되면 Claude에게 알림이 갑니다. 터미널, 데스크톱 앱, VS Code 세션의 백그라운드 명령어에는 시간 제한이 없습니다(v2.1.285–v2.1.287에서는 모든 세션에 제한이 적용되었음).

---

## Monitor 도구(이벤트 기반 스트림)

> **v2.1.98에서 새로 추가**: Monitor 도구를 쓰면 Claude가 백그라운드 명령어의 stdout을 지켜보다가 일치하는 이벤트가 나타나는 순간 반응할 수 있습니다 — 오래 걸리는 프로세스를 기다리던 폴링 반복문과 `sleep`을 대신합니다.

Monitor는 stdout에 출력하는 모든 셸 명령어에 붙일 수 있습니다. 명령어가 출력하는 stdout 줄 하나하나가 세션을 깨우는 알림이 됩니다. Claude가 명령어를 지정하면 하네스가 출력을 흘려보내며 이벤트가 생길 때마다 전달합니다. 바탕이 되는 프로세스를 실행하는 방법은 관련 섹션인 [백그라운드 작업](#백그라운드-작업)을 참고하세요.

> **시간 제한 (v2.1.271)**: 이제 모든 Monitor 감시에 기한이 있습니다 — 최대 30분, 단일 프롬프트 `-p` 실행에서는 10분. 기한이 지나면 Claude에게 알림이 가므로 감시를 다시 걸 수 있습니다. 시간 제한이 없는 감시를 거는 방법은 더 이상 없습니다.

### 왜 중요한가

`/loop`나 `sleep`으로 폴링하면 무언가 바뀌었든 아니든 주기마다 API 왕복을 한 번씩 소모합니다. Monitor는 이벤트가 생길 때까지 조용히 있으므로, 명령어가 아무것도 출력하지 않는 동안에는 **토큰을 전혀** 쓰지 않습니다. 이벤트가 생기면 Claude가 바로 반응하므로, 다음 폴링 주기까지 기다렸다가 뒤늦게 알아채는 일이 없습니다. 몇 분 넘게 실행되는 작업이라면 폴링 반복문보다 더 싸고 빠릅니다.

### 자주 쓰는 두 가지 패턴

**스트림 필터**는 오래 실행되는 소스의 연속 출력을 지켜봅니다. 명령어는 계속 실행되며, 일치하는 줄마다 이벤트가 됩니다.

```bash
tail -f /var/log/app.log | grep --line-buffered "ERROR"
```

**폴링 후 출력 필터**는 소스를 주기적으로 확인하다가 무언가 바뀌었을 때만 출력합니다. API, 데이터베이스처럼 자체 스트림이 없는 대상에 쓰세요.

```bash
last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
while true; do
  gh api "repos/owner/repo/issues/123/comments?since=$last" || true
  last=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  sleep 30
done
```

### 구체적인 예

"개발 서버를 시작하고 오류가 나는지 지켜봐 줘." Claude는 서버를 백그라운드 작업으로 실행하고 Monitor 필터(`tail -F server.log | grep --line-buffered -E "ERROR|FATAL"`)를 붙인 뒤 조용히 기다립니다. 로그에 오류 줄이 나타나는 순간 Claude가 깨어나 오류를 읽고 대응할 수 있습니다 — 서버를 다시 시작하거나, 버그를 고치거나, 사용자에게 알리는 식으로 — 사용자가 직접 확인할 필요가 없습니다.

> **경고**: `grep`으로 파이프할 때는 **항상** `grep --line-buffered`를 쓰세요. 이 플래그가 없으면 grep이 stdout을 4KB 단위로 버퍼링하므로, 출력이 적은 스트림에서는 이벤트가 몇 분씩 늦어질 수 있습니다. 실제로 Monitor가 동작하지 않는 가장 흔한 원인입니다 — 필터가 반응해야 할 때 조용하다면 `--line-buffered` 플래그부터 확인하세요.

---

## 동적 워크플로우

> **v2.1.154에서 새로 추가**

동적 워크플로우를 쓰면 Claude가 수십에서 수백 개의 백그라운드 [서브에이전트](../04-subagents/README.md)를 **결정적으로** 조율합니다 — 팬아웃, 파이프라인, 병렬 단계를 모델의 즉흥에 맡기지 않고 스크립트에 담습니다. 에이전트 하나가 컨텍스트 윈도우 하나를 쓰는 데 비해, 워크플로우는 작업을 여러 에이전트로 나눈 뒤 결과를 다시 합칩니다.

v2.1.219부터 동적 워크플로우의 기본값은 **중간 규모 가이드라인**(에이전트 10개 미만 목표)이며, v2.1.271부터 Pro 요금제로 로그인한 경우에는 **소규모**입니다. 다른 규모나 제한 없음을 고르려면 `/config`의 **Dynamic workflow size**(동적 워크플로우 규모)를 쓰거나 설정 파일에 `workflowSizeGuideline` 키를 지정하세요. 실행 중인 워크플로우의 상태 표시줄에 현재 규모가 표시되며, 바꾸려면 `/config`로 가라고 안내합니다.

### 언제 쓰는가

- **포괄적인 범위** — 여러 파일이나 관점에 걸친 감사나 리뷰를 병렬로.
- **신뢰도** — 독립적인 관점을 여럿 만든 뒤, 확정하기 전에 발견 사항을 반대 입장에서 검증.
- **컨텍스트 하나를 넘는 규모** — 대규모 마이그레이션, 광범위한 전수 점검, 컨텍스트 하나에 담을 수 없는 조사.

이미 잘 이해하고 있는 일회성 작업이라면 여전히 에이전트 하나(또는 직접 편집)가 맞는 도구입니다 — 워크플로우는 작업이 여러 갈래로 퍼질 때 진가를 발휘합니다.

### 실행과 확인

- **실행**: 작업을 위한 워크플로우를 만들어 달라고 Claude에게 요청하세요(예: "`src/`의 모든 파일을 리뷰하는 워크플로우를 실행해 줘"). Claude가 조율 스크립트를 작성해 백그라운드에서 실행합니다.
- **확인**: `/workflows` 명령어는 실행 중이거나 완료된 워크플로우 실행을 실시간 진행 상황과 함께 보여 줍니다.
- **`ultracode`**: `/effort` 슬라이더의 Ultracode 토글(Tab)이나 `/effort ultracode [on|off]`로 켭니다 — 그러면 세션이 어떤 노력 수준으로 실행되든 Claude가 기본으로 동적 워크플로우를 조율합니다. v2.1.284부터 이 토글은 노력 수준을 바꾸지 않으며(예전에는 `xhigh`를 강제함), `--effort ultracode`와 Agent SDK의 `effortLevel: "ultracode"`는 여전히 `xhigh`로 설정합니다. `/effort ultracode`는 그 세션 동안 유지되며, 모든 세션을 이 상태로 시작하려면 설정에 `ultracode` 키를 지정하세요(`effortLevel`과 `CLAUDE_CODE_EFFORT_LEVEL`은 `ultracode`를 받지 않음). (v2.1.160부터 트리거 키워드는 `ultracode`이며, "workflow"라는 단어만으로는 더 이상 실행되지 않습니다.)

워크플로우는 서브에이전트 모델을 바탕으로 합니다 — 개별 에이전트를 정의하고 범위를 정하는 방법은 [서브에이전트](../04-subagents/README.md)를 참고하세요.

---

## 예약 작업

예약 작업을 쓰면 프롬프트를 반복 일정에 따라 자동으로 실행하거나 일회성 알림으로 실행할 수 있습니다. 작업은 세션 범위입니다 — Claude Code가 실행 중일 때 동작하며 세션이 끝나면 사라집니다. v2.1.72+부터 쓸 수 있습니다.

> **claude.com에서는 "Routines"로 소개됨 (2026-05-14)**: Anthropic의 제품 블로그는 이 기능을 **Routines**로 소개합니다. CLI 명령어는 그대로 `/schedule`이며, 이 가이드는 일관성을 위해 원래 이름인 "Scheduled Tasks"(예약 작업)를 씁니다. claude.com 문서나 데스크톱 앱에서 "Routines"를 보면 같은 기능입니다.

### `/loop` 명령어

```bash
# 간격을 명시
/loop 5m 배포가 끝났는지 확인해 줘

# 자연어로
/loop 30분마다 빌드 상태를 확인해 줘
```

정확한 일정을 위해 표준 5필드 cron 표현식도 지원합니다.

### 일회성 알림

특정 시각에 한 번 울리는 알림을 설정합니다:

```
오후 3시에 release 브랜치를 푸시하라고 알려 줘
45분 뒤에 통합 테스트를 실행해 줘
```

### 예약 작업 관리

| 도구 | 설명 |
|------|-------------|
| `CronCreate` | 새 예약 작업 만들기 |
| `CronList` | 활성화된 모든 예약 작업 나열. v2.1.136부터는 출력에 조건과 예약된 프롬프트 본문도 들어 있어, 각 cron이 무엇을 실행할지 열어 보지 않고도 점검할 수 있습니다. |
| `CronDelete` | 예약 작업 제거 |

**한도와 동작**:
- 세션당 예약 작업 **최대 50개**
- 세션 범위 — 세션이 끝나면 사라짐
- 반복 작업은 **3일** 뒤에 자동 만료
- Claude Code가 실행 중일 때만 실행되며, 놓친 실행을 나중에 몰아서 하지 않음

### 동작 세부 사항

| 측면 | 세부 사항 |
|--------|--------|
| **반복 작업의 지터** | 간격의 최대 10%(최대 15분) |
| **일회성 작업의 지터** | :00/:30 경계에서 최대 90초 |
| **놓친 실행** | 몰아서 실행하지 않음 — Claude Code가 실행 중이 아니었으면 건너뜀 |
| **지속성** | 다시 시작하면 유지되지 않음 |

### 클라우드 예약 작업

`/schedule`을 쓰면 Anthropic 인프라에서 실행되는 클라우드 예약 작업을 만들 수 있습니다:

```
/schedule 매일 오전 9시에 테스트 스위트를 실행하고 실패를 보고해 줘
```

클라우드 예약 작업은 다시 시작해도 유지되며, 로컬에서 Claude Code가 실행 중일 필요가 없습니다.

### 예약 작업 끄기

```bash
export CLAUDE_CODE_DISABLE_CRON=1
```

> **API 키 사용 시 `/schedule` 자동 비활성화 (v2.1.139)**: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper` 중 하나라도 설정되어 있으면 클라우드 `/schedule`을 아무 알림 없이 쓸 수 없습니다 — claude.ai로 함께 로그인했더라도 마찬가지입니다. 같은 조건에서 [Remote Control](#remote-control-끄기-disableremotecontrol-v21128), claude.ai MCP 커넥터, 알림 설정도 꺼집니다. `/schedule`을 쓰려면 API 키 설정을 해제하세요(또는 Pro/Max OAuth 등급으로 실행). 로컬 `CronCreate`는 영향을 받지 않습니다.

### 예: 배포 모니터링

```
/loop 5m 스테이징 환경의 배포 상태를 확인해 줘.
        배포가 성공했으면 알려 주고 반복을 멈춰 줘.
        실패했으면 오류 로그를 보여 줘.
```

> **팁**: 예약 작업은 세션 범위입니다. 다시 시작해도 유지되는 자동화가 필요하면 CI/CD 파이프라인, GitHub Actions, 데스크톱 앱의 예약 작업을 쓰세요.

---

## 권한 모드

권한 모드는 Claude가 명시적인 승인 없이 할 수 있는 작업을 제어합니다.

### 사용 가능한 권한 모드

| 모드 | 동작 |
|---|---|
| `manual` | 파일 읽기만 가능하며, 그 밖의 모든 작업은 확인을 요청. v2.1.200에서 `default`에서 이름이 바뀌었으며 `default`도 별칭으로 계속 쓸 수 있음 |
| `acceptEdits` | 파일 읽기와 편집 가능, 명령어는 확인을 요청 |
| `plan` | 파일 읽기만 가능(조사 모드, 편집 없음) |
| `auto` | 백그라운드 안전 분류기 검사를 거쳐 모든 작업 가능. 지원되는 모델(모든 제공업체에서 Sonnet 5 이상, Opus 4.7 이상, Haiku 5.5, Fable 모델. Anthropic API와 AWS의 Claude Platform에서는 Opus 4.6과 Sonnet 4.6도 해당)과 제공업체가 필요 — 모든 요금제에서 사용 가능, [자동 모드](#자동-모드) 참고 |
| `bypassPermissions` | 모든 작업 가능, 권한 검사 없음(위험) |
| `dontAsk` | 사전 승인된 도구만 실행, 나머지는 모두 거부 |

> **참고**: v2.1.200에서 `default` 권한 모드의 이름이 **Manual**로 바뀌었으며(CLI, `--help`, VS Code, JetBrains 전반), 이 모드가 켜져 있으면 하단에 회색 ⏸ 배지가 표시됩니다(v2.1.203). `--permission-mode manual`과 `--permission-mode default` 모두 동작하며, 설정의 `"defaultMode": "manual"`과 `"defaultMode": "default"`도 마찬가지입니다. 설정 키는 `permissions.defaultMode`입니다 — `permissions.mode` 키는 없으므로 아래 예제는 정식 표기를 씁니다.

CLI에서는 `Shift+Tab`으로 모드를 순환합니다. 기본값은 `--permission-mode` 플래그나 `permissions.defaultMode` 설정으로 지정합니다. 권한 모드가 설정되어 있지 않으면, v2.1.284부터 대화형 터미널과 VS Code 세션은 모든 요금제와 제공업체에서 자동 모드로 시작합니다(v2.1.283에서는 Bedrock, Google Cloud의 Agent Platform, Foundry 같은 서드파티 제공업체이거나 텔레메트리가 꺼진 경우에만 그랬음). `permissions.defaultMode`가 여전히 이를 재정의하며, 자동 모드를 쓸 수 없는 세션은 대신 Manual로 시작합니다. v2.1.302부터는 권한 모드를 지정하지 않은 `claude -p`와 Agent SDK 세션이 서드파티 제공업체이거나, 텔레메트리가 꺼져 있거나, 새로 설치한 경우 `default` 모드로 시작합니다. 자동 모드를 유지하려면 `--permission-mode auto`를 넘기세요.

> **계획 모드에서 셸 명령어는 분류기가 판단 (v2.1.218)**: [자동 모드](#자동-모드)를 쓸 수 있고 `useAutoModeDuringPlan` 설정이 켜져 있으면(기본값은 켜짐), 계획 중에 셸 명령어를 사용자에게 묻는 대신 분류기가 검토합니다. 승인된 명령어는 실행되고 거부된 명령어는 막힙니다. 계획 모드는 여전히 파일 쓰기를 무조건 막습니다.

v2.1.160부터는 `acceptEdits`에서도 셸 시작 파일(`.zshenv`, `.zlogin`, `.bash_login`, `~/.config/git/`)과 코드를 실행하는 빌드 설정(`.npmrc`, `.yarnrc*`, `bunfig.toml`, `.bazelrc`, `.pre-commit-config.yaml`, `.devcontainer/`, …)에 쓰기 전에는 확인을 요청합니다. 그러지 않으면 의도하지 않은 명령어 실행으로 이어질 수 있기 때문입니다.

> **`--dangerously-skip-permissions`의 경로 범위 확장 (v2.1.121, v2.1.126)**: 이제 `--dangerously-skip-permissions` CLI 플래그(그리고 같은 효과의 `bypassPermissions` 모드)는 훨씬 넓은 허용 목록 — `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, `.claude/`, `.git/`, `.vscode/`, 셸 설정 파일 — 에 대한 쓰기 확인도 건너뜁니다. 치명적인 삭제 명령어(`rm -rf /` 등)는 이 모드에서도 여전히 확인을 요청합니다 — v2.1.281부터 이 확인은 2분을 기다린 뒤 명령어를 다시 쓰라는 힌트와 함께 거부하므로 무인 세션이 계속 진행됩니다(`CLAUDE_CODE_DISABLE_DANGEROUS_RM_TIMEOUT=1`로 끌 수 있음). (자동 모드에서는 핵심 경로의 삭제를 대신 분류기가 판단하지만, `rm -rf "$(pwd)"` 같은 다른 위험한 `rm` 형태는 여전히 확인을 요청합니다 — [자동 모드](#자동-모드) 참고.) 이 플래그는 전보다 더 날카로운 도구로 여기고, 버려도 되는 샌드박스에서만 쓰세요.

> **Windows 셸 감지 (v2.1.120, v2.1.126)**: 이제 Git for Windows / Git Bash가 필요 없습니다. Git Bash가 없으면 Claude Code는 PowerShell을 셸 도구로 씁니다. v2.1.126부터는 PowerShell 도구가 켜져 있으면 PowerShell이 *기본* 셸이며, Microsoft Store로 설치했거나, PATH 없이 MSI로 설치했거나, `.NET global tool`로 설치한 PowerShell 7도 감지합니다.

> **Bedrock/Vertex/Foundry의 Windows에서 PowerShell 도구 기본 활성화 (v2.1.143)**: v2.1.143부터 Bedrock, Vertex, Foundry 사용자의 **Windows에서는 PowerShell 도구가 기본으로 켜져 있습니다**. Claude Code는 시스템 정책이 `Restricted`여도 스크립트가 실행되도록 `-ExecutionPolicy Bypass`로 PowerShell을 호출합니다. 시스템 실행 정책을 따르게 하려면 `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`을 설정하세요. PowerShell 도구를 완전히 끄려면 `CLAUDE_CODE_USE_POWERSHELL_TOOL=0`을 설정하세요.

### 켜는 방법

**키보드 단축키**:
```bash
Shift + Tab  # default → acceptEdits → plan 순서로 순환하고, 쓸 수 있으면 bypassPermissions/auto도 포함(dontAsk는 순환에 나타나지 않음)
```

**슬래시 명령어**:
```bash
/plan                  # 계획 모드로 들어가기
```

**CLI 플래그**:
```bash
claude --permission-mode plan
claude --permission-mode auto
```

**설정**:
```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

### 권한 모드 예

#### 기본 모드
Claude가 중요한 작업마다 확인을 요청합니다:

```
사용자: auth.ts의 버그를 고쳐 줘

Claude: 버그를 고치려면 src/auth.ts를 수정해야 합니다.
비밀번호 검증 로직이 바뀝니다.

이 변경을 승인할까요? (예/아니요/보기)
```

#### 계획 모드
실행 전에 구현 계획을 검토합니다:

```
사용자: /plan 사용자 인증 시스템 구현

Claude: 인증 구현 계획을 세우겠습니다.

## 구현 계획
[단계와 절차가 담긴 상세 계획]

진행할까요? (예/아니요/수정)
```

#### 편집 자동 승인 모드
파일 수정을 자동으로 승인합니다:

```
사용자: acceptEdits
사용자: auth.ts의 버그를 고쳐 줘

Claude: [묻지 않고 변경]
```

### 활용 사례

**코드 리뷰**:
```
사용자: claude --permission-mode plan
사용자: 이 PR을 리뷰하고 개선점을 제안해 줘

Claude: [코드를 읽고 피드백을 주지만 수정은 할 수 없음]
```

**페어 프로그래밍**:
```
사용자: claude --permission-mode default
사용자: 같이 기능을 구현해 보자

Claude: [변경할 때마다 승인을 요청]
```

**자동화 작업**:
```
사용자: claude --permission-mode acceptEdits
사용자: 코드베이스의 린트 문제를 모두 고쳐 줘

Claude: [묻지 않고 파일 편집을 자동 승인]
```

---

## 헤드리스 모드

print 모드(`claude -p`)를 쓰면 대화형 입력 없이 Claude Code를 실행할 수 있어 자동화와 CI/CD에 딱 맞습니다. 예전 `--headless` 플래그를 대체하는 비대화형 모드입니다.

### print 모드란?

print 모드로 할 수 있는 일:
- 자동화된 스크립트 실행
- CI/CD 통합
- 일괄 처리
- 예약 작업

### print 모드로 실행(비대화형)

```bash
# 특정 작업 실행
claude -p "모든 테스트를 실행해 줘"

# 파이프로 받은 내용 처리
cat error.log | claude -p "이 오류들을 분석해 줘"

# CI/CD 통합 (GitHub Actions)
- name: AI Code Review
  run: claude -p "PR을 리뷰해 줘"
```

### print 모드 추가 사용 예

```bash
# 출력을 저장하며 특정 작업 실행
claude -p "모든 테스트를 실행하고 커버리지 보고서를 만들어 줘"

# 구조화된 출력으로
claude -p --output-format json "코드 품질을 분석해 줘"

# stdin 입력과 함께
echo "코드 품질을 분석해 줘" | claude -p "이걸 설명해 줘"
```

### 예: CI/CD 통합

**GitHub Actions**:
```yaml
# .github/workflows/code-review.yml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p --output-format json \
            --max-turns 3 \
            "이 PR에서 다음을 리뷰해 줘:
            - 코드 품질 문제
            - 보안 취약점
            - 성능 우려 사항
            - 테스트 커버리지
            결과는 JSON으로 출력해 줘" > review.json

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review.json', 'utf8'));
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: JSON.stringify(review, null, 2)
            });
```

### print 모드 설정

print 모드(`claude -p`)는 자동화를 위한 여러 플래그를 지원합니다:

```bash
# 자율 턴 수 제한
claude -p --max-turns 5 "이 모듈을 리팩토링해 줘"

# 구조화된 JSON 출력
claude -p --output-format json "이 코드베이스를 분석해 줘"

# 스키마 검증과 함께
claude -p --json-schema '{"type":"object","properties":{"issues":{"type":"array"}}}' \
  "이 코드에서 버그를 찾아 줘"

# 세션 유지 끄기
claude -p --no-session-persistence "일회성 분석을 해 줘"
```

### 안전 모드(문제 해결용)

`--safe-mode`(그리고 `CLAUDE_CODE_SAFE_MODE` 환경 변수, 예: `CLAUDE_CODE_SAFE_MODE=1`)는 **모든 사용자 지정을 끈 상태로** Claude Code를 시작합니다 — CLAUDE.md, 플러그인, 스킬, 훅, MCP 서버가 모두 꺼집니다.

```bash
# 모든 사용자 지정을 끈 채로 실행
claude --safe-mode

# 같은 효과의 환경 변수
CLAUDE_CODE_SAFE_MODE=1 claude
```

문제 해결용 도구입니다: 사용자 설정이 문제를 일으킬 때 안전 모드로 실행하면, 문제가 내 설정에 있는지 Claude Code 자체에 있는지 가려낼 수 있습니다.

---

## 세션 관리

여러 Claude Code 세션을 효과적으로 관리합니다.

### 세션 관리 명령어

| 명령어 | 설명 |
|---------|-------------|
| `/resume` | ID나 이름으로 대화 재개 |
| `/rename` | 현재 세션 이름 지정 |
| `/fork [prompt]` | 대화를 독립된 새 백그라운드 세션으로 복사하고 지금 세션에서 계속 작업(v2.1.212+) |
| `/subtask <task>` | 전체 대화를 이어받은 포크된 서브에이전트를 생성하고, 결과를 이 대화로 보고받음(v2.1.212+) |
| `/branch [name]` | 원래 대화는 보존하고, 현재 시점의 대화 사본으로 전환 |
| `claude -c` | 가장 최근 대화 이어 가기 |
| `claude -r "session"` | 이름이나 ID로 세션 재개 |

### 세션 재개

**마지막 대화 이어 가기**:
```bash
claude -c
```

**이름이 붙은 세션 재개**:
```bash
claude -r "auth-refactor" "이 PR을 마무리해 줘"
```

**현재 세션 이름 바꾸기**(REPL 안에서):
```
/rename auth-refactor
```

> **v2.1.212 변경 사항**: 이제 에이전트 뷰에서 인수 없이 `/resume`을 입력하면 지난 세션 선택기가 열리며 — 보이는 목록에서 제거된 세션도 포함 — 고른 세션을 백그라운드 세션으로 재개합니다.

### 세션 포크와 분기

대화 사본을 만드는 명령어는 세 가지이며, *사본이 어디서 실행되는지가* 다릅니다:

`/subtask <task>`는 전체 대화를 이어받은 포크된 서브에이전트를 생성해, 사용자가 계속 작업하는 동안 그 작업을 처리합니다 — `claude agents`에 자체 행이 생기고, 끝나면 결과가 대화로 돌아옵니다:

```
/subtask auth 테스트가 왜 들쭉날쭉하게 실패하는지 조사해 줘
```

`/fork [prompt]`는 대신 대화를 새 **백그라운드 세션**으로 복사합니다. 사본은 지금까지의 모든 내용을 가지고 시작해 독립적으로 실행되며, 이 대화로는 아무것도 돌아오지 않습니다:

```
/fork OAuth 방식을 처음부터 끝까지 시도해 줘
```

위임하지 않고 직접 사본으로 전환하려면 `/branch [name]`을 쓰세요. 원래 대화는 보존되며 `/resume`으로 돌아갈 수 있습니다:

```
/branch try-oauth-instead
```

> **참고**: `/fork`와 `/subtask`는 **v2.1.212**에서 역할이 맞바뀌었습니다. v2.1.161 이전에는 `/fork`가 `/branch`의 별칭이었고, v2.1.161부터 v2.1.211까지는 포크된 서브에이전트를 시작했습니다 — 지금은 `/subtask`가 이 동작을 맡습니다. 에이전트 뷰가 꺼져 있으면 `/subtask`를 쓸 수 없고 `/fork`가 포크된 서브에이전트 동작을 유지합니다.

또는 CLI에서 포크하세요:
```bash
claude --resume auth-refactor --fork-session "대신 OAuth 방식을 시도해 줘"
```

### 세션 유지

세션은 자동으로 저장되며 재개할 수 있습니다:

```bash
# 마지막 대화 이어 가기
claude -c

# 이름이나 ID로 특정 세션 재개
claude -r "auth-refactor"

# 실험을 위해 재개하면서 포크
claude --resume auth-refactor --fork-session "다른 방식으로 시도해 줘"
```

### 사용 한도 자동 이어 하기 (v2.1.234)

**v2.1.234**부터 claude.ai 사용 한도에 막힌 세션은 한도가 초기화되면 자동으로 이어 갑니다 — 직접 다시 프롬프트를 보낼 필요가 없습니다. `/config`의 "Continue automatically at usage limit"(사용 한도 도달 시 자동으로 계속)에서 켜고 끌 수 있습니다.

### 세션 요약 (v2.1.108)

자리를 비웠다가 세션으로 돌아오면 Claude가 그동안 무엇을 했는지 짧게 요약해 보여 줄 수 있습니다. 모든 요금제와 제공업체에서 기본으로 켜져 있으며, `/config` → **Session recap**(세션 요약)에서 끌 수 있습니다.

> **OTEL 텔레메트리 — 피드백 설문 다시 켜기 (v2.1.136+)**: OpenTelemetry 데이터를 수집하는 조직은 `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL=1`을 설정해 Anthropic의 세션 품질 설문을 다시 켤 수 있습니다. 예전에 설문이 텔레메트리 파이프라인과 다른 곳으로 보내졌기 때문에, OTEL 배포에서는 기본으로 꺼져 있습니다.

> **OTEL 텔레메트리 — `assistant_response` 로그 이벤트 (v2.1.193+)**: Claude Code는 모델의 응답 텍스트를 담은 `claude_code.assistant_response` OpenTelemetry 로그 이벤트를 내보내므로, OTEL 파이프라인이 기존 도구/이벤트 텔레메트리와 함께 Claude가 한 말도 수집할 수 있습니다.

> **OTEL 텔레메트리 — 캐시와 GenAI 속성 (v2.1.300)**: `api_request` 이벤트에 `cache_creation_5m_tokens`/`cache_creation_1h_tokens`가 추가되고, 스팬에 `gen_ai.provider.name` 같은 GenAI 시맨틱 규칙 속성이 붙습니다.

> **OTEL 텔레메트리 — `tool_decision` 속성 (v2.1.301)**: `tool_decision` 이벤트에 `classifier_verdict`와 `permission_mode`가 추가됩니다.

**요약 동작 제어:**

```bash
/recap                                 # 요약을 직접 실행
/config                                # 자동 요약 켜고 끄기
```

또는 환경 변수로:
```bash
CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0 claude   # 요약 끄기
CLAUDE_CODE_ENABLE_AWAY_SUMMARY=1 claude   # 요약 강제로 켜기
```

---

## 세션 간 메시지

> **v2.1.224에서 추가**되어 v2.1.239까지 확장되었습니다. **macOS, Linux, (v2.1.239부터) Windows**에서 쓸 수 있습니다.

예전에는 세션이 각자 고립된 섬이었습니다. 세션 간 메시지를 쓰면 한 Claude Code 세션이 다른 세션과
대화할 수 있습니다 — 다른 컴퓨터의 세션과 클라우드 세션도 포함됩니다. 그래서 질문을 다시
설명하는 대신, 이미 알맞은 컨텍스트를 로드한 세션에 질문을 넘길 수 있습니다.

### 세션 찾기

`ListAgents`는 메시지를 보낼 수 있는 모든 대상을 나열합니다: 내가 생성한 서브에이전트, 이 컴퓨터의
다른 로컬 세션, 클라우드 세션, (Remote Control이 연결되어 있으면) 다른 컴퓨터의 세션. 각 행에는
종류가 표시되며, v2.1.229부터는 `offline`과 `cloud` 표시도 붙어 연결할 수 있는 세션과 잠든
세션을 구분할 수 있습니다.

**각 행의 이름이 곧 주소입니다** — 메시지를 보낼 때 그 이름을 씁니다.

### 메시지 보내기

`SendMessage`는 대상과 메시지를 받습니다:

```text
SendMessage({ to: "<session name>", message: "재시도 로직에 대해 어떤 결론을 내렸어?" })
```

v2.1.232부터는 이름만으로 충분합니다 — 두 행의 이름이 정말 같을 때가 아니면 구분용 참조를 덧붙일
필요가 없습니다.

### 세션이 유휴 상태가 될 때까지 기다리기(`notify_when_idle`, v2.1.236)

메시지를 보내는 세션이 작업 중이라면, 보통은 계속 확인하기보다 끝나는 시점을 알고 싶을 것입니다.
`SendMessage`는 바로 그런 경우를 위한 `notify_when_idle` 입력을 받습니다:

```text
SendMessage({
  to: "auth-refactor",
  message: "마이그레이션이 끝나면 알려 줘",
  notify_when_idle: true
})
```

이 기능은 **선택 사항이며 한 번만 동작합니다** — 대상 세션은 다음에 유휴 상태가 될 때 알림을 한 번
보내고, 구독은 그것으로 끝납니다. 폴링 반복문도 없고, 세션이 다시 바빠졌다가 유휴 상태가 되어도
알림이 반복되지 않습니다.

관련된 v2.1.239 변경 사항 두 가지: 이제 `ListAgents`가 활성 팀원과 함께 **세션 자신의 이름**도
알려 주므로(다른 세션에게 자신을 부르는 방법을 알려 줄 수 있음), 세션 간 메시지를 **Windows**에서도
쓸 수 있게 되었습니다.

### `@` 멘션 약식 (v2.1.232)

도구를 명시적으로 호출하는 대신, 프롬프트에서 세션을 `@`로 멘션해 바로 메시지를
보낼 수 있습니다:

```text
@auth-refactor 마이그레이션 테스트는 통과했어?
```

### 받는 메시지 제어: `crossSessionInbound`

들어오는 메시지는 `crossSessionInbound` 설정(v2.1.224+)으로 제어합니다:

| 값 | 동작 |
|---|---|
| `"accept"` | 들어온 메시지를 이 세션의 Claude에게 전달 |
| `"hold"` | 메시지가 왔다는 알림만 표시하고 전달하지 않음 |
| `"refuse"` | 들어온 메시지를 버림 |

이 값들은 단계를 이룹니다 — `accept < hold < refuse`.
그리고 **프로젝트 설정과 로컬 설정은 사용자 범위 값보다 엄격할 때만 적용됩니다**.
프로젝트는 받는 메시지 전달을 더 엄격하게 할 수는 있어도 느슨하게 할 수는 없습니다. v2.1.232부터는 `/config`에도 "Messages from your other sessions"(다른 세션에서
온 메시지) 항목이 있습니다.

### 범위와 한도

- 같은 컴퓨터의 로컬 세션과 클라우드 세션.
- 다른 컴퓨터의 Remote Control 세션. 이름으로 지정할 수 있음(v2.1.225).
- 클라우드 세션은 메시지를 **받지만** 아직 로컬 세션에 답장을 보낼 수는 없습니다 —
  답은 그 세션의 대화 기록에서 확인하세요.
- macOS와 Linux는 v2.1.224부터, Windows는 v2.1.239부터.

---

## 대화형 기능

### 키보드 단축키

Claude Code는 효율적인 작업을 위한 키보드 단축키를 지원합니다. 공식 문서에 나온 전체 목록은 다음과 같습니다:

| 단축키 | 설명 |
|----------|-------------|
| `Ctrl+C` | 현재 입력/생성 취소 |
| `Ctrl+D` | Claude Code 종료 |
| `Ctrl+G` | 외부 편집기에서 계획 편집 |
| `Ctrl+L` | 화면 다시 그리기(다시 그리기만 함 — 두 번 눌러 `/clear`하던 단축키는 v2.1.238에서 제거됨) |
| `Ctrl+O` | 상세 출력 켜고 끄기(추론 보기) |
| `Ctrl+R` | 기록 역방향 검색. 기본으로 **모든 프로젝트의 모든 프롬프트**를 검색합니다(v2.1.129+). 선택기 안에서 `Ctrl+S`를 누르면 현재 프로젝트로 좁혀집니다. 이전 버전의 기본값은 현재 프로젝트만이었습니다. |
| `Ctrl+T` | 작업 목록 보기 켜고 끄기 |
| `Ctrl+B` | 실행 중인 작업을 백그라운드로 |
| `Esc+Esc` | 코드/대화 되감기 |
| `Shift+Tab` / `Alt+M` | 권한 모드 순환 |
| `Option+P` / `Alt+P` | 모델 전환 |
| `Option+T` / `Alt+T` | 확장 사고 켜고 끄기 |
| `Option+O` / `Alt+O` | 빠른 모드 켜고 끄기(`/fast`) |
| `Ctrl+X` `Ctrl+K` | 모든 백그라운드 서브에이전트 중지 |
| `Ctrl+Enter`(또는 `Ctrl+X` `Ctrl+S`) | 지금 보내기 — 대기 중인 메시지를 한꺼번에 보냄. v2.1.281부터는 턴을 취소하지 않고 실행 중인 도구와 서브에이전트를 백그라운드로 보냄. 보냈거나 대기 중인 메시지는 모델이 받을 때까지 회색으로 표시됨(v2.1.275) |
| `Ctrl+S` | 현재 프롬프트를 잠시 보관. 다시 누르면 복원 |
| `Ctrl+_` | 프롬프트 입력의 마지막 편집 취소 |
| `:` | 단어 맨 앞에서 `:`를 입력하면 이모지 단축 코드 자동 완성이 열림(예: `:heart:`, v2.1.217+) |

**줄 편집(표준 readline 단축키):**

| 단축키 | 동작 |
|----------|--------|
| `Ctrl + A` | 줄 맨 앞으로 이동 |
| `Ctrl + E` | 줄 맨 끝으로 이동 |
| `Ctrl + K` | 줄 끝까지 잘라 내기 |
| `Ctrl + U` | 줄 맨 앞까지 잘라 내기 |
| `Ctrl + W` | 앞 단어 삭제 |
| `Ctrl + Y` | 붙여 넣기(yank) |
| `Tab` | 자동 완성 |
| `↑ / ↓` | 명령어 기록 |

### 접근성

화면 낭독기 모드(v2.1.208+)는 CLI를 화면 낭독기에 맞춘 일반 텍스트 렌더링 모드로 바꿉니다. CLI 플래그, 환경 변수, 설정 키로 켤 수 있습니다:

```bash
claude --ax-screen-reader
```

```bash
export CLAUDE_AX_SCREEN_READER=1
```

```json
{
  "axScreenReader": true
}
```

### 키 바인딩 사용자 지정

`/keybindings`를 실행하면 `~/.claude/keybindings.json`이 편집용으로 열려 사용자 정의 키보드 단축키를 만들 수 있습니다(v2.1.18+).

**설정 형식**:

```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null,
        "ctrl+k ctrl+s": "chat:stash"
      }
    },
    {
      "context": "Confirmation",
      "bindings": {
        "ctrl+a": "confirmation:yes"
      }
    }
  ]
}
```

기본 단축키를 해제하려면 바인딩을 `null`로 설정하세요.

### 사용 가능한 컨텍스트

키 바인딩은 특정 UI 컨텍스트 범위로 적용됩니다:

| 컨텍스트 | 주요 동작 |
|---------|-------------|
| **Chat** | `submit`, `cancel`, `cycleMode`, `modelPicker`, `thinkingToggle`, `undo`, `externalEditor`, `stash`, `imagePaste` |
| **Confirmation** | `yes`, `no`, `previous`, `next`, `nextField`, `cycleMode`, `toggleExplanation` |
| **Global** | `interrupt`, `exit`, `toggleTodos`, `toggleTranscript` |
| **Autocomplete** | `accept`, `dismiss`, `next`, `previous` |
| **HistorySearch** | `search`, `previous`, `next` |
| **Settings** | 컨텍스트별 설정 탐색 |
| **Tabs** | 탭 전환과 관리 |
| **Help** | 도움말 패널 탐색 |

컨텍스트는 `Transcript`, `Task`, `ThemePicker`, `Attachments`, `Footer`, `MessageSelector`, `DiffDialog`, `ModelPicker`, `Select`를 포함해 모두 18개입니다.

### 연속 키 조합(chord) 지원

키 바인딩은 연속 키 조합(여러 키를 차례로 누르는 조합)을 지원합니다:

```
"ctrl+k ctrl+s"   → 두 키를 차례로: ctrl+k를 누른 다음 ctrl+s
"ctrl+shift+p"    → 수정 키를 동시에
```

**키 입력 문법**:
- **수정 키**: `ctrl`(또는 `control`), `alt`(또는 `opt`, `option`, `meta`), `shift`, `cmd`(또는 `command`, `super`, `win`) — `cmd`는 `meta`의 별칭이 아니라 별개의 수정 키이며, Super 키를 보고하는 터미널에서만 감지됩니다
- **대문자는 Shift를 뜻함**: `K`는 `shift+k`와 같습니다
- **특수 키**: `escape`, `enter`, `return`, `tab`, `space`, `backspace`, `delete`, 방향키

### 예약된 키와 충돌하는 키

| 키 | 상태 | 참고 |
|-----|--------|-------|
| `Ctrl+C` | 예약됨 | 다시 지정할 수 없음(중단) |
| `Ctrl+D` | 예약됨 | 다시 지정할 수 없음(종료) |
| `Ctrl+B` | 터미널과 충돌 | tmux 접두사 키 |
| `Ctrl+A` | 터미널과 충돌 | GNU Screen 접두사 키 |
| `Ctrl+Z` | 터미널과 충돌 | 프로세스 일시 중지 |

> **팁**: 단축키가 동작하지 않으면 터미널 에뮬레이터나 멀티플렉서와 충돌하는지 확인하세요.

### Tab 자동 완성

Claude Code는 똑똑한 Tab 자동 완성을 제공합니다:

```
사용자: /rew<TAB>
→ /rewind

사용자: /plu<TAB>
→ /plugin

사용자: /plugin <TAB>
→ /plugin install
→ /plugin enable
→ /plugin disable
```

### 명령어 기록

이전 명령어를 불러옵니다:

```
사용자: <↑>  # 이전 명령어
사용자: <↓>  # 다음 명령어
사용자: Ctrl+R  # 기록 검색

(reverse-i-search)`test': run all tests
```

### 여러 줄 입력

복잡한 질문은 `\` + Enter, Option+Enter(macOS), Shift+Enter, Ctrl+J로 새 줄을 시작하세요. `\end` 같은 종료 표시는 없으며 Enter를 누르면 보내집니다:

```bash
사용자: 길고 복잡한 프롬프트를 \
여러 줄에 걸쳐 입력
```

**예:**

```
사용자: 다음 요구 사항으로 사용자 인증 시스템을 \
구현해 줘: \
- JWT 토큰 \
- 이메일 인증 \
- 비밀번호 재설정 \
- 2단계 인증 지원

Claude: [여러 줄 요청 처리]
```

### 인라인 편집

보내기 전에 명령어를 편집합니다:

```
사용자: 프로덕숀<Backspace>션에 배포해 줘

[보내기 전에 그 자리에서 편집]
```

### Vim 모드

텍스트 편집에 Vi/Vim 키 바인딩을 씁니다:

**켜는 방법**:
- `/config`에서 켜거나("Editor / Vim mode" 토글) `~/.claude/settings.json`에 `editorMode: "vim"`을 지정하세요. 별도의 `/vim` 슬래시 명령어는 제거되었으며([issue #43370](https://github.com/anthropics/claude-code/issues/43370) 참고), 이제 vim 모드는 설정으로 켭니다.
- 모드 전환: `Esc`는 NORMAL, `i/a/o`는 INSERT, `v`는 VISUAL, `V`는 VISUAL-LINE(v2.1.118+)

**이동 키**:
- `h` / `l` - 왼쪽/오른쪽으로 이동
- `j` / `k` - 아래/위로 이동
- `w` / `b` / `e` - 단어 단위로 이동
- `0` / `$` - 줄 맨 앞/맨 끝으로 이동
- `gg` / `G` - 텍스트 맨 앞/맨 끝으로 이동
- `%` - 짝이 맞는 괄호로 이동. `d`, `c`, `y`와 함께 쓸 수 있음(v2.1.301)

**텍스트 객체**:
- `iw` / `aw` - 단어 안쪽/단어 전체
- `i"` / `a"` - 따옴표 문자열 안쪽/전체
- `i(` / `a(` - 괄호 안쪽/전체

**비주얼 모드 (v2.1.118+)**:

| 키 | 모드 | 동작 |
|-----|------|----------|
| `v` | Visual | 글자 단위 선택(선택 영역이 보임). 이동 키로 확장 |
| `V` | Visual-line | 줄 단위 선택. 항상 줄 전체를 선택 |
| `y` | Yank | 현재 비주얼 선택 영역 복사 |
| `d` / `x` | Delete | 현재 비주얼 선택 영역 삭제 |
| `c` | Change | 선택 영역을 지우고 INSERT 모드로 전환 |
| `Esc` | Exit | NORMAL 모드로 돌아감 |

비주얼 선택 영역은 입력란에 강조 표시되므로, 연산자를 실행하기 전에 무엇이 복사, 삭제, 변경될지 정확히 볼 수 있습니다.

### Bash 모드

`!` 접두사로 셸 명령어를 바로 실행합니다:

```bash
! npm test
! git status
! cat src/index.js
```

컨텍스트를 바꾸지 않고 명령어를 빠르게 실행할 때 쓰세요.

**v2.1.193부터:** bash 모드(`!`)에서 파일 경로가 실시간으로 자동 완성되므로, 프롬프트를 떠나지 않고 셸 명령어를 입력하면서 경로를 완성할 수 있습니다.

**v2.1.186부터:** 이제 `!` 명령어의 출력이 자동으로 Claude에게 전달되고 Claude가 이에 응답합니다. 출력을 응답 없이 컨텍스트에만 추가하던 이전 동작을 유지하려면 `settings.json`에 `"respondToBashCommands": false`를 설정하세요.

---

## 출력 스타일

출력 스타일은 Claude가 아는 내용이 아니라 **어떻게** 응답하는지를 바꿉니다. 시스템 프롬프트를 수정해 역할, 어조, 기본 응답 형식을 정합니다. 매 턴마다 같은 말투를 다시 요청하게 되거나, Claude가 소프트웨어 엔지니어가 아닌 다른 역할을 하길 원할 때 쓰세요.

프로젝트나 코드베이스에 대한 지침이라면 대신 [CLAUDE.md](../02-memory/)를 쓰세요 — 장단점이 다른 별개의 메커니즘입니다.

### 기본 제공 스타일

| 스타일 | 동작 |
|-------|----------|
| **Default** | 소프트웨어 엔지니어링 작업을 효율적으로 끝내도록 조정된 표준 시스템 프롬프트 |
| **Proactive** | Claude가 일상적인 결정에서 멈추지 않고, 합리적으로 가정한 뒤 바로 실행합니다. 자동 모드보다 자율 실행 지침이 강하지만 권한 모드는 **바꾸지 않으므로**, 권한 프롬프트는 여전히 표시됩니다 |
| **Explanatory** | 단계 사이에 교육용 "Insights"를 넣어 구현 선택과 코드베이스 패턴을 설명 |
| **Learning** | 직접 해 보며 배우는 협업 방식. Claude가 인사이트를 공유*하고*, 작고 전략적인 부분은 사용자가 직접 구현하도록 `TODO(human)` 표시를 남김 |
| **Concise**(v2.1.237) | Claude가 결과부터 말하고 서두와 진행 설명을 생략합니다. 철저함은 그대로이며 답을 둘러싼 말만 빠집니다. `/config` → Output style에서 고르거나 `"outputStyle": "Concise"`를 설정하세요 |

### 스타일 선택

`/config`를 실행해 **Output style**(출력 스타일)을 고르거나, `/output-style <style>`로 바로 전환하세요 — 인수 없이 실행하면 사용 가능한 스타일을 나열하고 현재 스타일을 표시합니다. 어느 방법이든 선택은 `.claude/settings.local.json`에 저장됩니다. 메뉴 없이 지정하려면 설정을 직접 편집하세요:

```json
{
  "outputStyle": "Explanatory"
}
```

> **참고**: 별도의 `/output-style` 명령어는 v2.1.73에서 지원 중단되고 v2.1.91에서 제거되었지만, **v2.1.269에서 다시 돌아왔으며** v2.1.278에서도 동작합니다. 헤드리스 세션과 Remote Control 세션에서도 동작합니다. `/config`와 `outputStyle` 설정도 여전히 쓸 수 있습니다.

출력 스타일은 Claude Code가 세션 시작 시 한 번 읽는 시스템 프롬프트의 일부이므로, 변경 사항은 `/clear` 후나 새 세션에서 적용됩니다.

### 사용자 정의 출력 스타일

사용자 정의 스타일은 frontmatter가 있는 마크다운 파일이며, 세 수준 중 하나에 저장합니다:

- 사용자: `~/.claude/output-styles/`
- 프로젝트: `.claude/output-styles/`
- 관리형 정책: 관리형 설정 디렉토리 안의 `.claude/output-styles/`

프로젝트 스타일은 작업 디렉토리와 저장소 루트 사이의 모든 `.claude/output-styles/`에서 로드됩니다. v2.1.178부터는 중첩된 디렉토리에 같은 이름의 스타일이 있으면 작업 디렉토리에 가장 가까운 것이 이깁니다.

```markdown
---
name: Diagrams first
description: 모든 설명을 다이어그램으로 시작
keep-coding-instructions: true
---

코드, 아키텍처, 데이터 흐름을 설명할 때는 구조를 보여 주는 Mermaid 다이어그램으로
시작한 다음, 글로 설명하세요.
```

| frontmatter | 목적 | 기본값 |
|-------------|---------|---------|
| `name` | 파일 이름과 다를 때의 스타일 이름 | 파일 이름을 따름 |
| `description` | `/config` 선택기에 표시 | 없음 |
| `keep-coding-instructions` | Claude Code의 기본 소프트웨어 엔지니어링 지침 유지 | `false` |
| `force-for-plugin` | 플러그인 스타일 전용: 플러그인이 켜져 있으면 사용자의 `outputStyle`을 무시하고 자동 적용 | `false` |

Claude의 소통 방식은 바꾸되 코딩 방식은 그대로 두고 싶다면 **`keep-coding-instructions: true`를 설정하세요**. Claude가 소프트웨어 엔지니어링을 전혀 하지 않는 경우 — 글쓰기 도우미나 데이터 분석가 — 에는 빼세요.

### 범위와 비용

출력 스타일은 **메인 대화에만** 적용됩니다. 서브에이전트는 자체 시스템 프롬프트로 실행되므로 스타일이 서브에이전트의 응답 방식을 바꾸지 않습니다. 단, 포크는 상위 세션의 시스템 프롬프트 전체를 물려받으므로 예외입니다.

지침을 더하면 입력 토큰이 늘지만, 첫 요청 이후에는 프롬프트 캐싱이 대부분을 흡수합니다. Explanatory와 Learning은 원래 응답이 길도록 설계되어 출력 토큰이 늘어납니다.

### 다른 기능과 비교

| 기능 | 동작 방식 | 쓰기 좋은 경우 |
|---------|--------------|-------------|
| 출력 스타일 | 시스템 프롬프트를 수정 | 매 턴 다른 역할, 어조, 형식을 원할 때 |
| [CLAUDE.md](../02-memory/) | 시스템 프롬프트 뒤에 사용자 메시지를 추가 | Claude가 프로젝트 규칙을 항상 알아야 할 때 |
| `--append-system-prompt` | 아무것도 지우지 않고 시스템 프롬프트에 덧붙임 | 한 번의 호출에만 일회성으로 추가할 때 |
| [서브에이전트](../04-subagents/) | 자체 시스템 프롬프트, 모델, 도구로 실행 | 범위가 분리된 도우미가 필요할 때 |
| [스킬](../03-skills/) | 호출될 때 작업별 지침을 로드 | 재사용 가능한 워크플로우가 있을 때 |

---

## 상태 표시줄

상태 표시줄은 출력이 세션 하단에 표시되는 사용자 정의 명령어입니다. `/statusline`으로 설정하거나 직접 지정하세요:

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

`padding`의 기본값은 `0`입니다. Claude Code가 stdin으로 JSON 객체를 명령어에 넘기므로, 무엇을 표시할지는 스크립트가 정합니다.

### 사용 가능한 입력 필드

| 그룹 | 필드 |
|-------|--------|
| 세션 | `session_id`, `session_name`, `prompt_id`, `transcript_path`, `cwd`, `version` |
| 모델 | `model.id`, `output_style.name`, `effort.level`, `fast_mode`, `thinking.enabled` |
| 에이전트 | `agent.name`, `vim.mode` |
| 비용 | `cost.total_cost_usd`, `cost.total_duration_ms`, `cost.total_api_duration_ms`, `cost.total_lines_added` |
| 컨텍스트 | `context_window.context_window_size`, `.current_usage`, `.remaining_percentage`, `.total_input_tokens`, `.used_percentage` |
| 한도 | `rate_limits.five_hour.used_percentage`, `.resets_at` |
| 저장소 | `pr.number`, `pr.review_state`, `workspace.project_dir`, `workspace.added_dirs`, `workspace.git_worktree`, `workspace.repo.host` |
| worktree | `worktree.name`, `.branch`, `.path`, `.original_branch`, `.original_cwd` |

### 예

```bash
#!/bin/bash
# ~/.claude/statusline.sh — 모델, 컨텍스트 사용량, 비용 표시
input=$(cat)
model=$(echo "$input" | jq -r '.model.id')
used=$(echo "$input" | jq -r '.context_window.used_percentage')
cost=$(echo "$input" | jq -r '.cost.total_cost_usd')
printf '%s | ctx %.0f%% | $%.2f' "$model" "$used" "$cost"
```

> **참고**: `statusLine`에는 작업 공간 신뢰가 필요합니다. 상태 표시줄 스크립트는 환경에서 `COLUMNS`와 `LINES`도 받으므로(v2.1.153+) 터미널 크기에 맞춰 출력할 수 있습니다.

---

## TUI 모드(전체 화면)

> **v2.1.110에서 새로 추가**

TUI(Text User Interface) 모드는 Claude Code를 깜박임 없는 전체 화면으로 표시합니다 — tmux 같은 터미널 멀티플렉서나 iTerm2 분할 창에 적합합니다.

### TUI 모드 켜기

`/tui` 명령어로 렌더러를 바꾸거나, 실행하기 전에 `CLAUDE_CODE_NO_FLICKER=1`을 설정하세요:

```bash
/tui fullscreen               # 세션 안에서 전체 화면으로 전환
/tui default                  # 기존 렌더러로 되돌리기
CLAUDE_CODE_NO_FLICKER=1 claude  # 처음부터 전체 화면으로 시작
```

### 설정

| 설정 | 설명 | 기본값 |
|---------|-------------|---------|
| `autoScrollEnabled` | 최신 메시지로 자동 스크롤 | `true` |

`/config`나 `settings.json`에서 자동 스크롤을 끌 수 있습니다:

```json
{
  "autoScrollEnabled": false
}
```

### 집중 보기

`/focus` 명령어는 집중 보기를 켜고 끕니다 — 가장 관련 있는 출력만 보여 주는, 방해 요소 없는 화면입니다. 이제 `Ctrl+O`는 일반 대화 기록과 상세 대화 기록 사이만 전환합니다(집중 보기는 `/focus`).

---

## 음성 받아쓰기

음성 받아쓰기는 Claude Code에 눌러서 말하기 음성 입력을 제공하므로, 프롬프트를 입력하는 대신 말로 할 수 있습니다.

### 음성 받아쓰기 켜기

```
/voice
```

### 기능

| 기능 | 설명 |
|---------|-------------|
| **눌러서 말하기** | 키를 누르고 있으면 녹음되고, 떼면 전송 |
| **20개 언어** | 음성 인식이 20개 언어를 지원 |
| **사용자 정의 키 바인딩** | `/keybindings`로 눌러서 말하기 키 설정 |
| **계정 요구 사항** | 음성 인식 처리에 Claude.ai 계정이 필요 |

### 설정

키 바인딩 파일(`/keybindings`)에서 눌러서 말하기 키를 바꿀 수 있습니다. 음성 받아쓰기는 음성 인식 처리에 Claude.ai 계정을 씁니다.

---

## 채널

채널은 외부 서비스의 이벤트를 MCP 서버를 통해 실행 중인 Claude Code 세션으로 보내는 연구 미리 보기 기능입니다. Telegram, Discord, iMessage, 임의의 웹훅을 소스로 쓸 수 있어, Claude가 폴링 없이 실시간 알림에 반응할 수 있습니다.

> **인증 (v2.1.128+)**: 이제 `--channels`는 Pro/Max OAuth 인증과 API 키(콘솔) 인증 **모두**에서 동작합니다. 이전 릴리스에서는 OAuth가 필요했습니다.

### 채널 구독

```bash
# 시작할 때 채널 플러그인 구독
claude --channels plugin:telegram@claude-plugins-official

# 여러 소스 구독(공백으로 구분)
claude --channels plugin:discord@claude-plugins-official plugin:telegram@claude-plugins-official
```

### 지원하는 통합

| 통합 | 설명 |
|-------------|-------------|
| **Discord** | 세션에서 Discord 메시지를 받고 응답 |
| **Telegram** | 세션에서 Telegram 메시지를 받고 응답 |
| **iMessage** | 세션에서 iMessage 알림 받기 |
| **Webhooks** | 임의의 웹훅 소스에서 이벤트 받기 |

### 설정

시작할 때 `--channels` 플래그로 채널을 설정합니다. 엔터프라이즈 배포에서는 관리형 설정으로 허용할 채널 플러그인을 제어하세요:

```json
{
  "channelsEnabled": true,
  "allowedChannelPlugins": [
    { "marketplace": "claude-plugins-official", "plugin": "discord" },
    { "marketplace": "claude-plugins-official", "plugin": "telegram" }
  ]
}
```

`allowedChannelPlugins` 관리형 설정은 조직 전체에서 허용할 채널 플러그인을 제어합니다. Anthropic이 관리하는 허용 목록을 대체하며, `channelsEnabled: true`가 필요합니다.

### 동작 방식

1. MCP 서버가 외부 서비스에 연결하는 채널 플러그인 역할을 합니다
2. 들어오는 메시지와 이벤트가 활성 Claude Code 세션으로 전달됩니다
3. Claude가 세션 컨텍스트 안에서 메시지를 읽고 응답할 수 있습니다
4. 채널 플러그인은 Anthropic이 관리하는 허용 목록에 있거나, 관리자가 설정한 경우 조직의 `allowedChannelPlugins` 목록에 있어야 합니다
5. 폴링이 필요 없습니다 — 이벤트가 실시간으로 전달됩니다

---

## Chrome 통합

Chrome 통합은 Claude Code를 Chrome이나 Microsoft Edge 브라우저에 연결해 실시간 웹 자동화와 디버깅을 할 수 있게 합니다. v2.0.73+부터 쓸 수 있는 베타 기능입니다(Claude in Chrome 확장 v1.0.36+ 필요).

### Chrome 통합 켜기

**시작할 때**:

```bash
claude --chrome      # Chrome 연결 켜기
claude --no-chrome   # Chrome 연결 끄기
```

**세션 안에서**:

```
/chrome
```

"Enabled by default"(기본으로 켜기)를 고르면 이후 모든 세션에서 Chrome 통합이 켜집니다. Claude Code는 브라우저의 로그인 상태를 공유하므로 인증이 필요한 웹 앱과도 상호작용할 수 있습니다.

> **참고**: v2.1.290부터 프로젝트의 설정 파일로는 Chrome 통합을 켤 수 없습니다 — `--chrome`, `/chrome`, 사용자 설정을 쓰세요.

### 할 수 있는 일

| 기능 | 설명 |
|------------|-------------|
| **실시간 디버깅** | 콘솔 로그 읽기, DOM 요소 검사, JavaScript를 실시간으로 디버깅 |
| **디자인 검증** | 렌더링된 페이지를 디자인 목업과 비교 |
| **양식 검증** | 양식 제출, 입력 검증, 오류 처리 테스트 |
| **웹 앱 테스트** | 인증이 필요한 앱(Gmail, Google Docs, Notion 등)과 상호작용 |
| **데이터 추출** | 웹 페이지의 내용을 수집하고 처리 |
| **세션 녹화** | 브라우저 상호작용을 GIF 파일로 녹화 |

### 사이트별 권한

Chrome 확장은 사이트별 접근을 관리합니다. 확장 팝업에서 언제든 특정 사이트의 접근을 허용하거나 취소할 수 있습니다. Claude Code는 명시적으로 허용한 사이트와만 상호작용합니다.

### 동작 방식

Claude Code는 눈에 보이는 창에서 브라우저를 제어하므로 동작을 실시간으로 지켜볼 수 있습니다. 브라우저가 로그인 페이지나 CAPTCHA를 만나면 Claude는 멈추고, 사용자가 직접 처리할 때까지 기다린 뒤 계속합니다.

### 알려진 제한 사항

- **브라우저 지원**: Chrome과 Edge. Claude Code는 Brave, Arc, Vivaldi, Opera 같은 다른 Chromium 기반 브라우저에도 연결됩니다
- **WSL**: Windows Subsystem for Linux에서는 쓸 수 없음
- **서드파티 제공업체**: Bedrock, Vertex, Foundry API 제공업체에서는 지원되지 않음
- **서비스 워커 유휴 상태**: 세션이 길어지면 Chrome 확장의 서비스 워커가 유휴 상태가 될 수 있음

> **팁**: Chrome 통합은 베타 기능입니다. 이후 릴리스에서 지원 브라우저가 늘어날 수 있습니다.

---

## Remote Control

Remote Control을 쓰면 로컬에서 실행 중인 Claude Code 세션을 휴대폰, 태블릿, 또는 어떤 브라우저에서든 이어서 진행할 수 있습니다. 로컬 세션은 계속 내 컴퓨터에서 실행되며, 클라우드로 옮겨지는 것은 없습니다. Pro, Max, Team, Enterprise 요금제에서 쓸 수 있습니다(v2.1.51+).

Remote Control은 **더 이상 연구 미리 보기가 아닙니다** — 2026년 34주 차에 이 표시가 사라졌습니다. 이제 `claude remote-control`을 실행 중인 컴퓨터는 모두 Claude 앱의 Code 탭에 **기기 카드**로 나타납니다. 그래서 먼저 그 컴퓨터에서 세션을 시작한 뒤 연결할 필요 없이, 휴대폰에서 바로 그 컴퓨터의 세션을 시작할 수 있습니다.

### Remote Control 시작하기

**CLI에서**:

```bash
# 기본 세션 이름으로 시작
claude remote-control

# 사용자 지정 이름으로 시작
claude remote-control --name "인증 리팩토링"
```

**세션 안에서**:

```
/remote-control
/remote-control "인증 리팩토링"
```

**사용할 수 있는 플래그**:

| 플래그 | 설명 |
|------|-------------|
| `--name "title"` | 쉽게 알아볼 수 있도록 세션 제목 지정 |
| `--verbose` | 자세한 연결 로그 표시 |

> **참고 (v2.1.300)**: `claude remote-control`은 더 이상 `--sandbox`나 `--no-sandbox`를 받지 않습니다(원래 아무 효과가 없었으며, 이제 둘 중 하나를 넘기면 오류와 함께 종료됩니다). Remote Control 세션을 샌드박스에서 실행하려면 설정 파일에서 `sandbox.enabled`를 설정하세요.

### 세션에 연결하기

다른 기기에서는 세 가지 방법으로 연결할 수 있습니다.

1. **세션 URL** — 세션이 시작될 때 터미널에 출력됩니다. 아무 브라우저에서나 여세요
2. **QR 코드** — 시작한 뒤 `spacebar`를 누르면 스캔할 수 있는 QR 코드가 표시됩니다
3. **이름으로 찾기** — claude.ai/code나 Claude 모바일 앱(iOS/Android)에서 내 세션 목록을 살펴보세요

### 보안

- 내 컴퓨터에 **인바운드 포트를 열지 않음**
- TLS를 통한 **아웃바운드 HTTPS만** 사용
- **범위가 제한된 자격 증명** — 수명이 짧고 범위가 좁은 토큰 여러 개
- **세션 격리** — 원격 세션은 각각 독립적

### Remote Control과 웹용 Claude Code 비교

| 항목 | Remote Control | 웹용 Claude Code |
|--------|---------------|-------------------|
| **실행 위치** | 내 컴퓨터에서 실행 | Anthropic 클라우드에서 실행 |
| **로컬 도구** | 로컬 MCP 서버, 파일, CLI에 모두 접근 | 로컬 의존성 없음 |
| **활용 사례** | 다른 기기에서 로컬 작업 이어 가기 | 아무 브라우저에서나 새로 시작 |

### 제한 사항

- 대화형 Claude Code 프로세스 하나에 원격 세션 하나 — 서버 모드(`claude remote-control`)는 여러 세션을 동시에 처리합니다(`--capacity`, 기본값 32)
- 호스트 컴퓨터에서 터미널이 계속 열려 있어야 함
- 네트워크에 연결할 수 없으면 서버 모드는 약 10분 뒤에 종료됩니다. 대화형 세션은 계속 재시도하다가 네트워크가 돌아오면 다시 연결됩니다

### 활용 사례

- 자리를 비운 동안 모바일 기기나 태블릿에서 Claude Code 제어
- 로컬 도구 실행은 그대로 둔 채 더 풍부한 claude.ai UI 사용
- 이동 중에도 로컬 개발 환경 전체를 갖춘 채로 빠르게 코드 리뷰

### 푸시 알림 (v2.1.110)

Remote Control이 켜져 있고 `/config`에서 "Push when Claude decides"가 켜져 있으면, Claude가 휴대폰으로 모바일 푸시 알림을 보낼 수 있습니다. 예를 들어 오래 걸리는 작업이 끝났거나 사용자의 입력이 필요할 때입니다.

켜는 방법:
1. Remote Control 켜기: `/remote-control` 또는 `claude --rc`
2. `/config`를 열고 **Push when Claude decides**(Claude가 판단할 때 푸시) 켜기

푸시 알림을 받으려면 Claude 구독과 Claude 모바일 앱이 필요합니다.

### Remote Control 끄기 (`disableRemoteControl`, v2.1.128+)

Team이나 Enterprise 요금제의 관리자는 `disableRemoteControl` 설정으로 Remote Control을 완전히 막을 수 있습니다. 값이 `true`이면 `claude remote-control`과 `/remote-control` 모두 시작을 거부합니다.

```json
{
  "disableRemoteControl": true
}
```

이 설정은 **관리형/정책** 범위(예: macOS의 `/Library/Application Support/ClaudeCode/managed-settings.json`)에서 적용되므로 개별 사용자가 재정의할 수 없습니다. 조직 전체에 로컬 전용 실행을 강제해야 할 때 유용합니다.

> **API 키 사용 시 Remote Control 자동 비활성화 (v2.1.139)**: 다음 중 하나라도 설정되어 있으면, claude.ai로 함께 로그인했더라도 Remote Control이 **아무 알림 없이 꺼집니다**.
>
> - `ANTHROPIC_API_KEY`
> - `ANTHROPIC_AUTH_TOKEN`
> - `apiKeyHelper` (settings.json)
>
> 같은 조건에서 [`/schedule`](#예약-작업), claude.ai MCP 커넥터, 알림 설정도 꺼집니다 — claude.ai와 연결되는 이 네 가지 기능은 모두 OAuth 로그인이 활성 자격 증명일 때만 동작합니다. 이 기능들을 쓰려면 API 키 설정을 해제하세요(또는 Pro/Max OAuth 등급으로 실행).

---

## 웹 세션

웹 세션을 쓰면 claude.ai/code에서 브라우저로 Claude Code를 바로 실행하거나, CLI에서 웹 세션을 만들 수 있습니다.

### 웹 세션 만들기

```bash
# CLI에서 새 웹 세션 만들기
claude --remote "새 API 엔드포인트를 구현해 줘"
```

이렇게 하면 claude.ai에서 Claude Code 세션이 시작되며, 어떤 브라우저에서든 접속할 수 있습니다.

### 웹 세션을 로컬에서 재개하기

웹에서 시작한 세션을 로컬에서 이어 가려면:

```bash
# 로컬 터미널에서 웹 세션 재개 — 내 웹 세션을 고르는 선택 창이 열림
claude --teleport
```

또는 대화형 REPL 안에서:

```text
/teleport
```

`/tp`는 `/teleport`의 별칭입니다. 둘 다 claude.ai 구독이 필요합니다. 클라우드 세션에는
로컬에서 이어 가는 방법을 알려 주는 `/teleport` 안내가 표시됩니다(v2.1.223).

> **변경 로그 기반**: v2.1.223 변경 로그에는 알고 있는 세션으로 바로 이동하는 인수 형식
> `claude --teleport <session id>`가 나옵니다. CLI 레퍼런스에는 인수 없이 선택 창을 여는 형식만
> 문서화되어 있으므로, 세션 ID를 이미 알고 있는 경우가 아니라면 `claude --teleport`를 쓰세요.

### 활용 사례

- 한 컴퓨터에서 작업을 시작하고 다른 컴퓨터에서 이어 가기
- 팀원과 세션 URL 공유
- 웹 UI에서 시각적으로 diff를 검토한 다음, 실행할 때는 터미널로 전환

---

## 데스크톱 앱

Claude Code 데스크톱 앱은 시각적 diff 검토, 병렬 세션, 통합 커넥터를 갖춘 독립 실행형 애플리케이션입니다. macOS와 Windows에서 쓸 수 있습니다(Pro, Max, Team, Enterprise 요금제).

### 설치

[claude.ai](https://claude.ai)에서 플랫폼에 맞는 버전을 내려받으세요.
- **macOS**: 유니버설 빌드(Apple Silicon과 Intel)
- **Windows**: x64와 ARM64 설치 프로그램 제공

설치 방법은 [데스크톱 빠른 시작](https://code.claude.com/docs/ko/desktop-quickstart)을 참고하세요.

### CLI에서 넘기기

현재 CLI 세션을 데스크톱 앱으로 옮깁니다.

```
/desktop
```

### 핵심 기능

| 기능 | 설명 |
|---------|-------------|
| **Diff 보기** | 인라인 댓글을 달 수 있는 파일별 시각적 검토. Claude가 댓글을 읽고 수정합니다 |
| **앱 미리 보기** | 개발 서버를 자동으로 시작하고 내장 브라우저로 실시간 확인 |
| **PR 모니터링** | GitHub CLI 통합. CI 실패를 자동으로 고치고, 검사를 통과하면 자동 병합 |
| **병렬 세션** | 사이드바에서 여러 세션 사용. Git worktree로 자동 격리 |
| **예약 작업** | 앱이 열려 있는 동안 실행되는 반복 작업(매시간, 매일, 평일, 매주) |
| **풍부한 렌더링** | 구문 강조를 적용한 코드, 마크다운, 다이어그램 렌더링. GitHub Flavored Markdown 작업 목록 체크박스(`- [ ]` / `- [x]`)가 체크박스로 렌더링됩니다(v2.1.149+) |

### 앱 미리 보기 설정

`.claude/launch.json`에서 개발 서버 동작을 설정합니다.

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

### 커넥터

외부 서비스를 연결하면 더 풍부한 컨텍스트를 쓸 수 있습니다.

| 커넥터 | 기능 |
|-----------|------------|
| **GitHub** | PR 모니터링, 이슈 추적, 코드 리뷰 |
| **Slack** | 알림, 채널 컨텍스트 |
| **Linear** | 이슈 추적, 스프린트 관리 |
| **Notion** | 문서, 지식 베이스 접근 |
| **Asana** | 작업 관리, 프로젝트 추적 |
| **Calendar** | 일정 파악, 회의 컨텍스트 |

> **참고**: 원격(클라우드) 세션에서는 커넥터를 쓸 수 없습니다.

### 원격 세션과 SSH 세션

- **원격 세션**: Anthropic 클라우드 인프라에서 실행되며, 앱을 닫아도 계속 실행됩니다. claude.ai/code나 Claude 모바일 앱에서 접속할 수 있습니다
- **SSH 세션**: SSH로 원격 컴퓨터에 연결해 원격 파일 시스템과 도구에 모두 접근합니다. 원격 컴퓨터에 Claude Code가 설치되어 있어야 합니다

### 데스크톱의 권한 모드

데스크톱 앱은 CLI와 같은 권한 모드를 지원합니다.

| 모드 | 동작 |
|------|----------|
| **Manual** (기본값) | 모든 편집과 명령어를 검토하고 승인 |
| **Accept edits** | 파일 편집은 자동 승인, 명령어는 직접 승인 필요 |
| **Plan** | 변경하기 전에 접근 방식을 검토 |
| **Auto** | 일상적인 확인 없이 실행. 백그라운드 분류기가 먼저 작업을 검사 |
| **Bypass permissions** | 자동 실행(샌드박스 전용, 관리자가 제어) |

### 엔터프라이즈 기능

- **관리 콘솔**: 조직의 Code 탭 접근과 권한 설정 제어
- **MDM 배포**: macOS에서는 MDM으로, Windows에서는 MSIX로 배포
- **SSO 통합**: 조직 구성원에게 SSO(Single Sign-On) 로그인 요구
- **관리형 설정**: 팀 설정과 사용할 수 있는 모델을 중앙에서 관리

---

## 작업 목록

작업 목록은 컨텍스트 컴팩션(대화 기록을 컨텍스트 윈도우에 맞게 줄이는 일) 후에도 사라지지 않는 작업 추적 기능입니다.

### 작업 목록 켜고 끄기

세션 중에 `Ctrl+T`를 누르면 작업 목록 보기를 켜거나 끌 수 있습니다.

### 지속되는 작업

작업은 컨텍스트 컴팩션이 일어나도 유지되므로, 대화 컨텍스트가 줄어들어도 오래 걸리는 작업 항목을 잃지 않습니다. 여러 단계로 이루어진 복잡한 구현에 특히 유용합니다.

### 이름 붙은 작업 디렉토리

`CLAUDE_CODE_TASK_LIST_ID` 환경 변수를 쓰면 여러 세션이 공유하는 이름 붙은 작업 디렉토리를 만들 수 있습니다.

```bash
export CLAUDE_CODE_TASK_LIST_ID=my-project-sprint-3
```

이렇게 하면 여러 세션이 같은 작업 목록을 공유하므로, 팀 워크플로우나 여러 세션에 걸친 프로젝트에 유용합니다.

---

## 프롬프트 제안

프롬프트 제안은 git 기록과 현재 대화 컨텍스트를 바탕으로 흐린 회색 글씨로 예시 명령어를 보여 줍니다.

### 동작 방식

- 제안은 입력 프롬프트 아래에 흐린 회색 텍스트로 나타납니다
- `Tab`을 누르면 제안을 받아들입니다
- `Enter`를 누르면 제안을 받아들이고 바로 보냅니다
- 제안은 git 기록과 대화 상태를 바탕으로 컨텍스트에 맞게 만들어집니다

### 프롬프트 제안 끄기

```bash
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

---

## Git worktree

Git worktree를 쓰면 격리된 worktree에서 Claude Code를 시작할 수 있어, stash하거나 브랜치를 전환하지 않고도 여러 브랜치에서 병렬로 작업할 수 있습니다.

### worktree에서 시작하기

```bash
# 격리된 worktree에서 Claude Code 시작
claude --worktree
# 또는
claude -w
```

### worktree 위치

worktree는 다음 위치에 만들어집니다.
```
<repo>/.claude/worktrees/<name>
```

### 모노레포를 위한 스파스 체크아웃

모노레포에서는 `worktree.sparsePaths` 설정으로 sparse-checkout을 해서 디스크 사용량과 클론 시간을 줄일 수 있습니다.

```json
{
  "worktree": {
    "sparsePaths": ["packages/my-package", "shared/"]
  }
}
```

### 기준 브랜치 참조 (`worktree.baseRef`)

**`worktree.baseRef`** (v2.1.133에서 추가) — `claude --worktree`가 `origin/<default>`에서 브랜치를 만들지, 로컬 `HEAD`에서 만들지를 정합니다.

- `"fresh"` (기본값) — 로컬에서 푸시하지 않은 커밋은 무시하고 `origin/<default-branch>`에서 브랜치를 만듭니다. **이는 v2.1.128에서 도입된 동작을 되돌립니다**. 따라서 v2.1.128 이후 로컬 HEAD에서 브랜치를 만드는 동작에 의존하던 사용자는 다시 직접 설정해야 합니다.
- `"head"` — 로컬 `HEAD`에서 브랜치를 만들어, 푸시하지 않은 커밋을 그대로 유지합니다.

`~/.claude/settings.json`에서 설정합니다.

```json
{ "worktree": { "baseRef": "head" } }
```

### 백그라운드 세션 격리 (`worktree.bgIsolation`)

**`worktree.bgIsolation`** (v2.1.143에서 추가) — 백그라운드 세션(예: `/bg`, `claude --bg`, 에이전트 뷰에서 시작한 세션)이 자체 worktree를 쓸지, 포그라운드 작업 사본을 직접 편집할지를 정합니다.

- *(기본값)* — 백그라운드 세션은 `--worktree`와 같은 방식으로 `<repo>/.claude/worktrees/` 아래에 격리된 worktree를 만듭니다.
- `"none"` — 백그라운드 세션이 현재 작업 사본을 직접 편집합니다. worktree를 쓰기 어려울 때(예: 무거운 네이티브 빌드 산출물이 있을 때)나 백그라운드 에이전트가 포그라운드 세션과 편집을 조율해야 할 때 쓰세요.

```json
{ "worktree": { "bgIsolation": "none" } }
```

트레이드오프: `"none"`은 worktree 격리라는 안전망을 없앱니다 — 백그라운드 세션과 포그라운드 세션이 동시에 편집하면 실제 작업 사본에서 병합 충돌이 생길 수 있습니다.

### worktree 도구와 훅

| 항목 | 설명 |
|------|-------------|
| `EnterWorktree` | worktree에 들어가는 도구. v2.1.157부터 세션 도중에 Claude가 관리하는 worktree 사이를 전환할 수 있습니다 |
| `ExitWorktree` | 현재 worktree에서 나와 정리하는 도구 |
| `WorktreeCreate` | worktree가 만들어질 때 발생하는 훅 이벤트 |
| `WorktreeRemove` | worktree가 제거될 때 발생하는 훅 이벤트 |

v2.1.157부터는 에이전트가 끝나도 Claude가 관리하는 worktree가 잠기지 않은 상태로 남으므로, `git worktree remove`/`prune`으로 정리할 수 있습니다.

### 자동 정리

worktree에서 아무것도 변경하지 않았다면 세션이 끝날 때 자동으로 정리됩니다.

### 활용 사례

- main 브랜치는 건드리지 않은 채 기능 브랜치에서 작업
- 작업 디렉토리에 영향을 주지 않고 격리된 환경에서 테스트 실행
- 쓰고 버릴 수 있는 환경에서 실험적인 변경 시도
- 모노레포에서 특정 패키지만 스파스 체크아웃해 더 빠르게 시작

---

## 샌드박싱

샌드박싱은 Claude Code가 실행하는 Bash 명령어에 OS 수준의 파일 시스템 격리와 네트워크 격리를 제공합니다. 권한 규칙을 보완하며, 보안 계층을 하나 더 더해 줍니다.

### 샌드박싱 켜기

**슬래시 명령어** (선택한 값을 이 프로젝트의 `.claude/settings.local.json`에 저장):
```text
/sandbox
```

**설정 파일** (모든 프로젝트): `~/.claude/settings.json`에서 `"sandbox": { "enabled": true }`를 설정합니다.

**세션 단위**로, 설정 파일을 쓰지 않고 켜려면:
```bash
claude --settings '{"sandbox": {"enabled": true}}'
```

> `claude --sandbox` / `--no-sandbox` 플래그는 없습니다. v2.1.300부터는 이 플래그를 `claude remote-control`에 넘기면 오류와 함께 종료됩니다.

### 설정 항목

| 설정 | 설명 |
|---------|-------------|
| `sandbox.enabled` | 샌드박싱 켜기 또는 끄기 |
| `sandbox.failIfUnavailable` | 샌드박싱을 켤 수 없으면 실패 처리 |
| `sandbox.filesystem.allowWrite` | 쓰기를 허용할 경로 |
| `sandbox.filesystem.allowRead` | 읽기를 허용할 경로 |
| `sandbox.filesystem.denyRead` | 읽기를 거부할 경로 |
| `sandbox.network.allowedDomains` | Bash로 실행한 프로세스가 접속할 수 있는 도메인(`*.` 와일드카드 지원) |
| `sandbox.network.deniedDomains` | `allowedDomains` 와일드카드가 허용하더라도 차단할 도메인(v2.1.113+) |
| `sandbox.network.strictAllowlist` | (v2.1.219) 샌드박스 안의 명령어가 허용 목록에 없는 호스트에 접속하면 묻지 않고 거부 |
| `sandbox.enableWeakerNetworkIsolation` | macOS에서 더 약한 네트워크 격리 사용 |
| `sandbox.bwrapPath` | (v2.1.133+, Linux/WSL) `bubblewrap` 바이너리 경로. 기본값: `$PATH`에서 찾음. |
| `sandbox.socatPath` | (v2.1.133+, Linux/WSL) `socat` 바이너리 경로. 기본값: `$PATH`에서 찾음. |
| `sandbox.credentials` | (v2.1.187+) 샌드박스 안의 명령어가 자격 증명 파일과 비밀 환경 변수를 읽지 못하게 막음. |
| `sandbox.allowAppleEvents` | (v2.1.181+, macOS) 샌드박스 안의 명령어가 Apple Events를 보낼 수 있도록 명시적으로 허용. |
| `sandbox.filesystem.disabled` | (v2.1.216+) 네트워크 격리는 유지한 채 파일 시스템 격리만 완전히 건너뜀 — 파일 샌드박싱 때문에 도구가 동작하지 않지만 네트워크 송신 제어는 유지해야 할 때 유용합니다. 사용자 설정, 관리형 설정, `--settings`에서만 적용되며 프로젝트 설정으로는 설정할 수 없습니다. |

**Linux/WSL 바이너리 경로** (v2.1.133+) — 표준이 아닌 위치에 설치한 바이너리를 Claude Code가 쓰도록 지정합니다.

```json
{
  "sandbox": {
    "bwrapPath": "/opt/bubblewrap/bin/bwrap",
    "socatPath": "/opt/socat/bin/socat"
  }
}
```

넓은 와일드카드를 `deniedDomains`가 덮어쓰는 예(v2.1.113+):

```json
{
  "sandbox": {
    "network": {
      "allowedDomains": ["*.example.com"],
      "deniedDomains": ["evil.example.com"]
    }
  }
}
```

와일드카드는 `example.com`의 모든 호스트를 허용하지만, `deniedDomains`에 이름을 명시한 호스트는 여전히 차단됩니다.

> **참고** (v2.1.243): 샌드박스 Bash 도구의 권한 확인 창은 **더 이상 허용된 네트워크 호스트를 나열하지 않습니다**. Claude는 그냥 요청을 시도하고, 새 호스트가 나올 때마다 사용자가 승인합니다 — 그러니 확인 창이 허용 목록을 미리 보여 줄 거라고 기대하지 마세요. 같은 릴리스에서는 차단된 명령어가 우연히 `0`으로 종료될 때 네트워크 위반 정보가 사라지던 문제도 고쳐졌으므로, 겉보기에 조용히 성공한 경우에도 무엇이 차단되었는지 보고됩니다.

### 자격 증명 마스킹 (v2.1.221, v2.1.224)

> **변경 로그 기반**: 이 `sandbox.credentials` 옵션들은 v2.1.221과 v2.1.224 변경 로그 항목에서
> 가져온 것으로, 설정 레퍼런스에는 아직 자세히 나와 있지 않습니다.

v2.1.221 이전에는 `sandbox.credentials`로 자격 증명 파일을 `deny`(거부)하는 것만 가능했습니다 — 그
자격 증명이 필요한 샌드박스 명령어는 그냥 실패했습니다. `mode: "mask"`는 비밀 값을 노출하지 않고도
명령어가 동작하게 합니다. 샌드박스 안의 프로세스는 파일의 **대리 값(sentinel)** 사본을 읽고,
샌드박스 프록시가 네트워크로 나가는 요청에서 실제 값으로 바꿔 넣습니다.

```json
{
  "sandbox": {
    "network": { "tlsTerminate": true },
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "mask" }
      ]
    }
  }
}
```

| 기능 | 도입 버전 | 하는 일 |
|---|---|---|
| 자격 증명 **파일**에 `mode: "mask"` | v2.1.221 | 샌드박스 안의 명령어는 대리 값을 읽고, 프록시가 외부로 나가는 요청에서 실제 값으로 바꿔 넣습니다. **Linux와 WSL 전용** — macOS에서는 파일 마스킹 대신 `deny`가 적용됩니다. |
| `extract` / `onExtractNoMatch` | v2.1.224 | 구조화된 환경 변수 값에서 변수 전체 대신 필드 하나만 마스킹하고, 패턴이 일치하지 않을 때의 동작을 정합니다. |
| `decode: "jwt"`와 `maskClaims` | v2.1.224 | JWT를 디코딩해 지정한 클레임만 마스킹하고 나머지는 읽을 수 있게 둡니다. |
| `awsPairs` / `sigv4` | v2.1.224 | 프록시에서 실제 액세스 키로 바꿔 넣은 뒤 AWS SigV4 요청에 다시 서명합니다. |

**놓치기 쉬운 두 가지 제약:**

- 모든 마스킹에는 `network.tlsTerminate`가 필요합니다 — 값을 바꿔 넣으려면 프록시가 요청 내부를
  볼 수 있어야 합니다.
- 이 옵션들은 사용자 설정, 관리형 설정, `--settings`에서**만** 적용됩니다.
  프로젝트 설정으로는 마스킹을 켜거나 마스킹 대상을 바꿀 수 없습니다.

### 설정 예

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "filesystem": {
      "allowWrite": ["/Users/me/project"],
      "allowRead": ["/Users/me/project", "/usr/local/lib"],
      "denyRead": ["/Users/me/.ssh", "/Users/me/.aws"]
    }
  }
}
```

### 동작 방식

- Bash 명령어는 파일 시스템 접근이 제한된 샌드박스 환경에서 실행됩니다
- 의도하지 않은 외부 연결을 막도록 네트워크 접근을 격리할 수 있습니다
- 권한 규칙과 함께 동작해 다층 방어를 이룹니다
- macOS에서는 Seatbelt가 샌드박스 프록시로 가는 연결을 제외한 모든 네트워크 연결을 차단합니다. `sandbox.enableWeakerNetworkIsolation`은 이 격리를 **약화**하며, MITM `httpProxyPort` 프록시 뒤에서 동작하는 Go CLI 같은 도구만을 위한 것입니다

### 활용 사례

- 신뢰할 수 없는 코드나 생성된 코드를 안전하게 실행
- 프로젝트 밖의 파일이 실수로 수정되는 것을 방지
- 자동화된 작업 중 네트워크 접근 제한

---

## 관리형 설정(엔터프라이즈)

관리형 설정을 쓰면 엔터프라이즈 관리자가 각 플랫폼 고유의 관리 도구로 조직 전체에 Claude Code 설정을 배포할 수 있습니다.

### 배포 방법

| 플랫폼 | 방법 | 도입 버전 |
|----------|--------|-------|
| macOS | 관리형 plist 파일(MDM) | v2.1.51+ |
| Windows | Windows 레지스트리 | v2.1.51+ |
| 크로스 플랫폼 | 관리형 설정 파일 | v2.1.51+ |
| 크로스 플랫폼 | 관리형 드롭인(`managed-settings.d/` 디렉토리) | v2.1.83+ |

### 관리형 드롭인

v2.1.83부터 관리자는 여러 관리형 설정 파일을 `managed-settings.d/` 디렉토리에 배포할 수 있습니다. 파일은 알파벳순으로 병합되므로 팀별로 설정을 모듈화할 수 있습니다. 이 디렉토리는 시스템 디렉토리의 `managed-settings.json` 옆에 있습니다(macOS는 `/Library/Application Support/ClaudeCode/`, Linux는 `/etc/claude-code/`, Windows는 `C:\Program Files\ClaudeCode\`).

```
/etc/claude-code/managed-settings.d/
  00-org-defaults.json
  10-team-policies.json
  20-project-overrides.json
```

### 사용할 수 있는 관리형 설정

| 설정 | 설명 |
|---------|-------------|
| `permissions.disableBypassPermissionsMode` | `"disable"`로 설정하면 사용자가 권한 우회 모드를 켤 수 없음 |
| `availableModels` | 사용자가 선택할 수 있는 모델 제한 |
| `enforceAvailableModels` | (v2.1.175) `true`이면 `availableModels` 허용 목록이 **기본(Default)** 모델에도 *함께* 적용됩니다 — 설정된 기본 모델이 목록에 없으면 Claude Code는 허용된 첫 번째 모델을 대신 씁니다. 사용자 설정과 프로젝트 설정으로는 더 이상 관리형 `availableModels` 목록을 넓힐 수 없습니다. |
| `allowedChannelPlugins` | 허용할 채널 플러그인 제어 |
| `autoMode.environment` | 자동 모드에서 신뢰할 인프라 설정 |
| `workflowSizeGuideline` | (v2.1.219) 권고용 [동적 워크플로우 규모 가이드라인](#동적-워크플로우) 설정. 관리형 설정뿐 아니라 어떤 설정 파일에서도 읽으며, 이 값이 설정되어 있는 동안에는 `/config`에서 **Dynamic workflow size** 행이 숨겨집니다 |
| `wslInheritsWindowsSettings` | Windows/WSL 전용(v2.1.118+): `true`이면 WSL 안에서 실행되는 Claude Code가 Windows 호스트의 관리형 설정을 상속하므로, 레지스트리/MDM으로 배포한 엔터프라이즈 정책이 Windows 셸과 WSL 셸에 똑같이 적용됩니다 |
| `parentSettingsBehavior` | (v2.1.133+, 관리자 등급) SDK의 `managedSettings`가 부모 프로세스 설정과 병합되는 방식을 제어합니다. `"first-wins"`는 기존 우선순위를 유지하고(충돌하면 먼저 정해진 설정이 이김), `"merge"`는 값을 깊은 병합합니다. |
| 사용자 지정 정책 | 조직별 권한 정책과 도구 정책 |

### 예: macOS plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>permissions</key>
  <dict>
    <key>disableBypassPermissionsMode</key>
    <string>disable</string>
  </dict>
  <key>availableModels</key>
  <array>
    <string>claude-sonnet-4-6</string>
    <string>claude-haiku-4-5</string>
  </array>
</dict>
</plist>
```

---

## 설정과 구성

### 설정 파일 위치

1. **사용자 설정**: `~/.claude/settings.json`
2. **프로젝트 설정**: `.claude/settings.json` (저장소에 체크인)
3. **로컬 프로젝트 설정**: `.claude/settings.local.json` (체크인하지 않음)
4. **관리형 설정**: 시스템 디렉토리의 `managed-settings.json` ([관리형 설정](#관리형-설정엔터프라이즈) 참고)

### 전체 설정 예

**핵심 고급 기능 설정** (`.claude/settings.json`):

```json
{
  "permissions": {
    "defaultMode": "manual"
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit", "hooks": [{ "type": "command", "command": "~/.claude/hooks/eslint-fix.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": "Write", "hooks": [{ "type": "command", "command": "~/.claude/hooks/security-scan.sh" }] }
    ]
  }
}
```

훅 스크립트는 도구 입력을 stdin에서 JSON으로 받습니다(예: `tool_input.file_path`). `${file_path}` 같은 치환은 없습니다. MCP 서버는 설정 키가 아닙니다 — 프로젝트 루트의 `.mcp.json`에 정의하세요.

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}" }
    }
  }
}
```

**확장 설정 예:**

```json
{
  "permissions": {
    "defaultMode": "manual",
    "allow": ["Bash(git log:*)", "Read"],
    "deny": ["Bash(rm -rf:*)"]
  },

  "hooks": {
    "PreToolUse": [{ "matcher": "Edit", "hooks": [{ "type": "command", "command": "~/.claude/hooks/eslint-fix.sh" }] }],
    "PostToolUse": [{ "matcher": "Write", "hooks": [{ "type": "command", "command": "~/.claude/hooks/security-scan.sh" }] }],
    "Stop": [{ "hooks": [{ "type": "command", "command": "~/.claude/hooks/notify.sh" }] }]
  }
}
```

이 설정에 쓰는 GitHub MCP 서버는 위에서 본 것처럼 `.mcp.json`에 둡니다.

### 사용자별 추가 설정

다음 키는 `~/.claude/settings.json`(또는 프로젝트의 `.claude/settings.json`)에 넣으며, 개별 사용자의 대화형 동작을 제어합니다.

| 설정 | 설명 |
|---------|-------------|
| `askUserQuestionTimeout` | 응답하지 않은 `AskUserQuestion` 대화 상자를 일정 시간 입력이 없으면 자동으로 계속 진행합니다. **v2.1.200**부터는 대화 상자가 기본적으로 자동 진행되지 않으므로, 시간 제한 자동 진행을 다시 쓰려면 이 값을 설정하세요. |
| `enableArtifact` | 사용자별로 Artifact 도구 켜기/끄기(v2.1.196). |
| `crossSessionInbound` | (v2.1.224) 들어오는 [세션 간 메시지](#세션-간-메시지)를 처리하는 방식 — `"accept"`, `"hold"`, `"refuse"` 중 하나. 프로젝트와 로컬 값은 `accept < hold < refuse` 순서에서 *더 엄격할* 때만 적용됩니다. v2.1.232부터 `/config`에 "Messages from your other sessions"(다른 세션에서 온 메시지)로 표시됩니다. |
| `dialogExpiry` | (v2.1.224) 응답하지 않은 대화 상자가 열려 있는 시간. 기본값은 `"5m"`이며 `"60s"`, `"5m"`, `"10m"`, `"never"`를 받습니다. `CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS`가 이 값을 재정의합니다. v2.1.232부터 `/config`에 "Dialog expiry"(대화 상자 만료)로 표시됩니다. |
| `modelPicker` | (v2.1.243) `/model` 선택 창에 표시할 모델을 원하는 순서와 이름표로 고릅니다. 설정 계층 사이에서 **병합되지 않고 대체되는** 몇 안 되는 설정 중 하나로, 가장 가까운 범위의 값이 그대로 이깁니다. |
| `promptCacheTtl` | (v2.1.243) 메인 대화의 프롬프트 캐시 수명을 고릅니다. |
| `subagentPromptCacheTtl` | (v2.1.243) 서브에이전트와 메인 대화 밖의 다른 요청에 대해 같은 선택을 합니다. |
| `modelPricing` | (v2.1.243) **관리형 설정.** 조직의 계약 요금을 지정해 `/cost`, 상태 표시줄, 텔레메트리가 정가 대신 그 요금으로 보고하게 합니다. |
| `keybindingFlavor` | **v2.1.261부터 지원 중단되었으며 아무 효과가 없습니다.** 프롬프트의 단어 편집 키는 Bash처럼 항상 readline 규칙을 따릅니다. `Ctrl+W`는 공백까지 뒤로 지우고, `Alt+F`와 `Alt+D`는 단어 끝에서 멈추며, 문장 부호는 단어를 나눕니다. Claude Code는 여전히 이 키를 받아들이므로, 이 키를 설정한 설정 파일도 그대로 유효합니다. (v2.1.238–v2.1.260에서는 `"classic"`과 `"readline"` 중에서 골랐습니다.) |
| `spellcheck` | (v2.1.235) `PATH`에 있는 `aspell`, `hunspell`, `ispell` 중 하나를 이 순서대로 찾아 프롬프트 입력의 맞춤법 오류에 밑줄을 긋습니다. 값은 객체 형식 — `{"enabled": true, "language": "en_GB"}` — 이며 기본값은 꺼짐입니다. **사용자 설정, `--settings` 플래그, 관리형 설정에서만 읽습니다**: 프로젝트의 `.claude/settings.json`이나 `.claude/settings.local.json`에 있는 `spellcheck` 블록은 무시됩니다. |
| `bashOutputMaxChars` | (v2.1.261) **성공한** Bash나 PowerShell 명령어의 출력 중 Claude가 인라인으로 받는 글자 수(최대 128K). 한도를 넘으면 Claude Code가 출력을 파일에 저장하고, Claude는 짧은 미리 보기와 파일 경로를 받습니다. 이 값을 설정하면 Claude Code는 `BASH_MAX_OUTPUT_LENGTH`를 무시합니다. |
| `taskOutputMaxChars` | (v2.1.261) **v2.1.278에서 대체되었으며 아무 효과가 없습니다.** 예전에는 `TaskOutput` 도구로 **백그라운드 작업**의 출력을 읽을 때 Claude가 인라인으로 받는 글자 수를 제한했습니다. v2.1.278에서 `TaskOutput` 도구가 제거되었으므로(이제 Claude는 `Read`로 백그라운드 작업의 출력 파일을 읽습니다) 이 키와 `TASK_MAX_OUTPUT_LENGTH` 모두 효과가 없습니다. Claude Code는 여전히 이 키를 받아들이므로, 이 키를 설정한 설정 파일도 그대로 유효합니다. |
| `maxEffortLevel` | (v2.1.267) Bedrock, Vertex, Foundry를 포함한 모든 제공업체에서 Claude Code가 쓸 수 있는 노력 수준의 상한을 정합니다. 최상위에 설정하거나 `modelSettings` 아래에 모델별로 설정합니다. 사용자는 여전히 더 낮은 수준을 고를 수 있습니다. |
| `bashEditDiffEnabled` | (v2.1.269) Bash 도구 결과에 명령어가 변경한 파일의 diff를 포함합니다. |
| `syncClaudeAiSkills` / `syncClaudeAiPlugins` | (v2.1.275) 둘 중 하나를 `false`로 설정하면 claude.ai 계정에서 켠 스킬이나 플러그인을 터미널 세션으로 동기화하지 않습니다. |

### 대체 모델 (`fallbackModel`)

`fallbackModel` 설정으로 기본 모델이 과부하 상태이거나 사용할 수 없을 때 차례로 시도할 대체 모델을 **최대 세 개**까지 설정할 수 있습니다.

```json
{
  "fallbackModel": ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5"]
}
```

**v2.1.166**부터 `--fallback-model` 플래그는 헤드리스 세션뿐 아니라 대화형 세션에도 적용됩니다. 대체 모델로 넘어갈 때 Claude Code는 원래 재시도하지 않는 예기치 않은 오류를 한 번 재시도합니다. 인증, 속도 제한, 요청 크기, 전송 오류는 여전히 바로 실패합니다.

### 환경 변수

환경 변수로 설정을 재정의할 수 있습니다.

```bash
# 모델 선택
export ANTHROPIC_MODEL=claude-opus-4-8
export ANTHROPIC_DEFAULT_MODEL=claude-opus-4-8   # (v2.1.236) 새 세션이 시작할 때 쓰는 모델. ANTHROPIC_MODEL과 달리 /model로 고른 모델이 여전히 우선하며, 그 선택은 재시작 후에도 유지됨
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-8
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5

# API 설정
export ANTHROPIC_API_KEY=sk-ant-...

# 사고 설정
export MAX_THINKING_TOKENS=16000
export CLAUDE_CODE_EFFORT_LEVEL=high   # low, medium, high, xhigh(Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8/4.7), max 중 하나 — Opus 5와 Opus 4.8의 기본값은 high(Opus 5.5, Sonnet 5.5, Haiku 5.5, Opus 5, Sonnet 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6에서 지원)

# 기능 토글
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1    # 자동 메모리 끄기(자동 메모리 파일을 만들거나 로드하지 않음)
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=true
export CLAUDE_CODE_DISABLE_CRON=1
export CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=true
export CLAUDE_CODE_DISABLE_TERMINAL_TITLE=true
export CLAUDE_CODE_DISABLE_1M_CONTEXT=true
export CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK=true
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
export CLAUDE_CODE_ENABLE_TASKS=0          # 기본은 작업(Task) 도구. 0이면 예전 TodoWrite 도구로 되돌림
export CLAUDE_CODE_SIMPLE=true              # --bare 플래그가 설정함

# MCP 설정
export MAX_MCP_OUTPUT_TOKENS=50000
export ENABLE_TOOL_SEARCH=true

# 프롬프트 캐싱
export ENABLE_PROMPT_CACHING_1H=1      # 모든 요청에 1시간 캐시 TTL 요청(기본값: 구독에서는 메인 대화가 1시간, API 키/클라우드 제공업체에서는 5분)

# 작업 관리
export CLAUDE_CODE_TASK_LIST_ID=my-project-tasks

# 에이전트 팀(실험적 기능)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 서브에이전트와 플러그인 설정
export CLAUDE_CODE_SUBAGENT_MODEL=sonnet
export CLAUDE_CODE_PLUGIN_SEED_DIR=./my-plugins
export CLAUDE_CODE_NEW_INIT=1

# 하위 프로세스와 스트리밍
export CLAUDE_CODE_SUBPROCESS_ENV_SCRUB="SECRET_KEY,DB_PASSWORD"
export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=80
export CLAUDE_STREAM_IDLE_TIMEOUT_MS=30000
export ANTHROPIC_CUSTOM_MODEL_OPTION=my-custom-model
export SLASH_COMMAND_TOOL_CHAR_BUDGET=50000

# 출력과 패키지 관리자(v2.1.129+)
export CLAUDE_CODE_FORCE_SYNC_OUTPUT=1                      # 자동 감지가 놓치는 터미널(Emacs eat 등)에서 동기 출력 강제
export CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1            # Homebrew/WinGet 설치에서 백그라운드 업그레이드 켜기
export CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1         # ANTHROPIC_BASE_URL이 설정되어 있을 때 /v1/models 게이트웨이 탐색 사용

# Windows PowerShell 도구(v2.1.143+) — Windows의 Bedrock/Vertex/Foundry에서는 기본으로 켜짐
export CLAUDE_CODE_USE_POWERSHELL_TOOL=0                    # PowerShell 도구를 완전히 끄기
export CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1    # `-ExecutionPolicy Bypass` 대신 시스템 ExecutionPolicy 따르기

# 워크로드 아이덴티티 페더레이션(v2.1.141+)
export ANTHROPIC_WORKSPACE_ID=ws_abc123                     # 규칙이 여러 작업 공간에 해당할 때 페더레이션 토큰을 특정 작업 공간으로 한정

# Stop 훅 안전 상한(v2.1.143+)
export CLAUDE_CODE_STOP_HOOK_BLOCK_CAP=8                    # 세션이 경고와 함께 끝나기 전까지 허용하는 연속 Stop 훅 차단 횟수. 0이면 상한 없음.

# 세션 전체 실행 상한(v2.1.212)
export CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION=200         # 검색이 끝없이 반복되는 것을 막기 위한 세션당 WebSearch 도구 호출 상한. 기본값 200.
export CLAUDE_CODE_WEB_SEARCH_REFILLS_PER_HOUR=100       # (v2.1.290) 그 예산이 다시 채워지는 속도(시간당 호출 수). 기본값은 대화형에서 100, -p에서는 0(다시 채우지 않음).

# 접근성(v2.1.208)
export CLAUDE_AX_SCREEN_READER=1                            # 일반 텍스트 화면 낭독기 렌더링 모드 켜기. --ax-screen-reader나 설정의 "axScreenReader": true와 같은 효과.

# 새 변수(v2.1.221–v2.1.234) — 변경 로그 기반. CLI 레퍼런스에는 환경 변수 섹션이 없음
export CLAUDE_CODE_ENABLE_TODO_TOOLS=1                      # (v2.1.233) 할 일/작업 추적 도구(TaskCreate/Get/Update/List, TodoWrite)를 되살림. 이 도구들은 Claude 3.x 모델, Opus 4부터 4.7까지, Sonnet 4부터 4.6까지, Haiku 4.5에서만 기본으로 제공됨(v2.1.268)
export CLAUDE_CODE_WEBFETCH_CACHE_TTL_MS=900000             # (v2.1.233) WebFetch URL 캐시 TTL. 기본값 15분.
export CLAUDE_CODE_TOOL_MEMORY_LIMIT=2G                     # (v2.1.233, Linux) Bash 명령어에 적용하는 메모리 cgroup(직접 켜야 적용됨)
export ANTHROPIC_BEDROCK_REGION_PREFIX=us                   # (v2.1.224) 특정 Bedrock 교차 리전 추론 프로필을 우선 사용
export CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1  # (v2.1.223) 인식되지 않는 모델 ID에 대해 v2.1.223 이전의 자동 컴팩션 동작으로 되돌림
export CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS=0             # (v2.1.229) 동적 워크플로우 팬아웃에서 프리픽스 시차 실행 끄기
export CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS=300000            # (v2.1.224) dialogExpiry 설정을 재정의
export CLAUDE_CODE_PROJECT_DIR_NAME=my-app                  # (v2.1.234) 프로젝트별 대화 기록 디렉토리의 짧은 이름. 세션마다 별도 설정 디렉토리를 주는 호스트용
export CLAUDE_CODE_GOAL_CHECKIN_MINUTES=30                  # (v2.1.234) /goal이 활성일 때 백그라운드 작업이 멈춘 뒤 Claude가 확인하러 오기까지의 시간(분). 0이면 확인하지 않음.

# 새 변수(v2.1.268-v2.1.278) - 변경 로그 기반
export CLAUDE_CODE_MCP_STARTUP_WAIT_MS=5000                 # (v2.1.274) 첫 비대화형 턴이 아직 연결 중인 MCP 서버를 기다리는 시간. 0이면 기다리지 않음. 단, --allowedTools나 mcp_tool 훅이 지정한 서버는 예외(여전히 최대 2초, v2.1.284+).
export CLAUDE_CODE_WEBFETCH_DEADLINE_MS=300000              # (v2.1.268) WebFetch에 새로 생긴 300초 마감 시간을 재정의. 0이면 마감 시간 없음.
export CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS=32        # (v2.1.269) Workflow 도구의 실행당 동시 에이전트 한도를 높임. 1-256 사이 값.
export CLAUDE_CODE_AUTO_MODE_SERVER=0                       # (v2.1.278. Anthropic API 직접 연결은 v2.1.281부터) 서버 측 자동 모드 분류기 검토를 쓰지 않음

# 새 변수(v2.1.299-v2.1.300)
export CLAUDE_CODE_DISABLE_FILE_MENTIONS=1                  # (v2.1.299) @ 파일/디렉토리 멘션을 펼치지 않음. Claude는 경로만 받고 파일 도구로 읽음. 프로젝트/로컬 설정에서는 무시됨.
export CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS=200000           # (v2.1.299, v2.1.290+ 필요) 유휴 컴팩션이 적용되는 컨텍스트 크기. 기본값 200000, 최솟값 100000. "idleCompaction": false로 끔.
export CLAUDE_CODE_GZIP_REQUEST_BODIES=0                    # (v2.1.300) api.anthropic.com으로 보내는 큰 요청 본문의 gzip 압축 끄기(TLS를 검사하는 프록시가 이를 제대로 처리하지 못할 때 사용).
export CLAUDE_CODE_ARTIFACT_PUBLISH_EDITS=0                 # (v2.1.300) 게시하면서 편집하는 대신, 파일 도구로 아티팩트 파일을 편집한 뒤 별도 단계로 게시.

# 새 변수(v2.1.301-v2.1.302)
export CLAUDE_CODE_AUTO_MODE_MODEL=claude-sonnet-5-5  # 클라이언트 측 자동 모드 분류기 모델(v2.1.302)
export CLAUDE_CODE_RETRY_WATCHDOG_MAX_USAGE_LIMIT_WAIT_MS=3600000  # 한참 뒤에 초기화되는 사용 한도는 기다리지 않음(v2.1.301)
```

> **v2.1.223 — `CLAUDE_CODE_DISABLE_1M_CONTEXT` 적용 범위 확대**: 이제 이 변수는 정해진 모델 ID 목록만이 아니라
> 1M 토큰 창을 기본으로 갖춘 **모든** Claude 모델을 자동 컴팩션으로 200K까지로 묶어 둡니다.

> **v2.1.108**: `ENABLE_PROMPT_CACHING_1H=1` — 메인 대화와 기타 요청에 1시간 프롬프트 캐시 TTL을 요청합니다. 이 값이 없으면 메인 대화는 요금제 사용량 안에서 쓰는 Claude 구독에서는 1시간, API 키·사용량 크레딧·클라우드 제공업체에서는 5분을 받습니다. `FORCE_PROMPT_CACHING_5M=1`은 5분으로 강제합니다. (v2.1.129에서 1시간 TTL이 아무 알림 없이 5분으로 낮아지던 회귀가 고쳐졌습니다.)

> **v2.1.129**: `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1`은 기능 자동 감지가 실패하는 터미널(예: Emacs `eat`)에서 동기 출력을 강제합니다. `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1`은 원래 자동 업데이트되지 않는 Homebrew/WinGet 설치에서 백그라운드 업그레이드를 켭니다.

### 설정 관리 명령어

```
사용자: /config
[대화형 설정 메뉴가 열림]
```

`/config` 명령어는 다음과 같은 설정을 바꿀 수 있는 대화형 메뉴를 엽니다.
- 확장 사고 켜기/끄기
- 자세한 출력
- 권한 모드
- 모델 선택
- 동적 워크플로우 규모(v2.1.219) — 설정 파일에 `workflowSizeGuideline`이 설정되어 있으면 숨겨짐. [동적 워크플로우](#동적-워크플로우) 참고
- 유휴 컴팩션(v2.1.302)

대화형 메뉴에서 Enter나 Space를 누르면 선택한 설정이 바뀌고, Esc를 누르면 저장하고 닫힙니다(v2.1.183+).

메뉴를 열지 않고 프롬프트에서 바로 설정을 지정할 수도 있습니다.

```bash
/config thinking=false      # 설정 하나를 인라인으로 지정(v2.1.181+)
/config --help              # 쓸 수 있는 약식 키 목록 보기(v2.1.183+)
```

`key=value` 약식은 대화형 세션, `-p`, Remote Control에서 동작합니다.

### 프로젝트별 설정

프로젝트에 `.claude/settings.json`을 만드세요.

```json
{
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "npm test && npm run lint" }] }]
  },
  "permissions": {
    "defaultMode": "manual"
  }
}
```

프로젝트의 MCP 서버는 프로젝트 루트의 `.mcp.json`에 넣으세요.

```json
{
  "mcpServers": {
    "project-db": {
      "command": "mcp-postgres",
      "env": {
        "DATABASE_URL": "${PROJECT_DB_URL}"
      }
    }
  }
}
```

---

## 신뢰와 권한 범위

> **변경 로그 기반 (v2.1.222, v2.1.232)**: 이 강화 사항들은 변경 로그에 나온 것으로,
> 설정 레퍼런스에는 아직 자세히 나와 있지 않습니다.

최근 릴리스에 반복해서 나타나는 흐름이 있습니다. 보안과 관련된 설정은 이제 클론한 저장소가
넓힐 수 없습니다. 알아 둘 변경 사항은 세 가지입니다.

**중첩된 저장소는 따로 신뢰를 확인받아야 합니다(v2.1.232).** 신뢰한 상위 디렉토리 안에 있는 git 저장소는
더 이상 그 신뢰를 물려받지 않습니다. `~/work/monorepo`를 신뢰했고 그 안에 외부에서 가져온(vendored) 서브모듈이 있다면,
Claude Code가 처음 그 서브모듈 안에서 작업할 때 서브모듈을 따로 신뢰할지 묻습니다.

**`sandbox.ripgrep`은 사용자 범위 전용입니다(v2.1.232).** 샌드박스가 쓸 ripgrep 바이너리를 지정하는 이 설정은
사용자 설정, 관리형 설정, `--settings`에서만 적용됩니다. 프로젝트 설정으로는 더 이상 샌드박스가 다른 바이너리를
쓰게 할 수 없습니다.

**Remote Control 자동 시작은 사용자 범위 전용입니다(v2.1.222).** 저장소 로컬 설정으로는 Remote Control
자동 시작을 켤 수 없으며, 사용자 범위에서 `/config`로만 켤 수 있습니다.

기억해 둘 원칙: 체크인된 파일이 내 컴퓨터에서 Claude Code가 할 수 있는 일을 넓히게 되는 설정이라면,
이제는 사용자 범위 전용이라고 생각하세요.

---

## 에이전트 팀

에이전트 팀은 여러 Claude Code 인스턴스가 하나의 작업을 함께 처리하게 하는 실험적 기능입니다. 기본적으로 꺼져 있습니다.

### 에이전트 팀 켜기

환경 변수나 설정으로 켭니다.

```bash
# 환경 변수
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

또는 설정 JSON에 추가합니다.

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 에이전트 팀의 동작 방식

- **팀 리드**가 전체 작업을 조율하고 하위 작업을 팀원에게 위임합니다
- **팀원**은 각자 자체 컨텍스트 윈도우를 가지고 독립적으로 작업합니다
- **공유 작업 목록**으로 팀원끼리 스스로 조율합니다
- 서브에이전트 정의(`.claude/agents/`나 `--agents` 플래그)로 팀원의 역할과 전문 분야를 정합니다

### 표시 모드

에이전트 팀은 두 가지 표시 모드를 지원하며, `--teammate-mode` 플래그로 설정합니다.

| 모드 | 설명 |
|------|-------------|
| `in-process` (기본값) | 팀원이 같은 터미널 프로세스 안에서 실행됨 |
| `tmux` | 팀원마다 전용 분할 창이 생김(tmux나 iTerm2 필요) |
| `auto` | 가장 알맞은 표시 모드를 자동으로 선택 |

```bash
# 팀원 표시에 tmux 분할 창 사용
claude --teammate-mode tmux

# in-process 모드를 명시적으로 사용
claude --teammate-mode in-process
```

### 활용 사례

- 팀원마다 다른 모듈을 맡는 대규모 리팩토링 작업
- 코드 리뷰와 구현을 병렬로 진행
- 코드베이스 전반에 걸쳐 여러 파일을 조율해서 변경

> **참고**: 에이전트 팀은 실험적 기능이며 앞으로의 릴리스에서 바뀔 수 있습니다. 전체 레퍼런스는 [code.claude.com/docs/ko/agent-teams](https://code.claude.com/docs/ko/agent-teams)를 참고하세요.

---

## 모범 사례

### 계획 모드
- ✅ 여러 단계로 이루어진 복잡한 작업에 사용
- ✅ 승인하기 전에 계획 검토
- ✅ 필요하면 계획 수정
- ❌ 간단한 작업에는 쓰지 않기

### 확장 사고
- ✅ 아키텍처 결정에 사용
- ✅ 복잡한 문제 해결에 사용
- ✅ 사고 과정 검토
- ❌ 간단한 질문에는 쓰지 않기

### 백그라운드 작업
- ✅ 오래 걸리는 작업에 사용
- ✅ 작업 진행 상황 모니터링
- ✅ 작업 실패를 깔끔하게 처리
- ❌ 동시에 너무 많은 작업을 시작하지 않기

### 권한
- ✅ 코드 리뷰(읽기 전용)에는 `plan` 사용
- ✅ 대화형 개발에는 `default` 사용
- ✅ 자동화 워크플로우에는 `acceptEdits` 사용
- ✅ 안전장치를 갖춘 자율 작업에는 `auto` 사용
- ❌ 꼭 필요한 경우가 아니면 `bypassPermissions`를 쓰지 않기

### 세션
- ✅ 작업마다 별도의 세션 사용
- ✅ 중요한 세션 상태 저장
- ✅ 오래된 세션 정리
- ❌ 관련 없는 작업을 한 세션에 섞지 않기

---

## 추가 자료

Claude Code와 관련 기능에 대한 자세한 정보:

- [공식 대화형 모드 문서](https://code.claude.com/docs/ko/interactive-mode)
- [공식 헤드리스 모드 문서](https://code.claude.com/docs/ko/headless)
- [CLI 레퍼런스](https://code.claude.com/docs/ko/cli-reference)
- [체크포인트 가이드](../08-checkpoints/) - 세션 관리와 되감기
- [슬래시 명령어](../01-slash-commands/) - 명령어 레퍼런스
- [메모리 가이드](../02-memory/) - 지속되는 컨텍스트
- [스킬 가이드](../03-skills/) - 자율적으로 쓰이는 기능
- [서브에이전트 가이드](../04-subagents/) - 작업 위임 실행
- [MCP 가이드](../05-mcp/) - 외부 데이터 접근
- [훅 가이드](../06-hooks/) - 이벤트 기반 자동화
- [플러그인 가이드](../07-plugins/) - 묶음 확장 기능
- [공식 예약 작업 문서](https://code.claude.com/docs/ko/scheduled-tasks)
- [공식 Chrome 통합 문서](https://code.claude.com/docs/ko/chrome)
- [공식 Remote Control 문서](https://code.claude.com/docs/ko/remote-control)
- [공식 키 바인딩 문서](https://code.claude.com/docs/ko/keybindings)
- [공식 데스크톱 앱 문서](https://code.claude.com/docs/ko/desktop)
- [공식 에이전트 팀 문서](https://code.claude.com/docs/ko/agent-teams)

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/output-styles
- https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- https://code.claude.com/docs/ko/permissions
- https://code.claude.com/docs/ko/workflows#set-a-size-guideline
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
- https://code.claude.com/docs/en/auto-mode-classifier-billing
- https://code.claude.com/docs/ko/env-vars
- https://code.claude.com/docs/ko/settings
- https://code.claude.com/docs/ko/sandboxing
- https://code.claude.com/docs/ko/commands
- https://code.claude.com/docs/ko/cli-reference
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/ko/permission-modes
- https://code.claude.com/docs/ko/settings.md
- https://code.claude.com/docs/en/settings-reference
- https://code.claude.com/docs/en/whats-new/2026-w34
- https://code.claude.com/docs/ko/model-config#adjust-effort-level
- https://code.claude.com/docs/ko/interactive-mode
- https://code.claude.com/docs/ko/keybindings#modifiers
- https://code.claude.com/docs/ko/model-config#extended-thinking
- https://github.com/anthropics/claude-code/releases/tag/v2.1.281
- https://github.com/anthropics/claude-code/releases/tag/v2.1.283
- https://code.claude.com/docs/ko/permission-modes#critical-paths
- https://code.claude.com/docs/en/settings-reference#ultracode
- https://code.claude.com/docs/ko/permission-modes#which-mode-a-session-starts-in
- https://code.claude.com/docs/ko/permission-modes#eliminate-prompts-with-auto-mode
- https://github.com/anthropics/claude-code/releases/tag/v2.1.284
- https://github.com/anthropics/claude-code/releases/tag/v2.1.285
- https://code.claude.com/docs/ko/tools-reference
- https://code.claude.com/docs/ko/chrome
- https://github.com/anthropics/claude-code/releases/tag/v2.1.288
- https://github.com/anthropics/claude-code/releases/tag/v2.1.290
- https://github.com/anthropics/claude-code/releases/tag/v2.1.293
- https://code.claude.com/docs/ko/remote-control
- https://code.claude.com/docs/en/changelog#2-1-299
- https://code.claude.com/docs/en/changelog#2-1-300
- https://code.claude.com/docs/en/settings-reference#sandbox-enabled
- https://code.claude.com/docs/ko/prompt-caching
- https://code.claude.com/docs/ko/agent-teams
- https://code.claude.com/docs/ko/monitoring-usage
- https://code.claude.com/docs/ko/hooks
- https://code.claude.com/docs/en/managed-settings
- https://code.claude.com/docs/ko/channels
- https://code.claude.com/docs/ko/desktop
- https://code.claude.com/docs/ko/fullscreen
- https://code.claude.com/docs/en/changelog#2-1-301
- https://code.claude.com/docs/en/changelog#2-1-302
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
