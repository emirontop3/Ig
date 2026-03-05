import os
import json
from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)
cl = Client()
SETTINGS_PATH = "session_settings.json"

def login_to_instagram():
    """Instagram'a giriş yapar veya kayıtlı oturumu yükler."""
    try:
        # Eğer daha önce giriş yapılmışsa ayarları dosyadan oku
        if os.path.exists(SETTINGS_PATH):
            print("> Mevcut oturum dosyası yükleniyor...")
            cl.load_settings(SETTINGS_PATH)
            try:
                # Oturumun hala canlı olup olmadığını küçük bir istekle test et
                cl.get_timeline_feed()
                print("> Oturum hala geçerli, devam ediliyor.")
                return True
            except Exception:
                print("> Oturumun süresi dolmuş, yeniden giriş yapılıyor...")

        # İlk kez giriş veya süresi dolmuş oturum
        print("> Yeni giriş yapılıyor: @anonimmessager")
        cl.login("anonimmessager", "1901Emir")
        
        # Giriş başarılıysa bu 'altın bileti' (oturumu) dosyaya kaydet
        cl.dump_settings(SETTINGS_PATH)
        print("> Yeni oturum ayarları kaydedildi.")
        return True
        
    except Exception as e:
        print(f"> KRİTİK GİRİŞ HATASI: {e}")
        return False

@app.route('/')
def home():
    return "Sistem Aktif: Instagram Botu Emir Emirattaa Tarafından Komut Bekliyor."

@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"status": "error", "message": "Hedef kullanıcı belirtilmedi."}), 400

    target_username = data['target'].replace('@', '') # @ işaretini temizle
    
    if login_to_instagram():
        try:
            print(f"> Hedef aranıyor: {target_username}")
            user_id = cl.user_id_from_username(target_username)
            cl.user_follow(user_id)
            return jsonify({
                "status": "success", 
                "message": f"@{target_username} başarıyla takip edildi!"
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Instagram giriş aşamasını geçemedi. Hesap onaya düşmüş olabilir."}), 403

if __name__ == "__main__":
    # RENDER İÇİN KRİTİK: Port numarasını Render'ın atadığı değişkenden alıyoruz
    port = int(os.environ.get("PORT", 10000))
    # 0.0.0.0 dış dünyaya açılmasını sağlar
    app.run(host='0.0.0.0', port=port)
