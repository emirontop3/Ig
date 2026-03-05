from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # İstek gövdesini oku
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)

        cl = Client()
        
        # Giriş Bilgileri (Senin hesabın)
        username = "SENIN_KULLANICI_ADIN"
        password = "SENIN_SIFREN"

        try:
            # 1. Giriş Yap (Çerez gerekmez, uygulama gibi giriş yapar)
            cl.login(username, password)
            
            action = body.get("action") # 'follow' veya 'message'
            target = body.get("target") # Hedef kullanıcı adı

            if action == "follow":
                user_id = cl.user_id_from_username(target)
                cl.user_follow(user_id) # Takip etme
                response_msg = f"{target} takip edildi."
                
            elif action == "message":
                message_text = body.get("text")
                user_id = cl.user_id_from_username(target)
                cl.direct_send(message_text, [int(user_id)]) # DM gönderme
                response_msg = f"Mesaj gönderildi: {target}"

            # Başarılı Yanıt
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": response_msg}).encode())

        except Exception as e:
            # Hata Yanıtı
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode())
