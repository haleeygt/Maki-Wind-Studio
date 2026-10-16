# v11.11.32 — Şeffaf yıllık enerji ve kapasite faktörü

## Kullanıcının ekranında neden hesaplanmadı?

Ekranda en uzun eksik/dışlanmış ölçüm aralığı 26,2 saat, genel geçerli ölçüm oranı %99,40 görünüyordu. Eski yazılım yıllık gösterimi en az 365 gün, her yıl-ayda ≥%90 geçerli referans ölçümü ve en uzun boşluk ≤2 saat koşullarına bağlıyordu. 26,2 saat bu iç sınırı aştığı için hem yıllık enerji hem buna bağlı yıllık kapasite faktörü gizleniyordu. Bu eşikler uygulama tercihidir; bilimsel sertifikasyon değildir. Ekrandaki 767.329 MWh seçili dönemin yalnız geçerli kayıtlarından hesaplanmış enerji tahminidir; yıllık AEP değildir.

## Yeni davranış

1. **Geçerli kayıtlardan net enerji** korunur. Ham veya temiz ölçümlere tahmini kayıt eklenmez.
2. **Geçerli saatlerin net kapasite faktörü** ayrıca hesaplanır: geçerli enerji / (kurulu güç × geçerli enerji saatleri) × 100. Kısa dönemde de gösterilebilir ve tam yıl faktörü olarak adlandırılmaz.
3. **Yıllık net eşdeğer** ayrı bir model sonucudur: her takvim ayının geçerli ortalama net gücü × standart 365 günlük yılın o ayına ait saatleri, sonra 12 ayın toplamı. Yıllık eşdeğer kapasite faktörü = bu enerji / (kurulu MW × 8760 saat) × 100.
4. Bu yıllık eşdeğer için ≥365 gün, bütün takvim aylarında geçerli güç kaydı ve aylık ≥%90 kapsam aranır. Kullanılan her direğin dönem/yıl-ay kapsamı da denetlenir. Yalnız uzun boşluk nedeniyle eski sıkı kontrol geçmiyorsa sayı açıkça **Eksik saat varsayımıyla** gösterilir: eksik saatlerin aynı ayın geçerli saatleriyle aynı ortalama güce sahip olduğu kabul edilir. Bu, doğrulanmış eksik veri tamamlama veya uzun dönem AEP değildir. Eksik mevsim/ay veya kısa dönemde yıllık sayı yine üretilmez; gerekçe yazılır.
5. Eksik saatlerin gücü 0 ile nominal güç × aynı kayıp çarpanı arasında alınarak seçili dönem ve yıllık eşdeğer için alt/üst sınırlar hesaplanır. Bu sınırlar yalnız eksik saatlerin model içindeki etkisini kapsar; ölçüm/shear/yoğunluk/güç eğrisi/wake/iklim belirsizliğini kapsamaz. İstatistiksel güven aralığı veya P50/P90 değildir.
6. Aylık kapsam/enerji katkıları, gerçek geçerli saatler, eksik saatler, eski sıkı kontrolün kesin engel nedenleri ve kullanılan shear/referans sensör bilgisi ekranda açıklanır.

## Başlık ve kayıp adları

Önceki başlık kayıp seçimi ve son enerji hesabından önce yazılıyordu; ekrandaki P50/P90 tutarsızlığı bu sıradan kaynaklanabiliyordu. Ayrıca manuel mod adının eski değeri kontrol edildiğinden başlık hedef adedi, hesap yerleşimdeki adedi kullanabiliyordu. Yeni başlık son hesapla aynı türbin sayısı, kurulu güç ve kayıp seçimini kullanır. Yerleşim varsa enerji yerleşimdeki gerçek aday türbin adediyle hesaplanır; yoksa hedef adet kullanıldığı açıkça yazılır. Bu aday yerleşimin doğrulandığı anlamına gelmez.

P50/P75/P90 sabit kayıp paketlerinin eski iç anahtarlarıdır. Görünür seçimler **Düşük / Orta / Yüksek kayıp varsayımı** oldu. Gerçek istatistiksel aşılma olasılığı hesaplanmıyor. Eski oturum anahtarları uyumluluk için korundu.

Wake %12, kullanılabilirlik %5, elektrik %3, diğer %4 örneğinde net çarpan 0,88 × 0,95 × 0,97 × 0,96 = 0,7784832'dir; kayıplar basitçe toplanmaz. Sabit kayıp paketindeki wake oranı ile haritanın Jensen ön wake sonucu birbirine karıştırılmaz; enerji hesabı paketteki sabit oranı kullanır.

## Enerji formülü ve geçerlilik

Her gerçek temiz zaman kaydı, o direğin ölçüm yüksekliklerinden türeyen shear ile hub seviyesine taşınır. Hub hızı güç tablosunda doğrusal enterpolasyonla kW'a çevrilir. Güç × özgün kayıt süresi × türbin adedi × kayıp çarpanı ile kWh hesaplanır. Ortalama rüzgâr hızını bir kez güç eğrisine vermek bu işlemle eşdeğer değildir.

Çoklu direkte aynı zamandaki mevcut hub hızları ortalanır. Bu bir mekânsal akış/wake modeli değildir. Yeni kontrol, farklı örnekleme aralığı veya zaman fazıyla gelen direklerin medyan süreyle sessizce birleştirilmesini engeller; açık yeniden örnekleme yöntemi olmadan enerji üretmez. Güç eğrisinin boyutu/sırası/sonlu olması/nominal sınırı, pozitif tamsayı türbin adedi ve %0–100 sonlu kayıplar denetlenir. Bunlar üretici eğrisi doğrulaması değildir.

Kütüphanede kullanıcıdan sağlandığı belirtilen güç tabloları var; bu çalışmada özgün üretici belgeleri bağımsız doğrulanmadı. Envision yoğunluk alanı “Site air density”, Goldwind “Belirtilmemiş”, Nordex “1.20 kg/m³” olarak kayıtlı. Saha yoğunluğu düzeltmesi otomatik yapılmaz. Mevcut motor tablonun alt/üst sınırı dışında 0 kW kabul eder; cut-in/cut-out/yüksek rüzgâr kontrol belgesiyle bu varsayım teyit edilmelidir. Yeni açıklama, aralık dışı kayıt sayılarını da gösterir.

## Yatırım için durum

Bu sürüm doğrulanmış yatırım AEP raporu değildir. Matematik ve arayüz testlerinin geçmesi projenin üretim doğruluğunu kanıtlamaz. Ölçüm/sensör kalibrasyonu ve temiz veri eşdeğerliği, eksik verinin bağımsız enerji doğrulaması, uzun dönem düzeltmesi (MCP), saha yoğunluğu ve güç eğrisi uygunluğu, türbin bazlı akış/wake, gerçek kayıp bütçesi ve belirsizlik analizi açık kalır. Gerçek P50/P75/P90 hesaplanmaz. GWA renk haritası doğrudan yıllık türbin üretimi yerine kullanılmaz. Bu nedenle yönetimin yalnız bu ön sonuçla yatırım kararı vermesi desteklenmez.

Kullanıcının yerel Çorlu-1 ölçüm dosyası bu geliştirme ortamında bulunmuyor. Ekrandaki yuvarlanmış 2,61 MW brüt tek türbin ortalaması, 8 MW nominal güç ve görünen yüksek kayıp paketi kullanılırsa geçerli saatler için net kapasite faktörü yaklaşık %25,4 çıkar; bu yalnız ekran sayılarının aritmetik çapraz kontrolüdür. Kesin yeni yıllık eşdeğer ekran görüntüsünden türetilmedi; kullanıcı kendi verisiyle yeni sürümü çalıştırdığında hesaplanır. Hiçbir tarih, mast ilişkisi veya sensör yüksekliği başka projeye sabitlenmedi.

## Test sonuçları

- Bağımsız analitik sabit güç örneği: 1 MW nominal/600 kW güç için tam 365 günde 5256 MWh ve %60 kapasite faktörü. Türbin adedi ve çarpımsal kayıplarla tam eşitlik doğrulandı.
- 26,17 saat boşluk: eski sıkı yıllık alanları NaN kaldı; ayrı varsayımlı eşdeğer analitik değeri verdi. Geçerli enerji, eksik saatler ve 0–nominal güç sınırları tam eşleşti. Ham tablo ve hesaplanan gerçek kayıt sayısı korunarak tahmini satır eklenmedi.
- Kısa dönem ve eksik mevsimde yıllık eşdeğer engellendi; geçerli saat kapasite faktörü kaldı.
- Artık yılda gözlenen 8784 saatlik enerji, standart 8760 saatlik eşdeğerden ayrıldı. Mevsimsel aylık güç ve doğrusal olmayan iki durumlu güç örnekleri bağımsız integralle eşleşti.
- Bozuk/nominali aşan güç tablosu, negatif/%100 üzeri/NaN kayıp, kesirli türbin adedi, farklı zaman aralığı ve fazdaki çoklu direk hesapları engellendi.
- Tam Streamlit AppTest'te 26 saat boşluk içeren sentetik tam yıl, 7 hedefe karşı 17 manuel yerleşim ve yeni seçilen yüksek kayıp paketi kullanıldı. Başlık, 136 MW kurulu güç, enerji, yıllık eşdeğer, kapasite faktörü, saatler ve uyarılar aynı hesapla eşleşti. Kısa tarih seçimi yıllık sonucu yeniden engelledi. Dış GWA indirmesi açıkça sentetik GeoTIFF ile değiştirildi.
- Önceki temiz enerji, manuel işaret, eksik dönem, mükerrer zaman/shear ve doğrudan sayfa geçişi testleri geçti. Tam harita/kare taşıma, sabit sınır/renk ve manuel editör regresyonları geçti.
- Python derleme ve git boşluk kontrolü geçti. Linux ortamında doğrulandı; kullanıcının Windows Python 3.14 arayüzü uzaktan test edilmedi.

## Çalıştırma

Tam uygulama dosyasını mevcut klasöre kaydedin. VS Code terminalinde eski uygulamayı Ctrl+C ile durdurun:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py
```

Aynı yerel sekmeyi yenileyin. Enerji sayfasındaki **Enerji hesabı nasıl yapılıyor?** bölümünde formüller, aylık katkılar, shear, güç eğrisi ve açık doğrulama işleri bulunur.

```bash
python work_checks/energy32.py
python work_checks/energy32_app.py
python work_checks/energy19.py
python work_checks/map25_integration.py
python work_checks/navigation19.py
```
