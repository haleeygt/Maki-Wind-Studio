# v11.11.31 — Türbin haritasındaki uzun rüzgâr şeridi

Manuel/Excel türbin yerleşimi ekranında düzenli raster noktalarıyla direk kalibrasyon kontrol noktaları aynı renk matrisine giriyordu. Çizici bütün hücrelerin genişlik/yüksekliğini ilk iki koordinatın farkından alıyordu. Uzak bir kontrol noktası, hem haritanın görünüm aralığını büyütebiliyor hem de hücreleri yüzlerce kilometrelik ince şeritlere çevirebiliyordu.

## Düzeltme

- Renk katmanı hazırlığında `Nokta Türü` varsa yalnızca `Raster grid` satırları kullanılır. Kontrol noktaları kaynak gridde ve hesaplarda kalır; renk yüzeyinin satır/sütun eksenlerine eklenmez.
- Manuel türbin editörü boşlukları koruyan katmanı kullanır. Boş, NaN ve sonsuz hücreler çizilmez; JavaScript null değerini sıfır rüzgâra dönüştürmez. Bu ekrandaki görsel boşluk doldurma kaldırıldı.
- Her hücrenin sınırı kendi komşu koordinatlarının orta çizgilerinden hesaplanır. Bütün hücrelere ilk koordinat aralığı uygulanmaz. Zoom seviyesine göre en az bir piksel genişliği veya hücrelerin üst üste binmesini zorlayan ek boyut uygulanmaz.
- Santral sınırı, türbin konumları, mevcut sürükleme/ekleme davranışı ve sabit renk ölçeği korunur. SVG'nin mevcut 1000×570 koordinat sistemi değiştirilmedi.
- v11.11.30 bellek temizliği korunur. Okuma, kalite, GWA kalibrasyonu ve enerji fonksiyonları değiştirilmedi. Katman için filtrelenen DataFrame kaynak tabloyu değiştirmez.

## Doğrulama

- Eski manuel akışın şeritleşmesi sentetik veride yeniden üretildi: 0,01 derecelik düzenli grid ve uzak kontrol noktası, eski çizicide 3 derece yüksekliğinde ve yaklaşık 0,0001 derece genişliğinde hücreye neden oldu.
- Yeni katman yalnızca gerçek raster eksenlerini aldı; kaynak DataFrame birebir aynı kaldı ve eksik hücre boş korundu.
- Gerçek Chromium'da 390, 960 ve 1400 piksel genişlikte katman kapsamı, eksik hücre, kaydırma/yakınlaştırma, yeniden boyutlandırma, türbin sürükleme koordinatları ve düzensiz koordinat aralıklarının hücre sınırları geçti.
- Tam Streamlit AppTest'te dış raster indirmesi açıkça sentetik coğrafi TIFF ile değiştirildi. Çalışma karesi dışındaki direk kontrol noktası manuel editörün renk matrisine ve görünüm sınırlarına eklenmedi. Kare taşıma, sabit renk referansı/santral sınırı ve sıfırlama da geçti.
- Önceki harita eşleşmesi, türbin haritası eşleşmesi ve temel TIFF örnekleme kontrolleri geçti. Sabit renk ölçeği testleri geçti.
- Enerji regresyonları geçti: geçerli temiz ölçümler, manuel işaretler, eksik dönem nedeniyle yıllık sonucun bastırılması, mükerrer zaman ve shear korumaları.
- Python derleme ve git boşluk kontrolleri geçti. AST karşılaştırmasında mevcut hesap fonksiyonları aynı kaldı; değişen mevcut fonksiyonlar iki görselleştirme işlevi ve sürüm etiketini taşıyan günlük işlevidir.

Linux geliştirme ortamında test edildi. Kullanıcının yerel Windows/Python 3.14 ekranı bu ortamdan görülüp doğrulanmadı. Önceki bilimsel doğrulama sınırları sürer: gerçek GWA raster doğruluğu, Windographer temiz veri eşdeğerliği, bağımsız tamamlama enerjisi, nihai AEP ve gerçek P50/P75/P90 tamamlanmış sayılmaz. Bu harita düzeltmesi buluttaki genel kapanma sorununun çözüldüğü iddiasını taşımaz.

## VS Code'da mevcut kurulumla çalıştırma

Tam kaynak dosyayı mevcut uygulama klasörüne kaydedin:
`appv11.11.31_TURBIN_RUZGAR_KATMANI_DUZELTMESI.py`

VS Code terminalinde eski uygulamayı Ctrl+C ile durdurup aynı klasörde şu komutu çalıştırın:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.31_TURBIN_RUZGAR_KATMANI_DUZELTMESI.py
```

Tarayıcıdaki mevcut yerel uygulama sekmesini yenileyin. Ana Sayfa'da sürüm v11.11.31 görünmelidir. Bu dosya önceki sürüme yönlendirme değil, tam uygulamadır.

Tekrarlanabilir kontroller:

```bash
python work_checks/turbine_wind31.py
python work_checks/map25.py
python work_checks/map25_integration.py
python work_checks/colors27.py
python work_checks/energy19.py
```
