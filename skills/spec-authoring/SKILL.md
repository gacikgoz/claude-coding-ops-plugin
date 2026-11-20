---
name: spec-authoring
description: Yazılım spesifikasyonu yazar ve günceller. Kapsamı sistem mimarisi otorite belgesi (master architecture), alt sistem/modül spesifikasyonları, kesişen mimari belgeleri, gereksinim kaydı, uçtan uca örnek spesifikasyonu, tutarlılık denetimi, ADR ve karar defteri. Dürüst durum satırları, sahiplik (owns / must not own) tabloları, sözleşmeler, gözlemlenebilir kabul kapıları, kararlı kimlikler ve belge senkron kuralını uygular. Kullanıcı "spesifikasyon yaz", "mimari belge", "modül spesifikasyonu", "master architecture", "gereksinim kaydı", "requirements", "ADR yaz", "karar kaydı", "tasarım dokümanı", "sistem tasarımı belgele", "spec güncelle" dediğinde ya da bir özellik, alt sistem veya mimari kararın kalıcı bir spesifikasyona dönüştürülmesi gerektiğinde bu skill'i kullan. Geliştirici kılavuzu ve öğrenme sitesi için developer-docs, son kullanıcı kılavuzu için user-guide, spesifikasyonu kodla kıyaslamak için spec-decision-page skill'ini kullan.
---

# Yazılım spesifikasyonu yazımı

Spesifikasyon, sistemin ne yapması gerektiğinin ve kimin neye sahip olduğunun kalıcı kaydıdır. İyi bir spesifikasyon seti iki şeyi aynı anda sağlar: bir geliştirici yalnız belgeye bakarak doğru sınırları ve sözleşmeleri uygulayabilir, ve herkes belgenin neyi iddia edip neyi etmediğini açıkça görür.

## Önce projenin belge sistemini öğren

Yazmadan önce projede ne varsa onu izle; yeni bir düzen icat etme:

- Belge dizini ve indeksi (`docs/README.md` ya da eşdeğeri), otorite belge, mevcut modül ve mimari belgeleri.
- Durum sözlüğü (öneri ve tanımlar `developer-docs` skill'inde), kimlik aileleri (ör. gereksinim `SYS-001`, karar `D-012`, açık soru `Q-003`, kabul vakası `AC-21`), tarih biçimi.
- Karar kayıtları (ADR'ler, karar defteri) ve hangi tür kararın nereye yazıldığı.
- Belge dili ve kullanıcıyla iletişim dili. Bazı projelerde belgeler İngilizce, iletişim Türkçedir. Bilmiyorsan bir kez sor.

Projede böyle bir sistem yoksa `references/templates.md` içindeki standart düzeni öner ve kullanıcının onayıyla kur.

## Belge türleri ve rolleri

| Belge | Rolü |
| --- | --- |
| Otorite belge (master architecture) | Sistem geneli ilkeler, modül kataloğu, bağımlılık yönü, kesişen kararlar, mimari kurallar, belge haritası, değişiklik protokolü. Sistem geneli kuralların tek kaynağı. |
| Alt sistem / modül spesifikasyonu | Bir alt sistemin sahipliği, sınırları, sözleşmeleri, yaşam döngüsü, hata davranışı, kabul kapıları ve mevcut kodla hedefin farkı. Kendi alanının ayrıntı otoritesi. |
| Kesişen mimari belgesi | Konfigürasyon, güvenlik, gözlemlenebilirlik, dağıtım, backend sınırları gibi birden çok alt sistemi kesen konular. |
| Gereksinim kaydı | Kabul edilmiş her isteğin kararlı ID'si, sahip belgesi ve dürüst teslim durumu. Tamamlanma raporu değil, izlenebilirlik indeksidir. |
| Uçtan uca örnek spesifikasyonu | Gerçek bir senaryo üzerinden tüm katmanları bağlayan referans: kimlikler, veri, wire sözleşmesi, iş akışı, hata, izinler, kabul. |
| Tutarlılık denetimi | Belgeler arası sınırların tek ve uyumlu sözleşme verip vermediğinin tarihli kontrolü ve kalan kanıt kapıları. |
| ADR | Kütüphane, yerleşim, sürüm ve sahiplik gibi kararlar; bağlam, karar, sonuç, geçici sapma ve çıkış koşulu. |
| Karar defteri | Sahibin tek tek kararları (`D-nnn`) ve açık sorular (`Q-nnn`). Eski satır silinmez, "superseded" işaretlenir. |

Şablonlar: `references/templates.md`.

Sınır: bu skill **hedef** mimariyi ve kararları yazar. Bugünkü kodun yapısını anlatan belge ve diyagramlar (repo yapısı, mevcut durum mimarisi), süreç belgeleri, izleyici ve kanıt `developer-docs` skill'inin işidir; son kullanıcı belgeleri `user-guide` skill'inin.

## Yazım kuralları

1. **Dürüst durum satırı.** Her belge `Status` satırıyla açılır ve gerçek olgunluğu söyler: yalnız spesifikasyon mu, iskelet mi, kısmi kod mu? Spesifikasyon yazmak uygulama tamamlandı demek değildir. Uygulanan kısım varsa tarih ve kanıtıyla belirtilir.
2. **Hedef ile mevcut ayrı tutulur.** Mimari cümleler hedefi anlatır. Var olan dosya ya da iskelet açıkça "mevcut" diye yazılır. Belgenin son bölümü mevcut kodun hedeften farkını söyler. Diyagramın altına bunun bir hedef sahiplik görünümü olduğu, uygulama raporu olmadığı yazılır.
3. **Sahiplik açıkça yazılır.** Her bileşen için "Owns" ve "Must not own" sütunları olan bir tablo kullanılır; ikinci sütun komşu bileşene ait olanları adıyla sayar ve boş bırakılmaz. Sahiplik belirsizliği uygulamada çift sahiplik ve kaçak bağımlılık olarak geri döner.
4. **Sözleşmeler somuttur.** Kimlik, şema, sürüm, yaşam döngüsü, eşzamanlılık, hata ve kapanış davranışı, birimler ve sınır değerler adıyla ve değeriyle yazılır. Sürümler tam yazılır; doğrulanmamış sayı test edilmiş sabit gibi sunulmaz.
5. **Kabul kapıları gözlemlenebilirdir.** Her kapı numaralıdır, kalın bir etiketle başlar ve hem olumlu hem olumsuz durumları içerir: başarı, bozuk girdi, zaman aşımı veya çakışma, kapatma ve yeniden başlatma, reddedilen yetki. Sayısal hedefler "ölçülmüş garanti değil, kabul hedefi" diye etiketlenir ve başarısızlık ölçütü yazılır.
6. **Kimlikler kararlıdır.** Gereksinim, karar, soru ve kabul vakası ID'leri asla yeniden numaralanmaz ve yeniden kullanılmaz. Değişen karar yeni satırla yazılır; eskisi kalır ve "superseded by" ile işaretlenir.
7. **Kullanıcının girdisi uydurulmaz.** Kullanıcıya ait alan bilgisi (gerçek paket şemaları, dağıtım profilleri …) belge içinde icat edilmez. Bunlar "sonra sağlanacak girdiler" listesine yazılır; genel davranış açıkça etiketli sentetik fixture ile ilerletilir.
8. **Açık sorular kaybolmaz.** Serbest "TODO" bölümü yazılmaz. Karar bekleyen konular karar defterinde `Q-nnn` olarak, kalan girdiler gereksinim kaydının sonunda, kalan kanıtlar tutarlılık denetiminde tutulur.
9. **Bağlantılar göreli ve çapalıdır.** Belgeler arası bağlantılar göreli Markdown linkidir ve bölüm çapası içerir. Metin içi iç referans "section 6" gibi yazılır; ID'ler kod aralığında yazılır.
10. **Üslup normatif ve sadedir.** "must", "never", "owns … does not own …", "is a … not a …" kalıpları kullanılır. Gereksiz süs ve dolgu yazılmaz. Kısaltmalar ilk geçtiği yerde açılır.
11. **"invariant / değişmez" terimini kullanma.** Kullanıcı tercihidir ve her projede uygulanır: terim okuru yanıltıyor; yerine kural, ilke ya da gereksinim de. Sistem geneli kesin kurallar bölümünün adı "Architectural rules" ya da "Mimari kurallar" olur. Fiil kullanımı gerekiyorsa "değiştirilmez" yaz.
12. **Sadeleştirirken içerik atma.** "Daha sade yaz" isteği dili sadeleştirmek demektir; gereksinim, değer ve kararlar korunur. Uzun bir belgeyi kısaltman gerekiyorsa ayrıntıyı alt belgeye taşı, silme.
13. **Yazılım yapısı önceliklidir.** Sınırlar, sahiplik, sözleşmeler ve desenler görsel ayrıntıdan önce gelir. Renk, ölçü, tipografi gibi görsel değerler yalnız genel düzeyde ve ayrı tasarım belgelerinde tutulur; modül spesifikasyonu davranışı, kimliği, yaşam döngüsünü ve kabulü yazar.
14. **Desenler adıyla yazılır.** Her alt sistem kullandığı tasarım desenlerini (Mediator, Observer/Publish-Subscribe, Factory/Abstract Factory, Builder, Strategy, Command, Adapter, Facade, State, Registry, Repository …) nerede ve hangi rolle kullandığıyla birlikte bir tabloda yazar. Desen adı, uygulayan geliştiriciye niyeti tek kelimeyle aktarır ve tasarım–kod karşılaştırmasını mümkün kılar.
15. **Konular genel düzeydedir.** Bölümler belgenin genel tasarım konularını izler; tek bir dosya, ayar ya da sınıf kendi başına bölüm olmaz, ilgili konunun içinde geçer.

## Değişiklik protokolü

Bir spesifikasyon değişikliği tek belgede kalmaz:

1. Değişikliğin kabul edilmiş kararlarla çatışıp çatışmadığına bak. Görünür bir çelişki varsa sessizce birini seçme; açıkça çöz ve kullanıcıya söyle.
2. Sahip belgeyi güncelle: kapsam, sahiplik, sözleşme, yaşam döngüsü, kabul.
3. Aynı değişiklikte bağlı belgeleri güncelle: sistem geneli bir kural değiştiyse otorite belge ve etkilenen tüm alt spesifikasyonlar; durum ya da kapsam değiştiyse gereksinim kaydı; varsa uygulama izleyicisi ve kök README. Belge haritasına ve indekse yeni belgeyi ekle.
4. Karar türüne göre kaydet: kütüphane, yerleşim ve sürüm seçimi için ADR; sahibin tekil kararı için karar defteri satırı. Projede aşamaya bağlı farklı karar kuralları tanımlıysa (ör. bir tasarım dondurma dönemi), geçerli olanı proje belgesinden doğrula.
5. Yerel bağlantıları ve çapaları denetle. Kırık bağlantı bırakma.

Kod varlığı bir görevi tamamlamaz. Durum yalnız kanıtla yükselir: komut, ortam, tarih, sonuç. Çalıştırılmayan test için "not run" yazılır. Kanıt ve izleyici kuralları için `developer-docs` skill'ine bak.

## Yeni bir alt sistem spesifikasyonu yazarken

1. Kullanıcının isteklerini ve kararlarını "Recorded requirement → Architectural result" tablosuna çevir.
2. Hedef sınırları ve akışı bir diyagramla (Mermaid), sahiplik tablosuyla ve desen tablosuyla ver.
3. Sözleşmeleri, yaşam döngüsünü, eşzamanlılığı, hata ve güvenlik davranışını yaz.
4. Kabul kapılarını, uygulama sırasını ve hazır olma kapılarını yaz; kalan girdileri listele.
5. "Current source versus target" bölümüyle bitir.
6. Otorite belgenin modül kataloğuna, belge haritasına ve gereksinim kaydına satırları ekle.

## Gözden geçirme listesi

- Durum satırı gerçeği söylüyor mu; hedef ve mevcut ayrımı var mı?
- Her bileşenin "Owns / Must not own" satırı dolu mu; desenler adıyla ve kullanım yeriyle yazıldı mı?
- Kabul kapıları gözlemlenebilir mi; olumsuz durumlar var mı?
- ID'ler kararlı ve tekil mi; superseded satırlar korunuyor mu?
- Otorite belge, gereksinim kaydı, indeks ve izleyici aynı değişiklikte güncellendi mi?
- Kullanıcıya ait bilgi uydurulmuş mu?
- Yasak terim ("invariant / değişmez") geçiyor mu?
- Sadeleştirme sırasında içerik kaybolmuş mu?
