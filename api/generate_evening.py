"""夜19:00 - note記事 + Twitter投稿文を生成してLINEに送信"""

import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Vercel Cron認証
        auth_header = self.headers.get("Authorization")
        expected = f"Bearer {os.environ.get('CRON_SECRET', '')}"
        if auth_header != expected:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

        try:
            from lib.topics import get_topic
            from lib.claude_client import generate_note_article, generate_twitter_post
            from lib.line_client import (
                send_line_message,
                format_note_and_twitter,
            )

            topic = get_topic("evening")

            # note記事を生成
            article = generate_note_article(topic)

            # Twitter投稿文を生成（note記事に関連）
            twitter_text = generate_twitter_post(topic, for_note=True)

            # LINEに送信
            message = format_note_and_twitter(
                article["title"], article["body"], twitter_text
            )
            send_line_message(message)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                f"OK: evening - {article['title']}".encode("utf-8")
            )

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode("utf-8"))
