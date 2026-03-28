import time
from src.spotify_api import SpotifyClient
from src.lastfm_api import LastFMClient
from src.database import SpotifyDB
from src.logger_config import setup_logger

logger = setup_logger("Main")

def sync_listening_data():
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

if __name__ == "__main__":
    logger.info("🚀 Motoru Çalıştırıldı!")

    sync_listening_data()