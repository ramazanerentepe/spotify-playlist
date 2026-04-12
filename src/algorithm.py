import datetime
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
                    logger.info(f"❤️ Beğenilen şarkı listeye eklendi: {track[1]} - {track[2]} ID :  {track[0]}")
            top_played = sorted(weekly_tracks, key=lambda x: x[7], reverse=True)
            added_top_tracks = 0
            for track in top_played:
                if added_top_tracks >= 3:
                    break
                if track[0] not in safe_track_ids:
                    safe_track_ids.append(track[0])
                    added_top_tracks += 1
                    logger.info(f"🔥 Haftanın Top Şarkısı eklendi: {track[1]} - {track[2]} ({track[7]} kere dinlendi) ID : {track[0]}")
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
        try:
                week_tracks = self.db.get_weekly_tracks()
                if not week_tracks:
                    logger.warning("Haftalık şarkı bulunamadı. Çalma listesi oluşturulamayacak.")
                    return []
                played_track_ids = set(track[0] for track in week_tracks)
                target_length = self._calculate_playlist_length(len(week_tracks))
                finally_playlist = self._build_safe_zone(week_tracks)
                needed_count = target_length
                if needed_count > 0:
                    top_tags = self.db.get_top_weekly_tags(limit=5)
                    new_tracks = self._discover_new_tracks(top_tags, played_track_ids, needed_count)
                    finally_playlist.extend(new_tracks)

                logger.info(f"🎉 AI DJ görevi tamamladı! Toplam {len(finally_playlist)} şarkılık liste hazır.")
                return finally_playlist
        except Exception as e:
            logger.error(f"Çalma listesi oluşturulurken hata: {e}")
            return []

    def create_weekly_summary(self):
        try:
            week_tracks = self.db.get_weekly_tracks()
            if not week_tracks:
                logger.warning("Raporlanacak şarkı bulunamadı.")
                return None

            created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            total_ms = sum((track[3] or 0) * track[7] for track in week_tracks)
            total_minutes = int(total_ms / 60000)

            sorted_by_play = sorted(week_tracks, key=lambda x: x[7], reverse=True)
            top_1 = f"{sorted_by_play[0][1]} - {sorted_by_play[0][2]}" if len(sorted_by_play) > 0 else None
            top_2 = f"{sorted_by_play[1][1]} - {sorted_by_play[1][2]}" if len(sorted_by_play) > 1 else None
            top_3 = f"{sorted_by_play[2][1]} - {sorted_by_play[2][2]}" if len(sorted_by_play) > 2 else None

            liked_count = sum(1 for track in week_tracks if track[8] == 1)

            top_tags = self.db.get_top_weekly_tags(limit=1)
            mood_label = top_tags[0][0].title() if top_tags else "Bilinmiyor"

            report_data = (
                created_at,    
                total_minutes, 
                top_1,         
                top_2,         
                top_3,        
                None,          
                None,          
                None,          
                mood_label,    
                liked_count    
            )

            logger.info(f"📈 Haftalık özet hesaplandı. Toplam Süre: {total_minutes} dk, Ruh Hali: {mood_label}")
            return report_data

        except Exception as e:
            logger.error(f"Haftalık rapor parametreleri hesaplanırken hata: {e}")
            return None
