# v11.11.25 — Sabit santral sınırı ve ilk sekmede rüzgâr katmanı

İlk sekmedeki çalışma alanı haritası yalnızca uydu ve sınır çiziyordu; hesaplanan rüzgâr gridi bu bileşene gönderilmiyordu. Uydu döşemeleri gerçek ekran pikselleriyle, sınır ise 960 piksele göre ölçeklenen SVG ile çizildiğinden dar/geniş ekranlarda kaydırma sırasında katmanlar birbirinden kopuyordu. Türbin editöründe de aynı ölçek uyuşmazlığı vardı.

## Sonuç

- Uydu, santral sınırı, rüzgâr hücreleri ve çalışma alanı aynı Web Mercator dönüşümü ve ekran piksel ölçeğiyle çizilir. Ekran boyutu değiştiğinde de bu eşleşme korunur.
- Haritayı normal sürüklemek yalnızca görünümü kaydırır. Santral KML/KMZ koordinatları ve çalışma merkezi değişmez. Turuncu alanın içi normal kaydırmaya açıktır; çalışma alanı yalnızca turuncu kenardan veya merkez tutamacından taşınır.
- İlk Rüzgâr Haritası sekmesinde mevcut hesaplanan hub rüzgâr gridi renkli hücreler ve m/s lejantıyla görünür. Hücreler santral sınırına kırpılır. Görünüm model önizlemesidir.
- Eksik/sonsuz grid değerleri renklendirilmez, görsel boşluklar uydurularak doldurulmaz. Direk kalibrasyon kontrol noktaları ayrı raster satır/sütunları olarak yüzeye eklenmez. Bu ayrım hesaplanan grid veya enerji sonuçlarını değiştirmez.
- Çalışma alanı taşınırken eski rüzgâr katmanı kaldırılır; yeni alanın hesabı geldiğinde güncellenir. Hareket olayları bir kez tüketilir; sıfırlama düğmesi eski olayı yeniden uygulamaz.
- Grid üretilemediğinde hata veya eksik girdi açıklaması ilk haritanın üstünde görünür. GWA okuması için gereken `tifffile==2026.9.20` bağımlılığı requirements.txt dosyasına eklendi.
- Haritaların üretilen HTML dosyaları uygulamanın .maki_runtime klasöründe tutulur. Bu klasör ölçüm dosyalarından ayrıdır ve Git deposuna gönderilmez.

## Değişmeyen bilimsel hesaplar

Ölçüm okuyucusu, kalite kuralları, ham/temiz/tahmini ayrımı, GWA örnekleme ve kalibrasyon hesabı, enerji fonksiyonları ve eksik dönemde yıllık sonuç sınırlamaları değiştirilmedi. Sensör yüksekliği, direk adı, arıza tarihi veya kalibrasyon katsayısı sabitlenmedi.

## Doğrulama

- Playwright/Chromium: 390, 960 ve 1400 piksel genişlikte uydu döşemeleri ile sınır koordinatları; kaydırma, fare tekerleğiyle yakınlaştırma ve pencere boyutu değişiminden sonra eşleşti. Testte referans uydu döşemesi pikseliyle vektör dönüşümü arasındaki fark 0,05 pikselden küçüktü.
- Normal kaydırmada çalışma merkezi ve KML koordinatları değişmedi. Tutamaç sürüklemesinde yalnızca çalışma merkezi için olay gönderildi; eski rüzgâr yüzeyi kaldırıldı.
- Türbin editöründeki katman eşleşmesi de kaydırma/yakınlaştırma/boyut değişiminde doğrulandı; türbin koordinatları korunuyor.
- Eksik hücrelerin eksik kalması, kontrol noktalarının raster yüzeyine karışmaması ve girdi tablosunun değiştirilmemesi kontrol edildi.
- Tam sayfa AppTest: dış GWA indirmesi açıkça sentetik GeoTIFF ile değiştirildi; gerçek uygulama hesabının ürettiği grid ve değişmemiş KML ilk harita bileşenine ulaştı. Sürükleme olayının bir kez işlenmesi ve sıfırlamanın sonraki çalışmada korunması geçti.
- Kurulan TIFF okuyucusu bilinen EPSG:4326 sentetik rasterın piksel merkezlerini doğru örnekledi. Bu, gerçek GWA rasterlarının bağımsız doğrulaması değildir.
- Ortak proje, enerji ve doğrudan sayfa geçişi regresyon kontrolleri geçti. AST karşılaştırmasında değişen üst seviye fonksiyonlar yalnızca üç harita/görselleştirme fonksiyonuydu.

Harita testinde dış uydu istekleri engellenmiştir; test koordinatların ve katmanların hizasını doğrular, canlı uydu servisinin erişilebilirliğini değil. Canlı Streamlit dağıtımı, kullanıcının gerçek proje GWA verisi ve Windows görsel doğrulaması bu ortamdan doğrulanamadı. Windographer eşdeğerliği, bağımsız tamamlama enerjisi, nihai AEP, gerçek P50/P75/P90 ve gerçek GWA raster doğruluğu açık kalır. GWA verisi indirilemez veya kalite kontrolü geçmezse renkli harita uydurulmaz; gerekçesi gösterilir.

## Çalıştırma

Bulut giriş dosyası değişmedi: `maki_server.py`. Bulut kullanımı için Windows komutu çalıştırılması gerekmez.

Mevcut Python 3.14 ile isteğe bağlı yerel çalıştırma:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.25_SABIT_SINIR_RUZGAR_HARITASI.py
```

Testler:

```bash
python work_checks/map25.py
python work_checks/map25_integration.py
python work_checks/cloud20.py
python work_checks/energy19.py
python work_checks/navigation19.py
```
