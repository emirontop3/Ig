from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json
import os

# --- GÜVENLİ BİLGİLER ---
SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"
USER_AGENT = "Instagram 269.1.0.18.231 Android (33/13.0; 450dpi; 1080x2340; samsung; SM-S911B; galaxy s23; qcom; en_US; 443213142)"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        target = data.get('target', '').replace('@', '').strip()

        cl = Client()
        # Vercel zaman aşımına girmesin diye her şeyi hızlandırıyoruz
        cl.request_timeout = 7 
        
        try:
            # 1. Adım: Cihazı ve User-Agent'ı tanıt (Instagram'ı kandır)
            cl.set_user_agent(USER_AGENT)
            
            # 2. Adım: Session ID ile sessizce sız
            cl.login_by_sessionid(SESSION_ID)
            
            # 3. Adım: Hedef ID'yi bul ve Takip Et
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            
            response_data = {"status": "success", "message": f"@{target} başarıyla takibe alındı!"}
            self._send_response(200, response_data)

        except Exception as e:
            err_msg = str(e)
            # Eğer hata "login_required" ise session düşmüş demektir
            if "login_required" in err_msg.lower():
                response_data = {"status": "error", "message": "Session ID süresi dolmuş, yenilemen lazım."}
            else:
                response_data = {"status": "error", "message": f"Hata: {err_msg}"}
            
            self._send_response(500, response_data)

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') # Panelden erişim için
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        # Vercel kontrolü için basit bir sayfa
        self._send_response(200, {"status": "online", "bot": "anonimmessager"})
