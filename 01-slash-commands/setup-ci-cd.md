---
name: setup-ci-cd
description: 품질 보증을 위한 pre-commit 훅과 GitHub Actions 구성
---

# CI/CD 파이프라인 설정

프로젝트 유형에 맞춰 종합적인 DevOps 품질 게이트를 구현하세요:

1. **프로젝트 분석**: 언어, 프레임워크, 빌드 시스템, 기존 도구 파악
2. 언어별 도구로 **pre-commit 훅 구성**:
   - 포매팅: Prettier/Black/gofmt/rustfmt 등
   - 린팅: ESLint/Ruff/golangci-lint/Clippy 등
   - 보안: Bandit/gosec/cargo-audit/npm audit 등
   - 타입 검사: TypeScript/mypy/flow(해당하는 경우)
   - 테스트: 관련 테스트 스위트 실행
3. **GitHub Actions 워크플로우 만들기**(.github/workflows/):
   - push/PR 때 pre-commit 검사를 똑같이 실행
   - 여러 버전/플랫폼 매트릭스(해당하는 경우)
   - 빌드와 테스트 검증
   - 배포 단계(필요한 경우)
4. **파이프라인 검증**: 로컬에서 테스트하고, 테스트용 PR을 만들어 모든 검사가 통과하는지 확인

무료/오픈 소스 도구를 쓰세요. 기존 설정을 존중하세요. 실행 속도를 빠르게 유지하세요.

---
**최종 업데이트**: 2026년 8월 4일
**Claude Code 버전**: 2.1.220
**출처**:
- https://code.claude.com/docs/ko/commands
**호환 모델**: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, Claude Sonnet 4.6, Claude Opus 4.8, Claude Haiku 4.5
