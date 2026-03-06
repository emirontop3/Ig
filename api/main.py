import os
import time
from flask import Flask, request, jsonify
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, LoginRequired

app = Flask(__name__)
cl = Client()

# --- AYARLAR ---
USER = "anonimmessager"
PASS = "1901Emir"
# Senin verdiğin Session ID
SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"

def setup_client():
    """Instagram'ı gerçek bir telefon olduğuna ikna eder."""
    cl.set_device({
        "app_version": "269.1.0.18.231",
        "android_version": 33,
        "android_release": "13.0",
        "dpi": "450dpi",
        "resolution": "1080x2340",
        "manufacturer": "samsung",
        "device": "SM-S911B",
        "model": "galaxy s23",
        "cpu": "qcom",
        "version_code": "443213142"
    })
    cl.set_user_agent("Instagram 269.1.0.18.231 Android (33/13.0; 450dpi; 1080x2340; samsung; SM-S911B; galaxy s23; qcom; en_US; 443213142)")

def login_logic():
    setup_client()
    try:
        print("> Session ID ile sızılıyor...")
        cl.login_by_sessionid(SESSION_ID)
        cl.get_timeline_feed() # Test
        return True, "Session ID Aktif"
    except Exception:
        try:
            print("> Session başarısız, normal giriş deneniyor...")
            cl.login(USER, PASS)
            return True, "Şifre ile Giriş Başarılı"
        except ChallengeRequired:
            return False, "Onay Gerekli! Instagram uygulamasını aç ve 'Benim' de."
        except Exception as e:
            return False, f"Giriş Başarısız: {str(e)}"

@app.route('/')
def home():
    return "<h1>SİSTEM AKTİF</h1><p>Emirattaa Bot Merkezi komut bekliyor.</p>"

@app.route('/follow', methods=['POST'])
def follow():
    data = request.get_json()
    target = data.get('target', '').replace('@', '').strip()
    
    if not target:
        return jsonify({"status": "hata", "mesaj": "Hedef kullanıcı yok."}), 400

    success, msg = login_logic()
    if success:
        try:
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            return jsonify({"status": "basarili", "mesaj": f"@{target} takibe alındı!"})
        except Exception as e:
            return jsonify({"status": "hata", "mesaj": f"İşlem reddedildi: {str(e)}"}), 500
    else:
        return jsonify({"status": "hata", "mesaj": msg}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
