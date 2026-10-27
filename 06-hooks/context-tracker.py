#!/usr/bin/env python3
"""
컨텍스트 사용량 추적기 - 요청마다 토큰 소비량을 추적합니다.

UserPromptSubmit을 "메시지 전" 훅으로, Stop을 "응답 후" 훅으로 써서
요청마다 토큰 사용량의 차이를 계산합니다.

이 버전은 글자 수 기반 추정을 씁니다(의존성 없음).
더 정확하게 계산하려면 context-tracker-tiktoken.py를 참고하세요.

사용법:
    두 훅이 같은 스크립트를 쓰도록 설정하세요:
    - UserPromptSubmit: 현재 토큰 수 저장
    - Stop: 차이를 계산하고 사용량 보고
"""
import json
import os
import sys
import tempfile

# 설정
CONTEXT_LIMIT = 1000000  # Opus 5, Sonnet 5, Opus 4.8, Sonnet 4.6은 1M, Haiku 4.5는 200000(사용하는 모델에 맞게 조정)


def get_state_file(session_id: str) -> str:
    """메시지 전 토큰 수를 저장할, 세션별로 분리된 임시 파일 경로를 가져옵니다."""
    return os.path.join(tempfile.gettempdir(), f"claude-context-{session_id}.json")


def count_tokens_estimate(text: str) -> int:
    """
    글자 수 기반 근삿값으로 토큰 수를 추정합니다.

    토큰당 약 4글자 비율을 쓰며, 영어 텍스트에서는 약 80-90% 정확도를 보입니다.
    코드나 영어가 아닌 텍스트(한국어 등)에서는 덜 정확합니다.
    """
    return len(text) // 4


def read_transcript(transcript_path: str) -> str:
    """대화 기록 파일의 내용을 모두 읽어 하나로 합칩니다."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    content = []
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                # 여러 메시지 형식에서 텍스트 내용 추출
                if "message" in entry:
                    msg = entry["message"]
                    if isinstance(msg.get("content"), str):
                        content.append(msg["content"])
                    elif isinstance(msg.get("content"), list):
                        for block in msg["content"]:
                            if isinstance(block, dict) and block.get("type") == "text":
                                content.append(block.get("text", ""))
            except json.JSONDecodeError:
                continue

    return "\n".join(content)


def handle_user_prompt_submit(data: dict) -> None:
    """메시지 전 훅: 요청 전에 현재 토큰 수를 저장합니다."""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens_estimate(transcript_content)

    # 나중에 비교하도록 임시 파일에 저장
    state_file = get_state_file(session_id)
    with open(state_file, "w") as f:
        json.dump({"pre_tokens": current_tokens}, f)


def handle_stop(data: dict) -> None:
    """응답 후 훅: 토큰 차이를 계산하고 보고합니다."""
    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")

    transcript_content = read_transcript(transcript_path)
    current_tokens = count_tokens_estimate(transcript_content)

    # 메시지 전 토큰 수 불러오기
    state_file = get_state_file(session_id)
    pre_tokens = 0
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
                pre_tokens = state.get("pre_tokens", 0)
        except (json.JSONDecodeError, IOError):
            pass

    # 차이 계산
    delta_tokens = current_tokens - pre_tokens
    remaining = CONTEXT_LIMIT - current_tokens
    percentage = (current_tokens / CONTEXT_LIMIT) * 100

    # 사용량 보고(훅 출력과 섞이지 않도록 stderr로)
    print(
        f"Context (estimated): ~{current_tokens:,} tokens "
        f"({percentage:.1f}% used, ~{remaining:,} remaining)",
        file=sys.stderr,
    )
    if delta_tokens > 0:
        print(f"This request: ~{delta_tokens:,} tokens", file=sys.stderr)


def main():
    data = json.load(sys.stdin)
    event = data.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        handle_user_prompt_submit(data)
    elif event == "Stop":
        handle_stop(data)

    sys.exit(0)


if __name__ == "__main__":
    main()
