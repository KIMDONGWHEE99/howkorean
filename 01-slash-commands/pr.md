---
description: 코드를 정리하고 변경 사항을 스테이징해 풀 리퀘스트 준비
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(npm test:*), Bash(npm run lint:*)
---

# 풀 리퀘스트 준비 체크리스트

PR을 만들기 전에 다음 단계를 실행하세요:

1. 린트 실행: `prettier --write .`
2. 테스트 실행: `npm test`
3. git diff 검토: `git diff HEAD`
4. 변경 사항 스테이징: `git add .`
5. Conventional Commits 형식에 맞춰 커밋 메시지 작성:
   - `fix:` 버그 수정
   - `feat:` 새 기능
   - `docs:` 문서
   - `refactor:` 코드 구조 개선
   - `test:` 테스트 추가
   - `chore:` 유지 관리

6. 다음을 담은 PR 요약 작성:
   - 무엇이 바뀌었는지
   - 왜 바뀌었는지
   - 수행한 테스트
   - 예상되는 영향

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
