# v11.11.28 — Turuncu çalışma karesinde rüzgâr haritası

Rüzgâr renk katmanı artık santral poligonuna değil, turuncu çalışma karesinin tamamına kırpılır. Kare kenarı veya orta tutamaç taşınıp bırakılınca yeni koordinatlardaki grid yeniden hesaplanır. Kırmızı santral sınırı coğrafi yerinde kalır. Haritanın boş zeminini sürüklemek yalnızca kamerayı taşır.

Çizilen kare ve kırpma alanı, Python hesabında kullanılan aynı köşe koordinatlarından üretilir; farklı km/derece yaklaşımı kaldırıldı. En dış renk hücreleri çalışma sınırında biter, iç hücre sınırları örnekleme noktalarının orta çizgisidir. Bu hücre gösterimi yeni hız değeri üretmez. Eksik hücreler boş kalır. Taşıma sırasında önceki bölgenin renk katmanı kaldırılır ve hesaplanan yeni grid geldiğinde çizilir. İptal edilen taşıma eski alanı ve katmanı geri getirir.

v11.11.27 sabit renk referansı korunur; aynı hız kare taşınınca farklı renge dönüşmez. Referans dışındaki hızlar renk çubuğunun uç renklerinde gösterilir; renk çubuğu bütün çalışma alanının min/max değeri değildir. Sayısal model, kalibrasyon, ölçüm temizliği ve enerji hesap fonksiyonları değiştirilmedi. Türbin adaylarının santral sınırı denetimi korunur.

## Doğrulama

- Chromium: 390/960/1400 pikselde uydu/vektör eşleşmesi; kaydırma, yakınlaştırma, boyut değişimi; renk katmanı ve kırpma alanı kareyle tam örtüşür. Tutamaç taşıma yalnızca çalışma alanını değiştirir ve eski katmanı kaldırır. Türbin editörü ve temel GeoTIFF örnekleme testleri geçti.
- Tam sayfa Streamlit AppTest: dış indirme yerine açıkça sentetik coğrafi TIFF kullanıldı. Kare santralden tamamen uzaklaştırıldığında yeni koordinatlarda farklı rüzgâr değerleri hesaplandı; kırmızı sınır ve sabit renk ölçeği değişmedi. Sıfırlama ve tek seferlik hareket olayı kontrolleri geçti.
- Aynı hızın tarayıcıda aynı RGB rengiyle gösterilmesi, tekdüze yüzey ve eksik hücre kontrolleri geçti.
- Enerji regresyon testleri: geçerli temiz kayıtlar, manuel işaretlerin dışlanması, eksik dönem nedeniyle yıllık sonucun bastırılması, mükerrer zaman ve eksik shear korumaları geçti.
- AST karşılaştırması: önceki sürümdeki üst seviye fonksiyonlardan yalnızca çalışma haritası bileşeni değişti.

Linux geliştirme ortamında doğrulandı. Canlı Streamlit dağıtımının tamamlanması ve kullanıcının gerçek GWA dosyası bu ortamdan doğrulanamadı. Windows Python 3.14 görsel kontrolü, gerçek GWA raster doğruluğu, Windographer temiz veri eşdeğerliği, bağımsız tamamlama enerjisi, nihai AEP ve gerçek P50/P75/P90 doğrulamaları açık kalır.

## Çalıştırma

Bulutta mevcut giriş dosyası `maki_server.py` yeni sürüme yönlenir. Yerel kurulum veya komut gerekmez; dağıtım tamamlandığında mevcut sekmeyi yenileyin. Sürüm Ana Sayfa'da v11.11.28 olarak görünür.

İsteğe bağlı mevcut Windows Python 3.14 komutu:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.28_CALISMA_KARESINDE_RUZGAR_HARITASI.py
```

Tekrarlanabilir kontroller:

```bash
python work_checks/map25.py
python work_checks/map25_integration.py
python work_checks/colors27.py
python work_checks/energy19.py
```
