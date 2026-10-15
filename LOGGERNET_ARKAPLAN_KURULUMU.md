# Maki Wind Studio v11.11.21

Bu sürüm mevcut uygulama ve tarayıcı aktarımını korur; Chrome kapalıyken çalışabilen Windows yardımcısı ile yetkilendirilmiş HTTPS aktarımı ekler. Ham, temiz ve tahmini veri ayrımı ve enerji hesapları değiştirilmedi. Aktarım bütünlüğü, ölçümlerin bilimsel doğrulanması anlamına gelmez.

## Streamlit Cloud'da bir kez

Uygulamanın yönetim ekranında Settings → Main file path alanını `maki_server.py` yapıp kaydedin. Streamlit sürümü requirements.txt içindeki 1.65.0 olmalıdır. Streamlit'in desteklediği st.App(routes=...) kullanılır; özel sunucu iç işleyişi değiştirilmez.

Önceki noktalı giriş dosyaları klasik uygulamayı açmaya devam eder; bu modda HTTPS aktarım servisi etkin değildir ve indirme düğmesi gösterilmez. Giriş ayarı otomatik değiştirilemez. Bu ortamdan Community Cloud yönetimi ve canlı HTTPS uç noktası doğrulanamadı.

## Windows'ta bir kez

Uygulamadaki LoggerNet otomatik bağlantı bölümünden projeye özel Windows yardımcısını indirin. Mevcut Python 3.14 ile açın, LoggerNet klasörünü seçin ve Kaydet ve bağlan deyin. Yeniden kurulum veya sanal ortam gerekmez. Proje adresi dosyada yer alır; bu özel dosyayı paylaşmayın.

Yardımcı yalnızca okur; kaynak dosyaları değiştirmez. Yalnızca seçilen klasörün doğrudan içindeki WindData.dat ile biten dosyalar gönderilir, RawData dosyaları dışlanır. Önce dosya boyutu/tarihi, son satır ve SHA256 kontrol edilir. Sunucu aynı LoggerNet okuyucusundan geçirdikten sonra bütün dosyayı atomik yayımlar. Zamanları bozuk dosyalar eski verinin üzerine geçmez. Başka klasör kimlikleri karıştırılmaz. İlk bağlama var olan projenin klasör kimliğini kullanır; bu nedenle doğru projeyi ve kaynak klasörü seçmek gerekir.

Yardımcı Windows kullanıcı oturumu açıldığında çalışır. Chrome gerekmez; bilgisayarın açık, oturumun açık ve internetin bağlı olması gerekir. Kontrol aralığı 30 saniyedir; hatada en çok 5 dakikaya çıkar. Değişmeyen dosyalar yeniden gönderilmez; sunucuda kayıp/bozuk dosya varsa yeniden aktarılır. Panel 10 saniyede bir güncelleme kontrolü yapar.

Dosyalar `%LOCALAPPDATA%\MakiWindStudio` altında tutulur; dizin mevcut kullanıcı ve SYSTEM erişimiyle sınırlandırılır. Kullanıcı oturumundaki başlangıç kaydı HKCU Run altında MakiWindStudioLoggerNet adındadır. Yardımcıyı yeniden açıp otomatik takip işaretini kaldırarak durdurabilirsiniz; çalışan takip en geç 5 dakikada sonlanır. Yönetici yetkisi gerekmez. Windows güvenlik denetimleri devre dışı bırakılmaz. İmzasız .pyw dosyası bu ortamda Windows üzerinde denenmedi; dosya ilişkilendirmesi ve otomatik başlangıç henüz doğrulanmadı.

Bulut deposu geçici sunucu diskidir, kalıcı yedek değildir. Sunucu yeniden kurulursa projeyi uygulamada açtıktan sonra kaynak yardımcı dosyaları yeniden gönderebilir. Proje bağlantısı erişim anahtarıdır. Yardımcı bu anahtarı HTTPS Authorization başlığında taşır, yönlendirmeleri izlemez ve TLS doğrulamasını kapatmaz. Windows başlangıç yardımcısı kapanmış/uyuyan bilgisayardan veri alamaz.

## Çalıştırma

Paket klasöründe, mevcut Windows Python 3.14 ile:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\maki_server.py
```

Yalnızca tam uygulama dosyasını klasik modda açmak için (arka plan servisi etkin olmaz):

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.21_LOGGERNET_ARKAPLAN.py
```

## Doğrulama

Linux ortamında gerçek çalışan HTTP sunucusu ve stdlib yardımcı istemcisiyle: yetkisiz/başka proje reddi, değişmeyen dosya atlama, RawData dışlama, tam satır bekleme, SHA256 doğrulama, bozuk/yarım/yanlış klasör aktarımında eski veri korunması, kayıp sunucu dosyasının onarılması geçti. Gerçek 27.781.322 baytlık LoggerNet örneği birebir aktarıldı. İstemci TLS ve yönlendirme kısıtlarını korur; testlerde yalnızca loopback bağlantısı istemci katmanında açıkça değiştirilmiştir, HTTPS/TLS canlı sunucuda denenmedi.

Gerçek Chromium oturumunda yardımcı indirmesi proje kimliğiyle eşleştirildi; tarayıcı kaynak sekmesi olmadan HTTP aktarımı panelde otomatik göründü, klasör seçici çağrılmadı. Mevcut iki tarayıcı paylaşımı, proje yalıtımı, metadata birleştirme, manuel veri korunması ve doğrudan enerji sayfası geçişi geçti. Enerjide temiz veri kullanımı, eksikte yıllık sonuç baskılama, yinelenen zamanlar ve shear kontrolleri geçti.

Windows/Python 3.14 otomatik başlangıcı ve Community Cloud canlı dağıtımı doğrulanmadı. Windographer temiz veri eşdeğerliği, bağımsız tamamlama enerjisi doğrulaması, nihai AEP, gerçek P50/P75/P90 ve GWA raster doğruluğu önceki sürümdeki gibi açık işlerdir.
