"""LINE Messaging API連携モジュール"""

import os
import requests

LINE_API_URL = "https://api.line.me/v2/bot/message/push"


def send_line_message(text: str) -> bool:
    """LINEにメッセージを送信する"""
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # LINEのメッセージは5000文字制限があるため、長い場合は分割
    messages = _split_message(text)

    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": msg} for msg in messages],
    }

    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    return response.status_code == 200


def _split_message(text: str, max_length: int = 5000) -> list:
    """長いメッセージを分割する（LINEの5000文字制限対応）"""
    if len(text) <= max_length:
        return [text]

    messages = []
    while text:
        if len(text) <= max_length:
            messages.append(text)
            break

        # 改行位置で分割を試みる
        split_pos = text.rfind("\n", 0, max_length)
        if split_pos == -1:
            split_pos = max_length

        messages.append(text[:split_pos])
        text = text[split_pos:].lstrip("\n")

    return messages


def format_note_and_twitter(note_title: str, note_body: str, twitter_text: str) -> str:
    """note記事とTwitter投稿文をLINE用に整形する"""
    return (
        f"📝 【note記事】\n"
        f"━━━━━━━━━━━━━━━\n"
        f"■ タイトル\n{note_title}\n\n"
        f"■ 本文\n{note_body}\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🐦 【Twitter投稿文】\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{twitter_text}"
    )


def format_twitter_only(twitter_text: str) -> str:
    """Twitter投稿文のみをLINE用に整形する"""
    return (
        f"🐦 【Twitter投稿文（昼）】\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{twitter_text}"
    )
