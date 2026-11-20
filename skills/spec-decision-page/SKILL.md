---
name: spec-decision-page
description: Bir yazılım spesifikasyon setini gerçek uygulamayla (kod tabanıyla) karşılaştırıp çevrimdışı çalışan interaktif bir karar sayfası üretir. Her genel konu için Önerilen (spesifikasyon), Şu anki (uygulama) ve Teklif edilen (uzlaştırma ve design pattern önerileri) tasarım, konunun eksiksiz spesifikasyon maddeleri, desen kullanım yerleri ve Kabul / Ertele / Red kararları sayfada yer alır; kararlar kullanıcının seçtiği bir JSON dosyasına yazılır. Kullanıcı "dokümanı kodla kıyasla", "tasarım uyumu", "neler çıkarılmış / eklenmiş / uyumsuz", "spesifikasyon farkları", "karar sayfası", "önerilen-şu anki-teklif", "kabul ertele red", "design review", "spec vs implementation", "gap analysis" dediğinde ya da bir mimari belge seti ile bir repo arasındaki farkları karar verilebilir bir listeye dönüştürmek gerektiğinde bu skill'i kullan.
---

# Spesifikasyon karar sayfası

Bu skill bir spesifikasyon setinin her genel konusunu uygulamayla yan yana koyar ve ekibin konu konu karar vermesini sağlar. Çıktı tek bir HTML dosyasıdır: internet ve sunucu istemez. Kararlar paylaşılabilen bir JSON kayıt dosyasında tutulur. İstenirse ayrıntılı bir uyum bulguları raporu da üretilir.

Bu bir analiz işidir. İncelenen repolarda kod değiştirilmez ve commit yapılmaz. Çıktılar projenin teslim klasörüne yazılır; proje bir klasör tanımlamıyorsa kullanıcıya sor (öneri: `docs/deliverables/`).

## Önce projeyi öğren

Bu skill her projede çalışır. Projeye özgü her şey projenin kendi belgelerinden okunur, kullanıcıya bir kez sorulur ya da gerekirse doğrulanır:

- **Spesifikasyon seti nerede:** otorite belge (master architecture ya da eşdeğeri), alt sistem belgeleri, ADR'ler, karar defteri, gereksinim kaydı. Alanlar bu belgelerin yapısından kurulur.
- **Uygulama nerede:** repo ve commit. Sayfanın alt başlığına yazılır.
- **Kabul edilmiş kararlar:** uygulamanın kendi ADR'leri ya da kullanıcının "bu doğru" dediği seçimler. Teklifler bunları geri almaz; orijinal yeteneği o seçimin üzerine genişletme olarak önerir.
- **Önceliği düşük alanlar:** örneğin "görsel tasarım ayrıntısı önemli değil". Bu alanlar yalnız genel düzeyde ele alınır.
- **Dil:** kalem metinleri kullanıcının dilinde yazılır; teknik terimler ve belge adları orijinal dilinde kalır. Sayfanın arayüzü Türkçedir; sütun adları, kaynak etiketleri ve dosya adı `meta.labels` ile değiştirilir.

## Sayfanın yapısı

- **Alanlar:** spesifikasyon setinin üst düzey yapısını izler (ör. sistem mimarisi, masaüstü/istemci, ortak modüller, iletişim, backend ve veritabanı, konfigürasyon ve güvenlik, dağıtım, eklentiler, görsel tasarım). Ayrıca bir "Tasarım desenleri" alanı vardır.
- **Kalemler:** her kalem bir genel konudur ve üç kart taşır:
  - **Önerilen:** spesifikasyon ne istiyor; tek cümle özet, en çok iki cümle ayrıntı, kaynak satırı.
  - **Şu anki:** uygulamada ne var; yoksa "Yok."
  - **Teklif edilen:** hedef spesifikasyon ve uyan desenler.
- **Spesifikasyon maddeleri:** her kalemin içinde o konunun spesifikasyondaki bütün maddeleri listelenir. Her maddede uygulamadaki durum (Var / Farklı / Başka çözüm / Kısmi / Yok / Çelişen) ve aksiyon (Koru / Uygula / Uyarla / Ertele / Gerek yok) yazar.
- **Desen kalemleri:** spesifikasyonun öngördüğü ve kodda bulunan her kullanım yeri durumuyla listelenir.
- **Kayıt:** kullanıcı bir tasarım seçer, Kabul / Ertele / Red verir ve not yazar. Kayıt seçilen JSON dosyasına anında yazılır; tarayıcı belleği yalnız yedektir. Ayrıca JSON, CSV ve Markdown dışa aktarma ve JSON içe aktarma vardır.

Veri şeması ve etiketlerin nasıl değiştirileceği: `references/seed-schema.md`.

## Yazım kuralları

Bu kurallar kullanıcı tercihidir; her birinin nedeni yanında yazılıdır. Hepsini uygula.

1. **Kalem = spesifikasyonun genel konusu.** Kalemleri belgelerin ana bölümlerinden türet, bulgulardan türetme. Tek dosya, tek ayar, satır sayısı ya da bir lint sınırı kalem olmaz; bunlar okuyanı boğar ve karar verilecek konuyu gizler.
2. **Spesifikasyon içeriği eksiltilmez.** "Sade ve kısa" yalnız kartlar içindir. Maddeler o konunun bütün gereksinimlerini taşır ve teknik adlar korunur. Ekip bu sayfadan karar veriyor; atılan madde, karar verilmemiş madde demektir.
3. **Aynı düzeyde kıyas.** Önerilen ve Şu anki aynı konuyu aynı ayrıntı düzeyinde anlatır. Genel bir ilkeyi tek bir sınıfla kıyaslama.
4. **Uygulama sütunu yalnız var olanı yazar.** Bir şey yoksa yalnız "Yok." yazılır. Açıklama, karşılaştırma ("spesifikasyondaki X yerine"), plan notu ("planlandı") ve değerlendirme ("eksik") yazılmaz; spesifikasyon zaten kendi başına yeterlidir. Gerekçe yalnız uygulamanın kendi ADR'sinde, planında ya da commit mesajında yazılıysa kısa bir kaynak olarak eklenir; yalnız çıkarım varsa `why` boş kalır.
5. **"değişmez / invariant" terimini kullanma.** Kullanıcı bu terimi istemiyor; yerine kural, ilke, gereksinim ya da karar de. Fiil gerekiyorsa "değiştirilmez" yaz (ayrıntı: `spec-authoring` kural 11).
6. **Kabul edilmiş kararlar korunur.** Teklif, uygulamanın bilinçli ve belgelenmiş bir seçimini körü körüne geri almaz; spesifikasyonun değerli özünü o seçimin üzerine taşır. Gerekirse "ertele + karar kaydı" önerir.
7. **Uygulamaya sonradan eklenenler ayrı grup olmaz.** Bir tasarım farkı yaratıyorlarsa ilgili kalemin Şu anki tarafında geçer. `new` durumu yalnız bir maddede ya da desen kullanım yerinde kullanılır; tek başına kalem ya da grup açmaz.
8. **Yazılım yapısı önceliklidir.** Kullanıcı aksini söylemedikçe görsel tasarım yalnız genel düzeyde ve birkaç kalemle yer alır.
9. **Desenler eksiksiz kapsanır.** Mediator, Observer, Factory, Builder, Strategy, Command gibi her desen ailesi, spesifikasyonun öngördüğü ve kodun kullandığı yerlerle birlikte listelenir.

## Süreç

Ayrıntılı tarif, ajan istemleri ve tuzaklar `references/workflow-recipe.md` içinde. Kısaca:

1. **Taban çizgisi:** iki tarafın commit'ini kaydet; bunun analiz olduğunu ve koda dokunulmayacağını söyle.
2. **Belge envanteri ve alan haritası:** otorite belgenin yapısına göre alanları kur.
3. **(İsteğe bağlı) Uyum bulguları:** alan başına analizci ve şüpheci doğrulayıcı; sonuç bir Markdown rapor. Bulgular yalnız ipucudur, kalem olmaz.
4. **Kontrol listesi:** belgelerden ince kalemler çıkarılır; eksiksizlik denetimi içindir.
5. **Alan yazarları:** genel kalemler ve eksiksiz maddeler yazılır. İnceleyiciler eksik maddeleri ekler ve durumları doğrular.
6. **Desen taraması ve desen kalemleri.**
7. **Kapsama denetimi:** kapsanmayan genel konular eklenir.
8. **Uygulama sütunu sadeleştirme:** yalnız var olan ya da "Yok."
9. **Doğrulama, derleme, yerel test ve teslim.**
10. **Repo değişti mi:** teslimden önce uygulama reposuna yeni commit gelip gelmediğine bak; geldiyse Şu anki tarafını tazele.

Bu iş çok ajanlı bir workflow ister. Rutin okuma, çıkarım, inceleme ve yeniden yazımı ucuz modelle (ör. Sonnet), tasarım muhakemesi isteyen yazar adımlarını oturum modeliyle yap ve bunu kullanıcıya söyle.

## Derleme ve test

```bash
SK=~/.claude/skills/spec-decision-page
python -I -X utf8 $SK/scripts/validate_seed.py seed.json
python -I -X utf8 $SK/scripts/build_page.py $SK/assets/template.html seed.json page.html
python -I -X utf8 $SK/scripts/build_offline.py page.html <font klasörü | -> <teslim klasörü>/<tarih>-<konu>.html
```

- `build_offline.py` font klasöründeki `Inter-Regular.ttf`, `Inter-Medium.ttf`, `Inter-SemiBold.ttf` ve `JetBrainsMono-Regular.ttf` dosyalarını alt kümeye indirip gömer; `fontTools` gerekir. Font klasörü yoksa `-` ver; sayfa sistem fontuyla çalışır. Çıktı klasörü yoksa açılır. Sayfa dili `--lang` ile verilir (varsayılan `tr`).
- Test için aynı komutu `--test-hook` ile ayrı bir dosyaya derle. Dosyayı `python -I -m http.server` ile 127.0.0.1'den sun ve tarayıcıda aç. Kayıt dosyası akışını OPFS tutamağıyla dene (`__sdpTest.attach`); ayrıntılar tarifte.
- Teslim dosyasında `"testHook":true` geçmemeli.
- Kullanıcı istemedikçe dosyayı bir web servisinde ya da artifact olarak yayınlama; varsayılan çıktı yerel dosyadır. Commit etme.

## Kararlar verildikten sonra

Kullanıcı kayıt dosyasını verdiğinde (`format: "spec-design-decisions"`; eski bir sayfanın farklı kimliği varsa `meta.legacyFormats` ile okunur), kararları kalem kimlikleriyle eşleştir:

- **Kabul:** seçilen tasarım spesifikasyona ya da yeni bir karar kaydına (ADR) işlenir; bunun için `spec-authoring` ve `developer-docs` skill'lerini kullan.
- **Ertele:** plana tetikleyicisiyle birlikte yazılır.
- **Red:** gerekçesi karar defterine girer.

Kalem kimliklerini sürümler arasında koru. Kimlik değişirse eski kayıtlar eşleşmez; bunu kullanıcıya söyle.
