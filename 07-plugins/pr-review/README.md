<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../../resources/logos/claude-howto-logo.svg">
</picture>

# PR 리뷰 플러그인

보안, 테스트, 문서 검사를 아우르는 종합 PR 리뷰 워크플로우입니다.

## 기능

✅ 보안 분석
✅ 테스트 커버리지 확인
✅ 문서 검증
✅ 코드 품질 평가
✅ 성능 영향 분석

## 설치

```bash
claude --plugin-dir ./07-plugins/pr-review
```

## 구성 요소

### 슬래시 명령어
- `/review-pr` - 종합 PR 리뷰
- `/check-security` - 보안 중심 리뷰
- `/check-tests` - 테스트 커버리지 분석

### 서브에이전트
- `security-reviewer` - 보안 취약점 감지
- `test-checker` - 테스트 커버리지 분석
- `performance-analyzer` - 성능 영향 평가

### MCP 서버
- PR 데이터를 위한 GitHub 통합

### 훅
- `pre-review.js` - 리뷰 전 검증

## 사용법

### 기본 PR 리뷰
```
/review-pr
```

### 보안 검사만
```
/check-security
```

### 테스트 커버리지 검사
```
/check-tests
```

## 요구 사항

- Claude Code 2.1+
- GitHub 접근 권한
- Git 저장소

## 설정

GitHub 토큰을 설정하세요:
```bash
export GITHUB_TOKEN="your_github_token"
```

## 워크플로우 예

```
사용자: /review-pr

Claude:
1. 리뷰 전 훅 실행(git 저장소 검증)
2. GitHub MCP로 PR 데이터 가져오기
3. 보안 리뷰는 security-reviewer 서브에이전트에게 위임
4. 테스트 검사는 test-checker 서브에이전트에게 위임
5. 성능 분석은 performance-analyzer 서브에이전트에게 위임
6. 모든 발견 사항 종합
7. 종합 리뷰 보고서 제공

결과:
✅ 보안: 심각한 문제 없음
⚠️  테스트: 커버리지 65%, 80% 이상 권장
✅ 성능: 큰 영향 없음
📝 권장 사항: 엣지 케이스 테스트 추가
```

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
