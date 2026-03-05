from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json
import requests
import random
import time

def get_fresh_proxies():
    """İnternetten anlık çalışan ücretsiz proxy listesini çeker."""
    try:
        # 100% Bedava ve kayıt istemeyen proxy kaynağı
        r = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=anonymous", timeout=5)
        if r.status_code == 200:
            return r.text.splitlines()
    except:
        return []
    return []

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            cl = Client()
            # Instagram'a 'ben gerçek bir Android telefonum' diyoruz
            cl.set_device({
                "app_version": "269.1.0.18.231",
                "android_version": 26,
                "android_release": "8.0.0",
                "dpi": "480dpi",
                "resolution": "1080x1920",
                "manufacturer": "samsung",
                "device": "herolte",
                "model": "SM-G930F",
                "cpu": "samsungexynos8890",
                "version_code": "443213142"
            })

            target = data.get('target')
            action = data.get('action', 'follow')
            msg_text = data.get('messageText', '')
            
            # Otomatik Proxy Avı Başlıyor
            proxies = get_fresh_proxies()
            random.shuffle(proxies) # Listeyi karıştır ki hep aynı proxy'ye yüklenmeyelim
            
            logged_in = False
            error_log = ""

            # En fazla 3 farklı proxy dene (Vercel 10sn sınırı olduğu için hızlı olmalıyız)
            for i in range(min(3, len(proxies))):
                proxy_url = f"http://{proxies[i]}"
                try:
                    cl.set_proxy(proxy_url)
                    # Sadece en gerekli bilgilerle hızlı login
                    cl.login("anonimmessager", "1901Emir")
                    logged_in = True
                    break
                except Exception as e:
                    error_log = str(e)
                    continue

            if not logged_in:
                raise Exception(f"Instagram tüm kapıları kapattı veya proxy yavaş kaldı: {error_log}")

            # Operasyon
            user_id = cl.user_id_from_username(target)
            if action == 'follow':
                cl.user_follow(user_id)
                res = f"@{target} gizlice takip edildi!"
            elif action == 'message':
                cl.direct_send(msg_text, [int(user_id)])
                res = f"@{target} kullanıcısına mesaj sızdırıldı!"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": res}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"Saldırı başarısız: {str(e)}"}).encode())
