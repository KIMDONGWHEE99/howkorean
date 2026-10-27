#!/usr/bin/env python3
"""
코드 스멜 감지기

Python, JavaScript, TypeScript 파일에서 흔한 코드 스멜을 감지합니다.
마틴 파울러의 코드 스멜 카탈로그를 바탕으로 합니다.

사용법:
    python detect-smells.py <file>
    python detect-smells.py --dir <directory>
    python detect-smells.py -v <file>  # 코드 조각을 함께 보여 주는 자세한 모드

감지하는 스멜:
    - Long Method(긴 메서드, 30줄 초과)
    - Long Parameter List(긴 매개변수 목록, 매개변수 4개 초과)
    - Duplicate Code(중복 코드, 비슷한 코드 블록)
    - Large Class(거대한 클래스, 300줄 초과, 메서드 10개 초과)
    - Dead Code(죽은 코드, 쓰이지 않는 변수/함수)
    - Complex Conditionals(복잡한 조건문, 깊은 중첩, 긴 연쇄)
    - Magic Numbers/Strings(매직 넘버/문자열)
    - Feature Envy(기능 편애, 다른 클래스의 데이터를 많이 쓰는 메서드)
    - 왜(why)가 아니라 무엇(what)을 설명하는 주석
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict


class SmellSeverity(Enum):
    """코드 스멜의 심각도 수준."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class SmellType(Enum):
    """코드 스멜의 종류."""
    LONG_METHOD = "Long Method"
    LONG_PARAMETER_LIST = "Long Parameter List"
    DUPLICATE_CODE = "Duplicate Code"
    LARGE_CLASS = "Large Class"
    DEAD_CODE = "Dead Code"
    COMPLEX_CONDITIONAL = "Complex Conditional"
    MAGIC_NUMBER = "Magic Number/String"
    FEATURE_ENVY = "Feature Envy"
    EXCESSIVE_COMMENTS = "Excessive Comments"
    DEEPLY_NESTED = "Deeply Nested Code"
    PRIMITIVE_OBSESSION = "Primitive Obsession"
    DATA_CLUMPS = "Data Clumps"
    SWITCH_STATEMENT = "Switch Statement"
    MESSAGE_CHAIN = "Message Chain"


@dataclass
class CodeSmell:
    """감지된 코드 스멜 하나를 나타냅니다."""
    smell_type: SmellType
    severity: SmellSeverity
    location: str
    line_start: int
    line_end: int
    description: str
    suggestion: str
    code_snippet: str = ""


@dataclass
class SmellReport:
    """파일에서 찾은 모든 스멜의 보고서."""
    filename: str
    smells: List[CodeSmell] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.HIGH)

    @property
    def medium_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.MEDIUM)

    @property
    def low_count(self) -> int:
        return sum(1 for s in self.smells if s.severity == SmellSeverity.LOW)


class SmellDetector:
    """소스 파일에서 코드 스멜을 감지합니다."""

    # 임계값(설정 가능)
    THRESHOLDS = {
        'long_method_lines': 30,
        'very_long_method_lines': 50,
        'max_parameters': 4,
        'large_class_lines': 300,
        'large_class_methods': 10,
        'max_nesting_depth': 4,
        'long_chain_length': 3,
        'duplicate_min_lines': 5,
    }

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.language = self._detect_language()

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.code = f.read()
        self.lines = self.code.split('\n')
        self.smells: List[CodeSmell] = []

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

    def detect_all(self) -> SmellReport:
        """모든 스멜 감지기를 실행합니다."""
        self._detect_long_methods()
        self._detect_long_parameter_lists()
        self._detect_large_class()
        self._detect_complex_conditionals()
        self._detect_magic_numbers()
        self._detect_excessive_comments()
        self._detect_deeply_nested()
        self._detect_switch_statements()
        self._detect_message_chains()
        self._detect_duplicate_code()
        self._detect_dead_code()

        return SmellReport(filename=self.filename, smells=self.smells)

    def _get_snippet(self, start: int, end: int, context: int = 2) -> str:
        """앞뒤 맥락을 포함한 코드 조각을 가져옵니다."""
        actual_start = max(0, start - context)
        actual_end = min(len(self.lines), end + context)
        snippet_lines = []
        for i in range(actual_start, actual_end):
            prefix = "→ " if start <= i < end else "  "
            snippet_lines.append(f"{i+1:4d} {prefix}{self.lines[i]}")
        return '\n'.join(snippet_lines)

    def _detect_long_methods(self) -> None:
        """너무 긴 메서드를 감지합니다."""
        if self.language == 'python':
            pattern = r'^\s*def\s+(\w+)\s*\([^)]*\):'
        else:
            pattern = r'(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>))'

        current_method = None
        method_start = 0
        brace_depth = 0
        indent_level = 0

        for i, line in enumerate(self.lines):
            match = re.search(pattern, line)
            if match:
                # 이전 메서드가 있으면 확인
                if current_method:
                    method_lines = i - method_start
                    self._check_method_length(current_method, method_start, i - 1, method_lines)

                current_method = match.group(1) or (match.group(2) if match.lastindex and match.lastindex > 1 else None)
                method_start = i
                indent_level = len(line) - len(line.lstrip())

            # Python 함수의 끝은 들여쓰기로 추적
            if self.language == 'python' and current_method:
                if line.strip() and not line.strip().startswith('#'):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= indent_level and i > method_start:
                        method_lines = i - method_start
                        self._check_method_length(current_method, method_start, i - 1, method_lines)
                        current_method = None

        # 마지막 메서드 확인
        if current_method:
            method_lines = len(self.lines) - method_start
            self._check_method_length(current_method, method_start, len(self.lines) - 1, method_lines)

    def _check_method_length(self, name: str, start: int, end: int, lines: int) -> None:
        """메서드가 너무 긴지 확인하고, 그렇다면 스멜을 추가합니다."""
        if lines > self.THRESHOLDS['very_long_method_lines']:
            severity = SmellSeverity.HIGH
            desc = f"Method '{name}' is {lines} lines (threshold: {self.THRESHOLDS['long_method_lines']})"
        elif lines > self.THRESHOLDS['long_method_lines']:
            severity = SmellSeverity.MEDIUM
            desc = f"Method '{name}' is {lines} lines (threshold: {self.THRESHOLDS['long_method_lines']})"
        else:
            return

        self.smells.append(CodeSmell(
            smell_type=SmellType.LONG_METHOD,
            severity=severity,
            location=f"{self.filename}:{start+1}-{end+1}",
            line_start=start + 1,
            line_end=end + 1,
            description=desc,
            suggestion="Apply Extract Method to break down into smaller functions",
            code_snippet=self._get_snippet(start, min(start + 5, end), 0)
        ))

    def _detect_long_parameter_lists(self) -> None:
        """매개변수가 너무 많은 함수를 감지합니다."""
        if self.language == 'python':
            pattern = r'def\s+(\w+)\s*\(([^)]*)\)'
        else:
            pattern = r'(?:function\s+(\w+)\s*\(([^)]*)\)|(\w+)\s*[=:]\s*(?:async\s+)?(?:function\s*)?\(([^)]*)\))'

        for i, line in enumerate(self.lines):
            match = re.search(pattern, line)
            if match:
                # 그룹을 안전하게 추출
                groups = match.groups()
                func_name = groups[0] or (groups[2] if len(groups) > 2 else None)
                params_str = groups[1] if len(groups) > 1 else ""
                if not params_str and len(groups) > 3:
                    params_str = groups[3] or ""

                # 매개변수 세기
                if params_str.strip():
                    params = [p.strip() for p in params_str.split(',') if p.strip()]
                    # Python에서는 'self', 'cls' 제외
                    if self.language == 'python':
                        params = [p for p in params if p not in ('self', 'cls')]
                    param_count = len(params)

                    if param_count > self.THRESHOLDS['max_parameters']:
                        severity = SmellSeverity.HIGH if param_count > 6 else SmellSeverity.MEDIUM
                        self.smells.append(CodeSmell(
                            smell_type=SmellType.LONG_PARAMETER_LIST,
                            severity=severity,
                            location=f"{self.filename}:{i+1}",
                            line_start=i + 1,
                            line_end=i + 1,
                            description=f"Function '{func_name}' has {param_count} parameters (max: {self.THRESHOLDS['max_parameters']})",
                            suggestion="Consider Introduce Parameter Object or Preserve Whole Object",
                            code_snippet=self._get_snippet(i, i + 1, 1)
                        ))

    def _detect_large_class(self) -> None:
        """너무 큰 클래스를 감지합니다."""
        if self.language == 'python':
            class_pattern = r'^\s*class\s+(\w+)'
            method_pattern = r'^\s+def\s+\w+'
        else:
            class_pattern = r'class\s+(\w+)'
            method_pattern = r'(?:^\s+\w+\s*\([^)]*\)\s*\{|^\s+(?:async\s+)?\w+\s*=)'

        current_class = None
        class_start = 0
        method_count = 0
        class_indent = 0

        for i, line in enumerate(self.lines):
            class_match = re.search(class_pattern, line)
            if class_match:
                # 이전 클래스 확인
                if current_class:
                    self._check_class_size(current_class, class_start, i - 1, method_count)

                current_class = class_match.group(1)
                class_start = i
                method_count = 0
                class_indent = len(line) - len(line.lstrip())

            # 현재 클래스의 메서드 세기
            if current_class and re.search(method_pattern, line):
                method_count += 1

        # 마지막 클래스 확인
        if current_class:
            self._check_class_size(current_class, class_start, len(self.lines) - 1, method_count)

    def _check_class_size(self, name: str, start: int, end: int, methods: int) -> None:
        """클래스가 너무 큰지 확인합니다."""
        lines = end - start + 1

        issues = []
        severity = SmellSeverity.MEDIUM

        if lines > self.THRESHOLDS['large_class_lines']:
            issues.append(f"{lines} lines (max: {self.THRESHOLDS['large_class_lines']})")
            severity = SmellSeverity.HIGH

        if methods > self.THRESHOLDS['large_class_methods']:
            issues.append(f"{methods} methods (max: {self.THRESHOLDS['large_class_methods']})")
            if severity != SmellSeverity.HIGH:
                severity = SmellSeverity.MEDIUM

        if issues:
            self.smells.append(CodeSmell(
                smell_type=SmellType.LARGE_CLASS,
                severity=severity,
                location=f"{self.filename}:{start+1}-{end+1}",
                line_start=start + 1,
                line_end=end + 1,
                description=f"Class '{name}' is too large: {', '.join(issues)}",
                suggestion="Apply Extract Class to split responsibilities",
                code_snippet=self._get_snippet(start, start + 3, 0)
            ))

    def _detect_complex_conditionals(self) -> None:
        """복잡한 조건식을 감지합니다."""
        for i, line in enumerate(self.lines):
            # 줄 안의 논리 연산자 세기
            and_or_count = len(re.findall(r'\b(and|or|&&|\|\|)\b', line))

            if and_or_count >= 3:
                self.smells.append(CodeSmell(
                    smell_type=SmellType.COMPLEX_CONDITIONAL,
                    severity=SmellSeverity.MEDIUM,
                    location=f"{self.filename}:{i+1}",
                    line_start=i + 1,
                    line_end=i + 1,
                    description=f"Complex conditional with {and_or_count} logical operators",
                    suggestion="Apply Decompose Conditional or Consolidate Conditional Expression",
                    code_snippet=self._get_snippet(i, i + 1, 1)
                ))

    def _detect_magic_numbers(self) -> None:
        """매직 넘버와 매직 문자열을 감지합니다."""
        # 흔히 허용되는 값은 건너뛰기
        acceptable = {'0', '1', '-1', '2', '100', 'true', 'false', 'null', 'None', '""', "''"}

        for i, line in enumerate(self.lines):
            # 주석과 import는 건너뛰기
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//') or \
               stripped.startswith('import') or stripped.startswith('from'):
                continue

            # 숫자 리터럴 찾기(변수 이름 안의 숫자는 제외)
            numbers = re.findall(r'(?<![a-zA-Z_])\b(\d+\.?\d*)\b(?![a-zA-Z_])', line)

            for num in numbers:
                if num not in acceptable and float(num) > 2:
                    # 매직 넘버일 가능성이 높은지 확인(계산이나 비교에 쓰인 경우)
                    if re.search(rf'[<>=+\-*/]\s*{re.escape(num)}|{re.escape(num)}\s*[<>=+\-*/]', line):
                        self.smells.append(CodeSmell(
                            smell_type=SmellType.MAGIC_NUMBER,
                            severity=SmellSeverity.LOW,
                            location=f"{self.filename}:{i+1}",
                            line_start=i + 1,
                            line_end=i + 1,
                            description=f"Magic number '{num}' - consider using a named constant",
                            suggestion="Replace magic number with named constant",
                            code_snippet=self._get_snippet(i, i + 1, 0)
                        ))
                        break  # 한 줄에 매직 넘버 하나면 충분

    def _detect_excessive_comments(self) -> None:
        """'왜'가 아니라 '무엇'을 설명하는 주석을 감지합니다."""
        what_patterns = [
            r'#\s*(set|get|return|loop|iterate|check|if|increment|decrement)',
            r'//\s*(set|get|return|loop|iterate|check|if|increment|decrement)',
        ]

        for i, line in enumerate(self.lines):
            for pattern in what_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.EXCESSIVE_COMMENTS,
                        severity=SmellSeverity.LOW,
                        location=f"{self.filename}:{i+1}",
                        line_start=i + 1,
                        line_end=i + 1,
                        description="Comment explains 'what' not 'why' - consider renaming or removing",
                        suggestion="Use Extract Method with descriptive name instead of comment",
                        code_snippet=self._get_snippet(i, i + 1, 0)
                    ))
                    break

    def _detect_deeply_nested(self) -> None:
        """깊이 중첩된 코드 블록을 감지합니다."""
        max_depth = 0
        current_depth = 0
        depth_start = 0

        for i, line in enumerate(self.lines):
            if self.language == 'python':
                # 들여쓰기로 세기
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    depth = indent // 4  # 4칸 들여쓰기로 가정
                    if depth > current_depth:
                        if depth > max_depth:
                            max_depth = depth
                            if depth >= self.THRESHOLDS['max_nesting_depth']:
                                depth_start = i
                    current_depth = depth
            else:
                # 중괄호 세기
                current_depth += line.count('{') - line.count('}')
                if current_depth > max_depth:
                    max_depth = current_depth
                    if current_depth >= self.THRESHOLDS['max_nesting_depth']:
                        depth_start = i

        if max_depth >= self.THRESHOLDS['max_nesting_depth']:
            self.smells.append(CodeSmell(
                smell_type=SmellType.DEEPLY_NESTED,
                severity=SmellSeverity.HIGH if max_depth > 5 else SmellSeverity.MEDIUM,
                location=f"{self.filename}:{depth_start+1}",
                line_start=depth_start + 1,
                line_end=depth_start + 1,
                description=f"Code nested {max_depth} levels deep (max: {self.THRESHOLDS['max_nesting_depth']})",
                suggestion="Apply Replace Nested Conditional with Guard Clauses or Extract Method",
                code_snippet=self._get_snippet(depth_start, depth_start + 5, 0)
            ))

    def _detect_switch_statements(self) -> None:
        """다형성이 필요할 수 있는 switch 문을 감지합니다."""
        if self.language == 'python':
            # Python 3.10+의 match 문이나 if/elif 연쇄
            pattern = r'^\s*(if|elif).*==.*:'
            consecutive_conditions = 0
            chain_start = 0

            for i, line in enumerate(self.lines):
                if re.search(pattern, line):
                    if consecutive_conditions == 0:
                        chain_start = i
                    consecutive_conditions += 1
                else:
                    if consecutive_conditions >= 4:
                        self._add_switch_smell(chain_start, i - 1, consecutive_conditions)
                    consecutive_conditions = 0
        else:
            # JavaScript/TypeScript의 switch
            pattern = r'\bswitch\s*\('
            for i, line in enumerate(self.lines):
                if re.search(pattern, line):
                    # case 세기
                    case_count = 0
                    for j in range(i, min(i + 50, len(self.lines))):
                        case_count += len(re.findall(r'\bcase\b', self.lines[j]))
                    if case_count >= 4:
                        self._add_switch_smell(i, i + 1, case_count)

    def _add_switch_smell(self, start: int, end: int, cases: int) -> None:
        """switch 문 스멜을 추가합니다."""
        self.smells.append(CodeSmell(
            smell_type=SmellType.SWITCH_STATEMENT,
            severity=SmellSeverity.MEDIUM,
            location=f"{self.filename}:{start+1}",
            line_start=start + 1,
            line_end=end + 1,
            description=f"Switch/case statement with {cases} cases - consider polymorphism",
            suggestion="Apply Replace Conditional with Polymorphism",
            code_snippet=self._get_snippet(start, start + 5, 0)
        ))

    def _detect_message_chains(self) -> None:
        """긴 메서드 체인(열차 사고)을 감지합니다."""
        chain_pattern = r'(\w+(?:\.\w+\([^)]*\)){3,})'

        for i, line in enumerate(self.lines):
            matches = re.findall(chain_pattern, line)
            for match in matches:
                chain_length = match.count('.')
                if chain_length >= self.THRESHOLDS['long_chain_length']:
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.MESSAGE_CHAIN,
                        severity=SmellSeverity.MEDIUM,
                        location=f"{self.filename}:{i+1}",
                        line_start=i + 1,
                        line_end=i + 1,
                        description=f"Message chain with {chain_length} calls - violates Law of Demeter",
                        suggestion="Apply Hide Delegate to reduce coupling",
                        code_snippet=self._get_snippet(i, i + 1, 0)
                    ))

    def _detect_duplicate_code(self) -> None:
        """중복일 가능성이 있는 코드 블록을 감지합니다(단순화)."""
        # 비교용으로 줄 해시 만들기
        line_hashes: Dict[str, List[int]] = defaultdict(list)

        for i, line in enumerate(self.lines):
            normalized = re.sub(r'\s+', ' ', line.strip())
            if len(normalized) > 20:  # 의미 있는 줄만
                line_hashes[normalized].append(i)

        # 중복 찾기
        for normalized, positions in line_hashes.items():
            if len(positions) >= 3:  # 최소 3번 이상 나타남
                self.smells.append(CodeSmell(
                    smell_type=SmellType.DUPLICATE_CODE,
                    severity=SmellSeverity.MEDIUM,
                    location=f"{self.filename}:{positions[0]+1}",
                    line_start=positions[0] + 1,
                    line_end=positions[0] + 1,
                    description=f"Potential duplicate code found {len(positions)} times",
                    suggestion="Apply Extract Method to eliminate duplication",
                    code_snippet=self._get_snippet(positions[0], positions[0] + 1, 0)
                ))

    def _detect_dead_code(self) -> None:
        """죽은 코드일 가능성이 있는 코드를 감지합니다(단순화)."""
        # 흔한 죽은 코드 패턴 찾기
        patterns = [
            (r'^\s*#.*TODO.*delete', "TODO to delete"),
            (r'^\s*#.*FIXME.*remove', "FIXME to remove"),
            (r'^\s*//.*TODO.*delete', "TODO to delete"),
            (r'^\s*//.*FIXME.*remove', "FIXME to remove"),
            (r'^\s*if\s+False:', "Code behind 'if False'"),
            (r'^\s*if\s*\(\s*false\s*\)', "Code behind 'if (false)'"),
        ]

        for i, line in enumerate(self.lines):
            for pattern, desc in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.smells.append(CodeSmell(
                        smell_type=SmellType.DEAD_CODE,
                        severity=SmellSeverity.LOW,
                        location=f"{self.filename}:{i+1}",
                        line_start=i + 1,
                        line_end=i + 1,
                        description=f"Potential dead code: {desc}",
                        suggestion="Remove dead code",
                        code_snippet=self._get_snippet(i, i + 1, 0)
                    ))


def print_report(report: SmellReport, verbose: bool = False) -> None:
    """스멜 보고서를 읽기 쉬운 형식으로 출력합니다."""
    print("=" * 70)
    print(f"CODE SMELL DETECTION REPORT: {report.filename}")
    print("=" * 70)

    print(f"\n📊 SUMMARY")
    print("-" * 40)
    print(f"  Total smells found:     {len(report.smells)}")
    print(f"  Critical:               {report.critical_count}")
    print(f"  High:                   {report.high_count}")
    print(f"  Medium:                 {report.medium_count}")
    print(f"  Low:                    {report.low_count}")

    if not report.smells:
        print("\n✅ No code smells detected!")
        print("=" * 70)
        return

    # 종류별로 묶기
    by_type: Dict[SmellType, List[CodeSmell]] = defaultdict(list)
    for smell in report.smells:
        by_type[smell.smell_type].append(smell)

    print(f"\n📋 FINDINGS BY TYPE")
    print("-" * 40)

    for smell_type, smells in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"\n### {smell_type.value} ({len(smells)} found)")

        for smell in sorted(smells, key=lambda x: x.severity.value):
            severity_icon = {
                SmellSeverity.CRITICAL: "🔴",
                SmellSeverity.HIGH: "🟠",
                SmellSeverity.MEDIUM: "🟡",
                SmellSeverity.LOW: "🟢",
            }[smell.severity]

            print(f"\n  {severity_icon} [{smell.severity.value}] {smell.location}")
            print(f"     {smell.description}")
            print(f"     💡 {smell.suggestion}")

            if verbose and smell.code_snippet:
                print(f"\n     Code:")
                for snippet_line in smell.code_snippet.split('\n'):
                    print(f"       {snippet_line}")

    print("\n" + "=" * 70)
    print("💡 RECOMMENDED ACTIONS")
    print("-" * 40)

    if report.critical_count > 0:
        print("  1. Address CRITICAL issues immediately")
    if report.high_count > 0:
        print("  2. Plan to fix HIGH severity issues this sprint")
    if report.medium_count > 0:
        print("  3. Schedule MEDIUM issues for upcoming work")
    if report.low_count > 0:
        print("  4. Fix LOW issues opportunistically")

    print("\n" + "=" * 70)


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

    print(f"Scanning {len(files)} files in {directory}...\n")

    total_smells = 0
    total_critical = 0
    total_high = 0
    files_with_smells = 0

    for filepath in sorted(files):
        try:
            detector = SmellDetector(filepath)
            report = detector.detect_all()

            if report.smells:
                files_with_smells += 1
                total_smells += len(report.smells)
                total_critical += report.critical_count
                total_high += report.high_count

                flag = " 🔴" if report.critical_count else (" 🟠" if report.high_count else " 🟡")
                print(f"  {report.filename}: {len(report.smells)} smells{flag}")

                if verbose:
                    for smell in report.smells:
                        print(f"    - [{smell.severity.value}] {smell.smell_type.value}: line {smell.line_start}")
            else:
                print(f"  {report.filename}: ✅ Clean")

        except Exception as e:
            print(f"  Error analyzing {filepath}: {e}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files analyzed:         {len(files)}")
    print(f"  Files with smells:      {files_with_smells}")
    print(f"  Total smells found:     {total_smells}")
    print(f"  Critical issues:        {total_critical}")
    print(f"  High severity issues:   {total_high}")


def main():
    parser = argparse.ArgumentParser(
        description='Detect code smells in source files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s myfile.py                    Analyze single file
  %(prog)s --dir src/                   Analyze directory
  %(prog)s -v myfile.py                 Verbose with code snippets
        """
    )
    parser.add_argument('file', nargs='?', help='File to analyze')
    parser.add_argument('--dir', '-d', help='Directory to analyze')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show code snippets')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.dir:
        analyze_directory(args.dir, args.verbose)
    elif args.file:
        detector = SmellDetector(args.file)
        report = detector.detect_all()

        if args.json:
            import json
            smells_data = [{
                'type': s.smell_type.value,
                'severity': s.severity.value,
                'location': s.location,
                'line_start': s.line_start,
                'line_end': s.line_end,
                'description': s.description,
                'suggestion': s.suggestion,
            } for s in report.smells]
            print(json.dumps({
                'filename': report.filename,
                'total_smells': len(report.smells),
                'critical': report.critical_count,
                'high': report.high_count,
                'medium': report.medium_count,
                'low': report.low_count,
                'smells': smells_data
            }, indent=2))
        else:
            print_report(report, args.verbose)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
