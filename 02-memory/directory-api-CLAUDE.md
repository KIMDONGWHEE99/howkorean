# API 모듈 표준

이 파일은 /src/api/ 안의 모든 것에 대해 루트 CLAUDE.md를 보완합니다. 메모리 파일은
덮어쓰지 않고 이어 붙으므로 루트 CLAUDE.md도 여전히 적용되며, Claude Code는
이 하위 트리의 파일을 읽거나 쓰거나 편집할 때 이 파일을 필요에 따라 로드합니다.

## API 전용 표준

### 요청 검증
- 스키마 검증에는 Zod 사용
- 입력은 항상 검증
- 검증 오류는 400으로 반환
- 필드 단위 오류 상세 포함

### 인증
- 모든 엔드포인트에 JWT 토큰 필요
- 토큰은 Authorization 헤더에 담기
- 토큰은 24시간 후 만료
- 리프레시 토큰 메커니즘 구현

### 응답 형식

모든 응답은 다음 구조를 따라야 합니다:

```json
{
  "success": true,
  "data": { /* 실제 데이터 */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

오류 응답:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "사용자에게 보여 줄 메시지",
    "details": { /* 필드 오류 */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 페이지네이션
- 커서 기반 페이지네이션 사용(오프셋 아님)
- `hasMore` 불리언 포함
- 최대 페이지 크기는 100으로 제한
- 기본 페이지 크기: 20

### 속도 제한
- 인증된 사용자는 시간당 요청 1000개
- 공개 엔드포인트는 시간당 요청 100개
- 초과하면 429 반환
- retry-after 헤더 포함

### 캐싱
- 세션 캐싱에는 Redis 사용
- 캐시 유지 시간: 기본 5분
- 쓰기 작업 시 무효화
- 캐시 키에 리소스 유형 태그 붙이기

---
**최종 업데이트**: 2026년 10월 10일
**Claude Code 버전**: 2.1.296
**출처**:
- https://code.claude.com/docs/ko/memory
- https://github.com/anthropics/claude-code/releases/tag/v2.1.288
- https://github.com/anthropics/claude-code/releases/tag/v2.1.293
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
