import sqlite3
import os
import logging

# --- LOGGING YAPILANDIRMASI ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DatabaseGuard")

# --- YAPILANDIRMA ---
DB_PATH = os.path.join("data", "spotify_listening.db")

# Profesyonel seviyede, beklenen kolon listesini bir küme (set) olarak tutuyoruz.
# Set kullanmak, karşılaştırma yaparken çok daha hızlı ve efektiftir.
EXPECTED_SCHEMAS = {
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
            )'''
    },
    "listening_history": {
        "columns": {"history_id", "track_id", "played_at"},
        "create_sql": '''
            CREATE TABLE IF NOT EXISTS listening_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_id TEXT NOT NULL,
                played_at TIMESTAMP NOT NULL,
                FOREIGN KEY (track_id) REFERENCES tracks (track_id) ON DELETE CASCADE
            )'''
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
            )'''
    }
}

def validate_table_structure(cursor, table_name):
    """
    Tablonun mevcut kolonlarını beklenen liste ile birebir karşılaştırır.
    
    Returns:
        bool: Tablo yapısı tamamen doğruysa True, fark varsa False.
    """
    # PRAGMA table_info: Tablodaki tüm kolon bilgilerini (id, isim, tip vb.) getirir.
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    if not columns:
        return False # Tablo hiç yoksa direkt hatalı kabul et
    
    # Mevcut tablodaki kolon isimlerini bir küme (set) haline getiriyoruz.
    # columns[i][1] ifadesi kolonun ismini verir.
    current_columns = {col[1] for col in columns}
    
    # Beklenen kolonlar ile mevcut kolonlar birebir aynı mı? (Ne eksik ne fazla)
    return current_columns == EXPECTED_SCHEMAS[table_name]["columns"]

def init_db():
    """
    Veritabanını başlatır ve tüm tabloların şema bütünlüğünü (Integrity) doğrular.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            
            for table_name, schema in EXPECTED_SCHEMAS.items():
                # Tablo yapısını derinlemesine kontrol et
                if not validate_table_structure(cursor, table_name):
                    logger.warning(f"BÜTÜNLÜK HATASI: '{table_name}' tablosu eksik veya fazla kolon içeriyor. Sıfırlanıyor...")
                    
                    # Şema uyuşmazlığında tabloyu temizle ve en güncel haliyle kur
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                    cursor.execute(schema["create_sql"])
                    logger.info(f"BAŞARILI: '{table_name}' tablosu doğru şema ile yeniden oluşturuldu.")
                else:
                    logger.info(f"DOĞRULANDI: '{table_name}' tablosu sağlıklı.")
            
            conn.commit()
            
    except sqlite3.Error as e:
        logger.error(f"Kritik veritabanı hatası: {e}")

if __name__ == "__main__":
    init_db()