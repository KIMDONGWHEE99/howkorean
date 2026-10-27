---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*)
argument-hint: [message]
description: 컨텍스트를 반영해 git 커밋 생성
---

## 컨텍스트

- 현재 git 상태: !`git status`
- 현재 git diff: !`git diff HEAD`
- 현재 브랜치: !`git branch --show-current`
- 최근 커밋: !`git log --oneline -10`

## 할 일

위 변경 사항을 바탕으로 git 커밋 하나를 만드세요.

인수로 메시지가 주어졌다면 그 메시지를 쓰세요: $ARGUMENTS

그렇지 않다면 변경 사항을 분석해 Conventional Commits 형식에 맞는 커밋 메시지를 만드세요:
- `feat:` 새 기능
- `fix:` 버그 수정
- `docs:` 문서 변경
- `refactor:` 코드 리팩토링
- `test:` 테스트 추가
- `chore:` 유지 관리 작업

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
