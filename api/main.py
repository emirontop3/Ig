import os
from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)
cl = Client()

# --- SENİN ÖZEL BİLGİLERİN ---
INSTAGRAM_SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"

# BURAYI GÜNCELLE: Google'a "my user agent" yaz ve çıkan metni buraya yapıştır.
MY_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
# ----------------------------

def connect_to_insta():
    try:
        # Önce cihaz kimliğini (User-Agent) set ediyoruz
        cl.set_user_agent(MY_USER_AGENT)
        # Sonra session ile sızıyoruz
        cl.login_by_sessionid(INSTAGRAM_SESSION_ID)
        cl.get_timeline_feed() 
        return True
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return False

@app.route('/')
def home():
    return "<h1>Sistem Çevrimiçi</h1><p>User-Agent Koruması Aktif.</p>"

@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"error": "Hedef belirtilmedi."}), 400

    target_username = data['target'].replace('@', '').strip()
    
    if connect_to_insta():
        try:
            user_id = cl.user_id_from_username(target_username)
            cl.user_follow(user_id)
            return jsonify({"status": "basarili", "mesaj": f"@{target_username} takibe alındı."})
        except Exception as e:
            return jsonify({"status": "hata", "mesaj": f"Instagram işlemi reddetti: {str(e)}"}), 500
    else:
        return jsonify({"status": "hata", "mesaj": "Bağlantı kurulamadı. Session veya User-Agent hatalı."}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
