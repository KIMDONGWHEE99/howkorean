<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

<p align="center">
  <a href="https://github.com/trending">
    <img src="https://img.shields.io/badge/GitHub-🔥%20%231%20Trending-purple?style=for-the-badge&logo=github"/>
  </a>
</p>

[![GitHub Stars](https://img.shields.io/github/stars/luongnv89/claude-howto?style=flat&color=gold)](https://github.com/luongnv89/claude-howto/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/luongnv89/claude-howto?style=flat)](https://github.com/luongnv89/claude-howto/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.302-brightgreen)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-2.1+-purple)](https://code.claude.com)

> **비공식 한국어판** — 이 저장소는 MIT 라이선스로 공개된 [luongnv89/claude-howto](https://github.com/luongnv89/claude-howto)를 한국어로 옮긴 것입니다. 원문 기준은 2026년 10월 20일 커밋 `188f468`이며, 번역 기준과 용어집은 [TRANSLATION.md](TRANSLATION.md)에 정리되어 있습니다.

# 주말에 마스터하는 Claude Code

`claude`를 입력하는 단계에서 에이전트, 훅, 스킬, MCP 서버를 자유롭게 조율하는 단계까지 — 시각적 튜토리얼, 복사해서 바로 쓰는 템플릿, 안내형 학습 경로가 함께합니다.

**[15분 만에 시작하기](#15분-만에-시작하기)** | **[내 수준 찾기](#어디서부터-시작할지-모르겠나요)** | **[기능 카탈로그 둘러보기](CATALOG.md)**

---

## 목차

- [문제점](#문제점)
- [Claude How To가 해결하는 방법](#claude-how-to가-해결하는-방법)
- [진행 방식](#진행-방식)
- [어디서부터 시작할지 모르겠나요?](#어디서부터-시작할지-모르겠나요)
- [15분 만에 시작하기](#15분-만에-시작하기)
- [이 가이드로 무엇을 만들 수 있나요?](#이-가이드로-무엇을-만들-수-있나요)
- [자주 묻는 질문](#자주-묻는-질문)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

---

## 문제점

Claude Code를 설치했습니다. 프롬프트도 몇 번 실행해 봤습니다. 그다음은요?

- **공식 문서는 기능을 설명하지만, 기능을 조합하는 방법은 보여 주지 않습니다.** 슬래시 명령어가 있다는 건 알아도, 그것을 훅·메모리·서브에이전트와 엮어 실제로 몇 시간을 아껴 주는 워크플로우로 만드는 방법은 모릅니다.
- **명확한 학습 경로가 없습니다.** 훅보다 MCP를 먼저 배워야 할까요? 서브에이전트보다 스킬이 먼저일까요? 결국 전부 훑어보기만 하고 제대로 익힌 것은 하나도 남지 않습니다.
- **예제가 너무 기초적입니다.** "hello world" 수준의 슬래시 명령어로는 메모리를 활용하고, 전문 에이전트에게 작업을 위임하고, 보안 검사까지 자동으로 실행하는 실무용 코드 리뷰 파이프라인을 만들 수 없습니다.

Claude Code가 가진 힘의 90%를 그냥 내버려 두고 있는 셈입니다. 게다가 무엇을 모르는지조차 모릅니다.

---

## Claude How To가 해결하는 방법

이 가이드는 또 하나의 기능 레퍼런스가 아닙니다. 오늘 바로 프로젝트에 복사해 쓸 수 있는 실전 템플릿으로 Claude Code의 모든 기능을 익히도록 돕는 **체계적이고 시각적인 예제 중심 가이드**입니다.

| | 공식 문서 | 이 가이드 |
|--|---------------|------------|
| **형식** | 레퍼런스 문서 | Mermaid 다이어그램을 곁들인 시각적 튜토리얼 |
| **깊이** | 기능 설명 | 내부 동작 원리까지 |
| **예제** | 기본 코드 조각 | 바로 쓸 수 있는 실무용 템플릿 |
| **구성** | 기능별 구성 | 단계별 학습 경로(입문부터 고급까지) |
| **온보딩** | 스스로 알아서 | 예상 소요 시간이 표시된 안내형 로드맵 |
| **자가 진단** | 없음 | 부족한 부분을 찾아 맞춤 경로를 만들어 주는 대화형 퀴즈 |

### 이 가이드에서 얻는 것:

- **10개 튜토리얼 모듈** — 슬래시 명령어부터 사용자 정의 에이전트 팀까지 Claude Code의 모든 기능을 다룹니다
- **복사해서 바로 쓰는 설정** — 슬래시 명령어, CLAUDE.md 템플릿, 훅 스크립트, MCP 설정, 서브에이전트 정의, 완성된 플러그인 번들
- **Mermaid 다이어그램** — 각 기능이 내부에서 어떻게 동작하는지 보여 주어 *어떻게*뿐 아니라 *왜*까지 이해할 수 있습니다
- **안내형 학습 경로** — 11~13시간 만에 입문자에서 파워 유저로 성장합니다
- **내장 자가 진단** — Claude Code에서 `/self-assessment`나 `/lesson-quiz hooks`를 바로 실행해 부족한 부분을 찾습니다

**[학습 경로 시작하기 ->](LEARNING-ROADMAP.md)**

---

## 진행 방식

### 1. 내 수준 찾기

[자가 진단 퀴즈](LEARNING-ROADMAP.md#-내-수준-찾기)를 풀거나 Claude Code에서 `/self-assessment`를 실행하세요. 이미 아는 내용을 바탕으로 맞춤 로드맵을 받을 수 있습니다.

### 2. 안내된 경로 따라가기

10개 모듈을 순서대로 학습하세요. 각 모듈은 앞 모듈의 내용을 바탕으로 합니다. 배우면서 템플릿을 프로젝트에 바로 복사해 넣으세요.

### 3. 기능을 조합해 워크플로우 만들기

진짜 힘은 기능을 조합하는 데서 나옵니다. 슬래시 명령어 + 메모리 + 서브에이전트 + 훅을 엮어 코드 리뷰, 배포, 문서 생성을 처리하는 자동화 파이프라인을 만드는 법을 배웁니다.

### 4. 이해도 점검하기

각 모듈을 마친 뒤 `/lesson-quiz [topic]`을 실행하세요. 놓친 부분을 정확히 짚어 주므로 빈틈을 빠르게 메울 수 있습니다.

**[15분 만에 시작하기](#15분-만에-시작하기)**

---

## 개발자들이 신뢰하는 가이드

- Claude Code를 매일 사용하는 개발자들이 누른 **GitHub 스타**
- 이 가이드를 자기 워크플로우에 맞게 고쳐 쓰는 팀들의 **포크**
- **활발한 유지 관리** — Claude Code 릴리스마다 동기화(최신: v2.1.302, 2026년 10월)
- **커뮤니티 주도** — 실제 설정을 공유하는 개발자들의 기여

[![Star History Chart](https://api.star-history.com/svg?repos=luongnv89/claude-howto&type=Date)](https://star-history.com/#luongnv89/claude-howto&Date)

---

## 어디서부터 시작할지 모르겠나요?

자가 진단을 하거나 내 수준을 고르세요:

| 수준 | 할 수 있는 것 | 시작 지점 | 소요 시간 |
|-------|-----------|------------|------|
| **입문** | Claude Code를 실행해 대화할 수 있음 | [슬래시 명령어](01-slash-commands/) | 약 2.5시간 |
| **중급** | CLAUDE.md와 사용자 정의 명령어를 쓸 수 있음 | [스킬](03-skills/) | 약 3.5시간 |
| **고급** | MCP 서버와 훅을 설정할 수 있음 | [고급 기능](09-advanced-features/) | 약 5시간 |

**10개 모듈 전체 학습 경로:**

| 순서 | 모듈 | 수준 | 소요 시간 |
|-------|--------|-------|------|
| 1 | [슬래시 명령어](01-slash-commands/) | 입문 | 30분 |
| 2 | [메모리](02-memory/) | 입문+ | 45분 |
| 3 | [체크포인트](08-checkpoints/) | 중급 | 45분 |
| 4 | [CLI 기초](10-cli/) | 입문+ | 30분 |
| 5 | [스킬](03-skills/) | 중급 | 1시간 |
| 6 | [훅](06-hooks/) | 중급 | 1시간 |
| 7 | [MCP](05-mcp/) | 중급+ | 1시간 |
| 8 | [서브에이전트](04-subagents/) | 중급+ | 1.5시간 |
| 9 | [고급 기능](09-advanced-features/) | 고급 | 2~3시간 |
| 10 | [플러그인](07-plugins/) | 고급 | 2시간 |

**[전체 학습 로드맵 ->](LEARNING-ROADMAP.md)**

---

## 15분 만에 시작하기

> **설치 참고**: v2.1.113부터 Claude Code는 플랫폼별 네이티브 바이너리(macOS/Linux/Windows)로 배포됩니다. 권장 설치 방법은 네이티브 설치 프로그램(`curl -fsSL https://claude.ai/install.sh | bash`)입니다. 공식 README에서 npm 설치는 지원 중단되었으므로 네이티브 설치 프로그램, Homebrew(`brew install --cask claude-code`), WinGet(`winget install Anthropic.ClaudeCode`)을 사용하세요. 참고로 `npm install -g @anthropic-ai/claude-code`도 설치 시점에 플랫폼별 선택적 의존성을 통해 같은 네이티브 바이너리를 내려받습니다. v2.1.116부터는 `https://downloads.claude.ai/claude-code-releases`에서 내려받으므로, 회사 프록시를 쓴다면 이 호스트를 허용 목록에 추가해야 합니다.

```bash
# 1. 가이드 내려받기
git clone https://github.com/KIMDONGWHEE99/howkorean.git claude-howto
cd claude-howto

# 2. 첫 번째 슬래시 명령어 복사
mkdir -p /path/to/your-project/.claude/commands
cp 01-slash-commands/optimize.md /path/to/your-project/.claude/commands/

# 3. 사용해 보기 — Claude Code에서 다음을 입력하세요:
# /optimize

# 4. 더 해 볼까요? 프로젝트 메모리를 설정하세요:
cp 02-memory/project-CLAUDE.md /path/to/your-project/CLAUDE.md

# 5. 스킬 설치:
cp -r 03-skills/code-review-specialist ~/.claude/skills/
```

전체 설정을 원하나요? **1시간 필수 설정**은 다음과 같습니다:

```bash
# 슬래시 명령어 (15분)
cp 01-slash-commands/*.md .claude/commands/

# 프로젝트 메모리 (15분)
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 스킬 설치 (15분)
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 주말 목표: 훅, 서브에이전트, MCP, 플러그인 추가
# 학습 경로를 따라가며 단계별로 설정하세요
```

**[전체 설치 참조 보기](#15분-만에-시작하기)**

---

## 이 가이드로 무엇을 만들 수 있나요?

| 활용 사례 | 조합할 기능 |
|----------|------------------------|
| **자동 코드 리뷰** | 슬래시 명령어 + 서브에이전트 + 메모리 + MCP |
| **팀 온보딩** | 메모리 + 슬래시 명령어 + 플러그인 |
| **CI/CD 자동화** | CLI 레퍼런스 + 훅 + 백그라운드 작업 |
| **문서 생성** | 스킬 + 서브에이전트 + 플러그인 |
| **보안 감사** | 서브에이전트 + 스킬 + 훅(읽기 전용 모드) |
| **DevOps 파이프라인** | 플러그인 + MCP + 훅 + 백그라운드 작업 |
| **복잡한 리팩토링** | 체크포인트 + 계획 모드 + 훅 |

---

## 자주 묻는 질문

**무료인가요?**
네. MIT 라이선스이며 영원히 무료입니다. 개인 프로젝트, 회사, 팀 어디서든 쓸 수 있고, 라이선스 고지를 포함하는 것 외에는 제약이 없습니다.

**계속 관리되나요?**
활발하게 관리됩니다. Claude Code 릴리스마다 가이드를 동기화합니다. 현재 버전은 v2.1.302(2026년 10월)이며 Claude Code 2.1+와 호환됩니다.

**공식 문서와 무엇이 다른가요?**
공식 문서는 기능 레퍼런스이고, 이 가이드는 다이어그램과 실무용 템플릿, 단계별 학습 경로를 갖춘 튜토리얼입니다. 둘은 서로를 보완합니다. 여기서 배우고, 세부 사항이 필요할 때 공식 문서를 참고하세요.

**전부 학습하는 데 얼마나 걸리나요?**
전체 경로는 11~13시간입니다. 하지만 15분이면 바로 효과를 볼 수 있습니다. 슬래시 명령어 템플릿 하나를 복사해서 써 보세요.

**Claude Sonnet / Haiku / Opus에서도 쓸 수 있나요?**
네. 모든 템플릿은 Claude Fable 5.1, Claude Fable 5, Claude Opus 5.5, Claude Opus 5, Claude Sonnet 5.5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 5.5, Claude Haiku 4.5에서 동작합니다.

**기여할 수 있나요?**
물론입니다. 가이드라인은 [CONTRIBUTING.md](CONTRIBUTING.md)(영문)를 참고하세요. 새 예제, 버그 수정, 문서 개선, 커뮤니티 템플릿을 환영합니다.

**오프라인에서도 읽을 수 있나요?**
네. `uv run scripts/build_epub.py`를 실행하면 모든 내용과 렌더링된 다이어그램이 담긴 EPUB 전자책이 만들어집니다.

---

## 지금 바로 Claude Code 마스터를 시작하세요

Claude Code는 이미 설치되어 있습니다. 생산성을 10배로 끌어올리는 데 남은 것은 사용법을 아는 것뿐입니다. 이 가이드는 그곳까지 가는 체계적인 경로와 시각적인 설명, 복사해서 바로 쓰는 템플릿을 제공합니다.

MIT 라이선스. 영원히 무료. 복제하고, 포크하고, 내 것으로 만드세요.

**[학습 경로 시작하기 ->](LEARNING-ROADMAP.md)** | **[기능 카탈로그 둘러보기](CATALOG.md)** | **[15분 만에 시작하기](#15분-만에-시작하기)**

---

<details>
<summary>빠른 탐색 — 모든 기능</summary>

| 기능 | 설명 | 폴더 |
|---------|-------------|--------|
| **기능 카탈로그** | 설치 명령어가 포함된 전체 레퍼런스 | [CATALOG.md](CATALOG.md) |
| **슬래시 명령어** | 사용자가 직접 호출하는 단축 명령 | [01-slash-commands/](01-slash-commands/) |
| **메모리** | 계속 유지되는 컨텍스트 | [02-memory/](02-memory/) |
| **스킬** | 재사용 가능한 기능 | [03-skills/](03-skills/) |
| **서브에이전트** | 전문화된 AI 어시스턴트 | [04-subagents/](04-subagents/) |
| **MCP 프로토콜** | 외부 도구 접근 | [05-mcp/](05-mcp/) |
| **훅** | 이벤트 기반 자동화 | [06-hooks/](06-hooks/) |
| **플러그인** | 기능 번들 | [07-plugins/](07-plugins/) |
| **체크포인트** | 세션 스냅샷과 되감기 | [08-checkpoints/](08-checkpoints/) |
| **고급 기능** | 계획, 사고, 백그라운드 작업 | [09-advanced-features/](09-advanced-features/) |
| **CLI 레퍼런스** | 명령어, 플래그, 옵션 | [10-cli/](10-cli/) |
| **블로그 글** | 실제 사용 사례 | [블로그 글](https://medium.com/@luongnv89) |

</details>

<details>
<summary>기능 비교</summary>

| 기능 | 호출 방식 | 지속성 | 적합한 용도 |
|---------|-----------|------------|----------|
| **슬래시 명령어** | 수동 (`/cmd`) | 세션 안에서만 | 빠른 단축 명령 |
| **메모리** | 자동 로드 | 세션 간 유지 | 장기 학습 |
| **스킬** | 자동 호출 | 파일 시스템 | 자동화된 워크플로우 |
| **서브에이전트** | 자동 위임 | 격리된 컨텍스트 | 작업 분배 |
| **MCP 프로토콜** | 자동 조회 | 실시간 | 실시간 데이터 접근 |
| **훅** | 이벤트로 실행 | 설정에 저장 | 자동화와 검증 |
| **플러그인** | 명령어 한 번 | 모든 기능 | 완성형 솔루션 |
| **체크포인트** | 수동/자동 | 세션 단위 | 안전한 실험 |
| **계획 모드** | 수동/자동 | 계획 단계 | 복잡한 구현 |
| **백그라운드 작업** | 수동 | 작업이 끝날 때까지 | 오래 걸리는 작업 |
| **CLI 레퍼런스** | 터미널 명령어 | 세션/스크립트 | 자동화와 스크립팅 |

</details>

<details>
<summary>설치 빠른 참조</summary>

```bash
# 슬래시 명령어
cp 01-slash-commands/*.md .claude/commands/

# 메모리
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 스킬
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 서브에이전트
cp 04-subagents/*.md .claude/agents/

# MCP
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# 훅
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 플러그인 (저장소 루트에서 로컬 플러그인 로드)
claude --plugin-dir ./07-plugins/pr-review

# 체크포인트 (자동으로 켜져 있으며 설정에서 구성)
# 08-checkpoints/README.md 참고

# 고급 기능 (설정에서 구성)
# 09-advanced-features/config-examples.json 참고

# CLI 레퍼런스 (설치 필요 없음)
# 사용 예시는 10-cli/README.md 참고
```

</details>

<details>
<summary>01. 슬래시 명령어</summary>

**위치**: [01-slash-commands/](01-slash-commands/)

**설명**: 마크다운 파일로 저장해 두고 사용자가 직접 호출하는 단축 명령

**예제**:
- `optimize.md` - 코드 최적화 분석
- `pr.md` - 풀 리퀘스트 준비
- `generate-api-docs.md` - API 문서 생성기

**설치**:
```bash
cp 01-slash-commands/*.md /path/to/project/.claude/commands/
```

**사용법**:
```
/optimize
/pr
/generate-api-docs
```

**더 알아보기**: [Discovering Claude Code Slash Commands](https://medium.com/@luongnv89/discovering-claude-code-slash-commands-cdc17f0dfb29)

</details>

<details>
<summary>02. 메모리</summary>

**위치**: [02-memory/](02-memory/)

**설명**: 세션이 바뀌어도 유지되는 컨텍스트

**예제**:
- `project-CLAUDE.md` - 팀 전체가 따르는 프로젝트 표준
- `directory-api-CLAUDE.md` - 디렉토리별 규칙
- `personal-CLAUDE.md` - 개인 선호 설정

**설치**:
```bash
# 프로젝트 메모리
cp 02-memory/project-CLAUDE.md /path/to/project/CLAUDE.md

# 디렉토리 메모리
cp 02-memory/directory-api-CLAUDE.md /path/to/project/src/api/CLAUDE.md

# 개인 메모리
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

**사용법**: Claude가 자동으로 로드

</details>

<details>
<summary>03. 스킬</summary>

**위치**: [03-skills/](03-skills/)

**설명**: 지침과 스크립트를 담은, 재사용 가능하고 자동으로 호출되는 기능

**예제**:
- `code-review-specialist/` - 스크립트를 포함한 종합 코드 리뷰
- `brand-voice/` - 브랜드 보이스 일관성 검사기
- `doc-generator/` - API 문서 생성기

**설치**:
```bash
# 개인 스킬
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 프로젝트 스킬
cp -r 03-skills/code-review-specialist /path/to/project/.claude/skills/
```

**사용법**: 관련이 있을 때 자동으로 호출

</details>

<details>
<summary>04. 서브에이전트</summary>

**위치**: [04-subagents/](04-subagents/)

**설명**: 격리된 컨텍스트와 사용자 정의 프롬프트를 가진 전문 AI 어시스턴트

**예제**:
- `code-reviewer.md` - 종합 코드 품질 분석
- `test-engineer.md` - 테스트 전략과 커버리지
- `documentation-writer.md` - 기술 문서 작성
- `secure-reviewer.md` - 보안 중심 리뷰(읽기 전용)
- `implementation-agent.md` - 기능 전체 구현

**설치**:
```bash
cp 04-subagents/*.md /path/to/project/.claude/agents/
```

**사용법**: 메인 에이전트가 자동으로 위임

</details>

<details>
<summary>05. MCP 프로토콜</summary>

**위치**: [05-mcp/](05-mcp/)

**설명**: 외부 도구와 API에 접근하기 위한 Model Context Protocol

**예제**:
- `github-mcp.json` - GitHub 통합
- `database-mcp.json` - 데이터베이스 쿼리
- `filesystem-mcp.json` - 파일 작업
- `multi-mcp.json` - 여러 MCP 서버 함께 쓰기

**설치**:
```bash
# 환경 변수 설정
export DATABASE_URL="postgresql://..."

# CLI로 MCP 서버 추가
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer YOUR_GITHUB_PAT"

# 또는 프로젝트의 .mcp.json에 직접 추가 (예시는 05-mcp/ 참고)
```

**사용법**: 설정을 마치면 Claude가 MCP 도구를 자동으로 사용할 수 있습니다

</details>

<details>
<summary>06. 훅</summary>

**위치**: [06-hooks/](06-hooks/)

**설명**: Claude Code 이벤트에 반응해 자동으로 실행되는 이벤트 기반 셸 명령어

**예제**:
- `format-code.sh` - 파일을 쓴 뒤 코드 자동 포맷
- `pre-commit.sh` - 커밋 전에 테스트 실행
- `security-scan.sh` - 보안 문제 검사
- `log-bash.sh` - 모든 bash 명령어 기록
- `validate-prompt.sh` - 사용자 프롬프트 검증
- `notify-team.sh` - 이벤트가 발생하면 알림 전송

**설치**:
```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

`~/.claude/settings.json`에서 훅을 설정하세요:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/format-code.sh" },
          { "type": "command", "command": "~/.claude/hooks/security-scan.sh" }
        ]
      }
    ]
  }
}
```

**사용법**: 이벤트가 발생하면 훅이 자동으로 실행

**훅 타입**(5가지): `command`, `http`, `prompt`, `mcp_tool`, `agent` — 훅이 실행되는 방식

**훅 이벤트**(33가지, 4개 분류) — 훅이 실행되는 시점:
- **도구 훅**: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `PermissionRequest`, `PermissionDenied`
- **세션 훅**: `SessionStart`, `Setup`, `SessionEnd`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`
- **작업 훅**: `UserPromptSubmit`, `UserPromptExpansion`, `MessageDisplay`, `TaskCompleted`, `TaskCreated`, `TeammateIdle` — `TaskCompleted`와 `TaskCreated`는 할 일(todo) 도구가 켜져 있을 때만 발생합니다. 할 일 도구는 Claude 3.x 모델, Opus 4–4.7, Sonnet 4–4.6, Haiku 4.5에서만 기본으로 제공됩니다(`CLAUDE_CODE_ENABLE_TODO_TOOLS=1`로 다시 켤 수 있음)
- **라이프사이클 훅**: `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `WorktreeCreate`, `WorktreeRemove`, `Notification`, `InstructionsLoaded`, `Elicitation`, `ElicitationResult`

</details>

<details>
<summary>07. 플러그인</summary>

**위치**: [07-plugins/](07-plugins/)

**설명**: 명령어, 에이전트, MCP, 훅을 하나로 묶은 번들

**예제**:
- `pr-review/` - 완성된 PR 리뷰 워크플로우
- `devops-automation/` - 배포와 모니터링
- `documentation/` - 문서 생성

**설치**:
```bash
# 저장소 루트에서 실행 (이 저장소는 마켓플레이스를 제공하지 않으므로 /plugin install은 쓸 수 없음)
claude --plugin-dir ./07-plugins/pr-review
claude --plugin-dir ./07-plugins/devops-automation
claude --plugin-dir ./07-plugins/documentation
```

**사용법**: 번들에 포함된 슬래시 명령어와 기능 사용

</details>

<details>
<summary>08. 체크포인트와 되감기</summary>

**위치**: [08-checkpoints/](08-checkpoints/)

**설명**: 대화 상태를 저장해 두고 이전 시점으로 되감아 다른 접근 방식을 시도

**핵심 개념**:
- **체크포인트**: 대화 상태의 스냅샷
- **되감기**: 이전 체크포인트로 돌아가기
- **분기점**: 같은 체크포인트에서 여러 접근 방식 탐색

**사용법**:
```
# 체크포인트는 사용자가 프롬프트를 보낼 때마다 자동으로 만들어집니다
# 되감으려면 Esc를 두 번 누르거나 다음을 입력하세요:
/rewind

# 그런 다음 여섯 가지 옵션 중 하나를 고릅니다:
# 1. Restore code and conversation (코드와 대화 복원)
# 2. Restore conversation (대화만 복원)
# 3. Restore code (코드만 복원)
# 4. Summarize from here (여기부터 요약)
# 5. Summarize up to here (여기까지 요약)
# 6. Never mind (취소)
```

**활용 사례**:
- 여러 구현 방식 시도
- 실수에서 복구
- 안전한 실험
- 대안 솔루션 비교
- 여러 디자인 A/B 테스트

</details>

<details>
<summary>09. 고급 기능</summary>

**위치**: [09-advanced-features/](09-advanced-features/)

**설명**: 복잡한 워크플로우와 자동화를 위한 고급 기능

**포함 내용**:
- **계획 모드** — 코딩 전에 상세한 구현 계획 수립
- **확장 사고** — 복잡한 문제를 위한 깊은 추론(`Alt+T` / `Option+T`로 켜고 끄기)
- **백그라운드 작업** — 오래 걸리는 작업을 기다리지 않고 실행
- **권한 모드** — `manual`(설정값 `default`), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`
- **헤드리스 모드** — CI/CD에서 Claude Code 실행: `claude -p "테스트를 실행하고 보고서를 만들어 줘"`
- **세션 관리** — `/resume`, `/rename`, `/fork`, `/branch`, `claude -c`, `claude -r`
- **설정** — `~/.claude/settings.json`에서 동작을 원하는 대로 조정

전체 설정 예시는 [config-examples.json](09-advanced-features/config-examples.json)을 참고하세요.

</details>

<details>
<summary>10. CLI 레퍼런스</summary>

**위치**: [10-cli/](10-cli/)

**설명**: Claude Code 명령줄 인터페이스 전체 레퍼런스

**간단한 예**:
```bash
# 대화형 모드
claude "이 프로젝트를 설명해 줘"

# print 모드 (비대화형)
claude -p "이 코드를 리뷰해 줘"

# 파일 내용 처리
cat error.log | claude -p "이 오류를 설명해 줘"

# 스크립트용 JSON 출력
claude -p --output-format json "함수 목록을 보여 줘"

# 세션 재개
claude -r "feature-auth" "구현을 계속해 줘"
```

**활용 사례**: CI/CD 파이프라인 통합, 스크립트 자동화, 일괄 처리, 다중 세션 워크플로우, 사용자 정의 에이전트 구성

</details>

<details>
<summary>워크플로우 예시</summary>

### 코드 리뷰 전체 워크플로우

```markdown
# 사용 기능: 슬래시 명령어 + 서브에이전트 + 메모리 + MCP

사용자: /review-pr

Claude:
1. 프로젝트 메모리(코딩 표준) 로드
2. GitHub MCP로 PR 가져오기
3. code-reviewer 서브에이전트에 위임
4. test-engineer 서브에이전트에 위임
5. 결과 종합
6. 종합 리뷰 제공
```

### 문서 자동 생성

```markdown
# 사용 기능: 스킬 + 서브에이전트 + 메모리

사용자: "auth 모듈의 API 문서를 만들어 줘"

Claude:
1. 프로젝트 메모리(문서 표준) 로드
2. 문서 생성 요청 감지
3. doc-generator 스킬 자동 호출
4. api-documenter 서브에이전트에 위임
5. 예제를 포함한 종합 문서 작성
```

### DevOps 배포

```markdown
# 사용 기능: 플러그인 + MCP + 훅

사용자: /deploy production

Claude:
1. pre-deploy 훅 실행 (환경 검증)
2. deployment-specialist 서브에이전트에 위임
3. Kubernetes MCP로 배포 실행
4. 진행 상황 모니터링
5. post-deploy 훅 실행 (상태 점검)
6. 결과 보고
```

</details>

<details>
<summary>디렉토리 구조</summary>

```
├── 01-slash-commands/
│   ├── optimize.md
│   ├── pr.md
│   ├── generate-api-docs.md
│   └── README.md
├── 02-memory/
│   ├── project-CLAUDE.md
│   ├── directory-api-CLAUDE.md
│   ├── personal-CLAUDE.md
│   └── README.md
├── 03-skills/
│   ├── code-review-specialist/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── templates/
│   ├── brand-voice/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── doc-generator/
│   │   ├── SKILL.md
│   │   └── generate-docs.py
│   └── README.md
├── 04-subagents/
│   ├── code-reviewer.md
│   ├── test-engineer.md
│   ├── documentation-writer.md
│   ├── secure-reviewer.md
│   ├── implementation-agent.md
│   └── README.md
├── 05-mcp/
│   ├── github-mcp.json
│   ├── database-mcp.json
│   ├── filesystem-mcp.json
│   ├── multi-mcp.json
│   └── README.md
├── 06-hooks/
│   ├── format-code.sh
│   ├── pre-commit.sh
│   ├── security-scan.sh
│   ├── log-bash.sh
│   ├── validate-prompt.sh
│   ├── notify-team.sh
│   └── README.md
├── 07-plugins/
│   ├── pr-review/
│   ├── devops-automation/
│   ├── documentation/
│   └── README.md
├── 08-checkpoints/
│   ├── checkpoint-examples.md
│   └── README.md
├── 09-advanced-features/
│   ├── config-examples.json
│   ├── planning-mode-examples.md
│   └── README.md
├── 10-cli/
│   └── README.md
└── README.md (이 파일)
```

</details>

<details>
<summary>모범 사례</summary>

### 권장 사항
- 슬래시 명령어로 간단하게 시작하기
- 기능을 하나씩 늘려 가기
- 팀 표준은 메모리에 기록하기
- 설정은 먼저 로컬에서 테스트하기
- 직접 만든 구현은 문서로 남기기
- 프로젝트 설정은 버전 관리하기
- 플러그인은 팀과 공유하기

### 피해야 할 것
- 중복되는 기능을 만들지 마세요
- 자격 증명을 하드코딩하지 마세요
- 문서화를 건너뛰지 마세요
- 간단한 작업을 지나치게 복잡하게 만들지 마세요
- 보안 모범 사례를 무시하지 마세요
- 민감한 데이터를 커밋하지 마세요

</details>

<details>
<summary>문제 해결</summary>

### 기능이 로드되지 않을 때
1. 파일 위치와 이름 확인
2. YAML frontmatter 문법 확인
3. 파일 권한 확인
4. Claude Code 버전 호환성 검토

### MCP 연결에 실패할 때
1. 환경 변수 확인
2. MCP 서버 설치 상태 확인
3. 자격 증명 테스트
4. 네트워크 연결 점검

### 서브에이전트에 위임되지 않을 때
1. 도구 권한 확인
2. 에이전트 설명(description)이 명확한지 확인
3. 작업 복잡도 검토
4. 에이전트를 단독으로 테스트

</details>

<details>
<summary>테스트</summary>

이 프로젝트에는 포괄적인 자동 테스트가 갖춰져 있습니다:

- **단위 테스트**: pytest를 사용한 Python 테스트(Python 3.10, 3.11, 3.12)
- **코드 품질**: Ruff를 사용한 린팅과 포맷팅
- **보안**: Bandit을 사용한 취약점 검사
- **타입 검사**: mypy를 사용한 정적 타입 분석
- **빌드 검증**: EPUB 생성 테스트
- **커버리지 추적**: Codecov 연동

```bash
# 개발 의존성 설치
uv pip install -r scripts/requirements-dev.txt

# 전체 단위 테스트 실행
pytest scripts/tests/ -v

# 커버리지 보고서와 함께 테스트 실행
pytest scripts/tests/ -v --cov=scripts --cov-report=html

# 코드 품질 검사
ruff check scripts/
ruff format --check scripts/

# 보안 검사
bandit -c scripts/pyproject.toml -r scripts/ --exclude scripts/tests/

# 타입 검사
mypy scripts/ --ignore-missing-imports
```

테스트는 `main`/`develop`에 푸시할 때마다, 그리고 `main`으로 향하는 모든 PR에서 자동으로 실행됩니다. 자세한 내용은 [TESTING.md](.github/TESTING.md)(영문)를 참고하세요.

</details>

<details>
<summary>EPUB 생성</summary>

이 가이드를 오프라인에서 읽고 싶나요? EPUB 전자책을 만드세요:

```bash
uv run scripts/build_epub.py
```

모든 내용과 렌더링된 Mermaid 다이어그램이 담긴 `claude-howto-guide.epub` 파일이 만들어집니다.

더 많은 옵션은 [scripts/README.md](scripts/README.md)(영문)를 참고하세요.

</details>

<details>
<summary>기여하기</summary>

문제를 발견했거나 예제를 기여하고 싶나요? 언제든 환영합니다!

**다음 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)(영문)에서 자세히 확인하세요:**
- 기여 유형(예제, 문서, 기능, 버그, 피드백)
- 개발 환경 설정 방법
- 디렉토리 구조와 콘텐츠 추가 방법
- 작성 가이드라인과 모범 사례
- 커밋과 PR 절차

**커뮤니티 기준:**
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)(영문) - 서로를 대하는 방식
- [SECURITY.md](SECURITY.md)(영문) - 보안 정책과 취약점 신고

### 보안 문제 신고

보안 취약점을 발견했다면 책임감 있게 신고해 주세요:

1. **GitHub 비공개 취약점 신고 사용**: https://github.com/luongnv89/claude-howto/security/advisories
2. **또는** 자세한 절차는 [.github/SECURITY_REPORTING.md](.github/SECURITY_REPORTING.md)(영문)를 확인하세요
3. 보안 취약점은 공개 이슈로 **올리지 마세요**

빠른 시작:
1. 저장소를 포크하고 복제합니다
2. 내용을 알 수 있는 이름으로 브랜치를 만듭니다(`add/feature-name`, `fix/bug`, `docs/improvement`)
3. 가이드라인에 따라 변경합니다
4. 명확한 설명과 함께 풀 리퀘스트를 제출합니다

**도움이 필요하신가요?** 이슈나 토론을 열어 주시면 과정을 안내해 드립니다.

</details>

<details>
<summary>추가 자료</summary>

- [Claude Code 문서](https://code.claude.com/docs/ko/overview)
- [MCP 프로토콜 명세](https://modelcontextprotocol.io)
- [스킬 저장소](https://github.com/luongnv89/skills) - 바로 쓸 수 있는 스킬 모음
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Boris Cherny의 Claude Code 워크플로우](https://x.com/bcherny/status/2007179832300581177) - Claude Code를 만든 사람이 체계화한 자신의 워크플로우를 공유합니다. 병렬 에이전트, 공유 CLAUDE.md, 계획 모드, 슬래시 명령어, 서브에이전트, 그리고 오래 실행되는 자율 세션을 위한 검증 훅을 다룹니다.

</details>

---

## 기여하기

기여를 환영합니다! 시작하는 방법은 [기여 가이드](CONTRIBUTING.md)(영문)를 참고하세요.

---

## 라이선스

MIT License - [LICENSE](LICENSE)(영문)를 참고하세요. 자유롭게 사용, 수정, 배포할 수 있으며, 유일한 조건은 라이선스 고지를 포함하는 것입니다.

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/en/tools-reference#task-tool-availability
- https://code.claude.com/docs/ko/hooks
- https://code.claude.com/docs/ko/overview
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/ko/permission-modes
- https://platform.claude.com/docs/en/about-claude/models/overview
- https://github.com/anthropics/claude-code/releases
- https://github.com/anthropics/claude-code/releases/tag/v2.1.154
- https://code.claude.com/docs/ko/model-config
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- https://github.com/anthropics/claude-code/releases/tag/v2.1.296
- https://code.claude.com/docs/ko/setup
- https://code.claude.com/docs/ko/mcp
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/ko/checkpointing
- https://github.com/anthropics/claude-code
- https://code.claude.com/docs/en/changelog#2-1-302
**호환 모델**: Claude Fable 5.1, Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
