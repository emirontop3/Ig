from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            cl = Client()
            # Vercel zaman aşımını önlemek için hızlı ayar
            cl.request_timeout = 9 
            
            user = data['username'] if data['mode'] == 'user' else "anonimmessager"
            pw = data['password'] if data['mode'] == 'user' else "1901Emir"
            verification_code = data.get('verificationCode')

            try:
                if verification_code:
                    # Eğer kullanıcı kod girdiyse, login işlemini kodla tamamla
                    cl.login(user, pw, verification_code=verification_code)
                else:
                    cl.login(user, pw)
            except Exception as login_err:
                if "challenge_required" in str(login_err).lower():
                    self.send_response(403) # Özel durum kodu
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "challenge", 
                        "message": "Instagram kod gönderdi! Lütfen mailini/uygulamanı kontrol et ve kodu gir."
                    }).encode())
                    return
                else:
                    raise login_err

            # İşlemler
            target = data['target']
            action = data['action']
            if action == 'follow':
                cl.user_follow(cl.user_id_from_username(target))
                res = f"@{target} takip edildi."
            elif action == 'message':
                cl.direct_send(data['messageText'], [int(cl.user_id_from_username(target))])
                res = "Mesaj gönderildi."
            else:
                res = "Giriş başarılı, işlem seçilmedi."

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": res}).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
