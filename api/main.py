from http.server import BaseHTTPRequestHandler
from instagrapi import Client
import json
import requests
import random

def get_free_proxies():
    """İnternetten güncel ve ücretsiz proxy listesini çeker."""
    try:
        # Ücretsiz ve anonim proxy sağlayan güvenilir bir kaynak
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
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
            proxies = get_free_proxies()
            
            # Rastgele 5 tane proxy dene (Vercel timeout sınırına kadar)
            success = False
            last_error = ""
            
            # Senin bot bilgilerin
            username = "anonimmessager"
            password = "1901Emir"

            # Proxy deneme döngüsü
            for _ in range(5):
                if not proxies: break
                proxy = random.choice(proxies)
                proxy_url = f"http://{proxy}"
                
                try:
                    cl.set_proxy(proxy_url)
                    cl.login(username, password)
                    success = True
                    break
                except Exception as e:
                    last_error = str(e)
                    continue

            if not success:
                raise Exception(f"Çalışan proxy bulunamadı veya Instagram engelledi: {last_error}")

            # İşlem (Örn: Takip Et)
            target = data['target']
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": f"@{target} proxy üzerinden takip edildi!"}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
