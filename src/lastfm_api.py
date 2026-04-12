import os
import re
import requests
import dotenv
import logging
from src.logger_config import setup_logger

logger = setup_logger("LastFMAPI")

class LastFMClient:
    def __init__(self):
        dotenv.load_dotenv()
        self.api_key = os.getenv("LASTFM_API_KEY")
        if not self.api_key:
            logger.error("LASTFM_API_KEY .env dosyasında tanımlı değil!")
            raise ValueError("Gerekli Last.fm API bilgileri eksik.")
        self.base_url = "http://ws.audioscrobbler.com/2.0/"
        logger.info("✅ Last.fm API motoru başlatıldı, kimlik belgeleri hazırlandı.")
    
    def get_artist_tags(self, artist_name, limit=5):
        """Eğer şarkı etiketi bulunamazsa, B planı olarak sanatçının etiketlerini çeker."""
        params = {
            'method': 'artist.getTopTags', # Sanatçı etiketleri için farklı bir metot kullanıyoruz
            'artist': artist_name,
            'api_key': self.api_key,
            'format': 'json',
            'autocorrect': 1
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if 'toptags' not in data or 'tag' not in data['toptags']:
                return []
                
            tags = data['toptags']['tag']
            return [tag['name'].lower() for tag in tags[:limit]]
        except Exception as e:
            logger.error(f"Last.fm Sanatçı API hatası: {e}")
            return []

    def get_track_tags(self, artist_name, track_name, limit=5):
        clean_track = re.sub(r"\(.*?\)|-.*", "", track_name).strip()
        if clean_track != track_name:
            logger.info(f"🔍 Şarkı adı temizlendi: '{track_name}' → '{clean_track}'")
            track_name = clean_track

        params = {

            'method': 'track.getTopTags',
            'artist': artist_name,
            'track': track_name,
            'api_key': self.api_key,
            'format': 'json',
            'autocorrect': 0
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if 'toptags' in data and 'tag' in data['toptags']:
                tags = data['toptags']['tag']
                top_tags = [tag['name'].lower() for tag in tags[:limit]]
                if top_tags:
                    logger.info(f"✅ '{artist_name} - {track_name}' şarkısı için bulunan etiketler: {top_tags}")
                    return top_tags
            logger.warning(f"⚠️ {track_name} için etiket bulunamadı. B Planı: '{artist_name}' etiketleri aranıyor...")
            artist_tags = self.get_artist_tags(artist_name, limit)
            if artist_tags:
                logger.info(f"🎤 {artist_name} - {track_name} için sanatçı etiketleri kullanıldı.")
                return artist_tags
            return []
        except Exception as e:
            logger.error(f"Last.fm API hatası (get_track_tags): {e}")
            return []
        
    def get_tracks_by_tag(self, tag_name, limit=10):
        params = {
            'method': 'tag.getTopTracks',
            'tag': tag_name,
            'api_key': self.api_key,
            'format': 'json',
            'limit': limit
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if 'tracks' in data and 'track' in data['tracks']:
                tracks = data['tracks']['track']
                recommended_tracks = []
                for t in tracks:
                    recommended_tracks.append({
                        'artist': t['artist']['name'],
                        'track': t['name']
                    })
                logger.info(f"🎧 Last.fm'den '{tag_name}' etiketi için {len(recommended_tracks)} şarkı tavsiyesi çekildi.")
                return recommended_tracks
            return []
        except Exception as e:
            logger.error(f"Last.fm API hatası (get_tracks_by_tag): {e}")
            return []
    