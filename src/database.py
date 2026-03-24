import sqlite3
import os
import logging

# --- LOGGING YAPILANDIRMASI ---
# İşlemleri takip etmek için profesyonel günlükleme sistemi.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DatabaseGuard")

class SpotifyDB:
    def __init__(self, db_path=None):
        """
        Veritabanı yöneticisini başlatır.
        Bağımlılıkların dışarıdan verilmesi (Dependency Injection) prensibine uygundur.
        """
        self.db_path = db_path or os.path.join("data", "spotify_listening.db")
        
        # Klasörün varlığını garanti altına al (Single Responsibility)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Beklenen şemalar ve performans için İndeks tanımları
        self.EXPECTED_SCHEMAS = {
            "tracks": {
                "columns": {"track_id", "track_name", "artist_name", "duration_ms", "energy", "tempo", "valence"},
                "create_sql": '''
                    CREATE TABLE IF NOT EXISTS tracks (
                        track_id TEXT PRIMARY KEY,
                        track_name TEXT NOT NULL,
                        artist_name TEXT NOT NULL,
                        duration_ms INTEGER,
                        energy REAL,
                        tempo REAL,
                        valence REAL
                    )''',
                "indices": [
                    "CREATE INDEX IF NOT EXISTS idx_track_artist ON tracks(artist_name)"
                ]
            },
            "listening_history": {
                "columns": {"history_id", "track_id", "played_at"},
                "create_sql": '''
                    CREATE TABLE IF NOT EXISTS listening_history (
                        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        track_id TEXT NOT NULL,
                        played_at TIMESTAMP NOT NULL,
                        FOREIGN KEY (track_id) REFERENCES tracks (track_id) ON DELETE CASCADE
                    )''',
                "indices": [
                    "CREATE INDEX IF NOT EXISTS idx_played_at ON listening_history(played_at)"
                ]
            },
            "weekly_reports": {
                "columns": {
                    "report_id", "created_at", "total_minutes", "top_track_1", "top_track_2", 
                    "top_track_3", "avg_energy", "avg_tempo", "avg_valence", "mood_label"
                },
                "create_sql": '''
                    CREATE TABLE IF NOT EXISTS weekly_reports (
                        report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        created_at TEXT NOT NULL,
                        total_minutes INTEGER,
                        top_track_1 TEXT,
                        top_track_2 TEXT,
                        top_track_3 TEXT,
                        avg_energy REAL,
                        avg_tempo REAL,
                        avg_valence REAL,
                        mood_label TEXT
                    )''',
                "indices": []
            }
        }

    def get_connection(self):
        """Veritabanı bağlantısı oluşturur ve kısıtlamaları aktif eder."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON") #
        return conn

    def _validate_table(self, cursor, table_name):
        """Tablo yapısını beklenen sütun listesiyle karşılaştırır."""
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        if not columns:
            return False
            
        current_columns = {col[1] for col in columns}
        return current_columns == self.EXPECTED_SCHEMAS[table_name]["columns"]

    def init_db(self):
        """
        Veritabanını başlatır, tabloları ve indeksleri kontrol/tamir eder.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for table_name, schema in self.EXPECTED_SCHEMAS.items():
                    # Yapı hatalıysa veya tablo yoksa yeniden oluştur
                    if not self._validate_table(cursor, table_name):
                        logger.warning(f"BÜTÜNLÜK HATASI: '{table_name}' tablosu yapılandırılıyor...")
                        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                        cursor.execute(schema["create_sql"])
                        
                        # Dizinleme (Indexing) işlemi: Arama hızını artırır
                        for index_sql in schema["indices"]:
                            cursor.execute(index_sql)
                            
                        logger.info(f"BAŞARILI: '{table_name}' tablosu ve indeksleri oluşturuldu.")
                    else:
                        logger.info(f"DOĞRULANDI: '{table_name}' tablosu sağlıklı.")
                
                conn.commit()
                logger.info("🚀 Veritabanı motoru hazır.")
                
        except sqlite3.Error as e:
            logger.error(f"Veritabanı başlatma hatası: {e}")

   
    def add_track(self, track_data):
        sql = ''' 
            INSERT OR IGNORE INTO tracks
            (track_id, track_name, artist_name, duration_ms, energy, tempo, valence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
          '''
        try:
            with self.get_connection() as conn:
                conn.execute(sql, track_data)
                
                conn.commit()
                logger.info(f"✅ Şarkı veritabanına kaydedildi: {track_data[1]}")
        except sqlite3.Error as e:
            logger.error(f"Şarkı eklenirken veritabanı hatası oluştu: {e}")

    def add_listening_history(self, track_id, played_at):
        sql = ''' 
            INSERT INTO listening_history
            (track_id, played_at) 
            VALUES (?, ?)
            '''
        try:
            with self.get_connection() as conn:
                conn.execute(sql, (track_id, played_at))
                
                conn.commit()
                logger.info(f"✅ Dinleme geçmişi kaydedildi: Track ID {track_id} - Played At {played_at}")
        except sqlite3.Error as e:
            logger.error(f"Dinleme geçmişi eklenirken veritabanı hatası oluştu: {e}")

    def process_played_track(self, track_data, played_at):
        self.add_track(track_data)
        self.add_listening_history(track_data[0], played_at)

    def get_last_played_time(self):
        sql = ''' 
            SELECT MAX(played_at) FROM listening_history'''
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(sql)
                result = cursor.fetchone()
                last_played = result[0] if result and result[0] else None
                logger.info(f"Son dinleme zamanı: {last_played}")
                return last_played  
        except sqlite3.Error as e:
            logger.error(f"Son dinleme zamanını çekerken veritabanı hatası oluştu: {e}")
            return None

    def clear_weekly_data(self):
        sql = '''
            DELETE FROM listening_history;
            DELETE FROM tracks;
        '''
        try:
            with self.get_connection() as conn:
                conn.executescript(sql)
                conn.commit()
                logger.info("✅ Haftalık veriler temizlendi. Yeni haftaya hazırız!")
        except sqlite3.Error as e:
            logger.error(f"Haftalık verileri temizlerken veritabanı hatası oluştu: {e}")

    def get_weekly_tracks(self):
        sql = '''
            SELECT t.track_id, t.track_name, t.artist_name, t.duration_ms, t.energy, t.tempo, t.valence,
                   COUNT(l.history_id) AS play_count
            FROM tracks t
            JOIN listening_history l ON t.track_id = l.track_id
            GROUP BY t.track_id
            ORDER BY play_count DESC'''
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(sql)
                tracks = cursor.fetchall()
                logger.info(f"Haftalık şarkılar çekildi: {len(tracks)} şarkı bulundu.")
                return tracks
        except sqlite3.Error as e:
            logger.error(f"Haftalık şarkıları çekerken veritabanı hatası oluştu: {e}")
            return []

# Modül testi için
if __name__ == "__main__":
    db_manager = SpotifyDB()
    db_manager.init_db()