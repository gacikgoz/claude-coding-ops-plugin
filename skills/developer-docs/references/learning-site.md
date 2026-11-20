# İnteraktif öğrenme sitesi

Bu yöntem, yeni bir geliştiricinin sistemi "ihtiyaç → sahiplik → çağrı sırası → kod koşulları → hata ve kapanış → test" sırasıyla öğrenmesi için kurulmuş, çevrimdışı açılan bir sitenin genelleştirilmiş tarifidir.

## İçindekiler

1. Hedef ve ilkeler
2. Site yapısı
3. Ders sayfası sözleşmesi
4. Etkileşimli yapı taşları
5. Başvuru sayfaları ve kaynak indeksleri
6. Doğrulama
7. Bakım ve bayatlama
8. Tuzaklar

## 1. Hedef ve ilkeler

- **Statik ve bağımsız:** sunucu, CDN, harici font ve analitik yok. Her sayfa `file://` altında, hava boşluklu ağda ve yazdırılarak çalışır.
- **Tek CSS ve tek JS:** bütün sayfalar aynı `assets/site.css` ve `assets/site.js` dosyalarını kullanır. Sayfa türü `<body data-page="home|lesson|reference" data-lesson="05">` ile seçilir. Kök dizine dönüş yolu sayfa derinliğinden hesaplanır.
- **Ders listesi tek yerde:** ders sırası ve başlıkları `site.js` içindeki tek bir listede tutulur; gezinme ve ilerleme buradan türer.
- **Anlatı elle, başvuru koddan:** dersler elle yazılır ve koddan okunarak doğrulanır. Başvuru sayfaları yalnız kaynak indekslerinden üretilir.
- **Her iddia kaynağa bağlanır:** sınıf ve metot adları kaynak dosyasına satır numarasıyla bağlanır; indeksteki hash, kaynağın değişip değişmediğini söyler.

## 2. Site yapısı

| Parça | İçerik |
| --- | --- |
| Giriş sayfası | Kaldığın yer (ilerleme), güncel durum (tarihli: ne bitti, ne kaldırıldı, sözleşme sürümü, sıradaki iş), nasıl çalışılır (ders iskeleti ve "bir sınıfı öğrendim" demek için soru listesi), okuma yolu, rol bazlı kısa yollar, ders tablosu (no, başlık, kazanım), başvuru kartları, "Nerede bulurum?" tablosu (ihtiyaç → ilk açılacak sembol → ders), kod kökleri ve arama komutları |
| Dersler | `lessons/NN.html`; büyük resim → açılış ve konfigürasyon → verinin iç yolu → yaşam döngüsü ve dayanıklılık → arayüze çıkış → yeni özellik hatları → laboratuvar (debug ve test) |
| Başvuru | Tip atlası (tip başına kart ve dizin), sözleşme kataloğu (varsa: şema, mesaj ya da API alanları ve sürüm), ikinci dil atlası (varsa), test haritası (modül başına test metotları), desen haritası (desen → koddaki yer → spesifikasyondaki yer), açılış zinciri kartı (varsa) |
| Değişiklik kaydı | `updates.html`: tarihli, en yeni üstte |
| İndeksler ve doğrulama | `SOURCE_INDEX.json`, `TEST_SOURCE_INDEX.json`, `CONTRACT_SOURCE_INDEX.json`, `VALIDATION.json` |

## 3. Ders sayfası sözleşmesi

```html
<body data-page="lesson" data-lesson="05">
<nav id="site-nav"></nav>  <!-- JS doldurur -->
<main>
  <p class="eyebrow">Ders 05</p><h1>…</h1><p class="lead">…</p>
  <section id="lesson-goal"><h2>Bu derste</h2><ul><li>X'i açıklayacaksın …</li></ul></section>
  <section id="ownership"><h2>1. Kim oluşturur, kaç örnek</h2>…</section>
  <!-- terim: <dfn title="tanım">…</dfn>; kod: <code>…</code>; kaynak: <a class="src" href="…/File.java#L42">…</a>; ders arası: <a href="08.html#allows">…</a> -->
  <figure class="diagram"><svg viewBox="0 0 640 240" role="img" aria-label="…">
    <g class="d-node accent" id="f-recv">…</g><path class="d-edge" id="f-e1" marker-end="url(#arrow)"/>
  </svg><figcaption>Şekil 1. …</figcaption></figure>
  <div class="flow">
    <figure class="diagram">…</figure>
    <ol class="steps"><li data-highlight="f-recv f-e1"><strong>Alım.</strong> …</li></ol>
  </div>
  <div class="callout note|warn|tip">…</div>
  <div class="quiz"><p class="q">Şu olursa ne olur?</p>
    <ul class="options"><li>…</li><li data-correct>…</li></ul>
    <p class="explain">Neden doğru: …</p></div>
  <button class="done">Bu dersi bitirdim</button>
</main>
```

Ders iskeleti: ihtiyaç → sahiplik → çağrı sırası (ve varsa eşzamanlılık) → kod koşulları (if/try/catch, sınırlar) → hata ve kapanış → hangi test koruyor. Diyagramlar satır içi SVG'dir; renkler CSS sınıflarından gelir, böylece tema değişince uyum korunur.

## 4. Etkileşimli yapı taşları

- **Gezinme ve arama:** sol sütun; arama dile özgü harfleri katlar (ör. Türkçe ı/İ), tüm kelimeler eşleşmelidir; Enter ilk sonuca gider, Esc temizler, sonuç yoksa mesaj gösterilir. Geçerli sayfa `aria-current` ile işaretlenir.
- **İlerleme:** "Bu dersi bitirdim" listesi önekli bir `localStorage` anahtarında tutulur. Her erişim try/catch içindedir; erişilemezse bellek içi saklanır. `storage` olayıyla sekmeler eşitlenir. Giriş sayfası ilk bitmemiş dersi önerir.
- **Tema:** işletim sistemi tercihi ve elle açık/koyu seçimi; tercih saklanır.
- **Adım adım akış:** `.flow` blokları "Önceki / Sonraki / Hepsini göster" düğmeleri ve "Adım k / n" sayacı kazanır. Her adım `data-highlight` içindeki SVG kimliklerini vurgular, diğerlerini soluklaştırır. Klavyeyle (←/→) gezilir; `aria-live` ile duyurulur.
- **Sınav:** tek seferlik cevap, doğru ve yanlış rengi, doğru seçeneğin gösterilmesi, "Tekrar dene" ve "Neden doğru" açıklaması. Sorular ezber değil, "şu olursa ne olur?" sorar.
- **Sayfa içi içindekiler:** h2/h3'ten üretilir; geniş ekranda yan sütun, dar ekranda gövde içinde.
- **Kod blokları:** dil sınıfına göre küçük bir jetonlaştırıcıyla renklendirilir ve "Kopyala" düğmesi alır. Tablolar yatay kaydırılabilir sarmalayıcıya alınır. `<dfn title>` odaklanabilir ipucu olur.
- **Erişilebilirlik:** `prefers-reduced-motion`, yazdırma stili, mobil menü.

## 5. Başvuru sayfaları ve kaynak indeksleri

İndeks şemaları:

```text
SOURCE_INDEX.json
  {scope:[klasörler], extras:[ek sınıflar], date,
   files:[{file, hash(sha256), lines, description?,
           types:[{line, signature}], fields:[{line, signature}],
           methods:[{line, end, signature, doc, flow:[{line, text}]}]}]}
  flow: yalnız kontrol akışı satırları (if/try/catch); derslerdeki "kod koşulları" için kanıt.
TEST_SOURCE_INDEX.json      {date, modules[], files:[{file, hash, methods:[{line, signature}]}]}
CONTRACT_SOURCE_INDEX.json  {date, contractVersion, files:[{file, hash}]}
VALIDATION.json             {date, html, localLinks, anchors, externalRefs, hashedSources,
                             staleSources, failures:[]}
```

- `scripts/hash_index.py` dosya, hash ve satır alanlarını üretir; `--merge` başka bir aracın eklediği alanları, hash'i değişmeyen dosyalar için korur. Tip, alan, metot ve akış alanlarını üreten betik projede yazılır ve belgeyle aynı repoda tutulur.
- Tip, alan ve metot imzaları dile özgü bir ayrıştırıcıyla eklenir.
- **Sınıf kartı:** rol cümlesi, kaynak yolu ve açıklaması; tipler (satır + imza), alanlar (satır | bildirim), metotlar (satır / uzunluk | imza ve doc). Her satır numarası kaynak dosyasına bağlanır. Sayfa adı `<ad-alanı>_<tip>.html` biçimindedir.
- **Test haritası:** test metodu bildirim sayısının koşu sonucu olmadığını yazan bir uyarı taşır.
- Dersler kartlara, kartlar derslere çift yönlü bağlanır. Dizin sayfası ve arama zorunludur.

## 6. Doğrulama

`scripts/validate_site.py` şunları denetler:

- bütün yerel bağlantılar hedef dosyaya çözülüyor mu;
- sayfa içi çapaların hedefi var mı;
- dış başvuru sayısı sıfır mı (çevrimdışı kuralı);
- isteğe bağlı olarak indeksteki hash'ler diskle eşleşiyor mu (kaynak değiştiyse ders bayattır).

`failures` boş değilse yayınlama.

Doğrulayıcı anlatımın doğruluğunu denetlemez. Sorular, açıklamalar ve sayısal iddialar için ayrı bir kod okuma gözden geçirmesi yap.

## 7. Bakım ve bayatlama

- Her sprint ya da dilimden sonra önce **eski** indeksle `hash_index.py check` çalıştır, bayat kaynaklara bağlı dersleri güncelle, sonra indeksi `--merge` ile yeniden üret ve doğrulayıcıyı çalıştır. Önce yeniden üretirsen bayatlık görünmez.
- Revizyonu değişiklik kaydına şu başlıklarla yaz: ne değişti (ürün), ders tarafında ne değişti, neye dokunulmadı, nereden okundu.
- Ders içindeki sabit sayı ve ad iddialarını kaynağa bağla; hash yalnız dosyanın değiştiğini söyler, iddianın bozulduğunu söylemez.
- Üretilen çıktıları ve indeksleri sürümlemeye karar verirsen üretimi deterministik yap: sıralı anahtarlar ve sabit tarih alanı.

## 8. Tuzaklar

- Üretici ve doğrulayıcı betikler repo dışında kalırsa site yeniden üretilemez. Betikleri ve çalıştırma komutunu belgeyle aynı repoya koy.
- Büyük indeksler (megabaytlarca) ve yüzlerce üretilmiş sayfa diff'i gürültülü yapar. Toplu tek commit geçmişi okunaksızlaştırır.
- Sınıf başına bir sayfa (yüzlerce kart) gezinmeyi ağırlaştırır; dizin ve arama olmadan kullanılmaz.
- `localStorage` kapalı olabilir (gizli pencere, `file://` kısıtları); ilerleme izlemeyi vazgeçilebilir yap.
