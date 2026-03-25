import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyPKCE
from dotenv import load_dotenv
from logger_config import setup_logger 

logger = setup_logger("SpotifyAPI")

class SpotifyClient:
    def __init__(self):
        """
        GÖREVİ: Sınıf başlatıldığında .env dosyasındaki bilgileri okur.
        NEDEN PKCE?: Masaüstü uygulaması yapacağımız için Client Secret KULLANILMAZ.
        """
        pass

    def authenticate(self):
        """
        GÖREVİ: Kullanıcıyı tarayıcıya yönlendirip Spotify'a güvenli giriş yapmasını sağlar.
        NASIL ÇALIŞACAK?: Eğer kullanıcı zaten giriş yaptıysa sessizce arkadan yenileyecek.
        """
        pass

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