
class StartupWorker:
    def __init__(self, app_name):
        pass

    def _is_compiled(self):
        # 2. ARAŞTIR: Uygulamanın PyInstaller ile paketlenip paketlenmediğini 
        # 'sys.frozen' bayrağına bakarak anlayan bir mantık yaz. (True/False dön)
        pass

    def _get_silent_command(self):
        # 3. İşletim sistemine ve '_is_compiled' durumuna göre, siyah konsol
        # penceresi açmadan çalışacak doğru terminal komutunu string olarak üret.
        pass

    def _install_windows_startup(self):
        # 4. 'winreg' kütüphanesini kullanarak Windows Registry'sine kayıt ekle.
        pass

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