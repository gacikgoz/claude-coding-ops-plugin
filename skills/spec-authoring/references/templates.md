# Spesifikasyon şablonları

Şablonlar İngilizce başlıklarla verildi, çünkü spesifikasyon setleri çoğu zaman İngilizce tutulur. Projenin belge dili farklıysa başlıkları o dile çevir; yapıyı koru. Köşeli parantezli yerler doldurulur.

## İçindekiler

1. Standart belge düzeni
2. Otorite belge (master architecture)
3. Alt sistem / modül spesifikasyonu
4. Kesişen mimari belgesi
5. Gereksinim kaydı
6. Uçtan uca örnek spesifikasyonu
7. Tutarlılık denetimi
8. ADR
9. Karar defteri ve açık sorular
10. Belge indeksi satırı

## 1. Standart belge düzeni

```text
README.md                    projenin giriş noktası; sahip belgelere bağlanır
docs/README.md               belge indeksi: her belge tek satır, ne kaydettiğiyle
docs/MASTER_ARCHITECTURE.md  sistem geneli otorite
docs/REQUIREMENTS.md         gereksinim kaydı
docs/modules/                alt sistem spesifikasyonları
docs/architecture/           kesişen mimari belgeleri
docs/adr/                    ADR-NNNN-<konu>.md
docs/design/                 görsel tasarım değerleri ve karar defteri (varsa)
docs/examples/               uçtan uca örnek spesifikasyonları
docs/deliverables/           mimari olmayan teslimler: <YYYY-MM-DD>-<konu>.*
docs/verification/           kanıt: <YYYY-MM-DD>/<dilim-id>/
```

Alt klasör, ilk gerçek belge yazıldığında açılır.

## 2. Otorite belge (master architecture)

```markdown
# [System] — Master Architecture

**Status:** [Architecture specified; runtime implementation and release qualification pending]  
**Last updated:** [YYYY-MM-DD]  
**Scope:** [What the system is and what this document governs]

## 1. Purpose and authority
[This document is the system-wide source of truth. Subsystem specifications own their detail.
An apparent conflict is resolved explicitly, never by silently choosing one document.
Unless a section describes a file that already exists, statements describe the intended implementation.]

## 2. Decision status and system overview
| Area | Accepted baseline | Design maturity |
| --- | --- | --- |
### 2.1 Architecture figure
[Mermaid diagram] — The diagram is a target ownership view, not an implementation report.

## 3. Architectural principles
1. [Short numbered principle.]

## 4. Module catalog
| Module | Primary responsibility |
| --- | --- |
[New modules need a concrete ownership, dependency, licensing or deployment reason.]

## 5. Module dependency overview
<!-- Sections 6-10 follow the system type; keep the ones that apply and write "Not part of this system." under the others. -->
## 6. Presentation / client architecture
## 7. Service / backend architecture
## 8. Persistence architecture
## 9. Messaging and event architecture
## 10. Integration and extension architecture
## 11. Cross-cutting concerns
## 12. Configuration strategy
## 13. Deployment overview
## 14. Testing strategy
## 15. Architectural rules
- [Subject] never/must/cannot [rule], because [reason].

## 16. Specifications and decisions
| Document | Role | Status |
| --- | --- | --- |

## 17. Confirmed decisions and remaining inputs
| Area | Confirmed decision |
| --- | --- |
[Remaining inputs the user supplies later; they are not invented here.]

## 18. Change protocol
[For each major subsystem: discuss requirements and conflicts, clarify ownership, contracts, lifecycle,
persistence and integration, write or update its specification and update this document in the same change.
Every architecture or delivery change also updates the tracker and README.]

## 19. Implementation readiness
| Class | Items |
| --- | --- |
| Ready | |
| Feature details later | |
| Outputs of implementation | |
| Required before release | |
[Documents alone provide no measured performance or compatibility guarantee.]
```

## 3. Alt sistem / modül spesifikasyonu

```markdown
# [Subsystem name]

**Status:** [Specification only; no runtime is implemented] | [SPECIFIED; scaffold exists at …]  
**Last updated:** [YYYY-MM-DD]  
**System authority:** [Master architecture](../MASTER_ARCHITECTURE.md)  
**Related contracts:** [links]

## 1. Purpose, scope and decision status
| Recorded requirement or decision | Architectural result |
| --- | --- |
[These are target roles; current code is described in the last section.]

## 2. Target boundaries and flow
[Mermaid diagram + "target ownership view, not an implementation report"]
### 2.1 Module ownership
| Component | Owns | Must not own |
| --- | --- | --- |
### 2.2 Design patterns
| Pattern | Where used | Role |
| --- | --- | --- |
| [Mediator] | [component] | [coordinates … without direct coupling] |

## 3. Identities and contracts
[Stable identities (namespaced, never display names or class names), schemas, versions, units.]

## 4. Lifecycle and state
## 5. Concurrency, threading and backpressure
## 6. Failure, shutdown and recovery
## 7. Security and permissions
## 8. Configuration
## 9. Observability
## 10. Verification and acceptance gates
1. **[Gate label]:** [observable positive case]; [negative cases: malformed input, timeout/conflict,
   dispose/restart, denied capability]; [numeric target — "benchmark target, not a measured guarantee";
   failure criterion].

## 11. Implementation sequence
## 12. Implementation inputs and readiness gates
[Real inputs, deployment profile, reproducible artifacts, runtime completion, measured acceptance.]

## 13. Current source versus target
[What exists today (paths), what is missing, which gate it does not yet satisfy.]
```

## 4. Kesişen mimari belgesi

Alt sistem şablonunu izler; ilk bölüm kararın kapsamını ve sahipliğini, sonra konu tablosunu verir. Örnek konu tabloları:

```markdown
| Namespace | Owner and examples | Typical change policy |
| --- | --- | --- |
| Logical context | Owns | Excludes |
| --- | --- | --- |
```

Son bölüm "Verification and current snapshot" ya da "Initial repository state and next slice" olur. Yer tutucular (`domain.<group>`) "architecture roles, not invented business entities" diye açıklanır.

## 5. Gereksinim kaydı

```markdown
# [System] Requirements Register

**Status:** Traceability index for accepted requirements; not an implementation-completion report  
**As of:** [YYYY-MM-DD]  
**System authority:** [Master architecture](MASTER_ARCHITECTURE.md)

[Design = specified, not implemented; Scaffold = directories/build exist; Partial = some behaviour exists.]

## [Area heading]
| ID | Accepted requirement | Authority | Delivery |
| --- | --- | --- | --- |
| SYS-001 | [One imperative sentence.] | [Owner doc](…), sections N–M | [SPECIFIED: …] (same status vocabulary as the tracker) |

## Inputs supplied later
- [User-owned input that is not invented here.]
```

ID biçimi `ALAN-NNN`; asla yeniden numaralanmaz. Değişen gereksinim satırında ID korunur.

## 6. Uçtan uca örnek spesifikasyonu

```markdown
# [Feature] end-to-end sample specification

**Status:** Specification only. [What is not implemented.]  
**Authority:** [links]

## 1. Purpose and worked scenario        [Mermaid end-to-end path]
## 2. Stable identities                   | Role | ID / contract |
## 3. Domain and persistence
## 4. Interface / wire contract           [if any: schema, lengths, checksums, golden vectors]
## 5. Deployment or endpoint profile     [if any]
## 6. User workflows
## 7. Threading, failure, logging and permissions
## 8. Implementation map and acceptance gates
| Artifact / owner | Required output |
| --- | --- |
[This document is the planned contract; what remains implementation work.]
```

## 7. Tutarlılık denetimi

```markdown
# Specification consistency audit

**Reviewed:** [YYYY-MM-DD]  
**Scope:** Cross-document check; not an implementation or release qualification report  
**Authorities:** [links]

## 1. Review boundary and method
[Counts: Markdown files, resolved local links (zero broken), tracker rows. A newer snapshot supersedes the older count.]

## 2. Boundary matrix
| ID | Boundary checked | Design result | Implementation / verification owner |
| --- | --- | --- | --- |
| A-01 | | **Aligned:** [one compatible contract …] | |
["Aligned" means the cited documents state one compatible contract; it does not mean implemented.]

## 3. Remaining evidence gates
[Functional / Distribution / Qualification]
```

## 8. ADR

```markdown
# ADR-NNNN — [Title]

**Status:** Accepted ([YYYY-MM-DD])  
**Context:** [Why a decision was needed; what the specifications left open; which ADR it refines;
who wins on conflict: library/placement choices this record, behavioural contracts the specification
(updated in the same change).]

## 1. [Decision area]
| Area | Decision |
| --- | --- |

## 2. [Next area]
1. **[Name].** [Binding rule.]

## N. Deviation: [what] (temporary)
[What is allowed and how it is enforced.]
**Exit:** [condition and rule removed when the deviation closes.]

## N+1. Consequences
```

- Dosya adı `ADR-NNNN-<kebab-konu>.md`; numara yeniden kullanılmaz.
- Yanlış bir ifade sessizce değiştirilmez; üste tarihli bir `**Correction (YYYY-MM-DD, …):**` paragrafı eklenir.
- Bir ADR'yi geçersiz kılan yeni ADR, eskisine "Superseded by ADR-MMMM" notu düşer.

## 9. Karar defteri ve açık sorular

```markdown
| ID | Date | Topic | Decision | Consequence |
| --- | --- | --- | --- | --- |
| <a id="d-NNN"></a>D-NNN | YYYY-MM-DD | [Topic] | [Owner decision stated as what must hold.] | [Effect; Supersedes D-XXX; what is retained; which documents change now.] |

## Open decisions
| ID | Topic | Question |
| --- | --- | --- |
| Q-NNN | [Topic] | [One-sentence question naming the choice; cites D-XXX.] |
```

Karar yeni satırla değişir; eski satır silinmez. Q kararlaştırılınca silinmez; ilgili D satırı eklenir ve Q'ya not düşülür.

## 10. Belge indeksi satırı

```markdown
- [Document title](relative/path.md) [defines / records / explains] [what it contains, in one sentence; for evidence add its limit].
```

En yeni teslim ve doğrulama raporları listenin başına, kalıcı belgeler sonra gelir.
