import os
from flask import Flask, request, jsonify
from instagrapi import Client

app = Flask(__name__)
cl = Client()

# --- SENİN ÖZEL ANAHTARIN ---
# Bu ID ile Instagram seni "tarayıcıda zaten açık olan oturum" olarak görecek.
INSTAGRAM_SESSION_ID = "43262476750%3ABX3ZPbvspHcVxX%3A6%3AAYhB0Y3fFOdX-lvumGG2EAvJFBdk3_ezWNYUbDzqhg"
# ----------------------------

def connect_to_insta():
    """Session ID kullanarak sessizce sızar."""
    try:
        # Önce kimliği doğrula
        cl.login_by_sessionid(INSTAGRAM_SESSION_ID)
        # Oturumun gerçekten çalışıp çalışmadığını ufak bir veri çekerek test et
        cl.get_timeline_feed() 
        return True
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return False

@app.route('/')
def home():
    return "<h1>Sistem Çevrimiçi</h1><p>Emirattaa Komuta Merkezi Aktif.</p>"

@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"error": "Hedef belirtilmedi."}), 400

    # @ işaretini temizle
    target_username = data['target'].replace('@', '').strip()
    
    if connect_to_insta():
        try:
            # Kullanıcı ID'sini bul ve takip et
            user_id = cl.user_id_from_username(target_username)
            cl.user_follow(user_id)
            return jsonify({
                "status": "basarili", 
                "mesaj": f"@{target_username} operasyonu tamamlandı. Hedef takibe alındı."
            })
        except Exception as e:
            return jsonify({"status": "hata", "mesaj": str(e)}), 500
    else:
        return jsonify({
            "status": "hata", 
            "mesaj": "Session ID geçersiz. Instagram oturumu kapatmış olabilir."
        }), 401

if __name__ == "__main__":
    # Render'ın atadığı portu kullan
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
