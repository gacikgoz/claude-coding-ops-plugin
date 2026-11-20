# Kılavuz yöntemi: dosya sözleşmeleri, simülatör ve derleme

Bu belge bir masaüstü GUI ürünü için kurulmuş bir kılavuzdan genelleştirildi. Adlar ve örnek içerik (harita, katmanlar, cetvel gibi) yalnız örnektir. Alan adları Türkçe (`durum: 'hazır'|'taslak'`) ya da İngilizce (`status: 'ready'|'draft'`) olabilir; motor hangisini kullanıyorsa tutarlı olsun.

## İçindekiler

1. Kabuk (index.html) ve motor (guide.js)
2. İçerik dosyaları
3. Tıklanabilir şema (FIGURE / ZONES)
4. Simülatör
5. Kapak animasyonu
6. Derleme betiği
7. Ekran görüntüsü üreteci
8. Tuzaklar

## 1. Kabuk ve motor

- **index.html:** sol tarafta içindekiler (arama kutusu ve ağaç), ortada kaydırılan içerik (kapak ve bölümler), sağ üstte tema düğmesi ve dil grubu, dar ekranda çekmece düğmesi. Sabit metinler `data-i18n` ve `data-i18n-attr` ile işaretlenir ve JS tarafından doldurulur. Betik yükleme sırası: ikonlar, motor, bölgeler, içerik dosyaları (her dil), simülatör, kapak verisi, kapak.
- **guide.js:**
  - Yardımcılar: `$`, `$$`, güvenli `localStorage` sarmalayıcısı, `icon()`.
  - Dil seçimi `?lang=` parametresiyle ya da kayıtlı tercihle yapılır. Arayüz metinleri `UI = {tr:{…}, en:{…}}` sözlüğündedir.
  - Bölümler HTML'e basılır ve içindekiler ağacı kurulur. Kaydırma izlemeyle geçerli başlık işaretlenir; bağlantıyla gidilen başlık kısa bir "flash" vurgusu alır.
  - Sekmeler ve arama: arama aksan ve büyük/küçük harf duyarsızdır, başlık ve gövdeyi süzer, bulunanı `<mark>` ile işaretler.
  - Tema düğmesi; dil değişince sayfa `?lang=` ile yeniden açılır ve aynı başlıkta kalır.
  - Kısayollar: `/` aramaya odaklanır, `Esc` temizler. F5 sayfanın en üstüne döner.

## 2. İçerik dosyaları

```js
// content.tr.js  (bir değişiklik diğer dil dosyasında da yapılmalı)
window.CHAPTERS = [
  { id: 'harita', icon: 'map', title: 'Harita', intro: '…',
    subs: [
      { id: 'katmanlar', title: 'Katmanlar', durum: 'hazır', html: `
        <p>…</p>${note('info', '…')}${picture('layers', 'alt metin', 'Şekil yazısı')}
        <p>Ayrıntı için <a href="#cizimler">Çizimler</a>.</p>` },
      { id: 'genel-bakis', title: 'Ana pencere', durum: 'hazır', html: 'FIGURE' },
      { id: 'sss', title: 'Sık sorulan sorular', durum: 'taslak', html: 'FAQ' } ] } ];
window.FAQ = [['Soru?', '<p>Cevap.</p>'], …];
window.ZONES = [{ key: 'rail', rect: [x, y, w, h], title: '…', text: '…', go: 'ray' }, …];
// content.en.js
window.CHAPTERS_EN = [ /* aynı id'ler */ ]; window.FAQ_EN = …; window.ZONE_TEXT_EN = { rail: { title, text } };
```

- Gövde HTML'inde alt başlık `<h4>`, tablo `<table>`, tuş `<kbd>`, iç bağlantı `<a href="#id">` olur.
- Yardımcılar:
  - `note('info'|'warn', html)`: uyarı kutusu.
  - `tabs([[etiket, html], …])`: sekmeler.
  - `picture(ad, alt, yazı, boyut, açıkTemaVar)`: tek ekran görüntüsü figürü.
  - `pictures([...])`: yan yana ekran görüntüleri.
- Resim adı sözleşmesi: `assets/img/<ad>-dark.png`, `<ad>-light.png`; ek diller `assets/img/<dil>/…`. CSS, temaya göre doğru resmi gösterir.

## 3. Tıklanabilir şema

- `ZONES` dikdörtgenleri ekran görüntüsünün piksel boyutuna oranlanır. Pencere boyutu ve panel dikdörtgenleri, ekran görüntüsü üretecinin yazdığı `zones.js` dosyasından gelir.
- Her bölge bir `<button>` olur ve yüzde konumlanır. Üstüne gelme ya da odak geçici açıklama gösterir; tıklama açıklamayı sabitler (`aria-pressed`) ve ilgili bölüme "Ayrıntılı anlatım" bağlantısı verir.

## 4. Simülatör

**Mimari:**
- Durum tek bir nesnede tutulur (`S`). Ekran durumdan çizen render fonksiyonlarıyla kurulur.
- Bütün tıklamalar tek bir `act(e)` yönlendiricisinden geçer. Öğeler `data-a` (eylem) ve `data-v` (değer) öznitelikleriyle işaretlenir.
- Sabit tasarım boyutunda çizilir ve kapsayıcıya göre ölçeklenir.

**Metinler:** tek sözlükte, `K['anahtar'] = [tr, en]` biçiminde tutulur. Ürünün gerçek adları kullanılır.

**Dünya:**
- Örnek nesneler (ör. örnek kayıtlar ya da hareketli öğeler) zaman ölçeğiyle hızlandırılmış değişir.
- Değerler her tikte güncellenir.
- Gerçek ürünün onay akışları taklit edilir (ör. seçim onay kartı).

**Rehber:** görevler veridir.

```js
TASKS = [{ id: 'olcum', title: K.t_ruler, steps: [
  step('s_open_tools', '[data-a="tool"][data-v="ruler"]', () => S.tool === 'ruler', null),
  step('s_click_two', '.sim-map', () => S.ruler.length >= 2, 's_open_tools') ] }]
// step(metinAnahtarı, tıklanacakÖğeSeçicisi, bittiMi(S), yoldanÇıkınca dönülecekAdım)
```

- Rehber önce ortada kısa bir açıklama kartı gösterir ("Devam"). Sonra tıklanacak öğenin üstüne ince bir halka, yanına da altyazı koyar. Altyazı açık liste ya da pencereyi örtmeyecek bir yer seçer.
- Görev listesi ve ilerleme çubuğu (n/N), "Baştan başla" düğmesi; okur rehberi kapatıp serbest deneyebilir ya da istediği görevi seçebilir.
- Simülatörde olmayan bir şey (ör. 3B görünüm, ayrı pencere) "simülatörde yok" diye yazılır.

## 5. Kapak animasyonu (isteğe bağlı)

Ürünün açılış ekranında bir animasyon varsa verisi dışa aktarılır (ör. tel kafes kenar listesi) ve kapakta canvas ile oynatılır. Kapak ekran dışındayken durur; `prefers-reduced-motion` açıksa tek kare çizilir.

## 6. Derleme betiği

Tek komut `src`'den `dist`'i üretir. Adımlar:

1. **Fontlar:** ürünün kaynak klasöründen kopyalanır; lisansı dağıtıma uygun olmayanlar atlanır.
2. **Logo, açılış ekranı ve benzeri görseller:** ürünün kaynaklarından kopyalanır.
3. **Renkler:** ürünün tema dosyalarındaki değişken satırları düzenli ifadeyle CSS değişkenlerine çevrilir ve `tokens.css` (`:root[data-theme="dark|light"]`) üretilir. Dosyanın başına "Do not edit" yazılır.
4. **İkonlar:** ürünün ikon listesinden `window.ICONS = {ad: svgYolu}` biçiminde `icons.js` üretilir.
5. **Diğer veriler:** logo ve animasyon verisi kopyalanır ya da dönüştürülür.
6. **Elle yazılan dosyalar:** `src`'den `dist/assets`'e kopyalanır.
7. **Ekran görüntüleri:** atlama bayrağı verilmediyse üretilir (bkz. 7).
8. **Son işlem:** saydam kenarlar kırpılır, gereksiz boşluklar kesilir, artık kullanılmayan resimler silinir.

Betik, projede tanımlayacağın bayraklar sunabilir (ör. ekran görüntüsü atlama, yalnız menüler).

## 7. Ekran görüntüsü üreteci

- Ürünün test kaynaklarında yaşar ve ürünün kendi kodunu kullanır. Gerçek ana pencereyi ve gerçek içeriği deterministik örnek veriyle açar.
- Parametre örnekleri (projeye göre): `--out --theme --lang --size --open=<paneller> --active=<seçim> --just=<menus|…> --hide=<öğeler>`.
- Tıklama göndermez; paneller ve menüler koddan açılır. Menüler saydam arka planla ayrıca çekilir.
- Her tema ve dil için ayrı süreçte çalışır ve her çalıştırmanın bir süre sınırı vardır.
- Ana pencere ölçüsünü ve panel dikdörtgenlerini `zones.js` olarak yazar.
- Çalışan başka bir ürün kopyasıyla çakışmamak için yapılandırmanın bir kopyasını kullanır ve örnek kimliğini değiştirir.
- Canlı veri gerektiren görüntüler için gerekli servisler (ör. veri geçidi, simülatör) ayakta olmalıdır.

## 8. Tuzaklar

- Diller elle senkron tutulur. İçerik dosyası dışında metin taşıyan yerler (simülatör sözlüğü, bölge metinleri) de unutulabilir. `check_guide.py`'yi her değişiklikte çalıştır.
- `dist` repoya işleniyorsa ekran görüntüleri her derlemede değişebilir ve repoyu şişirir. Görüntüleri yalnız ilgili ekran değişince yeniden üret.
- Ekran görüntüsü üretimi pahalıdır: birkaç tam ekran pencere açılır; derleme aracı, çalışma zamanı ve servis bağımlılıkları vardır.
- Bölge koordinatları ekran görüntüsü boyutuna bağlıdır. Görüntü farklı çözünürlükte üretilirse `zones.js` de yeniden üretilmelidir.
- Simülatörün ekran kalibrasyon sayıları (ör. bir harita ya da tuval kadrajı) sabittir; görüntü ya da kadraj değişince elle yeniden kalibre et.
- Arama normalizasyonu (NFD) bazı harflerde metin uzunluğunu değiştirir; bulunan eşleşme vurgulanmayabilir. Türkçe gibi dillerde özel katlama tablosu kullan.
- Ürün sürümü ve tarih elle yazılıyorsa ürünle senkronunu kaybeder; mümkünse derleme betiğinde üründen oku.
