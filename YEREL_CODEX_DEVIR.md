# Maki Wind Studio — Yerel VS Code Codex devri

Kullanıcı dosya indirip komut kopyalamadan, kod değişikliklerini aynı bilgisayardaki uygulamada görmek istiyor. Bu belge yerel projeye geçiş içindir; henüz Windows'ta uygulandığı iddia edilmez.

## Kaynak ve mevcut durum

- Depo: haleeygt/Maki-Wind-Studio.
- Devir dalı: codex/local-vscode-handoff.
- Tam güncel uygulama: appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py.
- Eski kök appv*.py dosyaları güncel tam dosyaya uyumluluk yönlendirmeleridir; tarihsel tam dosyalar previous_versions/ altındadır.
- Bu dala erişmek için mevcut GitHub oturumunu kullanın. Erişim yoksa kimlik bilgisini sohbetten istemeyin; desteklenen hesap bağlama akışını kullanın.
- Kullanıcının mevcut klasörünü, ölçüm dosyalarını ve yerel proje durumunu koruyun. Yerel klasör Git deposu değilse mevcut dosyaların üzerine körlemesine yazmayın; önce klasörü inceleyip kaynağı güvenli bir kardeş klasöre alın.
- Proje verileri ve aktif tarayıcı URL'sindeki pid/msid değerleri kullanıcıya özeldir. Günlüklere veya Git'e koymayın. Mevcut sekme bağlantısını korumak yerel proje durumunun devamına yardımcı olur.

## Windows'ta çalıştırma

Kullanıcı Windows ve mevcut Python 3.14 kurulumunu kullanıyor. Yeniden kurulum, Python 3.12 veya sanal ortam önermeyin.

Mevcut PowerShell komutu, uygulama klasöründe:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m streamlit run .\appv11.11.32_SEFFAF_YILLIK_ENERJI_VE_KAPASITE.py
```

Önce Python yolunu, Streamlit'i ve çalışan uygulamayı kontrol edin. Kullanıcının uygulaması genellikle localhost:8501 üzerinde çalışıyor. İlgisiz süreçleri sonlandırmayın. Mevcut çalışan sürümü değiştirmek için yalnız bu projeye ait süreç üzerinde işlem yapın. Değişiklikten sonra uygulamayı açılış ve gerçek işlevle doğrulayın. Bu devir, bulut dağıtımı veya main dalına gönderme talebi değildir.

Kod üzerinde sonraki çalışmalarda mevcut tasarımı ve çalışan özellikleri koruyun; uygulamayı baştan yazmayın. Kullanıcının her kod değişikliği için yeni sürüm numarası, tam .py dosyası, çalıştırma komutu ve uygun test sonuçları isteği sürer. İndirme zorunluluğu yaratmadan yerel dosyaları doğrudan düzenleyin; tam dosyayı yine proje içinde koruyun.

## Bilimsel sınırlar ve son düzeltmeler

Önce SURUM_11_11_32_NOTLARI.md, gerekirse önceki sürüm notlarını okuyun.

- Ham ölçüm, gerçek temiz ölçüm ve tahmini kayıtlar ayrıdır. Tahmini kayıtları gerçek temiz ölçüm diye sunmayın.
- Direk adı, sensör yüksekliği, arıza tarihi veya başka direkten türetilen katsayıları yeni direklere sabitlemeyin.
- v31: manuel türbin haritası kontrol noktalarını renk ızgarasına katmaz; boş hücreler boş kalır ve komşu koordinat sınırlarıyla çizilir. Turuncu çalışma karesi hareket edince yeni bölge hesaplanır; santral poligonu sabittir.
- v30: ağır dosya akışından önce ve normal sayfa sonunda erişilemez döngüsel nesneler toplanır. Tam uygulamanın tekrar çalıştırmalarında RAM artışı yerelde yeniden üretilip azaltıldı. Her koşulda çöküş olmayacağı garantisi verilmez.
- v32: geçerli kayıtların enerjisi ve geçerli saat kapasite faktörü, varsayımlı 365 günlük yıllık eşdeğerden ayrıdır. Eksik saatler için aylık temsil varsayımı ve yalnız eksik saatlere ilişkin 0–nominal güç sınırları açıkça gösterilir. Ham/temiz tabloya tamamlama satırı eklenmez.
- Eski sıkı yıllık kapsam alanları uzun boşlukta engellenmeye devam eder; ayrı yıllık eşdeğer bu kontrolün bilimsel olarak geçtiği anlamına gelmez.
- Gerçek P50/P75/P90 yoktur. Eski kayıp paketi anahtarları sadece oturum uyumluluğu için korunur; görünen adlar düşük/orta/yüksek kayıp varsayımıdır.
- Enerji başlığı güncel hesap adedi, kurulu güç ve kayıp seçimiyle aynı sonucu kullanır.
- Windographer eşdeğerliği, tamamlamanın bağımsız enerji testi, uzun dönem MCP, yoğunluk/güç eğrisi uygunluğu, türbin bazlı akış/wake, gerçek belirsizlik, nihai AEP ve GWA raster doğruluğu tamamlanmış değildir. Yatırım için doğrulanmış rapor iddiasında bulunmayın.

## Uygun kontroller

```text
work_checks/energy32.py
work_checks/energy32_app.py
work_checks/energy19.py
work_checks/map25_integration.py
work_checks/turbine_wind31.py
work_checks/navigation19.py
```

Bunlar Linux geliştirme ortamında geçti. Windows/Python 3.14 uyumluluğunu yeniden varsaymayın; yerelde yürütüp raporlayın. Bazı tarayıcı testleri Linux Chromium yolunu içerir; yerel yürütümde uygun kurulu tarayıcı yolu gerekebilir. Özel ölçüm örneği Git'te bulunmaz; fixture isteyen testler için mevcut kullanıcı dosyasını yerelden kullanın, depoya eklemeyin.
