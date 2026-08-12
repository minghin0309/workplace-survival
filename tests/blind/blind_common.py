import hashlib


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def case_input_text(case: dict, turn: dict) -> str:
    return (
        f"RECIPIENT:{case['recipient_description']}\n"
        f"IMAGE:{turn['image_path']}\n"
        f"USER:{turn['input_raw']}"
    )


def context_transcript_text(case: dict, raw_turns: list[dict], turn_index: int) -> str:
    parts = [f"RECIPIENT:{case['recipient_description']}"]
    for index in range(turn_index):
        parts.append(f"USER:{case['turns'][index]['input_raw']}")
        if index < turn_index - 1:
            parts.append(f"ASSISTANT:{raw_turns[index]['raw_output']}")
    return "\n---TRANSCRIPT---\n".join(parts)
