# 👨‍🦯 Akıllı Baston – Görme Engelliler İçin Akıllı Yardımcı

Bu proje, görme engelli bireylerin günlük yaşamlarında daha güvenli ve bağımsız hareket etmelerini sağlamak amacıyla geliştirilmiş bir **akıllı baston sistemidir**. Raspberry Pi tabanlı bu cihaz, çevredeki engelleri algılayarak kullanıcıyı sesli uyarılarla bilgilendirir.

## 🚀 Proje Özeti

- **Amaç:** Görme engellilere yönelik, çevredeki nesneleri algılayan ve kullanıcıyı uyaran taşınabilir bir sistem geliştirmek.
- **Platform:** Raspberry Pi
- **Kullanılan Teknolojiler:** Python, OpenCV, Ultrasonik Sensör (HC-SR04), Buzzer
- **Çıktı:** Sesli uyarılarla engel bilgisi iletimi

## 🧠 Proje Özellikleri

- 🚧 **Engel Algılama:** HC-SR04 sensörü ile 0.5 - 2 metre arasındaki engeller tespit edilir.
- 🔊 **Sesli Uyarı Sistemi:** Engel mesafesine göre farklı sesli uyarılar gönderilir.
- 📷 **Görüntü İşleme (Opsiyonel):** Kameradan alınan görüntüler işlenerek nesne tanıma yapılabilir.
- 🔋 **Taşınabilirlik:** Pil ile çalışabilen ve kolay taşınabilir bir tasarım.

## 🛠️ Donanım Gereksinimleri

- Raspberry Pi 4 / 5 (önerilen)
- HC-SR04 Ultrasonik Mesafe Sensörü
- Buzzer
- Kamera Modülü (isteğe bağlı)
- Powerbank veya pil paketi
- USB Mikrofon / Hoparlör (isteğe bağlı sesli yönlendirme için)

## 💻 Yazılım Gereksinimleri

- Python 3.x
- OpenCV
- GPIO kütüphaneleri (`RPi.GPIO` veya `gpiozero`)
- `pygame` veya `espeak` gibi sesli çıktı kütüphaneleri

## 🔧 Kurulum ve Çalıştırma

1. Raspberry Pi'yi başlatın ve Python ortamınızı kurun:
   ```bash
   sudo apt update
   sudo apt install python3-opencv python3-pip espeak
   pip3 install RPi.GPIO pygame
