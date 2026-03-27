import os
import logging
import spotipy
import datetime
from spotipy.oauth2 import SpotifyPKCE
from dotenv import load_dotenv
from logger_config import setup_logger 

logger = setup_logger("SpotifyAPI")

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
        if not self.client_id or not self.redirect_uri:
            logger.error("SPOTIPY_CLIENT_ID veya SPOTIPY_REDIRECT_URI .env dosyasında tanımlı değil!")
            raise ValueError("Gerekli Spotify API bilgileri eksik.")
        self.scope = "user-read-recently-played user-library-read playlist-modify-public playlist-modify-private playlist-read-private"
        self.auth_manager = SpotifyPKCE(client_id=self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)
        self.sp = None
        logger.info("✅ Spotify API motoru başlatıldı, kimlik belgeleri hazırlandı.")

    def authenticate(self):
        try:
            self.auth_manager.get_access_token()
            self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
            user_profile = self.sp.me()
            logger.info(f"✅ Spotify bağlantısı BAŞARILI! Hoş geldin, {user_profile['display_name']}!")
        except Exception as e:
            logger.error(f"Spotify kimlik doğrulama hatası: {e}")
            if os.path.exists(".cache"):
                os.remove(".cache")  # Eski token'ı temizle
                logger.info("Eski token temizlendi, lütfen tekrar deneyin.")
                self.auth_manager = SpotifyPKCE(client_id=self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)  # Auth manager'ı sıfırla
                self.sp = spotipy.Spotify(auth_manager=self.auth_manager)  
                user_profile = self.sp.me()
                logger.info(f"✅ Spotify bağlantısı BAŞARILI! Hoş geldin, {user_profile['display_name']}!")
            else: 
                raise e

    def get_recently_played(self, after_timestamp=None):
        try :
            result = self.sp.current_user_recently_played(limit=50, after=after_timestamp)
            items = result.get("items", [])
            tracks_data = []
            for item in items:
                track = item['track']
                clean_track = {
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'artist_name': track['artists'][0]['name'], 
                    'duration_ms': track['duration_ms'],
                    'played_at': item['played_at']
                }
                tracks_data.append(clean_track)
            logger.info(f"🎧 Son dinlenen {len(tracks_data)} şarkı başarıyla çekildi.")
            return tracks_data
        except Exception as e:
            logger.error(f"Spotify API hatası (get_recently_played): {e}")
            return []

    """
    def get_audio_features(self, track_ids):
        try:
            if not track_ids:
                return []
            clean_features = []
            for i in range(0, len(track_ids),100):
                batch = track_ids[i:i+100]
                features = self.sp.audio_features(tracks=batch)
                for f in features:
                    if f is not None:
                        clean_features.append({
                            'track_id': f['id'],
                            'energy': f['energy'],
                            'tempo': f['tempo'],
                            'valence': f['valence'],
                        })
            logger.info(f"🎵 {len(clean_features)} şarkının müzikal özellikleri başarıyla çekildi.")
            return clean_features
        except Exception as e:
            logger.error(f"Spotify API hatası (get_audio_features): {e}")
            return []
    """
    def get_liked_tracks(self, limit=50 ,after_timestamp=None):
        try:
            liked_tracks = []
            ofset_count = 0
            while True:
                result = self.sp.current_user_saved_tracks(limit = limit, offset=ofset_count*limit)
                if not result['items']:
                    break
                for item in result['items']:
                    if after_timestamp and item['added_at'] <= after_timestamp:
                        logger.info(f"🎶 Liked tracks çekme tamamlandı. Toplam {len(liked_tracks)} şarkı çekildi.")
                        return liked_tracks
                    track = item['track']
                    liked_tracks.append({
                        'track_id': track['id'],
                        "added_at": item['added_at']
                    })
                ofset_count += 1
            logger.info(f"❤️ Kütüphanedeki tüm {len(liked_tracks)} beğenilen şarkı başarıyla çekildi.")
            return liked_tracks
        except Exception as e:
            logger.error(f"Spotify API hatası (get_liked_tracks): {e}")
            return []


    def get_or_create_playlist(self, name="Haftalık Modum", description="Ruh halime göre her hafta otomatik güncellenir."):
        try:
            ofset_count = 0
            while True:
                result = self.sp.current_user_playlists(limit=50 , offset=ofset_count*50)
                if not result['items']:
                    break
                for item in result['items']:
                    if item['name'] == name:
                        logger.info(f"✅ '{name}' adlı çalma listesi bulundu, ID'si: {item['id']}")
                        return item['id']
                ofset_count += 1
            user_id = self.sp.me()['id']
            new_playlist = self.sp.user_playlist_create(user=user_id, name=name, public=False, description=description)
            logger.info(f"✅ '{name}' adlı yeni çalma listesi oluşturuldu, ID'si: {new_playlist['id']}")
            return new_playlist['id']
        except Exception as e:
            logger.error(f"Spotify API hatası (get_or_create_playlist): {e}")
            return None

    def clear_playlist(self, playlist_id):
        try:
            self.sp.playlist_replace_items(playlist_id, [])
            logger.info(f"🧹 Çalma listesi (ID: {playlist_id}) temizlendi, artık yeni şarkılar eklenmeye hazır!")
        except Exception as e:
            logger.error(f"Spotify API hatası (clear_playlist): {e}")

    def update_playlist_tracks(self, playlist_id, track_ids):
        """
        GÖREVİ: Algoritmanın (algorithm.py) seçtiği yepyeni şarkıları, 
        az önce temizlediğimiz o sabit listenin içine doldurur.
        """
        try:
            if not track_ids:
                logger.warning("⚠️ Güncellenecek şarkı ID'si yok, çalma listesi güncellenmeyecek.")
                return
            self.sp.playlist_replace_items(playlist_id, track_ids)
            logger.info(f"✅ Çalma listesi (ID: {playlist_id}) başarıyla güncellendi! Toplam {len(track_ids)} şarkı eklendi.")
        except Exception as e:
            logger.error(f"Spotify API hatası (update_playlist_tracks - ID toplama): {e}")
            return

# Modül testi için (Test Pisti) - GÜNCELLENDİ
if __name__ == "__main__":
    logger.info("🚀 SPOTIFY API GENEL TESTİ BAŞLIYOR...")
    
    # 1. Motoru başlat
    spotify_bot = SpotifyClient()
    spotify_bot.authenticate()
    
    # 2. Son dinlenenleri çek
    logger.info("--- TEST 1: Son Dinlenenler ---")
    recent_tracks = spotify_bot.get_recently_played()
    
    # KRİTİK DÜZELTME: Şarkı ID'lerini bir listeye topluyoruz
    test_track_ids = [t['track_id'] for t in recent_tracks] if recent_tracks else []
    
    # 3. Beğenilenleri çek (SADECE SON 1 HAFTA!)
    logger.info("--- TEST 3: Beğenilen Şarkılar (1 Haftalık Sınır) ---")
    bir_hafta_once = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    logger.info(f"Frenleme tarihi: {bir_hafta_once}")
    liked = spotify_bot.get_liked_tracks(limit=50, after_timestamp=bir_hafta_once) 
    
    # 4. Liste İşlemleri
    logger.info("--- TEST 4: Çalma Listesi Operasyonları ---")
    playlist_id = spotify_bot.get_or_create_playlist(name="Haftalık Modum Test", description="API Test Listesidir.")
    
    if playlist_id:
        spotify_bot.clear_playlist(playlist_id)
        if test_track_ids: # Yukarıda oluşturduğumuz listeyi kullanıyoruz
            spotify_bot.update_playlist_tracks(playlist_id, test_track_ids)
            
    logger.info("🎉 TÜM TESTLER BAŞARIYLA TAMAMLANDI!")