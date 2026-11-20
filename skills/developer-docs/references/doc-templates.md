# Geliştirici belgesi şablonları

Başlıklar belge diline çevrilebilir; yapı korunur. Köşeli parantezli yerler doldurulur.

## İçindekiler

1. Künye (bütün sprint/dilim belgeleri)
2. API / geliştirici rehberi
3. Sınıf envanteri
4. Teslim raporu
5. İş günlüğü
6. Plan ve dilimler
7. Repo yapısı ("bugünkü durum")
8. İzleyici satırları ve değişiklik günlüğü
9. Kanıt dosyası
10. Teslim notu (araç, demo ya da paket teslimi)

## 1. Künye

```markdown
| Alan | Değer |
| --- | --- |
| Sprint / dilim | [S6] |
| Modül | [modül] |
| Hedef kitle | [UI geliştiricileri …] |
| Dal | [branch] |
| Başlangıç commit | [sha] |
| Tarih | [YYYY-MM-DD] |
| Durum | [Tamamlandı / İnceleme turu 2 …] |
```

## 2. API / geliştirici rehberi

```markdown
# [Özellik] geliştirici rehberi
[Künye]
## 1. Temel ilkeler
## 2. API başvurusu          (her API öğesi — sınıf, fonksiyon, anotasyon, komut — için ayrı alt bölüm: amaç, imza, parametreler, örnek)
## 3. Tek bileşende birleşik kullanım
## 4. Konfigürasyon           (ör. hız sınırı, kuyruk, taşma stratejisi)
## 5. Çoklu örnek ve bağımsızlık
## 6. Yaşam döngüsü, temizlik ve hata yalıtımı
## 7. Eksiksiz şablon kod
## 8. Sık hatalar ve kontrol listesi
```

## 3. Sınıf envanteri

```markdown
# [Sprint] sınıf envanteri
[Künye]
## 1. Mimari sınırlar          (hangi modül neyi bilebilir; mimari testlerle nasıl korunur)
## 2. Bağımlılık diyagramı     (Mermaid)
## 3. Eklenen sınıflar         | Modül | Sınıf | Rol | Sahip / ömür |
## 4. Değişen sınıflar         | Sınıf | Değişiklik | Neden |
## 5. Emekliye ayrılan sınıflar | Sınıf | Yerine | Silinme commit'i |
## 6. Sahiplik ve yaşam döngüsü matrisi
## 7. Emekli testler → yeni testler
## 8. Kaynak kontrol özeti
```

## 4. Teslim raporu

```markdown
# [Sprint] teslim raporu
[Künye] + referans belgeler
## 1. Yönetici özeti
## 2. Bulgu çözüm matrisi     | Bulgu (S6-B3) | Kök neden | Çözüm | Kanıt testi |
## 3. Sözleşme özeti
## 4. Gerçek derlenmiş API örneği
## 5. Doğrulama sonuçları     | Komut | Ortam | Tarih | Sonuç |
## 6. Git durumu ve teslim güvenceleri
```

Bulgu kimlikleri tur ve sıra numarası taşır (`S6-B3`). Her bulgu kök neden → çözüm → kanıt testi zincirine bağlanır.

## 5. İş günlüğü

```markdown
# [Sprint] uygulama günlüğü
## 1. Kod tabanı bulguları ve mimari sınırlar
## 2. Modül, bileşen ve yaşam döngüsü kararları
## 3. Eski → yeni tüketici geçişi   | Eski | Yeni | Durum |
## 4. Kaldırılan kod
## 5. Eşzamanlılık ve iptal (varsa)
## 6. İnceleme turu N             (bulgu → kök neden → düzeltme → doğrulama)
```

## 6. Plan ve dilimler

```markdown
# [Konu] planı
**Durum:** [taslak / kararlar alındı ve ADR-NNNN'e yazıldı]

## 1. Kapsam                    | Kapsamda | Kapsam dışı (hangi plana) |
## 2. Alınan / alınmayan        | Kaynak | Hedef | Nasıl | Dilim |
## 3. Hedef yapı ve bağımlılık yönü
## 4. Dilimler                  | Dilim | İçerik | Durum (☐/☑) | Kanıt |
## 5. Her dilim için "bitti" tanımı
## 6. Riskler
## 7. Açık kararlar             | No | Karar | Öneri |   (K1, K2 …)
```

Kararlar alınınca kalıcı yeri ADR olur; plan tarihçe olarak kalır ve durum satırı bunu söyler. Planın kendisi koddan geride kalırsa (☐ ama yapılmış) tabloyu güncelle; bayat plan yanıltıcıdır.

## 7. Repo yapısı ("bugünkü durum")

```markdown
# Repository structure
**Status:** Current state, accepted [YYYY-MM-DD] ([ADR-NNNN](…)); every listed module builds and is tested.

## 1. Root build and scope
## 2. Tree                       (kısa ağaç)
## 3. Modules                    | Module | Folder | Package / responsibility | Spec / ADR | Note |
### 3.1 Planned modules          | Module | Opens when | Spec |
## 4. Dependency direction       (ve hangi testle korunduğu)
## 5. Naming rules               | Kind | Rule | Example |
## 6. Profiles
## 7. Localization and configuration
## 8. Documents
```

Spesifikasyon başka bir hedef yapı tanımlıyorsa, hedef modüllerin bu repoda nereye eşlendiğini ayrı bir tabloyla ver.

## 8. İzleyici satırları ve değişiklik günlüğü

```markdown
| ID | Requirements | Owner | Deliverable | Depends | State | Acceptance test/evidence |
| W-<ALAN>-NN | SYS-001 | [modül] | [bitince ne var] | [W-…] | SPECIFIED | [tarihli komut + sonuç ya da gereken test; not run] |

| Date | Change | Evidence and remaining limit |
| YYYY-MM-DD | [kısa başlık] | [rapor linki, sayılar, hash'ler]. [Kalan sınır.] [Hangi satırların ilerlemediği.] |
```

## 9. Kanıt dosyası

```markdown
# [ID]: [kısa ad]

| Item | Record |
| --- | --- |
| Tracker ID / requirement IDs | [ID] ([REQ]); state claimed: **[STATE]** |
| Source revision and fixture/schema versions | [commit sha; dosya sha256 …] |
| Environment | [OS; runtime sürümleri; araç sürümleri; topoloji] |
| Command or test profile | see "Commands" |
| Result | **pass** / **fail** / **not run** — [sayılar], [YYYY-MM-DD HH:MM ±TZ] |
| Observed limits | [maks/p99, kayıp, kuyruk] ya da N/A |
| Known gap and next executable task | [ne gösterilmedi; sonraki görev] |

## Commands
[komut]   # raw/<log-dosyası>

## What exists for this row
## Tests that evidence it
```

## 10. Teslim notu (araç, demo ya da paket teslimi)

```markdown
# [Konu] — [YYYY-MM-DD]
[Hangi teslimi nitelendirdiği; hangi raporun onu geçersiz kıldığı.]

## Delivered artifact and qualification   | Item | Verified value |   (ör. özet değeri, boyut, kapsam, kontrol sayısı)
## Delivered behaviour
## Evidence and limits
[Bu bir araç ya da örnek teslimidir; üretim satırları ve kabul ID'leri değiştirilmez.]
```
