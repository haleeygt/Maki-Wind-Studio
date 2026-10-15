# v11.11.29 — Çoklu dosyalarda bellek kontrolü ve sunucu tanı kaydı

## Gözlem ve sınır

Kullanıcının bulut ekranı genel “Oh no / Error running app” mesajını gösterdi. Paylaşılan günlük görüntüsünde yalnızca bağımlılık güncellemesi ve kullanımdan kaldırma uyarıları görüldü; Python traceback, bellekten öldürülme kaydı veya kesin kapanma nedeni görülmedi. `st.components.v1.html` ve `use_container_width` uyarıları tek başına bu kapanmayı açıklamaz. Canlı bulut günlükleri ve kaynak ölçerine geliştirme ortamından erişilemedi; HTTPS kontrolü ortam proxy'sinde 403 ile engellendi. Bu sürüm kesin kök neden çözümü iddiası taşımaz.

## Yapılan değişiklik

Önceki akış, her sayfa çalışmasında bütün yüklenmiş dosyaların tam DataFrame tablolarını `tum_veri_setleri` sözlüğünde birlikte tutuyordu. Artık dosya listesi ve tüm dosyaların kalite özeti korunurken tam tablolar ihtiyaç halinde mevcut disk önbelleğinden okunur. Koleksiyon yalnızca son istenen tabloyu tutar. Kullanılmayan tablolar ve toplu kalite taramasının geçici çıktıları serbest bırakılır. Aktif hesapların kullandığı tablolar normal Python referanslarıyla hesap bitene kadar yaşar; bu değişiklik toplam süreç belleğine kesin üst sınır koymaz.

Sensör yüksekliği başlık kontrolü, yerel dosyanın tamamını okuyup ilk 20.000 baytı ayırmak yerine doğrudan en fazla 20.000 bayt okur.

Sunucu stderr günlüğüne `MAKI_RUNTIME` satırları eklendi: sürüm, işlem aşaması ve desteklenen sistemlerde süreç RAM/tepe RAM sayaçları. Dosya adı, ölçümler, koordinat veya proje bağlantı anahtarı yazılmaz. Dosya taraması başlangıcı/sonu, seçili tablonun hazırlanması, micrositing başlangıcı ve normal sayfa sonu kaydedilir. Erken duran sayfalarda sayfa sonu satırının bulunmaması tek başına çökme kanıtı değildir. Linux'ta sayaç birimi KiB'dir; Windows'ta desteklenmeyen sayaçlar atlanır.

Bilimsel kontrol, kalite motoru, gerçek temiz ölçüm ayrımı, eksik dönem enerjisi kuralları, GWA modeli, enerji ve harita fonksiyonları korunur. Turuncu karenin tamamını gösteren v11.11.28 haritası korunur.

## Tamamlanan kontroller

- Gerçek örnek dosyadan test amacıyla beş ayrı tablo üretildi; her birine yalnızca test içinde farklı hız ofseti uygulanarak bağımsız kalite önbelleği girdileri oluşturuldu. İki ayrı Python sürecinde eski ve yeni akış karşılaştırıldı: tepe bellek 486,6 MiB → 339,4 MiB (yaklaşık %30 azalma). Bu, kullanıcının beş gerçek direğinin veya tam haritalı iki canlı oturumunun ölçümü değildir. Tüm tablo hash değerleri ve beş kalite özeti birebir aynı kaldı. Koleksiyonun önceki tabloyu tutmadığı weakref ile kontrol edildi.
- Tam Streamlit AppTest: beş ayrı sentetik dosya seçim listesinde kaldı; 1. dosyadan 5. dosyaya geçince gösterilen tablo değişti ve 1. dosyaya dönünce ilk tablo birebir geri geldi.
- Tam sayfa harita AppTest: dış raster kaynağı açıkça sentetik TIFF ile değiştirilerek kare taşıma, santralden uzak bölgede yeni rüzgâr değerleri, sabit sınır/renk ölçeği ve sıfırlama geçti.
- Enerji regresyonları, eksik kayıt nedeniyle yıllık sonucun bastırılması, manuel işaretler, mükerrer zaman/shear korumaları geçti.
- Ortak proje veri bütünlüğü, iki tarayıcı arasında paylaşım, proje yalıtımı, eşzamanlı ayar değişiklikleri, bozuk aktarım ve yeniden açılış kontrolleri geçti.
- Doğrudan sayfa geçişi ve onay gerektirmeyen mevcut akış geçti.
- Gerçek Streamlit sunucusunda sağlık ve script sağlık uçları HTTP 200 verdi; Chromium'da iki bağımsız boş oturum v11.11.29'u açtı. Bu kontrol canlı Streamlit Community Cloud'da yapılmadı.
- Yeni tanı satırlarının gerçekten stderr'e yazıldığı AppTest çalışmasında doğrulandı.
- AST karşılaştırmasında mevcut fonksiyonlardan yalnızca başlık okuma işlevi değişti; yükleme koleksiyonu ve tanı işlevi eklendi. Bilimsel fonksiyonların AST'leri aynı.

Gerçek GWA raster doğruluğu, Windographer eşdeğerliği, bağımsız tamamlama enerjisi, nihai AEP ve gerçek P50/P75/P90 doğrulamaları açık kalır. Windows Python 3.14 görsel kontrolü yapılmadı.

## Çalıştırma

Bulut giriş dosyası `maki_server.py` yeni sürüme yönlenir. Kullanıcının yerel kurulum veya komut çalıştırması gerekmez. Dağıtım tamamlandığında mevcut sekmede Ana Sayfa sürümü v11.11.29 görünmelidir. Dağıtımın canlıda tamamlandığı bu ortamdan doğrulanamadı.

İsteğe bağlı mevcut Windows Python 3.14 komutu:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.29_COKLU_DOSYA_BELLEK_KONTROLU.py
```

Kontroller:

```bash
MAKI_LARGE_FIXTURE=/path/to/example.dat python work_checks/multifile29.py
python work_checks/multifile29_app.py
python work_checks/map25_integration.py
python work_checks/navigation19.py
python work_checks/energy19.py
python work_checks/cloud20.py
```
