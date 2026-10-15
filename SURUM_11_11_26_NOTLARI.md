# v11.11.26 — Teknik metni kaldırma ve bellek yükünü sınırlama

## Tespit ve sınır

Ekrandaki tekrarlanan LoggerNet açıklaması, v11.11.24'te okuyucu açıklamasının `with` bloğuna taşınmasından kaynaklanıyordu. Streamlit magic bunu açıklama yerine kullanıcıya gösterilecek metin olarak çalıştırıyor, `cache_data` tekrar okumada aynı çıktıyı yeniden oynatıyordu. Eski sürümle gerçek AppTest bu hata davranışını yeniden üretti. Yeni sürüm açıklamayı gerçek fonksiyon docstring'i olarak tutuyor; ilk ve tekrar okumada teknik metin basılmıyor. Kaynak dosyada başka beklenmeyen bağımsız string ifadeleri de kontrol edildi.

Kullanıcının canlı Community Cloud sürecinin neden kapandığına ilişkin hata/OOM kaydı bu ortamda yoktur. Önceki ve bu sürümdeki yerel testler, canlı sunucunun kesintisiz çalıştığına dair kanıt değildir. Bu sürüm, kodda doğrulanan büyük bellek tahsislerini ve önbellek birikimini azaltır; dış servis, sunucu limiti veya başka hatalar nedeniyle hiçbir kesinti olmayacağı garantisi vermez.

## Yapılanlar

- Çözülmüş ölçüm tabloları artık dosya adedine göre RAM'de biriken iki cache_data katmanında tutulmuyor. İçeriğin SHA256 imzasına göre, uygulamanın özel .maki_runtime/parsed_wind_v1 klasöründe toplam 256 MiB sınırla saklanıyor. Aynı ölçüm her çağrıda ayrı DataFrame olarak döner; bir tarayıcının değişikliği diğerinin ham ölçümünü değiştirmez. Eski önbellek dosyaları önce çıkarılır; kaynak ölçüm dosyaları silinmez. Bozuk cache yeniden oluşturulur. Cache diski kullanılamazsa okunabilir ölçüm normal okuyucudan döner.
- GWA HTTP yanıtı 1 MiB parçalarla diske indirilir. JSON/URL yanıtları en fazla 1 MiB metin olarak incelenir. ZIP/GZIP diske parça parça çıkarılır. Ağ indirmesi 512 MiB, arşivden çıkarılan raster 1 GiB disk sınırına tabidir; bunlar veri kalite kuralları değil sunucuyu koruyan kaynak sınırlarıdır. TLS doğrulaması kapatılmadı.
- Ülke raster cache'i bütün dosyayı bytes olarak RAM'e yüklemeden dosya yolu döndürür. Okuyucu bu yolu veya eski bytes girdisini kabul eder.
- GeoTIFF örneklemesi rasterın tamamına `page.asarray()` uygulamaz. İstenen piksel koordinatlarının bulunduğu tile/strip parçalarını okur ve sırayla çözer. Tek bantlı 2B raster gereklidir. Çözülmüş tek parça veya sıkıştırılmış parça 16 MiB'ı aşıyorsa açılmadan açıklamalı hata verir; daha küçük tile/strip içeren saha rasterı gerekir. Küçük parça sınırı, özellikle float predictor'ın geçici dizilerini de sınırlamayı amaçlar.
- Aynı girdilerle üretilen küçük saha gridi en fazla altı kayıt ve on dakika süreyle önbelleğe alınır. Harita görüntüsünü tekrar çalıştırmak gereksiz ülke indirmesi ve raster çözümü başlatmaz. Girdiler değiştiğinde anahtar da değişir.
- İptal edilmiş HTTP yükleme servisi için eklenen st.App girişine artık ihtiyaç olmadığından maki_server.py standart Streamlit çalıştırma girişine döndürüldü. Buluttaki giriş dosyası adı aynı kaldı; yeni uygulama kurulması gerekmez. Windows arka plan yardımcısı geri getirilmedi.

## Test sonuçları

- Gerçek AppTest: eski sürümde teknik metin sızıntısı yeniden üretildi; yeni sürümde ilk ve tekrar okumada yok.
- Disk önbelleği: çağrılar bağımsız tablo döndürür; bozuk cache onarılır, yarım dosya yayımlanmaz.
- TIFF: tiled/stripped ve sıkıştırılmamış/deflate örneklerde piksel değerleri birebir aynı. Test sırasında tam sayfa açma metodu hata verecek şekilde yasaklandı; örnekleme yine geçti. Yalnızca istenen piksellere ait segmentler okundu.
- 16.384 × 16.384 float32, açıldığında 1 GiB olan sentetik raster: üç nokta doğru örneklendi; ayrı test sürecinde tepe RSS yaklaşık 75,9 MiB oldu. Bu sayı bütün Streamlit sunucusunun, iki tarayıcının veya canlı GWA verisinin toplam belleği değildir.
- Büyük tek strip açılmadan reddedildi. Tam uygulama testi, kontrollü raster kaynak hatasında sınırın gösterilmeye devam ettiğini, açıklamalı hata verildiğini ve diğer sayfaya geçilebildiğini doğruladı.
- ZIP/GZIP çıkarma birebir dosya eşitliği verdi. Sahte HTTP yanıtlarıyla sınırlı okuma, JSON indirme bağlantısı takibi, boyut reddi ve geçici dosya temizliği geçti; gerçek GWA ağ erişimi denenmedi.
- Gerçek LoggerNet dosyası: 115.088 kayıt için önceki okuyucuyla birebir eşitlik; 36 CSV varyantı geçti. Doğrudan okuyucu karşılaştırma sürecinde tepe RSS yaklaşık 655,8 → 257,7 MiB oldu; bu ölçüm disk cache'in sıcak okuması değil ayrıştırıcının soğuk çalışmasıdır.
- Gerçek Chromium ile kaynak ve bağımsız görüntüleyici oturumu: 27.781.322 bayt LoggerNet dosyası birebir aktarıldı; güncelleme, yenileme ve proje yalıtımı geçti.
- Harita hizalama, merkez sıfırlama, ortak proje, enerji ve doğrudan sayfa geçişi kontrolleri geçti. Yerel sunucu sağlık ve script sağlık uçları 200/ok döndürdü.

Ölçüm temizleme kuralları, yükseklik ve enerji formülleri değiştirilmedi. Sensör/yükseklik/arıza/ilişki katsayısı başka direğe sabitlenmedi. Tahminler gerçek temiz ölçüme dönüştürülmedi. Gerçek GWA rasterlarının bağımsız doğruluğu, predictor doğrulaması, Windographer eşdeğerliği, tamamlama enerjisinin bağımsız doğrulaması, nihai AEP ve gerçek P50/P75/P90 açık kalır. Windows görsel doğrulaması ve canlı bulut kararlılığı bu ortamdan doğrulanamadı.

## Çalıştırma

Bulutta mevcut giriş dosyası: `maki_server.py`. Kullanıcının yerel kurulum yapması gerekmez.

Mevcut Windows Python 3.14 ile isteğe bağlı çalıştırma:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.26_KARARLILIK_VE_TEMIZ_EKRAN.py
```

Özel kontroller:

```bash
python work_checks/stability26.py
python work_checks/raster26_memory.py
python work_checks/stability26_app.py
MAKI_LARGE_FIXTURE=/path/to/WindData.dat python work_checks/stability24.py
python work_checks/map25.py
python work_checks/map25_integration.py
python work_checks/cloud20.py
python work_checks/energy19.py
python work_checks/navigation19.py
```
