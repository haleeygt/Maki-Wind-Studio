# v11.11.27 — Çalışma merkezinden bağımsız saha renk ölçeği

## Sorun ve düzeltme

İlk harita rüzgâr hücrelerini santral sınırına kırpıyor, fakat renk alt/üst değerlerini bütün turuncu çalışma alanından alıyordu. Çalışma alanını taşımak santral dışındaki düşük/yüksek değerleri bu aralığa ekleyip çıkarabiliyor; aynı saha değerleri daha mavi veya daha sıcak renge dönüşebiliyordu. Ayrıca alt ve üst değeri aynı olan düz bir yüzey, renk fonksiyonunda otomatik olarak en düşük mavi renge düşüyordu.

Renk referansı artık değişmeyen santral poligonu için aynı girdilerle hesaplanan, önbelleğe alınmış 60×60 örnekleme alanından elde edilir. Renk aralığı, turuncu çalışma merkezine ve turuncu alan genişliğine bağlı değildir. Direkler, ölçüm dönemi, temiz ölçümlerden türeyen hub hızları, hedef yükseklik veya santral değişirse referans yeniden hesaplanır. Bu renk referansı santral içindeki geçerli raster noktalarını kullanır; dış noktalar ve direk kalibrasyon kontrol noktaları min/max değerlerine katılmaz.

İlk harita, türbin editörüne gönderilen yüzey ve Plotly harita renk sınırları aynı saha ölçeğini kullanır. Hareketli alanın sayısal grid değerleri değiştirilmez. Gösterimde yapay kontrast yaratmamak için renk çubuğunun genişliği en az 0,5 m/s'dir. Bu bir gösterim tercihidir; ölçülmüş veya hesaplanan hıza ekleme/çıkarma yapılmaz. Tam sabit yüzey, eşit alt/üst değer nedeniyle otomatik olarak maviye düşmez; lejant uygun durumda “Tekdüze saha” yazar. Gerçekte küçük veya olmayan saha farkı yapay bir gökkuşağıyla gösterilmez.

Santral referansı üretilemezse ilk harita çalışma alanından yeni bir ölçek uydurmaz; sınırı gösterip ölçek hatasını açıklar. Renk referansı örneklenmiş bir model aralığıdır, her gerçek saha pikselinin bağımsız doğrulanmış minimum/maksimumu değildir.

## Değişmeyenler

Ölçüm okuyucusu, kalite ve eksik veri kuralları, raster örnekleme, GWA kalibrasyon fonksiyonu ve enerji fonksiyonları v11.11.26 ile aynı kaldı. Harita girdileri değişmediğinde aynı sayısal rüzgâr değerinin aynı renkte gösterilmesi sağlandı; enerjiye veya hızlara görsel amaçla müdahale edilmedi. Çalışma alanı taşındığında farklı koordinatlar yeniden örneklendiği için hareketli gridin düğümleri yine değişebilir; bu sürüm modelin örnekleme yöntemini değiştirmez.

v11.11.26'daki teknik metin düzeltmesi, sınırlı disk önbelleği, parça bazında TIFF okuma ve kaynak korumaları korundu. Windows yardımcısı geri getirilmedi. Bulut giriş dosyası yine maki_server.py'dir.

## Testler

- Eski ölçek fonksiyonuyla, saha dışı değerler değişirken aynı santral değerlerinin farklı renk aralığına düştüğü yeniden üretildi.
- Yeni ölçek dış noktaları ve direk kontrol noktalarını dışladı; kaynak DataFrame ve içindeki sayısal hızlar birebir korundu.
- Gerçek Chromium'da çalışma merkezi değişirken aynı hızın çizilen RGB rengi ve lejant sınırları aynı kaldı. Tekdüze yüzeyin eşit min/max nedeniyle otomatik maviye düşmediği kontrol edildi.
- Tam sayfa AppTest'te dış GWA indirmesi açıkça sentetik GeoTIFF ile değiştirildi. Çalışma merkezi santral dışından santral ortasına taşınınca saha ölçeği, referans metadata ve alt/üst sınırlar birebir aynı kaldı. Sıfırlama da ölçeği değiştirmedi. Teknik LoggerNet açıklaması sayfada görünmedi.
- 390, 960 ve 1400 piksel genişlikte harita kaydırma/yakınlaştırma/boyut değiştirme eşleşmesi, tutamaç davranışı, türbin haritası eşleşmesi ve temel GeoTIFF piksel örneklemesi geçti.
- v11.11.26 teknik metin, disk cache, sınırlı TIFF segment okuması, ZIP/GZIP ve sınırlı HTTP yanıt testleri geçti.
- Enerji ve doğrudan sayfa geçişi kontrolleri geçti. AST karşılaştırması, mevcut üst seviye fonksiyonlardan yalnızca iki harita/görselleştirme fonksiyonunun değiştiğini doğruladı; yeni saha renk referansı fonksiyonu eklendi.

Canlı kullanıcının GWA dosyası ve canlı bulut arayüzü bu ortamdan doğrulanamadı. Gerçek GWA raster doğruluğu/predictor doğrulaması, Windographer eşdeğerliği, bağımsız tamamlama enerjisi, nihai AEP ve gerçek P50/P75/P90 açık kalır. Renklerin tutarlı olması bilimsel doğrulama veya üretim garantisi değildir.

## Çalıştırma

Bulutta mevcut uygulama ve giriş dosyası kullanılmaya devam eder. Kullanıcının yeni yerel kurulum yapması gerekmez.

Mevcut Windows Python 3.14 ile isteğe bağlı çalıştırma:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.27_SABIT_SAHA_RENK_OLCEGI.py
```

Kontroller:

```bash
python work_checks/colors27.py
python work_checks/map25.py
python work_checks/map25_integration.py
python work_checks/stability26.py
python work_checks/energy19.py
python work_checks/navigation19.py
```
