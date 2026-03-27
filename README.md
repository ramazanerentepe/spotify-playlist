# 🎵 Context-Aware Weekly Playlist Generator (Spotify x Last.fm)

> **"Spotify algoritmalarının yankı odasından çıkın, API sınırlarını zekice aşın. Kendi müzik zevkinizin patronu olun."**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Local_Vault-lightgrey?style=flat&logo=sqlite)
![Spotify API](https://img.shields.io/badge/Spotify_API-Data_Source-1ED760?style=flat&logo=spotify)
![Last.fm API](https://img.shields.io/badge/Last.fm_API-Mood_Enrichment-d51007?style=flat&logo=last.fm)
![Security](https://img.shields.io/badge/Security-PKCE_Flow-red?style=flat&logo=security)

## 🚀 Projenin Vizyonu

Spotify'ın size sürekli aynı 50 şarkıyı önermesinden sıkılmadınız mı? Üstelik Spotify'ın yakın zamanda geliştiricilere şarkı ruh hali (`audio-features`) verilerini kapatmasıyla standart tavsiye algoritmaları da tıkandı.

**Biz duvarlara takılmayız, etrafından dolaşırız.** Bu proje; Spotify'ın API kısıtlamalarını **Last.fm'in devasa insan odaklı veri tabanıyla (Data Enrichment)** aşan kişisel bir yapay zeka DJ'idir. Sizi arka planda sessizce dinler, dinlediğiniz şarkıların hissini gerçek insanların girdiği etiketlerle (tag) analiz eder ve her hafta size nokta atışı, bağlam odaklı (context-aware) yeni bir çalma listesi sunar.

## ✨ Temel Özellikler (Mühendislik & Deneyim)

- 🏷️ **Organik Ruh Hali Analizi (Data Enrichment):** Şarkılarınızı ruhsuz, kapalı kutu algoritmalarla değil; milyonlarca insanın girdiği _"melankolik", "gece sürüşü", "yüksek enerji"_ gibi gerçek Last.fm etiketleriyle analiz ederiz.
- 🧠 **Haftalık Hafıza Kaybı (Ephemeral Data Strategy):** Algoritmalar geçmişinize pranga vurur. Bizim motorumuz ise her hafta sonu yerel SQLite hafızasını tamamen siler. Geçmiş önyargısını (bias) yok ederek %100 _o anki_ ruh halinize odaklanır.
- ♻️ **Zen Kütüphane (Single-Playlist Strategy):** Her hafta yeni liste oluşturup kütüphanenizi çöplüğe çevirmez. Belirlenen tek bir "Haftalık Modum" listesinin içeriği her hafta otonom olarak temizlenir ve güncellenir.
- 🛡️ **Görünmez Güvenlik (Stateless PKCE Auth):** Uygulama hiçbir şekilde statik bir `Client Secret` barındırmaz. İstemci tarafında maksimum güvenlik sağlar ve rahatça paylaşılabilir.

## 🏗️ Kaputun Altında Ne Var? (Mikroservis Mimarisi)

Proje, "Tek Sorumluluk Prensibi" (SOLID) merkeze alınarak modüler bir yapıda tasarlanmıştır:

- `database.py`: Kendi kendini kuran, şema doğrulamalı yerel veri bankamız.
- `spotify_api.py`: PKCE yetkilendirmesini ve Spotify üzerindeki CRUD işlemlerini yöneten **1. İstihbarat Ajanımız.**
- `lastfm_api.py`: Şarkı ve sanatçı bazlı etiket verilerini çekerek Spotify verilerini zenginleştiren **2. İstihbarat Ajanımız.**
- `algorithm.py`: Veritabanındaki dinleme frekanslarını ve Last.fm etiketlerini ağırlıklandırarak (weighting) haftalık öneri setini hesaplayan **Matematiksel Beyin.**
- `main.py`: Tüm modülleri ve zamanlanmış görevleri asenkron yöneten ana orkestratör.

## 🚀 Hızlı Başlangıç

1. Projeyi klonlayın ve motoru indirin:
   ```bash
   pip install spotipy python-dotenv requests
   ```
