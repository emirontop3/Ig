from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        cl = Client()
        
        # Mod Seçimi
        if data['mode'] == 'anon':
            # Buraya senin sabit bot hesabını yazıyorsun
            username = "anonimmessager"
            password = "1901Emir"
        else:
            # Kullanıcının arayüzden girdiği bilgiler
            username = data['username']
            password = data['password']

        try:
            cl.login(username, password)
            target = data['target']
            action = data['action']
            
            result = ""
            if action == 'follow':
                user_id = cl.user_id_from_username(target)
                cl.user_follow(user_id)
                result = f"Başarıyla @{target} takip edildi."
            
            elif action == 'unfollow':
                user_id = cl.user_id_from_username(target)
                cl.user_unfollow(user_id)
                result = f"@{target} takipten çıkarıldı."
            
            elif action == 'message':
                user_id = cl.user_id_from_username(target)
                cl.direct_send(data['messageText'], [int(user_id)])
                result = f"@{target} kullanıcısına mesaj gönderildi."

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": result}).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
