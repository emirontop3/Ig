import time
import os
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, VerificationCodeInvalid

def login_to_instagram():
    try:
        if os.path.exists(SETTINGS_PATH):
            cl.load_settings(SETTINGS_PATH)
            try:
                cl.get_timeline_feed()
                return True, "Oturum Hazır"
            except:
                print("> Oturum düşmüş, yenileniyor...")

        # Instagram'ı kuşkulandırmamak için rastgele bir bekleme
        time.sleep(2)
        
        # Giriş denemesi
        cl.login("anonimmessager", "1901Emir")
        cl.dump_settings(SETTINGS_PATH)
        return True, "Giriş Başarılı"

    except ChallengeRequired as e:
        # Instagram onay istiyorsa linki loglara ve cevaba basıyoruz
        challenge_url = cl.last_json.get('challenge', {}).get('url', 'Link bulunamadı')
        print(f"> ONAY GEREKLİ: {challenge_url}")
        return False, f"ONAY GEREKLİ: Lütfen şu linke tıkla ve 'Benim' de: {challenge_url}"
    
    except Exception as e:
        return False, f"Hata: {str(e)}"

# Flask route kısmını da buna göre güncelle:
@app.route('/follow', methods=['POST'])
def follow_user():
    data = request.get_json()
    target_username = data['target'].replace('@', '')
    
    success, message = login_to_instagram()
    
    if success:
        try:
            user_id = cl.user_id_from_username(target_username)
            cl.user_follow(user_id)
            return jsonify({"status": "success", "message": f"@{target_username} takip edildi!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        # Burası sana onay linkini gönderecek olan kısım
        return jsonify({"status": "challenge", "message": message}), 403
