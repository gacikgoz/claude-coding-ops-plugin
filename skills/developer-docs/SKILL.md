---
name: developer-docs
description: Kod yazacak ya da değiştirecek geliştiricilere yönelik dokümantasyon üretir ve bakımını yapar; interaktif kısmı geliştiriciye yönelik öğrenme sitesidir. Kapsamı süreç belgeleri (API/geliştirici rehberi, sınıf envanteri, teslim raporu, iş günlüğü, plan ve dilimler, "bugünkü durum" repo yapısı belgesi ve mevcut mimari diyagramı), uygulama izleyicisi ve kanıt dosyaları ile koddan türetilen, çevrimdışı çalışan interaktif öğrenme sitesi (dersler, adım adım akışlar, sınavlar, sınıf atlası, sözleşme kataloğu, test haritası, hash'li kaynak indeksi ve doğrulayıcı). Kullanıcı "geliştirici dokümantasyonu", "developer docs", "developer guide", "API rehberi", "geliştirici onboarding", "öğrenme sitesi", "ders yaz", "sınıf envanteri", "teslim raporu", "sprint raporu", "iş günlüğü", "repo yapısı belgesi", "mevcut yapı diyagramı", "kanıt / evidence", "izleyiciyi güncelle" dediğinde ya da kod değişikliğinin geliştirici belgelerine yansıtılması gerektiğinde bu skill'i kullan. Son kullanıcı kılavuzu için user-guide, spesifikasyon için spec-authoring skill'ini kullan.
---

# Geliştirici dokümantasyonu

Geliştirici dokümantasyonu, kodu yazacak ya da değiştirecek kişinin sistemi doğru öğrenmesi ve yaptığı işin izini bırakması içindir. Spesifikasyondan farkı şudur: spesifikasyon hedefi anlatır, geliştirici belgesi bugünkü kodu, nasıl kullanılacağını ve neyin kanıtlandığını anlatır.

**Hangi skill?** Okur kod yazacak ya da değiştirecekse bu skill (öğrenme sitesi gibi interaktif kısımlar dahil). Okur ürünü kullanan kişiyse `user-guide`. Hedef mimari, sözleşme ya da karar yazılıyorsa `spec-authoring`.

Bu skill hazır bir site iskeleti sağlamaz; site ve üreticiler aşağıdaki sözleşmeye göre projede yazılır. Skill ile gelen betikler: `hash_index.py` ve `validate_site.py`.

## Önce projeyi öğren

- Mevcut belge düzeni: belge indeksi, plan/dilim belgeleri, sprint belgeleri, izleyici, kanıt klasörü, öğrenme sitesi varsa yeri ve üreticisi.
- Belge dili ve kullanıcıyla iletişim dili. Örneğin süreç belgeleri Türkçe, spesifikasyonlar İngilizce olabilir.
- Kod tabanının dilleri, modül kökleri, test kökleri ve sözleşme dosyaları (şema, proto, üretilmiş kayıtlar).

Projede düzen yoksa bu skill'deki yapıları öner ve onayla kur.

## Belge türleri

Dokümantasyonu üç türe ayır ve her birine ayrı biçim ver. Şablonlar `references/doc-templates.md` içinde.

**A. Süreç belgeleri (Markdown, elle):**

| Belge | Ne zaman | İçerik |
| --- | --- | --- |
| API / geliştirici rehberi | Bir özelliği başka geliştiriciler kullanacaksa | Künye, temel ilkeler, API öğeleri başvurusu (sınıf, fonksiyon, anotasyon, komut), birleşik örnek, konfigürasyon, yaşam döngüsü ve hata yalıtımı, eksiksiz şablon kod, sık hatalar ve kontrol listesi |
| Sınıf envanteri | Bir sprint/dilim kod ekleyip kaldırdığında | Eklenen, değişen ve emekliye ayrılan sınıflar modül modül; sınırlar, bağımlılık diyagramı, sahiplik ve yaşam döngüsü matrisi, eski→yeni test eşlemesi |
| Teslim raporu | Bir dilim teslim edildiğinde | Künye (tarih, dal, başlangıç commit, durum), yönetici özeti, bulgu → çözüm → kanıt testi matrisi, doğrulama sonuçları, git durumu |
| İş günlüğü | Uygulama sırasında | Kod tabanı bulguları, kararlar, eski→yeni geçiş tablosu, kaldırılan kod, inceleme turlarının kök nedenleri |
| Plan ve dilimler | İş başlamadan | Kapsam / kapsam dışı, hedef yapı, dilim tablosu ve durum işaretleri, plan içi açık kararlar (K1, K2 …; proje bir karar defteri kullanıyorsa orada `Q-nnn` olarak açılır ve buradan bağlanır) |
| Repo yapısı belgesi | Yapı değiştiğinde | "Bugünkü durum": durum satırı, ağaç, profiller, modül tablosu, bağımlılık yönü, adlandırma kuralı, planlanan modüller ayrı tabloda |
| Mevcut durum mimari belgesi ve diyagramı | Kod yapısı değiştiğinde | Bugünkü sistemi anlatan tek ve sürümlü belge; diyagram metin kaynağından (Mermaid) üretilir, svg/png yanında tutulur. Hedef mimari `spec-authoring`'in işidir; burada yalnız bağlantısı verilir |
| Değişiklik kaydı | Her revizyonda | Ne değişti, belge tarafında ne değişti, neye dokunulmadı, nereden okundu |

**B. İzleyici ve kanıt:** uygulama durumunu izleyen tablo (ör. `IMPLEMENTATION.md`) ve kanıt klasörü (`docs/verification/<YYYY-MM-DD>/<dilim-id>/`). Kurallar aşağıda.

**C. İnteraktif öğrenme sitesi:** elle yazılan dersler, koddan üretilen başvuru sayfaları ve hash'li kaynak indeksleri. Yöntem `references/learning-site.md` içinde.

## Dürüstlük kuralları

Bu kurallar belgelerin güvenilir kalmasını sağlar. Okuyan kişi belgedeki her iddiaya güvenebilmeli.

1. **Durum yalnız kanıtla yükselir.** Kanıt dört şeydir: komut, ortam, tarih ve sonuç. Çalıştırılmayan test için "not run" yazılır. Bir derleme tanım dosyasının (pom, csproj, package.json …), iskeletin ya da arayüzün varlığı durumu yükseltmez. Tek başına bir betik, kodlayıcı ya da şema tanımı uçtan uca akışı kanıtlamaz.
2. **Kapsam dar söylenir.** "VERIFIED" yalnız o satırın kapsamı için geçerlidir; gerekirse "VERIFIED: model only" gibi sınır eklenir.
3. **Geçmiş yeniden etiketlenmez.** Eski geçiş ve hata kayıtları kendi artefakt hash'iyle kalır. Yeni teslim eskisini geçersiz kılıyorsa eski rapora "superseded by" notu düşülür; içerik silinmez.
4. **Sayılar kaynağıyla verilir.** Test sayısı gibi değerler yalnız üretildiği koşunun kapsamıyla verilir; yeni koşu iddia edilmez. Bildirim sayısı (ör. test metodu sayısı) koşu sonucu değildir; bu açıkça yazılır.
5. **Repoda olmayana yalnız adla gönderme yapma.** Gerekli olanı repoya al ya da özetini belgeye yaz. Başka repolara giden bağlantıları "o repo yan yana klonlanınca açılır" diye belirt.
6. **Yeniden adlandırmaları açıkça yaz.** Eski ve yeni adlar yan yana kullanılıyorsa "güncel durum" bölümünde eşlemeyi ver.
7. **"invariant / değişmez" terimini kullanma.** Kullanıcı tercihidir; yerine kural ya da ilke de, fiil için "değiştirilmez" yaz (ayrıntı: `spec-authoring` kural 11).
8. **Desenler görünür olur.** Öğrenme sitesinde bir desen haritası sayfası tutulur: desen → koddaki yer → spesifikasyondaki yer. Sınıf envanterinde her sınıfın rolü varsa desen adıyla yazılır.

## İzleyici satırı ve kanıt

- İzleyicide her satırın tek sahibi, sonraki yürütülebilir görevi ve test kapısı vardır. Sütunlar: `ID | Requirements | Owner | Deliverable | Depends | State | Acceptance test/evidence`.
- Durum sözlüğü (projede yoksa bunu öner): SPECIFIED, SCAFFOLDED, PARTIAL, IMPLEMENTED, VERIFIED, RELEASE_READY.
- Her değişiklikte etkilenen satır aynı değişiklikte güncellenir. Satır sayıları değişince yeniden sayılır. Değişiklik günlüğüne tarihli bir satır eklenir ve hangi üretim satırlarının ilerlemediği açıkça yazılır.
- Kanıt dosyası (`evidence.md`) yedi alanlı bir tabloyla başlar: tracker/gereksinim ID'leri, kaynak revizyonu ve fixture/şema sürümleri, ortam, komut, sonuç, gözlenen sınırlar, bilinen boşluk ve sonraki görev. Ardından komutlar ve ham log yolları gelir. Sırlar ve hassas veriler redakte edilir.
- Tarih klasörü kanıtın üretildiği günü gösterir. Eski klasör yeniden yazılmaz; yeni sonuç yeni klasöre girer.

## Kod değişince ne güncellenir

1. Etkilenen izleyici satırları ve kanıt.
2. Repo yapısı belgesi (modül, paket ya da yol değiştiyse) ve gerekiyorsa kök README.
3. API / geliştirici rehberi ve sınıf envanteri (API ya da sınıf değiştiyse).
4. Öğrenme sitesi, bu sırayla: (a) **eski** indeksle `hash_index.py check` çalıştır ve bayat kaynakları listele; (b) bu kaynaklara bağlı dersleri koda göre güncelle ve değişiklik kaydına yaz, eski anlatım değiştiyse derse "Not" kutusuyla eski ve yeni davranışı yaz; (c) indeksi `--merge` ile yeniden üret; (d) `validate_site.py` çalıştır. İndeksi önce yeniden üretirsen hash'ler hep eşleşir ve bayat dersler görünmez.
5. Sözleşme ya da davranış değiştiyse spesifikasyon tarafı için `spec-authoring` skill'ini kullan.

## Betikler

- `scripts/hash_index.py`: belirtilen kök ve kalıplardaki dosyaların SHA-256 ve satır sayısını tarihli bir JSON indekse yazar. Bir indeksi diskteki dosyalarla karşılaştırıp bayatlamış kayıtları da listeler.
- `scripts/validate_site.py`: statik bir HTML sitesinde yerel bağlantıları, sayfa içi çapaları ve dış başvuruları denetler, isteğe bağlı olarak hash indeksinin güncelliğini kontrol eder. Sonucu `VALIDATION.json` olarak yazar. `failures` boş değilse siteyi yayınlama.

```bash
# ör. --include "src/**/*.java", "**/*.cs", "app/**/*.py"; varsayılan dışlamalar: target, build, node_modules, .git, bin, obj
python -I -X utf8 ~/.claude/skills/developer-docs/scripts/hash_index.py check --root . --index docs/learning/SOURCE_INDEX.json
python -I -X utf8 ~/.claude/skills/developer-docs/scripts/hash_index.py build --merge --root . --include "src/**/*.java" --out docs/learning/SOURCE_INDEX.json
python -I -X utf8 ~/.claude/skills/developer-docs/scripts/validate_site.py --site docs/learning/site --index docs/learning/SOURCE_INDEX.json --root . --out docs/learning/VALIDATION.json
```

Hash'ler satır sonları LF'ye normalleştirilerek hesaplanır; başka bir araçla üretilmiş indeksler ham baytı hash'liyor olabilir, karıştırma. `validate_site.py` JavaScript ile çalışma anında üretilen bağlantıları denetlemez.

Sınıf atlası gibi imza çıkarımı dile özgüdür. Proje dilinde bir ayrıştırıcıyla (Java için JavaParser, C# için Roslyn, Python için `ast`) ya da basit ve belgelenmiş düzenli ifadelerle üret. Üretici betiği belgeyle aynı repoda tut; dışarıda kalırsa yeniden üretilemez.
