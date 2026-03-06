from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json
import time

# --- HESAP BİLGİLERİ ---
USER = "anonimmessager"
PASS = "1901Emir"
# En son aldığın Session ID
SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        target = data.get('target', '').replace('@', '').strip()
        message = data.get('message', 'Selam!')

        cl = Client()
        cl.request_timeout = 15 # Vercel için maksimum süreye yakın

        # KRİTİK: Instagram'ı kandıran Windows/Chrome kimliği
        cl.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")

        try:
            # ÖNCE SESSION İLE DENE (En güvenli yol)
            try:
                cl.login_by_sessionid(SESSION_ID)
            except:
                # SESSION OLMAZSA ŞİFRE İLE DENE
                cl.login(USER, PASS)

            # 1. Takip Et
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            
            # 2. Kısa bir bekleme (Bot algılanmasın diye)
            time.sleep(2)
            
            # 3. Mesaj Gönder
            cl.direct_send(message, [user_id])
            
            self._send_response(200, {"status": "success", "message": f"@{target} takibe alındı ve mesaj iletildi!"})

        except Exception as e:
            error_msg = str(e)
            # IP engeli varsa temiz bir mesaj ver
            if "Expecting value" in error_msg or "403" in error_msg:
                error_msg = "Instagram IP adresini blokladı. Lütfen yeni bir Vercel projesi açarak farklı bir IP almayı deneyin."
            
            self._send_response(500, {"status": "error", "message": error_msg})

    def _send_response(self, status, res_data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(res_data).encode())
