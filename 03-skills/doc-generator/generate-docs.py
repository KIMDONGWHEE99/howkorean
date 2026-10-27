#!/usr/bin/env python3
import ast


class APIDocExtractor(ast.NodeVisitor):
    """Python 소스 코드에서 API 문서를 추출합니다."""

    def __init__(self):
        self.endpoints = []

    def visit_FunctionDef(self, node):
        """함수 문서를 추출합니다."""
        if node.name.startswith("get_") or node.name.startswith("post_"):
            doc = ast.get_docstring(node)
            endpoint = {
                "name": node.name,
                "docstring": doc,
                "params": [arg.arg for arg in node.args.args],
                "returns": self._extract_return_type(node),
            }
            self.endpoints.append(endpoint)
        self.generic_visit(node)

    def _extract_return_type(self, node):
        """함수 어노테이션에서 반환 타입을 추출합니다."""
        if node.returns:
            return ast.unparse(node.returns)
        return "Any"


def generate_markdown_docs(endpoints: list[dict]) -> str:
    """엔드포인트 정보로 마크다운 문서를 생성합니다."""
    docs = "# API Documentation\n\n"

    for endpoint in endpoints:
        docs += f"## {endpoint['name']}\n\n"
        docs += f"{endpoint['docstring']}\n\n"
        docs += f"**Parameters**: {', '.join(endpoint['params'])}\n\n"
        docs += f"**Returns**: {endpoint['returns']}\n\n"
        docs += "---\n\n"

    return docs


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        tree = ast.parse(f.read())

    extractor = APIDocExtractor()
    extractor.visit(tree)

    markdown = generate_markdown_docs(extractor.endpoints)
    print(markdown)
