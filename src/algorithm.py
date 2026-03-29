from src.database import SpotifyDB
from src.spotify_api import SpotifyClient
from src.lastfm_api import LastFMClient
from src.logger_config import setup_logger

logger = setup_logger("Algorithm")

class WeeklyAlgorithm:
    
    def __init__(self):
        try:
            self.db = SpotifyDB()
            logger.info("Veritabanı bağlantısı başarılı.")
            self.spotify = SpotifyClient()
            logger.info("Spotify ajanı başlatıldı.")
            self.lastfm = LastFMClient()
            logger.info("Last.fm ajanı başlatıldı.")
            self.spotify.authenticate()
            logger.info("Spotify ajanı başarıyla doğrulandı.")
            logger.info("Algoritma başarıyla başlatıldı.")
        except Exception as e:
            logger.error(f"Algoritma başlatılırken hata: {e}")
            raise e

    def _calculate_playlist_length(self, total_tracks):
        try:
            total_tracks = int(total_tracks)
            calculated_length = int(total_tracks * 0.25)
            if calculated_length < 20:
                calculated_length = 20
            elif calculated_length > 100:
                calculated_length = 100
            logger.info(f"Toplam şarkı: {total_tracks}, Hesaplanan liste uzunluğu: {calculated_length}")    
            return calculated_length 
        except Exception as e:
            logger.error(f"Playlist uzunluğu hesaplanırken hata: {e}")
            return 20  

    def _build_safe_zone(self, weekly_tracks):
        try:
            safe_track_ids = []
            for track in weekly_tracks:
                if track[8] == 1:  
                    safe_track_ids.append(track[0])
                    logger.info(f"Beğenilen şarkı eklendi: {track[0]}")
            top_played = sorted(weekly_tracks, key=lambda x: x[7], reverse=True)
            added_top_tracks = 0
            for track in top_played:
                if added_top_tracks >= 3:
                    break
                if track[0] not in safe_track_ids:
                    safe_track_ids.append(track[0])
                    added_top_tracks += 1
                    logger.info(f"Top şarkı eklendi: {track[0]} (Play Count: {track[7]})")
            return safe_track_ids
        except Exception as e:
            logger.error(f"Güvenli bölge oluşturulurken hata: {e}")
            return []
        
    def _discover_new_tracks(self, top_tags, played_track_ids, needed_count):
        try:
            new_track_ids = []
            for tag in top_tags:
                tag_name = tag[0]
                recommended_tracks = self.lastfm.get_tracks_by_tag(tag_name , limit=10)
                for rec_track in recommended_tracks:
                    if len(new_track_ids) >= needed_count:
                        break
                    sp_id = self.spotify.search_track(rec_track['artist'], rec_track['track'])
                    if sp_id and sp_id not in played_track_ids and sp_id not in new_track_ids:
                        new_track_ids.append(sp_id)
                        logger.info(f"Yeni şarkı keşfedildi: {rec_track['track']} - {rec_track['artist']} (Spotify ID: {sp_id})")
                if len(new_track_ids) >= needed_count:
                    break
            return new_track_ids
        except Exception as e:
            logger.error(f"Yeni şarkılar keşfedilirken hata: {e}")
            return []

    def generate_playlist(self):
        """
        GÖREV: ANA ORKESTRATÖR. Yukarıdaki tüm parçaları birleştirip nihai listeyi basmak.
        1. DB'den haftalık şarkıları (get_weekly_tracks) çek. Boşsa işlemi durdur (return []).
        2. _calculate_playlist_length ile hedef uzunluğu (target_length) bul.
        3. Yankı odası kalkanı için haftalık şarkıların ID'lerini bir Set (küme) içine al (played_track_ids).
        4. _build_safe_zone fonksiyonunu çağırıp güvenli şarkıları al ve final_playlist listene koy.
        5. Kalan boşluğu (target_length - len(final_playlist)) hesapla.
        6. Eğer boşluk varsa: DB'den en iyi 3 etiketi çek, _discover_new_tracks'i çağır, gelen yeni şarkıları final_playlist'e ekle.
        7. final_playlist'i tam target_length sayısından kesip döndür.
        """
        pass

if __name__ == "__main__":
    # Test Pisti
    brain = WeeklyAlgorithm()
    liste = brain.generate_playlist()
    print(f"Oluşturulan Çalma Listesi ID'leri: {liste}")