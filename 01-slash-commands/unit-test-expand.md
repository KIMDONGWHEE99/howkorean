---
name: unit-test-expand
description: 테스트되지 않은 분기와 엣지 케이스를 겨냥해 테스트 커버리지 확대
---

# 단위 테스트 확장

프로젝트의 테스트 프레임워크에 맞춰 기존 단위 테스트를 확장하세요:

1. **커버리지 분석**: 커버리지 보고서를 실행해 테스트되지 않은 분기, 엣지 케이스, 커버리지가 낮은 부분 파악
2. **빈틈 찾기**: 코드에서 논리 분기, 오류 경로, 경계 조건, null/빈 입력 검토
3. 프로젝트의 프레임워크로 **테스트 작성**:
   - Jest/Vitest/Mocha (JavaScript/TypeScript)
   - pytest/unittest (Python)
   - Go testing/testify (Go)
   - Rust 테스트 프레임워크 (Rust)
4. **특정 시나리오 겨냥**:
   - 오류 처리와 예외
   - 경계값(최솟값/최댓값, 빈 값, null)
   - 엣지 케이스와 코너 케이스
   - 상태 전이와 부수 효과
5. **개선 확인**: 커버리지를 다시 실행해 측정 가능한 만큼 늘었는지 확인

새 테스트 코드 블록만 제시하세요. 기존 테스트 패턴과 이름 규칙을 따르세요.

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
