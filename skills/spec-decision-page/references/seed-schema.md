# Seed JSON şeması

Sayfa tek bir JSON belgesinden çizilir (`assets/template.html` içindeki `__SEED_JSON__`). `scripts/validate_seed.py` bu şemayı ve yazım kurallarını denetler.

```json
{
  "meta": {
    "title": "<Proje> Tasarım Kararları",
    "storeKey": "<proje>-design-decisions",
    "subline": "Spesifikasyon ↔ uygulama (<commit>) · spesifikasyon kararları, <tarih>",
    "basis": "Kalemlerin nasıl üretildiğini anlatan bir cümle.",
    "labels": {
      "specTitle": "Önerilen tasarım",       "specSource": "Spesifikasyon",      "specLegend": "spesifikasyon setindeki tasarım",
      "currentTitle": "Şu anki tasarım",     "currentSource": "Uygulama",        "currentLegend": "uygulamanın bugünkü hali",
      "proposalTitle": "Teklif edilen tasarım", "proposalSource": "Uzlaştırma önerisi", "proposalLegend": "ikisini uzlaştıran öneri ve desenler",
      "newSite": "Yalnız uygulamada",
      "fileSlug": "<proje>-tasarim-kararlari"
    }
  },
  "groups": [
    { "id": "C6", "title": "Backend, kalıcılık ve veritabanı", "desc": "Alanın tek cümlelik kapsamı." }
  ],
  "items": [ /* aşağıdaki kalem nesneleri */ ]
}
```

- `meta.title`: sayfa ve sekme adı. Markdown dışa aktarımının başlığı da budur.
- `meta.storeKey`: tarayıcı yedeği ve IndexedDB adı. Her sayfaya ayrı bir değer ver; aynı değer iki sayfada olursa `file://` altında birbirlerinin yedeğini görürler.
- `meta.subline` ve `meta.basis`: başlığın altındaki satır ve giriş notu. Hangi commit'e göre yazıldığını burada söyle.
- `meta.labels`: sütun adları, kaynak etiketleri ve dışa aktarım dosya adı. Hepsi isteğe bağlıdır; verilmeyen alan varsayılan değeri alır. Örneğin "Şu anki" sütununu repo adıyla göstermek için `currentSource: "<repo-adı>"` ver.
- `groups`: sırası sayfadaki sıradır. Kalemler `group` alanıyla bağlanır; içinde kalem olmayan grup gösterilmez.

## Kalem

```json
{
  "id": "C6-08",
  "group": "C6",
  "title": "Kalıcılık yeteneği ve veritabanı veri modeli",
  "kind": "removed",
  "impact": "high",
  "priority": "P2",
  "recommended": "proposal",
  "summary": "Liste satırında görünen tek cümle.",
  "spec":     { "summary": "...", "detail": "...", "refs": ["docs/modules/persistence.md:40-88"] },
  "current":  { "summary": "Yok.", "detail": "", "refs": [], "why": "", "whySource": "" },
  "proposal": { "summary": "...", "detail": "...", "patterns": [{ "name": "Repository", "why": "..." }], "effort": "M" },
  "points": [
    { "spec": "Her eklenti depolama grubu kendi veritabanı şemasına sahiptir.",
      "ref": "docs/modules/persistence.md:52",
      "status": "removed", "current": "Yok.", "action": "adopt" }
  ],
  "parts": [],
  "findings": [],
  "reqs": ["SYS-003"],
  "reviewNote": ""
}
```

| Alan | Değerler | Anlamı |
| --- | --- | --- |
| `kind` | `kept`, `changed`, `replaced`, `removed`, `partial`, `incompatible`, `doc-drift`, `pattern` | Kalemin baskın durumu. `pattern` yalnız desen alanında; `doc-drift` uygulama belgesinin kendi koduyla çeliştiği kalemler içindir. |
| `impact` | `high`, `medium`, `low` | Kartın sol çizgisinin rengi. |
| `priority` | `P1`, `P2`, `P3` | P1 başlıkta işaretlenir. |
| `recommended` | `spec`, `current`, `proposal` | "Analiz önerisi" rozetinin konduğu kart. |
| `points[].status` | `kept` Var, `changed` Farklı, `replaced` Başka çözüm, `partial` Kısmi, `removed` Yok, `incompatible` Çelişen, `new` Yalnız uygulamada | Maddenin uygulamadaki durumu. `removed` ile `current: "Yok."` birlikte kullanılır. |
| `points[].action` | `keep` Koru, `adopt` Uygula, `adapt` Uyarla, `defer` Ertele, `drop` Gerek yok | Önerilen aksiyon. |
| `parts[]` | `{title, ref}` ya da `{title, status, ref}` | Durumsuz: kapsanan belge bölümleri. Durumlu: desen kullanım yerleri (varsayılan açık gelir). |

Kurallar:

- `points` o konunun spesifikasyondaki tüm maddeleridir; spesifikasyon içeriği burada eksiltilmez.
- `points[].current` ve `current.summary` yalnız uygulamada var olanı söyler; yoksa tam olarak `Yok.` yazılır.
- `whySource`: `documented` (ADR/plan), `commit`, `inferred`, `none` ya da boş. Yalnız yazılı bir gerekçe varsa (`documented`, `commit`) `why` doldurulur; `inferred` ve `none` için `why` boş kalır.
- Kimlikler sayfa boyunca tekildir ve sürümler arasında değiştirilmemeye çalışılır, çünkü kararlar kimliğe bağlı saklanır.
- `findings` ve `reqs` alanları kalemin içinde "Kaynak bulgular ve gereksinimler" bölümünde gösterilir. `reviewNote` aynı bölümde "İnceleme notu" olarak görünür.

## Karar kaydı dosyası

Sayfa kararları kullanıcının seçtiği JSON dosyasına yazar (Edge/Chrome, File System Access API) ve tarayıcıda yedekler. JSON dışa aktarımı aynı biçimdedir. Biçim kimliği `spec-design-decisions`'dır; eski bir sayfanın yazdığı farklı kimlikler `meta.legacyFormats` dizisiyle (ör. `["eski-kimlik"]`) okunur:

```json
{
  "format": "spec-design-decisions",
  "version": 1,
  "exportedAt": "2026-11-19T10:22:17.000Z",
  "decisions": {
    "C6-08": {
      "choice": "proposal",
      "decision": "accept",
      "note": "…",
      "updatedAt": "…",
      "updatedBy": null,
      "history": [{ "at": "…", "by": null, "choice": "proposal", "decision": "accept" }]
    }
  }
}
```

`choice` ∈ `spec|current|proposal`, `decision` ∈ `accept|defer|reject` (Kabul/Ertele/Red). Kararları sonraki işe (karar kaydı, spesifikasyon güncellemesi, plan) dönüştürmek için bu dosyayı oku.
