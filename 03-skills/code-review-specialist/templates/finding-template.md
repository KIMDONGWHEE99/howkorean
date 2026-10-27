# 코드 리뷰 발견 사항 템플릿

코드 리뷰 중에 찾은 문제를 하나씩 기록할 때 이 템플릿을 쓰세요.

---

## 문제: [제목]

### 심각도
- [ ] Critical(배포를 막음)
- [ ] High(병합 전에 고쳐야 함)
- [ ] Medium(곧 고쳐야 함)
- [ ] Low(고치면 좋음)

### 범주
- [ ] 보안
- [ ] 성능
- [ ] 코드 품질
- [ ] 유지 보수성
- [ ] 테스트
- [ ] 디자인 패턴
- [ ] 문서화

### 위치
**파일:** `src/components/UserCard.tsx`

**줄:** 45-52

**함수/메서드:** `renderUserDetails()`

### 문제 설명

**무엇이 문제인가:** 문제가 무엇인지 설명하세요.

**왜 중요한가:** 영향과 이 문제를 고쳐야 하는 이유를 설명하세요.

**현재 동작:** 문제가 되는 코드나 동작을 보여 주세요.

**기대 동작:** 대신 어떻게 동작해야 하는지 설명하세요.

### 코드 예시

#### 현재(문제 있음)

```typescript
// N+1 쿼리 문제를 보여 줌
const users = fetchUsers();
users.forEach(user => {
  const posts = fetchUserPosts(user.id); // 사용자마다 쿼리 실행!
  renderUserPosts(posts);
});
```

#### 제안하는 수정

```typescript
// JOIN 쿼리로 최적화
const usersWithPosts = fetchUsersWithPosts();
usersWithPosts.forEach(({ user, posts }) => {
  renderUserPosts(posts);
});
```

### 영향 분석

| 측면 | 영향 | 심각도 |
|--------|--------|----------|
| 성능 | 사용자 20명에 쿼리 100개 이상 | High |
| 사용자 경험 | 페이지 로딩이 느림 | High |
| 확장성 | 규모가 커지면 무너짐 | Critical |
| 유지 보수성 | 디버깅이 어려움 | Medium |

### 관련 문제

- `AdminUserList.tsx` 120번째 줄에도 비슷한 문제
- 관련 PR: #456
- 관련 이슈: #789

### 추가 자료

- [N+1 쿼리 문제](https://en.wikipedia.org/wiki/N%2B1_problem)
- [데이터베이스 조인 문서](https://docs.example.com/joins)

### 리뷰어 메모

- 이 코드베이스에서 흔히 보이는 패턴입니다
- 코드 스타일 가이드에 추가하는 것을 고려하세요
- 도우미 함수를 만들 만한 가치가 있을 수 있습니다

### 작성자 응답(피드백용)

*코드 작성자가 채웁니다:*

- [ ] 수정을 반영한 커밋: `abc123`
- [ ] 수정 상태: 완료 / 진행 중 / 논의 필요
- [ ] 질문이나 우려 사항: (설명)

---

## 발견 사항 통계(리뷰어용)

발견 사항이 여러 개라면 다음을 집계하세요:

- **찾은 문제 총수:** X
- **Critical:** X
- **High:** X
- **Medium:** X
- **Low:** X

**권장:** ✅ 승인 / ⚠️ 변경 요청 / 🔄 논의 필요

**전체 코드 품질:** 별 1-5개

---

**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/skills
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
