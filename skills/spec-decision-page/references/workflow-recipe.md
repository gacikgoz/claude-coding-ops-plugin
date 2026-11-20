# Süreç tarifi: spesifikasyon ↔ uygulama karar sayfası

Bu tarif büyük bir spesifikasyon seti ile sonradan açılmış bir uygulama reposu arasındaki çalışma için genelleştirildi. Örneklerdeki adlar yalnız örnektir. "Ucuz model" rutin okuma ve yeniden yazım için hızlı bir modeldir (ör. Sonnet); "oturum modeli" tasarım muhakemesi için çalışan ana modeldir.

Adımlar sırayla gider; her adımın çıktısı bir sonrakinin girdisidir. Ara dosyalar oturumun geçici klasöründe tutulur. Teslim dosyası repoya yalnız son adımda yazılır.

## İçindekiler

1. Taban çizgisi
2. Belge envanteri ve alan haritası
3. (İsteğe bağlı) Uyum bulguları
4. Kontrol listesi: ince kalem çıkarımı
5. Alan yazarları ve inceleyiciler
6. Tasarım desenleri
7. Kapsama denetimi
8. Uygulama sütununu sadeleştirme
9. Derleme, test ve teslim
10. Uygulama reposu değişirse
11. Ajan istemi parçaları
12. Bilinen tuzaklar

## 1. Taban çizgisi

- İki tarafın commit'ini kaydet: `git -C <repo> rev-parse --short HEAD` ve `git -C <repo> status --short`.
- Kullanıcıya bunun yalnız analiz olduğunu, koda dokunulmayacağını söyle. Commit edilmemiş değişiklikler kullanıcınındır; onlara dokunma.
- Uygulamanın kabul edilmiş kararlarını topla (uygulama reposundaki ADR'ler, plan belgeleri, kullanıcının açık ifadeleri). Bunlar yazar istemlerindeki "kabul edilmiş kararlar" maddesine girer.
- Sayfanın `meta.subline` alanına uygulama commit'ini yaz.

## 2. Belge envanteri ve alan haritası

- `find <docs> -name '*.md' | xargs wc -l` ve her belge için `grep -n '^#'` ile içindekileri çıkar.
- Alanları otorite belgenin (master architecture vb.) bölüm yapısına göre kur. Tipik alan seti:

| Alan | Tipik belgeler |
| --- | --- |
| Tasarım desenleri | Tüm belgeler (desen taraması) + uygulama kodu |
| Sistem mimarisi ve proje yapısı | Otorite belgenin ilke/katalog/test/süreç bölümleri, repo yapısı, temel ADR'ler |
| Sunum katmanı ve kullanıcı çalışma alanı | Uygulama kabuğu ya da web arayüzü, düzen, kullanıcı etkileşimleri |
| Ortak model ve arayüz bileşenleri | Ortak model, birimler, UI bileşenleri, yerelleştirme |
| Alana özgü alt sistemler | Her büyük alt sistem bir alan (ör. işlem hattı, iletişim, raporlama) |
| Backend, kalıcılık ve veritabanı | Backend tabanı, servis sınırları, varlık modeli, şema ve migration |
| Konfigürasyon, gözlemlenebilirlik ve güvenlik | Konfigürasyon, loglama/denetim, güvenlik |
| Dağıtım ve dış entegrasyonlar | Paketleme, kurulum, dış sistemler |
| Eklentiler ve alan yetenekleri | Eklenti modeli ve türleri, ürüne özgü yetenekler |
| Görsel tasarım (yalnız genel) | Tasarım sistemi belgeleri, tasarım otoritesi |

- 1000 satırı aşan belgeyi bölüm sınırlarından ikiye ya da dörde böl ve her parçaya ayrı yazar ver.

## 3. (İsteğe bağlı) Uyum bulguları

Kullanıcı "ne çıkarılmış, ne eklenmiş, ne uyumsuz" diye ayrıntılı bir analiz istediyse, karar sayfasından önce bir bulgu raporu üret:

- Alan başına bir analizci ve bir şüpheci doğrulayıcı (ikisi de ucuz model). Analizci şu sınıfları kullanır: `removed`, `replaced`, `changed`, `incompatible`, `partial`, `kept`, `new`, `doc-drift`. Her bulgu kanıt ister: belge yol:satır, kod yol:satır, gerekçe ve gerekçenin kaynağı (`documented`, `commit`, `inferred`, `none`).
- Doğrulayıcı her bulguyu çürütmeye çalışır; `confirmed`, `corrected`, `refuted` ya da `unverifiable` döner ve kaçırılanları ekler.
- Sonunda bir tamlık eleştirmeni kapsanmayan belge ve modülleri arar; bulduklarına ek analizciler çalışır.
- Rapor `<teslim klasörü>/<tarih>-<konu>-uyum-analizi.md` olur.

Bu bulgular karar kalemi DEĞİLDİR. Yalnız yazarlara "uygulamada ne var" ipucu olarak verilir.

## 4. Kontrol listesi: ince kalem çıkarımı

- Belge parçası başına bir ucuz model ajanı, belgenin bütün normatif içeriğini orta ayrıntıda kalemlere çıkarır. Ölçü: 400 satıra 20-40 kalem. Her kalemde `doc`, `lines`, `title`, `spec` (en çok 3 cümle) bulunur.
- Bu liste yalnız eksiksizlik denetimi içindir; sayfada gösterilmez.

## 5. Alan yazarları ve inceleyiciler

- **Yazar** (oturum modeli; tasarım muhakemesi istediği için ucuz modele verilmez, bunu kullanıcıya söyle): alanın belgelerini baştan sona okur ve 4-15 genel kalem kurar. Her kalemin `points` listesine konunun tüm spesifikasyon maddelerini sade tek cümleler halinde yazar. Her madde için uygulamadaki `status`, `current` ve `action` değerlerini verir. Kalem kartları kısa olur.
- **İnceleyici** (ucuz model): kontrol listesine göre eksik maddeleri ekler (`add_points`), en az 10 maddenin durumunu dosyaları açarak doğrular (`fix_points`) ve üslubu düzeltir (`patches`).
- Pipeline kur, bariyer koyma: her yazarın çıktısı biter bitmez kendi inceleyicisine gider.
- `fix_points` için istemde maddeleri 0 tabanlı `i` ile numaralı ver ve inceleyiciden `i` ile birlikte maddenin ilk 40 karakterini iste; uygularken ikisini karşılaştır.

## 6. Tasarım desenleri

- **Tarama** (ucuz model, paralel):
  - Belge taramaları: desen adının geçtiği ya da yapıdan anlaşılan kullanımlar. Örneğin "listener kaydı ve abonelik iptali" Observer'dır, "draft → save/cancel" Memento'dur, "provider descriptor + üretilmiş kayıt" Registry/Abstract Factory'dir.
  - Kod taramaları: sınıf adları (`*Factory`, `*Builder`, `*Listener` …), reaktif akışlar, sealed tipler, DI kayıtları, `Abstract*`/`*Base` sınıflar.
- **Yazar** (oturum modeli): desen ailesi başına bir kalem. En az şunlar: Mediator, Observer/Publish-Subscribe, Factory/Abstract Factory, Builder, Strategy, Adapter/Ports & Adapters, Facade, Command/Undo, Memento, State, Registry/Microkernel, Template Method, Composite, Decorator, Null Object, Repository, Value Object, MVVM, DI/Composition Root, Anti-Corruption Layer, Interpreter, Event Sourcing. `parts` alanı kullanım yerleridir (`title`, `status`, `ref`).
- Spesifikasyonda olup kodda olmayan desen mutlaka kalem olur. Hiçbir yerde olmayan desen kalem olmaz.

## 7. Kapsama denetimi

Bir ucuz model ajanı belgelerin `##` başlıklarını kalemlerin kapsadığı bölümlerle karşılaştırır ve kapsanmayan **genel** konuları listeler. Gerçek boşluklar ilgili alana genel kalem olarak eklenir. Sık çıkan örnekler: sistem geneli hata ve bozulma modeli, sürümleme ve geriye uyumluluk politikası.

## 8. Uygulama sütununu sadeleştirme

- Programla: `status == removed` olan her maddenin `current` değeri `Yok.` olur.
- Kalan maddeler 380 maddelik parçalar halinde ucuz model ajanlarına gider. Kural: yalnız var olanı yaz. Açıklama, karşılaştırma, plan notu ve değerlendirme yazılmaz.
- Çıktıyı `{id, i, current}` satırları olarak iste; `i` maddenin 0 tabanlı sırasıdır ve istemde her maddenin yanında açıkça verilir. Dizi olarak istenirse ajanlar sayıyı kaçırıyor.

## 9. Derleme, test ve teslim

```bash
SK=~/.claude/skills/spec-decision-page
python -I -X utf8 $SK/scripts/validate_seed.py seed.json
python -I -X utf8 $SK/scripts/build_page.py $SK/assets/template.html seed.json page.html
python -I -X utf8 $SK/scripts/build_offline.py page.html <font klasörü | -> out.html
python -I -X utf8 $SK/scripts/build_offline.py page.html <font klasörü | -> out-test.html --test-hook
```

Font klasörü: `Inter-Regular.ttf`, `Inter-Medium.ttf`, `Inter-SemiBold.ttf` ve `JetBrainsMono-Regular.ttf` dosyalarını içeren bir klasör (ör. ürünün UI kitindeki font kaynakları), yoksa `-`.

Test:

- Geçici klasörü `python -I -m http.server <port> --bind 127.0.0.1 --directory <klasör>` ile sun ve tarayıcıda `http://127.0.0.1:<port>/out-test.html` aç. Yerel dosya yolu bazı gömülü tarayıcılarda açılmaz.
- Kalem ve grup sayısını, konsol hatasını, yasak kelimeyi ve 375 px genişlikte yatay taşmayı kontrol et.
- Kayıt dosyası akışını OPFS ile dene: `navigator.storage.getDirectory()` → `getFileHandle('t.json',{create:true})` → `__sdpTest.attach(h,'new')`. Ardından bir kalem seç, kararla ve dosyayı oku. Testten sonra OPFS dosyasını, `localStorage`'ı ve IndexedDB'yi temizle.
- Gerçek işletim sistemi dosya seçicisini otomatik testte deneyemezsin; bunu kullanıcıya söyle.

Teslim:

- `--test-hook` olmadan derlenmiş dosyayı `<teslim klasörü>/<tarih>-<konu>.html` olarak kopyala ve `"testHook":true` geçmediğini kontrol et.
- Kullanıcı istemedikçe yayınlama; yerel dosya teslim edilir.
- Commit etme; kullanıcı isterse ayrıca sor.

## 10. Uygulama reposu değişirse

Çalışma sürerken uygulama reposuna yeni commit gelebilir; bir yapı değişikliği binlerce dosyayı taşıyabilir. Teslimden önce `git -C <repo> log -5` ve `git reflog -5` ile bak.

- Değiştiyse: `git diff --name-status -M <eski>..<yeni>` ile taşıma haritasını çıkar, dizin düzeyinde özetle ve alan başına bir "Şu anki tazeleme" ajanıyla bir doğrulayıcı çalıştır.
- Font ve yol gibi sabitleri de yeni yerlerine göre güncelle.

## 11. Ajan istemi parçaları

Her yazar ve inceleyici istemine şu blok konur. Köşeli parantezli yerleri projeye göre doldur:

```text
KULLANICININ KURALLARI:
1) Kalem = GENEL konu (belgenin ana konusu); gruplama mantıklı olsun; ince ayrıntı ayrı kalem olmaz.
2) SPESİFİKASYON İÇERİĞİ EKSİLTİLMEZ: her kalemin points listesi o konunun belgelerdeki TÜM gereksinim ve kararlarını içerir; her madde sade tek cümle; teknik adlar korunur.
3) SADE dil.
4) Uygulama sütunu yalnız var olanı yazar; yoksa "Yok." Açıklama, karşılaştırma, plan notu yok.
5) Kalem kartları kısa: özetler tek cümle, ayrıntılar en çok 2 cümle.
6) "değişmez/değişmezler/invariant" terimi hiçbir alanda geçmez (fiil gerekiyorsa "değiştirilmez").
7) Kabul edilmiş kararlar korunur: [ör. "iletişim omurgası X kabul edildi; teklifler Y'ye dönüş önermez"].
8) Uygulamaya sonradan eklenenler ayrı kalem olmaz; tasarım farkı yaratıyorlarsa ilgili kalemde geçer.
9) [Önceliği düşük alan] yalnız genel düzeyde; yazılım yapısı önceliklidir.
10) Salt okunur çalış; hiçbir dosyayı değiştirme.
```

## 12. Bilinen tuzaklar

- `python -I` `PYTHONIOENCODING` değişkenini yok sayar. UTF-8 çıktı için `-X utf8` kullan.
- "değişmez" toplu değiştirilirken fiil kullanımları bozulur ("…düzenlemeyle değişmez" → "…düzenlemeyle değiştirilmez"). Değiştirmeden önce bağlama bak.
- Gruplar arası tekrar ayıklayıcı fazla agresif olabilir; şemsiye kalemleri alakasız bir kaleme birleştirebilir. Kümeleri tek tek gözden geçir ve yanlış olanı uygulama.
- Ajanlar kalemleri bulgulardan türetirse sayfa ince ve anlamsız kalemlerle dolar. Kalemleri her zaman belgelerin genel konularından türet; bulguları yalnız ipucu olarak kullan.
- Ajanlara "kısa yaz" denince spesifikasyon içeriğini atarlar. "Kısa" yalnız kartlar içindir; maddeler eksiksiz olur.
- `file://` altındaki sayfalar aynı `localStorage`'ı paylaşabilir. Her sayfaya ayrı `meta.storeKey` ver.
- Uzun bir yeniden yazım sırasında kullanıcı yön değiştirirse, çalışan workflow'u durdurup yeni kurallarla yeniden başlatmak çoğu zaman yamamaktan ucuzdur. Yarıda olan yazarlar bittiyse ise sonuçlarını tut ve yalnız gereken adımı ek geçiş olarak çalıştır.
