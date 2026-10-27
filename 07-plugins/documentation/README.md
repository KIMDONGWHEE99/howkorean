<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# 문서화 플러그인

프로젝트를 위한 종합적인 문서 생성과 유지 관리입니다.

## 기능

✅ API 문서 생성
✅ README 작성과 갱신
✅ 문서 동기화
✅ 코드 주석 개선
✅ 예제 생성

## 설치

```bash
claude --plugin-dir ./07-plugins/documentation
```

## 구성 요소

### 슬래시 명령어
- `/generate-api-docs` - API 문서 생성
- `/generate-readme` - README 만들기 또는 갱신
- `/sync-docs` - 코드 변경 사항에 맞춰 문서 동기화
- `/validate-docs` - 문서 검증

### 서브에이전트
- `api-documenter` - API 문서화 전문가
- `code-commentator` - 코드 주석 개선
- `example-generator` - 코드 예제 작성

### 템플릿
- `api-endpoint.md` - API 엔드포인트 문서 템플릿
- `function-docs.md` - 함수 문서 템플릿
- `adr-template.md` - 아키텍처 결정 기록(ADR) 템플릿

### MCP 서버
- 문서 동기화를 위한 GitHub 통합

## 사용법

### API 문서 생성
```
/generate-api-docs
```

### README 만들기
```
/generate-readme
```

### 문서 동기화
```
/sync-docs
```

### 문서 검증
```
/validate-docs
```

## 요구 사항

- Claude Code 2.1+
- GitHub 접근 권한(선택 사항)

## 워크플로우 예

```
사용자: /generate-api-docs

Claude:
1. /src/api/의 모든 API 엔드포인트 스캔
2. api-documenter 서브에이전트에게 위임
3. 함수 시그니처와 JSDoc 추출
4. 모듈/엔드포인트별로 정리
5. api-endpoint.md 템플릿 사용
6. 종합적인 마크다운 문서 생성
7. curl, JavaScript, Python 예제 포함

결과:
✅ API 문서 생성 완료
📄 만든 파일:
   - docs/api/users.md
   - docs/api/auth.md
   - docs/api/products.md
📊 커버리지: 엔드포인트 23/23개 문서화
```

## 템플릿 사용법

### API 엔드포인트 템플릿
전체 예제와 함께 REST API 엔드포인트를 문서화할 때 쓰세요.

### 함수 문서 템플릿
개별 함수/메서드를 문서화할 때 쓰세요.

### ADR 템플릿
아키텍처 결정을 문서화할 때 쓰세요.

## 설정

문서 동기화용 GitHub 토큰을 설정하세요:
```bash
export GITHUB_TOKEN="your_github_token"
```

## 모범 사례

- 문서를 코드 가까이 두기
- 코드를 바꾸면 문서도 갱신하기
- 실용적인 예제 포함하기
- 정기적으로 검증하기
- 일관성을 위해 템플릿 쓰기

---

**최종 업데이트**: 2026년 10월 18일
**Claude Code 버전**: 2.1.302
**출처**:
- https://code.claude.com/docs/ko/plugins
- https://github.com/anthropics/claude-code/releases/tag/v2.1.131
- https://github.com/anthropics/claude-code/releases/tag/v2.1.138
- https://code.claude.com/docs/ko/model-config
- https://code.claude.com/docs/en/plugins/cli-reference
- https://code.claude.com/docs/en/plugins/install
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
