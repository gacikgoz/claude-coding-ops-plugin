---
name: user-guide
description: Kod yazmayan son kullanıcı ya da operatör için interaktif, çevrimdışı çalışan kullanım kılavuzu üretir ve bakımını yapar. Kılavuz tek klasörlük ve sunucusuzdur, bir ya da daha çok dillidir, açık/koyu temayı ve aramayı destekler. Ekran görüntüleri, renkler, ikonlar ve fontlar ürünün kendisinden otomatik üretilir. Ana pencere tıklanabilir bir şema olarak verilir ve okurun adım adım görevlerle denediği bir ürün simülatörü vardır. Kullanıcı "kullanım kılavuzu", "user guide", "kullanıcı dokümantasyonu", "operatör kılavuzu", "yardım sayfası", "nasıl kullanılır", "ekran görüntülerini güncelle", "kılavuza yeni özellik ekle", "sürüm notları", "SSS", "eğitim/simülatör" dediğinde ya da bir ürün değişikliğinin son kullanıcı belgelerine yansıtılması gerektiğinde bu skill'i kullan. Okur geliştiriciyse (API rehberi, öğrenme sitesi) developer-docs, spesifikasyon için spec-authoring skill'ini kullan.
---

# İnteraktif kullanım kılavuzu

Kullanım kılavuzu ürünü kullanacak kişi içindir: kodu değil, ekranı, işi ve hataları anlatır. Okur önce bulur, sonra okur, sonra dener. Bu yüzden kılavuz aranabilir, gerçek ekranlarla aynı görünür ve içinde güvenle denenebilecek bir simülatör taşır.

Bu skill hazır bir kılavuz iskeleti, derleme betiği ya da ekran görüntüsü üreteci sağlamaz; bunlar `references/guide-method.md` sözleşmesine göre projede yazılır. Skill ile gelen betik: `check_guide.py`. Yöntem masaüstü GUI ürünlerinde geliştirildi; web ürünlerinde ekran görüntüsü için tarayıcı otomasyonu, CLI araçlarında komut çıktısı kaydı kullanılır.

## Önce ürünü ve okuru öğren

- **Okur rolleri:** örneğin kurulumcu, günlük operatör, yaparak öğrenen. Girişte her role "nereden başlamalı" yolu verilir.
- **Ürünün ekranları, menüleri, kısayolları ve mesaj dosyaları.** Menü ve düğme adları ürünün kendi mesaj dosyalarından birebir alınır; kılavuzda uydurma ad kullanılmaz.
- **Ürünün görsel kaynakları:** tema dosyaları (renk değişkenleri), ikon seti, fontlar ve lisansları.
- **Ürünün eksik ya da yer tutucu kısımları:** gri menüler, henüz yapılmamış paneller. Bunlar gizlenmez; kılavuzda açıkça yazılır.
- **Diller:** varsayılan dil ve ek dil(ler).

## Yapı

```text
docs/user-guide/
  src/                 elle yazılan: index.html, guide.css, guide.js, content.<dil>.js, sim.js, sim.css, cover.js
  dist/                üretilen ve dağıtılan: index.html + assets/ (js, css, tokens.css, icons.js, fonts/, img/, img/<dil>/, zones.js)
tools/guide/build-guide.<ps1|sh>   derleme betiği
<ürün test kaynakları>/<shots>     ekran görüntüsü üreteci (küçük bir uygulama)
```

`dist/index.html` çift tıklanarak açılır. Sunucu, internet ve kurulum gerekmez.

## İlkeler

1. **Tek klasör, çevrimdışı.** CDN ve harici font yoktur. İçerik `.json` yerine `.js` dosyalarında `window.X = …` olarak tutulur; böylece `file://` altında `fetch` ve CORS sorunu olmaz.
2. **İçerik veri olarak modellenir.** Bölüm > alt başlık yapısı kullanılır: `{id, icon, title, intro, subs:[{id, title, durum:'hazır'|'taslak', html}]}`. Numaralama, içindekiler, arama dizini ve "taslak" etiketi koddan türetilir. Tekrarlayan HTML için küçük yardımcılar kullanılır: `note()`, `tabs()`, `picture()`. Ayrıntı ve dosya sözleşmeleri `references/guide-method.md` içinde.
3. **Diller aynı kimlikleri paylaşır.** Her dil ayrı bir içerik dosyasındadır ve bölüm/alt başlık `id`'leri ortaktır; bağlantılar böylece bozulmaz. Çeviri yoksa varsayılan dile düşülür ve "çeviri hazır değil" notu gösterilir. Ekran görüntüleri de dile göre ayrı klasörde üretilir.
4. **Görsel kimlik üründen türetilir.** Renk değişkenleri, ikonlar, fontlar ve logo gibi görseller derleme betiğiyle ürünün kaynağından üretilir. Üretilen dosyaların başına "Do not edit" yazılır. Lisansı dağıtıma izin vermeyen varlıklar (ör. yalnız kişisel kullanıma açık bir logo fontu) bilerek dışarıda bırakılır.
5. **Ekran görüntüleri elle çekilmez.** Ürünün test kaynaklarına, gerçek ana pencereyi deterministik örnek veriyle açıp sahneyi PNG olarak yazan küçük bir "shots" uygulaması eklenir. Bu uygulama:
   - tıklama göndermez; durumu kodla kurar;
   - her tema ve her dil için ayrı süreçte çalışır;
   - pencere ölçüsünü ve bölge dikdörtgenlerini (hotspot'lar için) aynı çalıştırmada bir veri dosyasına yazar;
   - çalışan başka bir ürün örneğini bozmamak için ayrı bir örnek kimliği ve ayar kullanır.

   Derleme betiği saydam kenarları kırpar ve kılavuzun artık göstermediği resimleri siler. Web ürününde aynı işi tarayıcı otomasyonu (ör. Playwright) yapar.
6. **Ana pencere tıklanabilir bir şemadır.** Gerçek ekran görüntüsünün üstüne yüzde koordinatlı görünmez düğmeler konur. Üstüne gelinince bölgenin adı ve açıklaması görünür; tıklayınca sabitlenir ve ilgili bölüme bağlantı verir. Klavyeyle de çalışır.
7. **Okur denesin.** Kılavuz ürünün sadeleştirilmiş bir simülatörünü taşır. Simülatör gerçek ürüne bağlı değildir, ama gerçek metinleri ve gerçek ekran görüntülerini kullanır. Görevler adım adım rehberle yapılır. Simülatörde olmayan bir şey "simülatörde yok" diye açıkça yazılır; sahte işlev uydurulmaz.
8. **Eksikler dürüstçe yazılır.** Henüz yapılmamış özellikler kılavuzda belirtilir, SSS'de "bu normal" diye karşılanır ve sürüm notlarında "henüz yapılmayanlar" listesi verilir.
9. **Terim kuralı.** "invariant / değişmez" terimi kullanılmaz (kullanıcı tercihi; ayrıntı `spec-authoring` kural 11).
10. **Erişilebilir ve dayanıklı.** `aria-label`'lar, klavye odağı, `prefers-reduced-motion`, try/catch içinde `localStorage`, dar ekran çekmecesi ve yazdırma CSS'i kullanılır. Adresteki `#id` açılışta o başlığa gider.

## Bölüm sırası

Başlarken (gereksinimler, kurulum, ilk açılış, komut satırı, ayar dosyası) → Dene (simülatör) → Arayüze genel bakış (tıklanabilir şema) → özellik bölümleri → Ayarlar ve görünüm → Sorun giderme → Ekler (sözlük, sürüm notları, SSS).

## Ürün değişince ne güncellenir

1. İlgili bölüm ve alt başlıklar; her dilde aynı `id` ile.
2. Ekran görüntüleri: derleme betiğini çalıştır. Ürün ve gerekli servisler ayakta olmalı; çekim sırasında fare ve klavye kullanılmamalı. Bölge ölçüleri değiştiyse `zones` dosyası da yeniden üretilir.
3. Simülatör: değişen ekranların simülatördeki karşılığı ve rehber adımları. Simülatörün kullandığı ekran görüntüsü değiştiyse konum ve kalibrasyon sayıları elle güncellenir.
4. Sürüm notları ve "henüz yapılmayanlar" listesi; ürün sürüm numarası.
5. Denetimleri çalıştır.

## Denetim

`scripts/check_guide.py` bu skill'in içerik modelini izleyen kılavuzlarda şunları denetler: çevirilerde fazladan `id` olmaması (eksik `id` uyarıdır, varsayılan dile düşülür), iç bağlantıların (`href="#id"`) hedefi, `picture('ad')` ile anılan resimlerin her dil klasöründe bulunması ve `icon:` adlarının ikon dosyasında bulunması.

```bash
python -I -X utf8 ~/.claude/skills/user-guide/scripts/check_guide.py --src docs/user-guide/src --dist docs/user-guide/dist --base content.<varsayılan-dil>.js
python -I -X utf8 ~/.claude/skills/developer-docs/scripts/validate_site.py --site docs/user-guide/dist
```

Ardından `dist/index.html` dosyasını bir tarayıcıda aç ve şunları dene: arama, tema, dil, bir hotspot ve simülatörde bir görev. Ekran görüntüsü üretimi kırılgandır; başarısız olursa nedenini kullanıcıya söyle, eski görüntüleri sessizce bırakma.

Daha ayrıntılı yöntem, simülatör mimarisi ve tuzaklar: `references/guide-method.md`.
