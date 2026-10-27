#!/usr/bin/env python3
"""
코드 복잡도 분석기

Python, JavaScript, TypeScript 파일의 코드 복잡도 지표를 분석합니다.
변경 전후 지표를 비교해 리팩토링의 효과를 측정하는 데 도움이 됩니다.

사용법:
    python analyze-complexity.py <file>
    python analyze-complexity.py <before_file> <after_file>  # 비교 모드
    python analyze-complexity.py --dir <directory>           # 디렉토리 분석

지표:
    - 순환 복잡도(Cyclomatic Complexity): 코드의 결정 지점
    - 인지 복잡도(Cognitive Complexity): 코드를 이해하기가 얼마나 어려운지
    - 유지 보수성 지수(Maintainability Index): 전체 유지 보수성 점수(0-100)
    - 코드 줄 수(Lines of Code): 전체 줄 수
    - 함수 수(Function Count): 함수/메서드 개수
    - 평균 함수 길이(Average Function Length): 함수당 줄 수
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class FunctionMetrics:
    """함수 하나의 지표."""
    name: str
    start_line: int
    end_line: int
    lines: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    parameter_count: int


@dataclass
class FileMetrics:
    """파일 하나의 지표."""
    filename: str
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    function_count: int
    class_count: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    maintainability_index: float
    avg_function_length: float
    max_function_length: int
    functions: List[FunctionMetrics]


class ComplexityAnalyzer:
    """여러 언어의 코드 복잡도를 분석합니다."""

    # 언어별 패턴
    PATTERNS = {
        'python': {
            'function': r'^\s*def\s+(\w+)\s*\(',
            'class': r'^\s*class\s+(\w+)',
            'decision': [r'\bif\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
                        r'\bexcept\b', r'\band\b(?!$)', r'\bor\b(?!$)',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*#',
            'multiline_comment_start': r'^\s*["\'][\"\'][\"\']',
            'multiline_comment_end': r'["\'][\"\'][\"\']',
        },
        'javascript': {
            'function': r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+(\w+)',
            'decision': [r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bwhile\b',
                        r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*//',
            'multiline_comment_start': r'/\*',
            'multiline_comment_end': r'\*/',
        },
        'typescript': {
            'function': r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))',
            'class': r'class\s+(\w+)',
            'decision': [r'\bif\b', r'\belse\s+if\b', r'\bfor\b', r'\bwhile\b',
                        r'\bcatch\b', r'\b\?\b', r'\b&&\b', r'\b\|\|\b',
                        r'\bcase\b', r'\btry\b'],
            'comment': r'^\s*//',
            'multiline_comment_start': r'/\*',
            'multiline_comment_end': r'\*/',
        }
    }

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.language = self._detect_language()
        self.patterns = self.PATTERNS.get(self.language, self.PATTERNS['python'])

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.code = f.read()
        self.lines = self.code.split('\n')

    def _detect_language(self) -> str:
        """파일 확장자로 프로그래밍 언어를 감지합니다."""
        ext = os.path.splitext(self.filepath)[1].lower()
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
        }
        return ext_map.get(ext, 'python')

    def calculate_cyclomatic_complexity(self, code: Optional[str] = None) -> int:
        """
        McCabe 방법으로 순환 복잡도를 계산합니다.
        CC = E - N + 2P (E=간선, N=노드, P=연결 요소)
        단순화: 결정 지점 수 + 1
        """
        if code is None:
            code = self.code

        complexity = 1  # 기본 복잡도

        for pattern in self.patterns['decision']:
            matches = re.findall(pattern, code)
            complexity += len(matches)

        return complexity

    def calculate_cognitive_complexity(self, code: Optional[str] = None) -> int:
        """
        인지 복잡도를 계산합니다.
        코드를 이해하기가 얼마나 어려운지 측정합니다.
        중첩 깊이와 제어 흐름의 끊김을 반영합니다.
        """
        if code is None:
            code = self.code

        lines = code.split('\n')
        cognitive = 0
        nesting_depth = 0
        in_function = False

        for line in lines:
            stripped = line.strip()

            # 함수 경계 추적
            if re.search(self.patterns['function'], line):
                in_function = True
                nesting_depth = 0

            # 제어 흐름 구조마다 증가
            if re.search(r'\b(if|for|while|switch)\b', stripped):
                nesting_depth += 1
                cognitive += nesting_depth  # 중첩된 구조일수록 비용이 큼

            elif re.search(r'\b(elif|else if|else|catch|finally)\b', stripped):
                cognitive += nesting_depth  # 부모와 같은 수준

            # 중괄호/들여쓰기로 중첩 추적
            if self.language in ['javascript', 'typescript']:
                nesting_depth += stripped.count('{') - stripped.count('}')
                nesting_depth = max(0, nesting_depth)

            # 직선 흐름이 끊기면 가산점
            if re.search(r'\b(break|continue|return|throw)\b', stripped):
                if nesting_depth > 1:
                    cognitive += 1

            # 재귀에 가산점
            # (단순화: 함수가 자기 자신을 호출하는지만 확인)

        return cognitive

    def calculate_maintainability_index(self) -> float:
        """
        유지 보수성 지수(0-100)를 계산합니다.
        Halstead Volume, 순환 복잡도, 코드 줄 수를 바탕으로 합니다.

        MI = max(0, (171 - 5.2*ln(V) - 0.23*CC - 16.2*ln(LOC)) * 100/171)

        해석:
        - 85-100: 유지 보수하기 매우 쉬움
        - 65-84: 유지 보수하기 적당함
        - 50-64: 유지 보수하기 어려움
        - 0-49: 유지 보수하기 매우 어려움
        """
        import math

        loc = len([l for l in self.lines if l.strip()])
        cc = self.calculate_cyclomatic_complexity()

        # 단순화한 Halstead Volume 근삿값
        # 고유한 연산자와 피연산자 세기
        operators = len(re.findall(r'[+\-*/%=<>!&|^~]', self.code))
        operands = len(re.findall(r'\b\w+\b', self.code))
        volume = (operators + operands) * math.log2(max(1, operators + operands))

        # MI 계산
        mi = 171 - 5.2 * math.log(max(1, volume)) - 0.23 * cc - 16.2 * math.log(max(1, loc))
        mi = max(0, min(100, mi * 100 / 171))

        return round(mi, 2)

    def count_lines(self) -> Dict[str, int]:
        """종류별 줄 수를 셉니다."""
        total = len(self.lines)
        blank = 0
        comment = 0
        in_multiline_comment = False

        for line in self.lines:
            stripped = line.strip()

            # 여러 줄 주석 확인
            if re.search(self.patterns['multiline_comment_start'], stripped):
                in_multiline_comment = True
            if re.search(self.patterns['multiline_comment_end'], stripped):
                in_multiline_comment = False
                comment += 1
                continue

            if in_multiline_comment:
                comment += 1
            elif not stripped:
                blank += 1
            elif re.match(self.patterns['comment'], stripped):
                comment += 1

        return {
            'total': total,
            'blank': blank,
            'comment': comment,
            'code': total - blank - comment
        }

    def find_functions(self) -> List[FunctionMetrics]:
        """모든 함수를 찾아 각각의 지표를 계산합니다."""
        functions = []
        current_function = None
        function_start = 0
        brace_depth = 0

        for i, line in enumerate(self.lines):
            # 함수 정의인지 확인
            match = re.search(self.patterns['function'], line)
            if match:
                # 이전 함수가 있으면 저장
                if current_function:
                    func_code = '\n'.join(self.lines[function_start:i])
                    functions.append(self._create_function_metrics(
                        current_function, function_start, i - 1, func_code
                    ))

                current_function = match.group(1) or match.group(2) if match.lastindex and match.lastindex > 1 else match.group(1)
                function_start = i
                brace_depth = 0

            # JS/TS는 중괄호 추적
            if self.language in ['javascript', 'typescript']:
                brace_depth += line.count('{') - line.count('}')

        # 마지막 함수도 잊지 말기
        if current_function:
            func_code = '\n'.join(self.lines[function_start:])
            functions.append(self._create_function_metrics(
                current_function, function_start, len(self.lines) - 1, func_code
            ))

        return functions

    def _create_function_metrics(self, name: str, start: int, end: int, code: str) -> FunctionMetrics:
        """함수 하나의 지표를 만듭니다."""
        lines = end - start + 1

        # 매개변수 세기(단순화)
        param_match = re.search(r'\(([^)]*)\)', code.split('\n')[0])
        param_count = 0
        if param_match and param_match.group(1).strip():
            param_count = len([p for p in param_match.group(1).split(',') if p.strip()])

        return FunctionMetrics(
            name=name,
            start_line=start + 1,
            end_line=end + 1,
            lines=lines,
            cyclomatic_complexity=self.calculate_cyclomatic_complexity(code),
            cognitive_complexity=self.calculate_cognitive_complexity(code),
            parameter_count=param_count
        )

    def analyze(self) -> FileMetrics:
        """파일 전체를 분석합니다."""
        line_counts = self.count_lines()
        functions = self.find_functions()

        # 클래스 세기
        class_count = len(re.findall(self.patterns['class'], self.code))

        # 평균 계산
        func_lengths = [f.lines for f in functions] if functions else [0]
        avg_func_length = sum(func_lengths) / len(func_lengths)
        max_func_length = max(func_lengths)

        return FileMetrics(
            filename=self.filename,
            lines_of_code=line_counts['code'],
            blank_lines=line_counts['blank'],
            comment_lines=line_counts['comment'],
            function_count=len(functions),
            class_count=class_count,
            cyclomatic_complexity=self.calculate_cyclomatic_complexity(),
            cognitive_complexity=self.calculate_cognitive_complexity(),
            maintainability_index=self.calculate_maintainability_index(),
            avg_function_length=round(avg_func_length, 1),
            max_function_length=max_func_length,
            functions=functions
        )


def print_metrics(metrics: FileMetrics, verbose: bool = False) -> None:
    """지표를 읽기 쉬운 형식으로 출력합니다."""
    print("=" * 60)
    print(f"CODE COMPLEXITY ANALYSIS: {metrics.filename}")
    print("=" * 60)

    print("\n📊 OVERVIEW")
    print("-" * 40)
    print(f"  Lines of Code:          {metrics.lines_of_code}")
    print(f"  Blank Lines:            {metrics.blank_lines}")
    print(f"  Comment Lines:          {metrics.comment_lines}")
    print(f"  Functions/Methods:      {metrics.function_count}")
    print(f"  Classes:                {metrics.class_count}")

    print("\n📈 COMPLEXITY METRICS")
    print("-" * 40)
    print(f"  Cyclomatic Complexity:  {metrics.cyclomatic_complexity}")
    print(f"  Cognitive Complexity:   {metrics.cognitive_complexity}")
    print(f"  Maintainability Index:  {metrics.maintainability_index}")

    # 유지 보수성 해석
    mi = metrics.maintainability_index
    if mi >= 85:
        mi_label = "Highly maintainable ✅"
    elif mi >= 65:
        mi_label = "Moderately maintainable 🔶"
    elif mi >= 50:
        mi_label = "Difficult to maintain ⚠️"
    else:
        mi_label = "Very difficult to maintain ❌"
    print(f"    → {mi_label}")

    print("\n📐 FUNCTION METRICS")
    print("-" * 40)
    print(f"  Avg Function Length:    {metrics.avg_function_length} lines")
    print(f"  Max Function Length:    {metrics.max_function_length} lines")

    if verbose and metrics.functions:
        print("\n📋 FUNCTION DETAILS")
        print("-" * 40)
        for f in sorted(metrics.functions, key=lambda x: x.cyclomatic_complexity, reverse=True):
            flag = " ⚠️" if f.cyclomatic_complexity > 10 or f.lines > 50 else ""
            print(f"  {f.name}() [lines {f.start_line}-{f.end_line}]{flag}")
            print(f"    - Lines: {f.lines}, CC: {f.cyclomatic_complexity}, "
                  f"Cognitive: {f.cognitive_complexity}, Params: {f.parameter_count}")

    print("\n" + "=" * 60)


def print_comparison(before: FileMetrics, after: FileMetrics) -> None:
    """두 분석 결과의 비교를 출력합니다."""
    print("=" * 70)
    print("CODE COMPLEXITY COMPARISON")
    print("=" * 70)

    print(f"\n{'Metric':<30} {'Before':<15} {'After':<15} {'Change':<10}")
    print("-" * 70)

    def fmt_change(before_val, after_val, lower_is_better=True):
        diff = after_val - before_val
        if lower_is_better:
            symbol = "✅" if diff < 0 else ("⚠️" if diff > 0 else "➖")
        else:
            symbol = "✅" if diff > 0 else ("⚠️" if diff < 0 else "➖")
        return f"{diff:+.1f} {symbol}" if isinstance(diff, float) else f"{diff:+d} {symbol}"

    metrics = [
        ("Lines of Code", before.lines_of_code, after.lines_of_code, True),
        ("Function Count", before.function_count, after.function_count, False),
        ("Class Count", before.class_count, after.class_count, False),
        ("Cyclomatic Complexity", before.cyclomatic_complexity, after.cyclomatic_complexity, True),
        ("Cognitive Complexity", before.cognitive_complexity, after.cognitive_complexity, True),
        ("Maintainability Index", before.maintainability_index, after.maintainability_index, False),
        ("Avg Function Length", before.avg_function_length, after.avg_function_length, True),
        ("Max Function Length", before.max_function_length, after.max_function_length, True),
    ]

    for name, b_val, a_val, lower_better in metrics:
        change = fmt_change(b_val, a_val, lower_better)
        print(f"{name:<30} {b_val:<15} {a_val:<15} {change:<10}")

    print("\n" + "=" * 70)

    # 전체 평가
    print("\n🎯 ASSESSMENT")
    print("-" * 40)

    improvements = 0
    regressions = 0

    if after.maintainability_index > before.maintainability_index:
        print("  ✅ Maintainability improved")
        improvements += 1
    elif after.maintainability_index < before.maintainability_index:
        print("  ⚠️ Maintainability decreased")
        regressions += 1

    if after.cyclomatic_complexity < before.cyclomatic_complexity:
        print("  ✅ Complexity reduced")
        improvements += 1
    elif after.cyclomatic_complexity > before.cyclomatic_complexity:
        print("  ⚠️ Complexity increased")
        regressions += 1

    if after.avg_function_length < before.avg_function_length:
        print("  ✅ Functions are smaller on average")
        improvements += 1
    elif after.avg_function_length > before.avg_function_length:
        print("  ⚠️ Functions grew larger on average")
        regressions += 1

    print(f"\n  Summary: {improvements} improvements, {regressions} regressions")
    print("=" * 70)


def analyze_directory(directory: str, verbose: bool = False) -> None:
    """디렉토리 안의 지원되는 파일을 모두 분석합니다."""
    supported_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx']
    files = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in supported_extensions):
                files.append(os.path.join(root, filename))

    if not files:
        print(f"No supported files found in {directory}")
        return

    print(f"Analyzing {len(files)} files in {directory}...\n")

    total_loc = 0
    total_cc = 0
    total_functions = 0
    all_metrics = []

    for filepath in sorted(files):
        try:
            analyzer = ComplexityAnalyzer(filepath)
            metrics = analyzer.analyze()
            all_metrics.append(metrics)

            total_loc += metrics.lines_of_code
            total_cc += metrics.cyclomatic_complexity
            total_functions += metrics.function_count

            if verbose:
                print_metrics(metrics, verbose=True)
            else:
                flag = " ⚠️" if metrics.maintainability_index < 65 else ""
                print(f"  {metrics.filename}: LOC={metrics.lines_of_code}, "
                      f"CC={metrics.cyclomatic_complexity}, MI={metrics.maintainability_index}{flag}")
        except Exception as e:
            print(f"  Error analyzing {filepath}: {e}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files analyzed:         {len(all_metrics)}")
    print(f"  Total lines of code:    {total_loc}")
    print(f"  Total complexity:       {total_cc}")
    print(f"  Total functions:        {total_functions}")

    if all_metrics:
        avg_mi = sum(m.maintainability_index for m in all_metrics) / len(all_metrics)
        print(f"  Avg maintainability:    {avg_mi:.1f}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze code complexity metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s myfile.py                    Analyze single file
  %(prog)s before.py after.py           Compare two versions
  %(prog)s --dir src/                   Analyze directory
  %(prog)s -v myfile.py                 Verbose output with function details
        """
    )
    parser.add_argument('files', nargs='*', help='File(s) to analyze')
    parser.add_argument('--dir', '-d', help='Directory to analyze')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed function metrics')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.dir:
        analyze_directory(args.dir, args.verbose)
    elif len(args.files) == 1:
        analyzer = ComplexityAnalyzer(args.files[0])
        metrics = analyzer.analyze()

        if args.json:
            import json
            print(json.dumps({
                'filename': metrics.filename,
                'lines_of_code': metrics.lines_of_code,
                'cyclomatic_complexity': metrics.cyclomatic_complexity,
                'cognitive_complexity': metrics.cognitive_complexity,
                'maintainability_index': metrics.maintainability_index,
                'function_count': metrics.function_count,
                'avg_function_length': metrics.avg_function_length,
            }, indent=2))
        else:
            print_metrics(metrics, args.verbose)
    elif len(args.files) == 2:
        before_analyzer = ComplexityAnalyzer(args.files[0])
        after_analyzer = ComplexityAnalyzer(args.files[1])
        before_metrics = before_analyzer.analyze()
        after_metrics = after_analyzer.analyze()
        print_comparison(before_metrics, after_metrics)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
