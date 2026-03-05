from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json
import requests
import random

def get_best_free_proxies():
    """3 Farklı dev kaynaktan en taze proxyleri toplar."""
    proxy_list = []
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1500&country=all&ssl=all&anonymity=elite",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
    ]
    
    for url in sources:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                proxy_list.extend(r.text.splitlines())
        except:
            continue
    return list(set(proxy_list)) # Tekrarlananları temizle

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))

            cl = Client()
            cl.request_timeout = 4 # Instagram'dan hızlı cevap bekliyoruz
            
            # En iyi havuzdan rastgele seçim
            proxies = get_best_free_proxies()
            if not proxies:
                raise Exception("Proxy havuzu boşaldı, tekrar dene.")
            
            # Rastgele 1 tane seç ve dene
            fast_proxy = random.choice(proxies)
            cl.set_proxy(f"http://{fast_proxy}")

            # Giriş Operasyonu
            cl.login("anonimmessager", "1901Emir")
            
            target = data.get('target')
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "msg": f"@{target} avlandı! Proxy: {fast_proxy}"}).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "err", "msg": "Sistem meşgul veya proxy yavaş. Tekrar ateşle!"}).encode())
