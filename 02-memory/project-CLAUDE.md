# 프로젝트 설정

## 프로젝트 개요
- **이름**: 전자상거래 플랫폼
- **기술 스택**: Node.js, PostgreSQL, React 18, Docker
- **팀 규모**: 개발자 5명
- **마감**: 2025년 4분기

## 아키텍처
@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 개발 표준

### 코드 스타일
- 포맷팅에는 Prettier 사용
- airbnb 설정으로 ESLint 사용
- 최대 줄 길이: 100자
- 2칸 들여쓰기 사용

### 이름 규칙
- **파일**: kebab-case (user-controller.js)
- **클래스**: PascalCase (UserService)
- **함수/변수**: camelCase (getUserById)
- **상수**: UPPER_SNAKE_CASE (API_BASE_URL)
- **데이터베이스 테이블**: snake_case (user_accounts)

### Git 워크플로우
- 브랜치 이름: `feature/description` 또는 `fix/description`
- 커밋 메시지: Conventional Commits 규칙 준수
- 병합 전 PR 필수
- 모든 CI/CD 검사 통과 필수
- 최소 1명의 승인 필요

### 테스트 요구 사항
- 코드 커버리지 최소 80%
- 모든 핵심 경로에 테스트 필수
- 단위 테스트에는 Jest 사용
- E2E 테스트에는 Cypress 사용
- 테스트 파일 이름: `*.test.ts` 또는 `*.spec.ts`

### API 표준
- RESTful 엔드포인트만 사용
- JSON 요청/응답
- HTTP 상태 코드를 올바르게 사용
- API 엔드포인트 버전 관리: `/api/v1/`
- 모든 엔드포인트를 예제와 함께 문서화

### 데이터베이스
- 스키마 변경에는 마이그레이션 사용
- 자격 증명 하드코딩 금지
- 커넥션 풀링 사용
- 개발 환경에서는 쿼리 로깅 켜기
- 정기 백업 필수

### 배포
- Docker 기반 배포
- Kubernetes 오케스트레이션
- 블루-그린 배포 전략
- 실패 시 자동 롤백
- 배포 전에 데이터베이스 마이그레이션 실행

## 자주 쓰는 명령어

| 명령어 | 목적 |
|---------|---------|
| `npm run dev` | 개발 서버 시작 |
| `npm test` | 테스트 스위트 실행 |
| `npm run lint` | 코드 스타일 검사 |
| `npm run build` | 프로덕션 빌드 |
| `npm run migrate` | 데이터베이스 마이그레이션 실행 |

## 팀 연락처
- 테크 리드: Sarah Chen (@sarah.chen)
- 프로덕트 매니저: Mike Johnson (@mike.j)
- DevOps: Alex Kim (@alex.k)

## 알려진 문제와 우회 방법
- 사용량이 많은 시간대에는 PostgreSQL 커넥션 풀이 20개로 제한됨
- 우회 방법: 쿼리 대기열 구현
- Safari 14에서 async generator 호환성 문제
- 우회 방법: Babel 트랜스파일러 사용

## 관련 프로젝트
- 분석 대시보드: `/projects/analytics`
- 모바일 앱: `/projects/mobile`
- 관리자 패널: `/projects/admin`

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/memory
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
