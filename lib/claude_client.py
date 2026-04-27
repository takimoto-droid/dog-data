"""Claude API連携モジュール"""

import os
import anthropic


def generate_note_article(topic: str) -> dict:
    """note記事を生成する"""
    from lib.prompts import NOTE_SYSTEM_PROMPT, NOTE_USER_PROMPT

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=8000,
        system=NOTE_SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": NOTE_USER_PROMPT.format(topic=topic)}
        ],
    )

    text = message.content[0].text

    # タイトルと本文を分離
    lines = text.strip().split("\n")
    title = ""
    body_lines = []
    body_start = False

    for line in lines:
        if line.startswith("タイトル：") or line.startswith("タイトル:"):
            title = line.replace("タイトル：", "").replace("タイトル:", "").strip()
        elif title and not body_start and line.strip() == "":
            body_start = True
        elif title:
            body_start = True
            body_lines.append(line)

    if not title:
        title = lines[0] if lines else "無題"
        body_lines = lines[1:]

    return {
        "title": title,
        "body": "\n".join(body_lines).strip(),
    }


def generate_twitter_post(topic: str, for_note: bool = False) -> str:
    """Twitter投稿文を生成する"""
    from lib.prompts import (
        TWITTER_SYSTEM_PROMPT,
        TWITTER_FOR_NOTE_PROMPT,
        TWITTER_STANDALONE_PROMPT,
    )

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    if for_note:
        user_prompt = TWITTER_FOR_NOTE_PROMPT.format(topic=topic)
    else:
        user_prompt = TWITTER_STANDALONE_PROMPT.format(topic=topic)

    message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=500,
        system=TWITTER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text.strip()
