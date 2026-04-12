import time
import datetime
from src.spotify_api import SpotifyClient
from src.lastfm_api import LastFMClient
from src.database import SpotifyDB
from src.algorithm import WeeklyAlgorithm
from src.logger_config import setup_logger

logger = setup_logger("Main")

def run_weekly_dj():
    """
    GÖREV: Haftalık Yapay Zeka DJ'ini uyandırıp Spotify listesini günceller.
    
    1. WeeklyAlgorithm sınıfından bir 'brain' (beyin) objesi oluştur.
    2. brain.generate_playlist() fonksiyonunu çağırıp yeni şarkı ID'lerini al.
    3. Eğer liste boş değilse:
       - SpotifyClient'ı başlat ve authenticate() ile yetki al.
       - spotify.get_or_create_playlist() ile hedef listeyi bul/oluştur.
       - spotify.clear_playlist() ile listenin içini boşalt.
       - spotify.update_playlist_tracks() ile yeni şarkıları listeye doldur.
       - SpotifyDB'yi başlat ve .clear_weekly_data() ile veritabanını yeni hafta için sıfırla.
    """
    try:
        logger.info("🎧 Haftalık DJ başlatılıyor...")
        brain = WeeklyAlgorithm()
        new_tracks = brain.generate_playlist()
        if not new_tracks:
            logger.warning("⚠️ Yeni şarkı bulunamadı, haftalık DJ atlanacak.")
            return
        else:
            spotify = SpotifyClient()
            spotify.authenticate()
            playlist_id = spotify.get_or_create_playlist("Haftalık Modum", "Ruh halime göre her hafta otomatik güncellenir.")
            spotify.clear_playlist(playlist_id)
            spotify.update_playlist_tracks(playlist_id, new_tracks)
            db = SpotifyDB()
            db.clear_weekly_data()
            logger.info("🎉 Haftalık liste başarıyla Spotify'a gönderildi ve kasa sıfırlandı!")
            

    except Exception as e:
        logger.error(f"❌ Weekly DJ başlatılırken hata: {e}")
        return
    

def sync_listening_data():
    try:
        logger.info("🔄 Veri senkronizasyonu (toplama işlemi) başlıyor...")

        spotify_client = SpotifyClient()
        spotify_client.authenticate()
        lastfm_client = LastFMClient()
        db = SpotifyDB()
        db.init_db()

        last_played = db.get_last_played_time()
        recent_tracks = spotify_client.get_recently_played(after_timestamp=last_played)
        if not recent_tracks:
            logger.info("🎵 Yeni dinlenen şarkı bulunamadı, 5 dakika sonra tekrar denenecek.")
            return
        for track in recent_tracks:
            track_id = track['track_id']
            track_name = track['track_name']
            artist_name = track['artist_name']
        
            track_data = (track_id, track_name, artist_name, track['duration_ms'], None, None, None )
            db.process_played_track(track_data, track['played_at']) 

            tags = lastfm_client.get_track_tags(artist_name, track_name)
            if tags:
                db.add_track_tags(track_id, tags)
            time.sleep(0.5)
        logger.info(f"✅ Toplam {len(recent_tracks)} yeni şarkı başarıyla işlendi ve hafızaya alındı!")

    except Exception as e:
        logger.error(f"❌ Veri senkronizasyonu sırasında hata: {e}")
        return

if __name__ == "__main__":
    logger.info("🚀 AI DJ Motoru Çalıştırıldı!")
    run_weekly_dj() # Manuel test

    while True:
        try:
            sync_listening_data()
            
            now = datetime.datetime.now()
            
            if now.weekday() == 6 and now.hour == 23 and now.minute >= 50:
                logger.info("⏰ Vakit geldi! Haftalık DJ sahneye çıkıyor...")
                run_weekly_dj()
                
                logger.info("💤 DJ dinlenmeye çekildi, 1 saat bekleniyor...")
                time.sleep(3600)
                continue 
                
            logger.info("⏰ 5 dakika bekleniyor...")
            time.sleep(300)  
            
        except Exception as e:
            logger.error(f"❌ Ana döngüde hata: {e}")  
            logger.info("⏰ 30 dakika bekleniyor...")
            time.sleep(1800)