"""昼11:50 - Twitter投稿文のみを生成してLINEに送信"""

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
            from lib.claude_client import generate_twitter_post
            from lib.line_client import send_line_message, format_twitter_only

            topic = get_topic("noon")

            # Twitter投稿文を生成
            twitter_text = generate_twitter_post(topic, for_note=False)

            # LINEに送信
            message = format_twitter_only(twitter_text)
            send_line_message(message)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"OK: noon - {topic}".encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode("utf-8"))
