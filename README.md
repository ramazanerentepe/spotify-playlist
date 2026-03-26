# 🎵 Spotify Weekly Mood & Dynamic Playlist Generator

> **"Spotify algoritmalarının yankı odasından çıkın. Kendi müzik zevkinizin patronu olun."**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Local_Vault-lightgrey?style=flat&logo=sqlite)
![Spotify API](https://img.shields.io/badge/Spotify_API-Integrated-1ED760?style=flat&logo=spotify)
![Security](https://img.shields.io/badge/Security-PKCE_Flow-red?style=flat&logo=security)

## 🚀 Neden Bu Projeye İhtiyacın Var?
Spotify'ın size sürekli aynı 50 şarkıyı önermesinden sıkılmadınız mı? Sırf geçen ay birkaç melankolik şarkı dinlediniz diye tüm "Haftalık Keşif" listenizin mahvolmasına ne demeli? 

Standart algoritmalar geçmişinize pranga vurur. **Biz ise bu prangaları kırıyoruz.** Bu proje; kendi bilgisayarınızda çalışan, tamamen size özel ve %100 gizliliğe saygı duyan kişisel bir yapay zeka DJ'idir. Sizi arka planda sessizce dinler, o haftaki müzikal DNA'nızın (enerji, tempo, akustiklik) matematiğini çıkarır ve her hafta size nokta atışı, yepyeni bir "Ruh Hali" listesi sunar.

## ✨ Sizi Neler Bekliyor? (Özellikler)

* 🧠 **Haftalık Hafıza Kaybı (Gerçek Dinamiklik):** Diğer algoritmalar geçmişinize takılıp kalır. Bizim motorumuz ise her hafta sonu yerel hafızasını tamamen siler. Yeni haftaya "sıfırdan" ve %100 o anki ruh halinize (odaklanmış, enerjik, depresif) odaklanarak başlar.
* 🛡️ **Banka Seviyesinde Şifresiz Güvenlik (PKCE):** Uygulama hiçbir şekilde "Client Secret" (Gizli Şifre) barındırmaz. Bu sayede uygulamanın derlenmiş hali başkalarıyla güvenle paylaşılabilir. Kodlama bilmeyen arkadaşlarınız bile tek tıkla kendi Spotify hesaplarını güvenle bağlayabilir.
* ♻️ **Zen Kütüphane (Tek Liste Stratejisi):** Her hafta "Haftalık Mod 1, 2, 3..." diye onlarca liste oluşturup Spotify'ınızı çöplüğe çevirmez. Sadece bir adet **"Haftalık Modum"** listesi oluşturur ve her hafta içini acımasızca temizleyip yeni şaheserlerle doldurur.
* 📱 **Görünmez Senkronizasyon (Catch-up):** Müzik sadece bilgisayarda dinlenmez! Bilgisayarınız kapalıyken telefonda dinlediğiniz müzikler kaybolmaz. Uygulama açıldığı an eksik verileri Spotify'dan çeker ve açığı kapatır.
* 🩺 **Kendi Kendini Onarma (Self-Healing):** İnternet mi koptu? Giriş biletinizin (Token) süresi mi doldu? Program asla çökmez; bozuk dosyaları tespit edip yok eder ve sizi nazikçe yeni bir giriş ekranına yönlendirir.

## 🏗️ Kaputun Altında Ne Var? (Mimari)
Proje, "Tek Sorumluluk Prensibi" (SOLID) merkeze alınarak tasarlanmıştır ve son kullanıcıya yönelik tek tıkla çalışacak (`.exe` / `.app`) bir formata dönüşmeye hazırdır.

* `database.py`: Kendi kendini kuran ve onaran yerel SQLite motoru.
* `logger_config.py`: Merkezi ve standartlaştırılmış hata/log takip merkezi.
* `spotify_api.py`: Şifresiz PKCE OAuth2 süreçleri, otonom veri çekimi.
* `algorithm.py`: *(Geliştirme Aşamasında)* Beğenilen şarkılara ağırlık vererek ruh hali (mood) haritası çıkaran matematiksel beyin.
* `main.py`: Tüm sistemi asenkron (Thread) olarak yöneten ana orkestra şefi.

## 🚀 Hemen Başla (Geliştiriciler İçin)

1. Projeyi klonlayın ve motoru indirin:
   ```bash
   pip install spotipy python-dotenv
