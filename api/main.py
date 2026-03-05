import os
from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)
cl = Client()
SETTINGS_PATH = "session_settings.json"

def login_logic():
    # Eğer önceden giriş yapılmışsa dosyadan yükle
    if os.path.exists(SETTINGS_PATH):
        cl.load_settings(SETTINGS_PATH)
        try:
            cl.get_timeline_feed() # Oturum hala geçerli mi kontrol et
            return True
        except:
            print("Oturum süresi dolmuş, yeniden giriş yapılıyor...")

    # İlk kez giriş yapılıyorsa
    try:
        cl.login("anonimmessager", "1901Emir")
        cl.dump_settings(SETTINGS_PATH) # Giriş bilgilerini kaydet
        return True
    except Exception as e:
        print(f"Giriş hatası: {e}")
        return False

@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.json
    target = data.get('target')
    
    if login_logic():
        try:
            user_id = cl.user_id_from_username(target)
            cl.user_follow(user_id)
            return jsonify({"status": "success", "message": f"@{target} takip edildi!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Instagram girişini geçemedi."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
