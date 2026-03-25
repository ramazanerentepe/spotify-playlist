import os
import logging
import spotipy
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
        self.scope = "user-read-recently-played user-library-read playlist-modify-public playlist-modify-private"
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
            raise e

    def get_recently_played(self, after_timestamp=None):
        """
        GÖREVİ: Kullanıcının en son dinlediği şarkıları çeker (Catch-up).
        """
        pass

    def get_audio_features(self, track_ids):
        """
        GÖREVİ: Verilen şarkıların müzikal röntgenini (enerji, tempo vb.) çeker.
        """
        pass

    def get_liked_tracks(self, limit=50):
        """
        GÖREVİ: Kullanıcının beğendiği son şarkıları çeker. Algoritmayı beslemek için.
        """
        pass

    # --- YENİ EKLENEN / GÜNCELLENEN FONKSİYONLAR ---

    def get_or_create_playlist(self, name="Haftalık Modum", description="Ruh halime göre her hafta otomatik güncellenir."):
        """
        GÖREVİ: Kullanıcının kütüphanesini tarar. 
        Eğer 'name' adında bir liste ZATEN VARSA onun ID'sini döndürür.
        YOKSA (ilk kurulumsa) yeni bir liste oluşturup onun ID'sini döndürür.
        NEDEN LAZIM?: Kütüphaneyi çöplüğe çevirmemek, tek listeyi kullanmak için.
        """
        pass

    def clear_playlist(self, playlist_id):
        """
        GÖREVİ: Verilen çalma listesinin içindeki TÜM şarkıları siler.
        NEDEN LAZIM?: Yeni haftanın şarkılarını eklemeden önce, listeyi tertemiz 
        bir boş tuvale dönüştürmek için.
        """
        pass

    def update_playlist_tracks(self, playlist_id, track_ids):
        """
        GÖREVİ: Algoritmanın (algorithm.py) seçtiği yepyeni şarkıları, 
        az önce temizlediğimiz o sabit listenin içine doldurur.
        """
        pass

# Modül testi için
if __name__ == "__main__":
    logger.info("Spotify API iskeleti (Tek Liste Mantığı) hazır!")
    logger.info("Spotify API testi başlatılıyor...")
    
    # 1. Robotumuzu oluştur (Bu esnada __init__ çalışacak ve .env okunacak)
    spotify_bot = SpotifyClient()
    
    # 2. Giriş yapmayı dene (Bu esnada tarayıcı açılacak)
    spotify_bot.authenticate()