---
description: 소스 코드에서 종합적인 API 문서 생성
---

# API 문서 생성기

다음 순서로 API 문서를 생성하세요:

1. `/src/api/`의 모든 파일 스캔
2. 함수 시그니처와 JSDoc 주석 추출
3. 엔드포인트/모듈별로 정리
4. 예제를 포함한 마크다운 작성
5. 요청/응답 스키마 포함
6. 오류 문서 추가

출력 형식:
- `/docs/api.md`에 마크다운 파일로 저장
- 모든 엔드포인트에 curl 예제 포함
- TypeScript 타입 추가

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
