#!/usr/bin/env python3
"""
변경 전후 코드의 순환 복잡도를 비교합니다.
리팩토링이 실제로 코드 구조를 단순하게 만드는지 확인하는 데 도움이 됩니다.
"""

import re
import sys


class ComplexityAnalyzer:
    """코드 복잡도 지표를 분석합니다."""

    def __init__(self, code: str):
        self.code = code
        self.lines = code.split("\n")

    def calculate_cyclomatic_complexity(self) -> int:
        """
        McCabe 방법으로 순환 복잡도를 계산합니다.
        결정 지점을 셉니다: if, elif, else, for, while, except, and, or
        """
        complexity = 1  # 기본 복잡도

        # 결정 지점 세기
        decision_patterns = [
            r"\bif\b",
            r"\belif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\bexcept\b",
            r"\band\b(?!$)",
            r"\bor\b(?!$)",
        ]

        for pattern in decision_patterns:
            matches = re.findall(pattern, self.code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self) -> int:
        """
        인지 복잡도(코드를 이해하기가 얼마나 어려운지)를 계산합니다.
        중첩 깊이와 제어 흐름을 바탕으로 합니다.
        """
        cognitive = 0
        nesting_depth = 0

        for line in self.lines:
            # 중첩 깊이 추적
            if re.search(r"^\s*(if|for|while|def|class|try)\b", line):
                nesting_depth += 1
                cognitive += nesting_depth
            elif re.search(r"^\s*(elif|else|except|finally)\b", line):
                cognitive += nesting_depth

            # 들여쓰기가 줄어들면 중첩 깊이 줄이기
            if line and not line[0].isspace():
                nesting_depth = 0

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        유지 보수성 지수는 0-100 범위입니다.
        > 85: 매우 좋음
        > 65: 좋음
        > 50: 보통
        < 50: 나쁨
        """
        lines = len(self.lines)
        cyclomatic = self.calculate_cyclomatic_complexity()
        cognitive = self.calculate_cognitive_complexity()

        # 단순화한 MI 계산
        mi = (
            171
            - 5.2 * (cyclomatic / lines)
            - 0.23 * (cognitive)
            - 16.2 * (lines / 1000)
        )

        return max(0, min(100, mi))

    def get_complexity_report(self) -> dict:
        """종합 복잡도 보고서를 생성합니다."""
        return {
            "cyclomatic_complexity": self.calculate_cyclomatic_complexity(),
            "cognitive_complexity": self.calculate_cognitive_complexity(),
            "maintainability_index": round(self.calculate_maintainability_index(), 2),
            "lines_of_code": len(self.lines),
            "avg_line_length": round(
                sum(len(l) for l in self.lines) / len(self.lines), 2
            )
            if self.lines
            else 0,
        }


def compare_files(before_file: str, after_file: str) -> None:
    """두 코드 버전의 복잡도 지표를 비교합니다."""

    with open(before_file) as f:
        before_code = f.read()

    with open(after_file) as f:
        after_code = f.read()

    before_analyzer = ComplexityAnalyzer(before_code)
    after_analyzer = ComplexityAnalyzer(after_code)

    before_metrics = before_analyzer.get_complexity_report()
    after_metrics = after_analyzer.get_complexity_report()

    print("=" * 60)
    print("CODE COMPLEXITY COMPARISON")
    print("=" * 60)

    print("\nBEFORE:")
    print(f"  Cyclomatic Complexity:    {before_metrics['cyclomatic_complexity']}")
    print(f"  Cognitive Complexity:     {before_metrics['cognitive_complexity']}")
    print(f"  Maintainability Index:    {before_metrics['maintainability_index']}")
    print(f"  Lines of Code:            {before_metrics['lines_of_code']}")
    print(f"  Avg Line Length:          {before_metrics['avg_line_length']}")

    print("\nAFTER:")
    print(f"  Cyclomatic Complexity:    {after_metrics['cyclomatic_complexity']}")
    print(f"  Cognitive Complexity:     {after_metrics['cognitive_complexity']}")
    print(f"  Maintainability Index:    {after_metrics['maintainability_index']}")
    print(f"  Lines of Code:            {after_metrics['lines_of_code']}")
    print(f"  Avg Line Length:          {after_metrics['avg_line_length']}")

    print("\nCHANGES:")
    cyclomatic_change = (
        after_metrics["cyclomatic_complexity"] - before_metrics["cyclomatic_complexity"]
    )
    cognitive_change = (
        after_metrics["cognitive_complexity"] - before_metrics["cognitive_complexity"]
    )
    mi_change = (
        after_metrics["maintainability_index"] - before_metrics["maintainability_index"]
    )
    loc_change = after_metrics["lines_of_code"] - before_metrics["lines_of_code"]

    print(f"  Cyclomatic Complexity:    {cyclomatic_change:+d}")
    print(f"  Cognitive Complexity:     {cognitive_change:+d}")
    print(f"  Maintainability Index:    {mi_change:+.2f}")
    print(f"  Lines of Code:            {loc_change:+d}")

    print("\nASSESSMENT:")
    if mi_change > 0:
        print("  ✅ Code is MORE maintainable")
    elif mi_change < 0:
        print("  ⚠️  Code is LESS maintainable")
    else:
        print("  ➡️  Maintainability unchanged")

    if cyclomatic_change < 0:
        print("  ✅ Complexity DECREASED")
    elif cyclomatic_change > 0:
        print("  ⚠️  Complexity INCREASED")
    else:
        print("  ➡️  Complexity unchanged")

    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare-complexity.py <before_file> <after_file>")
        sys.exit(1)

    compare_files(sys.argv[1], sys.argv[2])
