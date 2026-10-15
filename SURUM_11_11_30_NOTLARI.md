# v11.11.30 — Yeniden çalıştırmalarda bellek temizliği

Tam uygulama ve uzun veriyle test, v11.11.29'daki dar dosya okuma ölçümünün yakalayamadığı ek bellek yükünü gösterdi. Beş dosya kaydı ve tekrar eden harita hareketleriyle önceki süreç yaklaşık 2,4 GiB RSS'ye ulaştı. Kayıtlar aynı gerçek örnek dosyaya işaret eder; bunlar kullanıcının beş ayrı gerçek direği değildir. Dış GWA indirmesi açıkça sentetik GeoTIFF ile değiştirilmiştir. Bu yerel sonuç canlı buluttaki kapanmanın kesin kök nedeni olarak sunulmaz.

Yeni sürüm, ağır dosya akışı başlamadan önce ve normal sayfa çalışması bittikten sonra Python'un erişilemez döngüsel nesneleri toplamasını açıkça çalıştırır (`gc.collect(2)`). Pandas/NumPy nesneleri büyük tamponlar taşıyabildiğinden, Python nesne sayısına dayanan otomatik toplama eşiğini beklemek yeniden çalıştırmalarda fazla RAM birikimine yol açabilir. Erişilebilir oturum verileri, kalite işaretleri ve hesap sonuçları silinmez. Matematiksel model, ölçüm temizliği, GWA kalibrasyonu, enerji ve harita fonksiyonları değiştirilmedi.

## Doğrulama ve sınırlar

- Aynı tam sayfa AppTest yükünde 15 art arda harita hareketi tamamlandı. Önceki sürümde RSS yaklaşık 1998–2484 MiB, yeni sürümde yaklaşık 714–826 MiB oldu; yeni testin süreç tepe RSS'si 849,1 MiB idi. Bölge değişimi, sabit santral sınırı, sabit renk referansı ve sıfırlama kontrolleri geçti.
- Gerçek Streamlit sunucusunda iki ayrı Chromium bağlamı aynı anda açıldı; her oturumda beş uzun dosya kaydı vardı. İki oturumda toplam 16 gerçek tutamaç hareketi, yeni rüzgâr katmanı ve Python hata kutusu bulunmaması kontrol edildi. Dış raster sentetik, uydu tile istekleri engellenmişti. Hareketlerden sonra sunucu RSS ölçümleri 1037–1357 MiB arasında değişti. Bu, 1 GiB gibi düşük bir barındırma sınırında iki ağır oturum için yeterlilik garantisi vermez. Canlı barındırma kotası bu ortamdan görülemiyor.
- Enerji regresyonları geçti: temiz/geçerli kayıtlar, manuel kalite işaretleri, eksik dönem nedeniyle yıllık sonucun bastırılması, mükerrer zaman ve shear korumaları.
- Python derleme ve git boşluk kontrolleri geçti.
- Linux geliştirme ortamında doğrulandı. Windows Python 3.14 görsel kontrolü ve canlı Streamlit dağıtımı doğrulanmadı.

Kullanıcının paylaştığı bulut günlüklerinde kesin hata izi yoktu; görünen kullanımdan kaldırma uyarıları çökme nedeni sayılmaz. Bu sürüm, ölçülebilen yeniden çalıştırma bellek yükünü azaltır; her koşulda veya her bulut kotasında çöküşün imkânsız olduğunu iddia etmez. Gerçek GWA raster doğruluğu, Windographer eşdeğerliği, bağımsız tamamlama enerjisi, nihai AEP ve gerçek P50/P75/P90 doğrulamaları açık kalır.

## Windows Python 3.14 ile VS Code'da çalıştırma

Tam dosya: `appv11.11.30_YENIDEN_CALISMA_BELLEK_KORUMASI.py`. Uyumluluk yönlendirme dosyası değil, uygulamanın tam kaynak kodudur. Mevcut proje klasörüne kaydedin ve o klasörde VS Code Terminal menüsünden terminali açın:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.30_YENIDEN_CALISMA_BELLEK_KORUMASI.py
```

Bu komut mevcut Python/Streamlit kurulumunu kullanır. Çalışmakta olan eski sürümü aynı terminalde Ctrl+C ile durdurduktan sonra komutu kullanabilirsiniz.

Bulut girişi `maki_server.py` yeni sürüme yönlenir; canlı dağıtımın tamamlandığı doğrulanmadı.

Uzun dosya testi:

```bash
MAKI_LARGE_FIXTURE=/path/to/example.dat python work_checks/repeated_map30.py
python work_checks/energy19.py
```
