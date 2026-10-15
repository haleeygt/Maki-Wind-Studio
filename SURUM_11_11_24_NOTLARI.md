# v11.11.24 — Bellek kullanımını azaltma

Kullanıcı, bulut uygulamasındaki genel “Oh no. Error running app” ekranından sonra reboot ile tekrar erişim sağlayabildiğini bildirdi. Canlı sunucu günlükleri alınamadığı için kesintinin kesin nedeni belirlenmedi. Bu düzeltme, gerçek LoggerNet dosyasıyla yerelde ölçülen yüksek dosya okuma belleğini azaltır; bulut kesintilerinin tamamının çözüldüğü anlamına gelmez.

## Değişiklikler

- Okuyucu yalnızca başlık için gereken ilk 12 satırı metin listesinde tutar; tüm dosyanın satır listesini oluşturmaz.
- CSV okuyucusu aynı Python ayrıştırıcısıyla 4096 kayıtlık parçalar okur. Sayı sütunları her parçada dönüştürülür; zaman sütunu öncekiyle aynı toplu normalizasyondan geçer. Kanal, yükseklik, arıza dönemi, ilişki katsayısı veya direk adına özel kural eklenmedi.
- Farklı soğuk dosya okumalarının geçici bellek kullanımları, oturumlar arasında ortak okuma kilidiyle üst üste bindirilmez. Okunan ölçüm tabloları yine ayrı kalır; sonuçlar oturumlar arasında değiştirilmez.
- Dosya yolundan okuma sonucunun hem yol hem bytes önbelleğinde iki kez saklanması kaldırıldı. Aktarım doğrulaması da ayrı bir kalıcı ölçüm tablosu önbelleği oluşturmaz.
- Tarayıcıdan tamamlanan aktarım, sunucuda tüm dosyayı tekrar base64 olarak büyütmeden aynı boyut, SHA256, son satır ve LoggerNet okuyucu kontrollerinden geçirilir. Dosyanın tamamı doğrulanmadan çalışma verisi değiştirilmez.
- Windows yardımcısı ve arka plan servisi iptal edilmiş olarak kalır. Aktif giriş dosyası yine `maki_server.py`; yeni dağıtım oluşturulması gerekmez.

## Ölçüm ve testler

Linux'ta ayrı Python süreçlerinde, 27.781.322 baytlık gerçek LoggerNet örneğiyle yapılan karşılaştırmada tepe RSS yaklaşık 655,7 MiB → 260,4 MiB oldu (%60 azalma). Bu yalnızca dosya okuyucusu testinin süreç belleğidir; bütün Streamlit sunucusunun veya canlı Community Cloud'un toplam belleği değildir. Dosyanın 115.088 kaydı için tüm değerler, veri tipleri, zamanlar ve okuyucu metadata sonucu eşdeğer kaldı. İlk bağımsız ölçümde eski okuyucu yaklaşık 682,6 MiB gördü; süreç tabanı ve çalışma koşulları nedeniyle ölçümler farklılaşabilir.

36 CSV varyantında virgül/noktalı virgül/sekme, LF/CRLF, BOM, TIMESTAMP/DateTime adları, bozuk zaman/sayı ve parça sınırlarının iki yanındaki kayıtlar önceki okuyucuyla kesin değer ve dtype eşitliği verdi. Bu testler her olası CSV şemasının doğrulanması anlamına gelmez.

Gerçek Chromium ile iki bağımsız tarayıcı oturumunda büyük dosya aktarımı, SHA256 eşitliği, otomatik güncelleme, yenileme ve proje yalıtımı geçti. Kaynak klasör seçici testte yerel OPFS klasörüyle taklit edildi; Windows'un gerçek izin penceresi denenmedi. Ayrı iş parçacıklarındaki soğuk okumaların aynı anda ayrıştırıcıya girmediği doğrulandı. Mevcut ortak proje, veri kalitesi, enerji ve onaysız sayfa geçiş testleri geçti. Eksik kayıtlarda yıllık sonuç baskılama ve ham/temiz ayrımı korunuyor.

Canlı bulut kesintisinin kesin nedeni, Windows görsel doğrulaması, Windographer eşdeğerliği, bağımsız tamamlama enerjisi doğrulaması, nihai AEP, gerçek P50/P75/P90 ve GWA raster doğruluğu açık kalıyor.

## Çalıştırma

Bulut giriş dosyası: `maki_server.py`. Mevcut Python 3.14 ile yerel çalıştırma:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.24_BELLEK_KULLANIMI_IYILESTIRMESI.py
```

Bulut kullanıcısının bu komutu çalıştırması gerekmez.

Tekrarlanabilir kontroller:

```bash
MAKI_LARGE_FIXTURE=/path/to/WindData.dat python work_checks/stability24.py
python work_checks/concurrent_reader24.py
python work_checks/cloud20.py
python work_checks/energy19.py
python work_checks/navigation19.py
MAKI_TEST_URL=http://127.0.0.1:8515 MAKI_LARGE_FIXTURE=/path/to/WindData.dat python work_checks/browser20_playwright.py
```
