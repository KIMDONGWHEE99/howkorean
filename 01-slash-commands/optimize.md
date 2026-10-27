---
description: 코드의 성능 문제를 분석하고 최적화 방안 제안
---

# 코드 최적화

주어진 코드에서 다음 문제를 우선순위 순서대로 검토하세요:

1. **성능 병목** - O(n²) 연산, 비효율적인 반복문 찾기
2. **메모리 누수** - 해제되지 않은 리소스, 순환 참조 찾기
3. **알고리즘 개선** - 더 나은 알고리즘이나 자료 구조 제안
4. **캐싱 기회** - 반복되는 계산 찾기
5. **동시성 문제** - 경쟁 조건이나 스레딩 문제 찾기

응답에는 다음을 담으세요:
- 문제 심각도(Critical/High/Medium/Low)
- 코드 내 위치
- 설명
- 코드 예제를 포함한 권장 수정 방법

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
