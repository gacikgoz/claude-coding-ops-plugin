# claude-coding-ops-plugin

Claude Code için yazılım dokümantasyonu iş akışı skill'leri. Depo hem bir plugin (ve onu listeleyen bir marketplace) hem de tek tek kopyalanabilen skill klasörleri içerir.

> Documentation workflow skills for Claude Code: specification authoring, developer documentation with an interactive learning site, interactive end-user guides, and an offline spec-vs-code decision page. The skill instructions are written in Turkish.

## Skill'ler

| Skill | Ne için | Okur |
| --- | --- | --- |
| [`spec-authoring`](skills/spec-authoring/SKILL.md) | Hedef mimari belgesi, modül ve kesişen spesifikasyonlar, gereksinim kaydı, ADR ve karar defteri. Sahiplik tabloları, sözleşmeler, gözlemlenebilir kabul kapıları, desen tabloları, kararlı kimlikler. | Tasarım yapan ve kararı veren kişi |
| [`developer-docs`](skills/developer-docs/SKILL.md) | API / geliştirici rehberi, sınıf envanteri, teslim raporu, iş günlüğü, plan, bugünkü repo yapısı ve mimarisi, uygulama izleyicisi ve kanıt. İnteraktif kısmı: dersler, adım adım akışlar ve sınavlar içeren, kaynak indeksiyle bayatlığı denetlenen çevrimdışı öğrenme sitesi. | Kod yazacak ya da değiştirecek geliştirici |
| [`user-guide`](skills/user-guide/SKILL.md) | Çevrimdışı, aranabilir, bir ya da daha çok dilli kullanım kılavuzu: tıklanabilir ana pencere şeması, görevli ürün simülatörü, üründen üretilen ekran görüntüleri ve görsel kimlik. | Ürünü kullanan, kod yazmayan kişi |
| [`spec-decision-page`](skills/spec-decision-page/SKILL.md) | Spesifikasyon setini kodla karşılaştırıp her genel konu için Önerilen / Şu anki / Teklif edilen tasarımı ve Kabul / Ertele / Red kararını içeren çevrimdışı karar sayfası üretir; kararlar seçilen bir JSON dosyasına yazılır. | Tasarım uyumuna karar veren kişi |

Her skill'in başında hangi işin hangi skill'e ait olduğu yazılıdır: hedef mimari `spec-authoring`'de, bugünkü yapı `developer-docs`'ta, son kullanıcı belgesi `user-guide`'da.

## Kurulum

### Plugin olarak

Claude Code içinde:

```text
/plugin marketplace add gacikgoz/claude-coding-ops-plugin
/plugin install coding-ops@claude-coding-ops
```

Skill'ler `coding-ops:spec-authoring` biçiminde adlarla görünür ve istekle eşleşince kendiliğinden yüklenir.

### Yalnız skill olarak

`skills/` altındaki klasörlerden istediğini kopyala:

- kişisel kullanım için `~/.claude/skills/<skill-adı>/`,
- ekiple paylaşmak için projenin `.claude/skills/<skill-adı>/` klasörü.

## Gereksinimler

- Betikler için Python 3 (3.13 ile denendi). Betikler standart kütüphane dışında yalnız `fontTools` kullanır: `spec-decision-page` fontları sayfaya gömerken gerekir (`pip install fonttools`; `brotli` da kuruluysa fontlar daha küçük WOFF2 olarak gömülür). Font klasörü verilmezse sayfa sistem fontuyla çalışır.
- Karar sayfasının kayıt dosyası için Edge ya da Chrome (File System Access API). Diğer tarayıcılarda kararlar tarayıcıda saklanır ve JSON olarak dışa aktarılır.

## Yapı

```text
.claude-plugin/
  plugin.json          plugin tanımı
  marketplace.json     bu depoyu marketplace olarak ekleyebilmek için
skills/
  spec-authoring/      SKILL.md, references/
  developer-docs/      SKILL.md, references/, scripts/ (hash_index.py, validate_site.py)
  user-guide/          SKILL.md, references/, scripts/ (check_guide.py)
  spec-decision-page/  SKILL.md, references/, scripts/ (validate_seed.py, build_page.py, build_offline.py), assets/template.html
```

## Lisans

[MIT](LICENSE)
