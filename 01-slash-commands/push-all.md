---
description: 모든 변경 사항을 스테이징하고 커밋한 뒤 원격으로 푸시(주의해서 사용)
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git diff:*), Bash(git log:*), Bash(git pull:*)
---

# 전부 커밋하고 푸시하기

⚠️ **주의**: 모든 변경 사항을 스테이징하고 커밋한 뒤 원격으로 푸시합니다. 모든 변경 사항이 한 커밋에 함께 들어가도 된다고 확신할 때만 쓰세요.

## 워크플로우

### 1. 변경 사항 분석
병렬로 실행:
- `git status` - 수정/추가/삭제/추적되지 않은 파일 표시
- `git diff --stat` - 변경 통계 표시
- `git log -1 --oneline` - 메시지 스타일을 참고할 최근 커밋 표시

### 2. 안전 검사

**❌ 다음이 감지되면 멈추고 경고:**
- 비밀 정보: `.env*`, `*.key`, `*.pem`, `credentials.json`, `secrets.yaml`, `id_rsa`, `*.p12`, `*.pfx`, `*.cer`
- API 키: 실제 값이 들어 있는 `*_API_KEY`, `*_SECRET`, `*_TOKEN` 변수(`your-api-key`, `xxx`, `placeholder` 같은 자리 표시자는 제외)
- 큰 파일: Git LFS 없이 `>10MB`인 파일
- 빌드 결과물: `node_modules/`, `dist/`, `build/`, `__pycache__/`, `*.pyc`, `.venv/`
- 임시 파일: `.DS_Store`, `thumbs.db`, `*.swp`, `*.tmp`

**API 키 검증:**
수정된 파일에서 다음과 같은 패턴을 확인하세요:
```bash
OPENAI_API_KEY=sk-proj-xxxxx  # ❌ 실제 키 감지!
AWS_SECRET_KEY=AKIA...         # ❌ 실제 키 감지!
STRIPE_API_KEY=sk_live_...    # ❌ 실제 키 감지!

# ✅ 허용되는 자리 표시자:
API_KEY=your-api-key-here
SECRET_KEY=placeholder
TOKEN=xxx
API_KEY=<your-key>
SECRET=${YOUR_SECRET}
```

**✅ 확인:**
- `.gitignore`가 제대로 설정되어 있음
- 병합 충돌 없음
- 올바른 브랜치(main/master이면 경고)
- API 키는 자리 표시자뿐임

### 3. 확인 요청

요약 제시:
```
📊 변경 사항 요약:
- 파일 X개 수정, Y개 추가, Z개 삭제
- 합계: +AAA줄 추가, -BBB줄 삭제

🔒 안전: ✅ 비밀 정보 없음 | ✅ 큰 파일 없음 | ⚠️ [경고]
🌿 브랜치: [name] → origin/[name]

실행할 작업: git add . → commit → push

진행하려면 'yes'(또는 '예'), 취소하려면 'no'(또는 '아니요')를 입력하세요.
```

**명시적으로 "yes"(또는 "예")라는 답을 받기 전에는 진행하지 마세요.**

### 4. 실행(확인 후)

순서대로 실행:
```bash
git add .
git status  # 스테이징 확인
```

### 5. 커밋 메시지 생성

변경 사항을 분석해 Conventional Commits 형식의 커밋 메시지를 만드세요:

**형식:**
```
[type]: 간단한 요약(최대 72자)

- 주요 변경 1
- 주요 변경 2
- 주요 변경 3
```

**유형:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`

**예:**
```
docs: 개념별 README 파일에 종합적인 문서 추가

- 아키텍처 다이어그램과 표 추가
- 실용적인 예제 포함
- 모범 사례 섹션 확장
```

### 6. 커밋과 푸시

```bash
git commit -m "$(cat <<'EOF'
[생성한 커밋 메시지]
EOF
)"
git push  # 실패하면: git pull --rebase && git push
git log -1 --oneline --decorate  # 확인
```

### 7. 성공 확인

```
✅ 원격으로 푸시했습니다!

커밋: [hash] [message]
브랜치: [branch] → origin/[branch]
변경된 파일: X개(+추가, -삭제)
```

## 오류 처리

- **git add 실패**: 권한과 잠긴 파일을 확인하고, 저장소가 초기화되어 있는지 확인
- **git commit 실패**: pre-commit 훅 문제를 고치고, git 설정(user.name/email) 확인
- **git push 실패**:
  - Non-fast-forward: `git pull --rebase && git push`
  - 원격 브랜치 없음: `git push -u origin [branch]`
  - 보호된 브랜치: 대신 PR 워크플로우 사용

## 언제 쓸까

✅ **적합한 경우:**
- 여러 파일에 걸친 문서 업데이트
- 테스트와 문서를 함께 갖춘 기능
- 여러 파일에 걸친 버그 수정
- 프로젝트 전체의 서식 정리/리팩토링
- 설정 변경

❌ **피해야 할 경우:**
- 무엇이 커밋되는지 확실하지 않음
- 비밀 정보/민감한 데이터가 들어 있음
- 리뷰 없이 보호된 브랜치에 푸시
- 병합 충돌이 남아 있음
- 커밋 기록을 잘게 나누고 싶음
- pre-commit 훅이 실패함

## 대안

사용자가 직접 제어하고 싶어 하면 다음을 제안하세요:
1. **선택적 스테이징**: 특정 파일만 검토하고 스테이징
2. **대화형 스테이징**: `git add -p`로 패치 단위 선택
3. **PR 워크플로우**: 브랜치 만들기 → 푸시 → PR(`/pr` 명령어 사용)

**⚠️ 기억하세요**: 푸시하기 전에 항상 변경 사항을 검토하세요. 확신이 서지 않으면 git 명령어를 하나씩 실행해 더 세밀하게 제어하세요.

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
