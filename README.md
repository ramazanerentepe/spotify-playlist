# 🎵 Spotify Weekly Mood & Dynamic Playlist Generator

> **Kullanıcının haftalık Spotify dinleme geçmişini analiz ederek dinamik çalma listeleri oluşturan, ruh hali raporu sunan ve çoklu cihaz senkronizasyonu sağlayan Python tabanlı yerel otomasyon aracı.**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Local_DB-lightgrey?style=flat&logo=sqlite)
![Spotify API](https://img.shields.io/badge/Spotify_API-Integrated-1ED760?style=flat&logo=spotify)

## 📌 Projenin Amacı
Bu proje, standart Spotify algoritmalarının dışına çıkarak kendi dinleme verilerinizle, o haftaki müzikal karakterinize en uygun listeleri üretmenizi sağlar. Proje tamamen kullanıcının kendi bilgisayarında (lokal) çalışır. Arka planda dinleme geçmişinizi biriktirir ve her hafta o anki ruh halinize uygun yepyeni bir "Benzer Şarkılar" listesi oluşturur.

## ✨ Öne Çıkan Özellikler
* **📱 Çoklu Cihaz Senkronizasyonu (Catch-up):** Müzik sadece bilgisayarda dinlenmez! Program bilgisayarda kapalıyken (örneğin telefonda müzik dinlerken) veriler kaybolmaz. Uygulama açıldığında veritabanındaki son kayıt tarihini kontrol eder ve aradaki tüm dinleme geçmişini Spotify'dan çekerek eksiksiz senkronizasyon sağlar.
* **🪶 Ultra Hafif Arka Plan Takibi:** Sistem kaynaklarını (CPU/RAM) tüketmemek için asenkron bir iş parçacığı (Thread) kullanır. Belirli aralıklarla uyanıp sessizce verileri günceller ve uyku moduna döner.
* **🧠 Haftalık Ruh Hali Analizi (Mood Tracking):** Spotify Audio Features API kullanılarak o hafta dinlenen şarkıların enerji, akustiklik ve tempo gibi değerleri analiz edilir ve haftanın "Ruh Hali" belirlenir.
* **🎛️ Dinamik Çalma Listesi:** Sabit limitler yoktur. O hafta müzik dinleme yoğunluğunuza göre özel boyutta bir liste üretilir ve her hafta aynı isimli liste otomatik güncellenir.
* **🧹 Otomatik Veri Temizliği:** Veriler yerel bir SQLite veritabanında tutulur. Sistem, zaman bazlı SQL sorguları kullanarak üzerinden 7 gün geçmiş eski kayıtları kalıcı olarak siler ve depolama optimizasyonu sağlar.

## 🏗️ Proje Mimarisi (SOLID Prensipleri)
Proje, "Tek Sorumluluk Prensibi" (Single Responsibility Principle) merkeze alınarak modüler bir yapıda tasarlanmıştır:

* `database.py`: Yalnızca SQLite işlemleri, veri ekleme, son dinleme tarihini bulma ve 7 günlük veri temizliği.
* `spotify_api.py`: Yalnızca Spotify OAuth2 süreçleri, API istekleri ve Catch-up (arayı kapatma) veri çekimi.
* `algorithm.py`: Verileri işleme, ruh hali (mood) hesaplama ve öneri seçme mantığı.
* `main.py` & `gui.py`: Arayüzü başlatan, arka plan dinleme iş parçacığını (thread) yöneten ve tüm modülleri koordine eden ana yapı.

## 🚀 Kurulum & Kullanım
*(Bu bölüm, proje tamamlandığında API anahtarlarının nasıl ekleneceği ve programın nasıl çalıştırılacağı ile ilgili adımlarla doldurulacaktır.)*
