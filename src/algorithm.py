from src.database import SpotifyDB
from src.spotify_api import SpotifyClient
from src.lastfm_api import LastFMClient
from src.logger_config import setup_logger

logger = setup_logger("Algorithm")

class WeeklyAlgorithm:
    
    def __init__(self):
        """
        GÖREV: İstihbarat ajanlarını ve veritabanını hayata geçirmek.
        1. self.db = SpotifyDB() ile kasayı bağla.
        2. self.spotify ve self.lastfm ajanlarını başlat.
        3. Spotify ajanının arama yapabilmesi için 'authenticate()' metodunu çağırıp uyandır.
        """
        pass

    def _calculate_playlist_length(self, total_tracks):
        """
        GÖREV: Dinamik liste uzunluğunu belirlemek.
        1. total_tracks sayısının %25'ini al ve tam sayıya (int) çevir.
        2. Eğer sonuç 10'dan küçükse 10 döndür.
        3. Eğer sonuç 50'den büyükse 50 döndür.
        4. İkisinin arasındaysa bulduğun sayıyı döndür.
        !!!NOT DEĞERLERLE OYNA!!!!
        """
        pass

    def _build_safe_zone(self, weekly_tracks):
        """
        GÖREV: Listenin temelini (Beğenilenler ve Top 3) oluşturmak.
        1. Gelen weekly_tracks listesindeki şarkıları dön. 'is_liked' (8. indeks) 1 olanların ID'lerini bir listeye al.
        2. Şarkıları 'play_count' (7. indeks) değerine göre büyükten küçüğe sırala.
        3. En baştaki 3 şarkıyı al, eğer az önce oluşturduğun listede yoklarsa onları da ekle.
        4. Bu güvenli şarkı ID'lerinin olduğu listeyi (safe_track_ids) döndür.
        """
        pass

    def _discover_new_tracks(self, top_tags, played_track_ids, needed_count):
        """
        GÖREV: Last.fm ve Spotify köprüsünü kurup, yankı odasını kırarak yepyeni şarkılar bulmak.
        1. top_tags içindeki her bir etiket için Last.fm'den (get_tracks_by_tag) şarkı isimlerini çek.
        2. Gelen her bir şarkı adı ve sanatçısını Spotify'da (search_track) aratıp ID'sini bul.
        3. FİLTRE: Bulunan ID geçerliyse VE played_track_ids (bu hafta dinlenenler) içinde YOKSA listene ekle.
        4. Topladığın yeni şarkı sayısı 'needed_count' (kalan boşluk) sayısına ulaştığı an döngüleri kır (break).
        5. Bulduğun bu taptaze yeni şarkı ID'lerini döndür.
        """
        pass

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