import time
import datetime
from src.spotify_api import SpotifyClient
from src.lastfm_api import LastFMClient
from src.database import SpotifyDB
from src.algorithm import WeeklyAlgorithm
from src.logger_config import setup_logger

logger = setup_logger("Main")

def run_weekly_dj():
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
        if last_played:
            dt = datetime.datetime.strptime(last_played[:19], "%Y-%m-%dT%H:%M:%S")
            after_timestamp = int(dt.timestamp() * 1000)
        else:
            after_timestamp = int(time.time() * 1000)
            logger.info("ℹ️ Veritabanı yeni temizlendiği için geçmiş çekilmiyor, takip şimdi başlıyor.")
        recent_tracks = spotify_client.get_recently_played(after_timestamp=after_timestamp)
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

        breakpoint = last_played
        if not breakpoint:
            breakpoint = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
            logger.info(f"⚠️ Kasa boş! Beğenilenler için 1 haftalık fren uygulandı: {breakpoint}")
        liked_tracks = spotify_client.get_liked_tracks(after_timestamp=breakpoint)
        for item in liked_tracks:
            db.add_liked_track(item['track_id'])
        logger.info(f"❤️ {len(liked_tracks)} yeni beğenilen şarkı kontrol edildi ve kasaya eklendi.")

    except Exception as e:
        logger.error(f"❌ Veri senkronizasyonu sırasında hata: {e}")
        return

if __name__ == "__main__":
    logger.info("🚀 AI DJ Motoru Çalıştırıldı!")
    while True:
        try:
            sync_listening_data()
            
            now = datetime.datetime.now()
            
            is_sunday_night = (now.weekday() == 6 and now.hour == 23 and now.minute >= 50)
            
            is_seven_days_passed = False
            db = SpotifyDB() 
            first_played = db.get_first_played_time()
            
            if first_played:
                try:
                    first_dt = datetime.datetime.strptime(first_played[:19], "%Y-%m-%dT%H:%M:%S")
                    if (now - first_dt).days >= 7:
                        is_seven_days_passed = True
                        logger.info("⚠️ Pazar gecesi kaçırılmış! B Planı devreye giriyor: Kasa 7 günlük sınırını doldurdu.")
                except Exception as e:
                    logger.warning(f"Tarih hesaplanırken ufak bir hata: {e}")

            if is_sunday_night or is_seven_days_passed:
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