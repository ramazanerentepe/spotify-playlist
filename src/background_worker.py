import sys
import platform
import pathlib
from src.logger_config import setup_logger

logger = setup_logger("StartupWorker")
class StartupWorker:
    def __init__(self, app_name : str) -> None:
        self.app_name = app_name
        self.os_name = platform.system()
        self.script_path = (pathlib.Path(__file__).parent.parent / "main.py").resolve()
        if not self.script_path.is_file():
            error_msg = f"Başlangıca eklenecek hedef dosya bulunamadı: {self.script_path}"
            logger.error(f"❌ Kritik Hata: {error_msg}")
            raise FileNotFoundError(error_msg)
        logger.info(f"✅ StartupWorker başlatıldı. OS: {self.os_name}, Hedef: {self.script_path.name}") #daha sonra kaldırılacak

    def _is_compiled(self) -> bool:
        return getattr(sys, 'frozen', False)

    def _get_silent_command(self) -> str:
        #paketlenmiş uygulamalarda, sys.executable üzerinden çalıştırılacak komutun tam yolunu döndürür.
        if self._is_compiled():
            return f'"{sys.executable}"'
        #windows'ta pythonw.exe kullanarak konsolsuz çalıştırma, diğer platformlarda normal python komutu yeterli olacaktır.
        if self.os_name == "Windows":
            return f'"{sys.executable.replace("python.exe", "pythonw.exe")}" "{self.script_path}"'
        # Diğer platformlarda normal python komutu kullanılır.
        return f'"{sys.executable}" "{self.script_path}"'
        
    def _install_windows_startup(self) -> None:
        import winreg
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, self._get_silent_command())
            winreg.CloseKey(key)
            logger.info(f"✅ Windows başlangıç kaydı eklendi: {self.app_name}")
        except Exception as e:
            logger.error(f"❌ Windows başlangıç kaydı eklenirken hata: {e}")
            raise

    def _install_linux_startup(self):
        # 5. Linux'ta '~/.config/autostart/' dizinine .desktop dosyası oluştur.
        pass

    def _install_mac_startup(self):
        # 6. ARAŞTIR: ~/Library/LaunchAgents dizinine bir .plist dosyası oluştur.
        # Formatın nasıl olması gerektiğini ve launchctl ile nasıl aktif edileceğini kurgula.
        pass

    def apply_startup(self):
        # 7. İşletim sistemini tespit ederek uygun startup kurulum fonksiyonunu çağır.
        pass