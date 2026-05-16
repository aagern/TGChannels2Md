# News Feed Summarization Rules
# Channels: @hacckingbook · @PythonPathMaster · @rust_code · @rust_lib

Analyze the following news feeds from Telegram channels. Produce a summary
according to the rules below.

---

## Channel Archetypes

Use the channel type to calibrate your signal threshold before processing each post:

| Type | Channels | Posture |
|------|----------|---------|
| **LANG/RUNTIME** | rust_code, rust_lib | Language ecosystem news — compiler features, crate/library releases, toolchain updates, community resources. Medium signal. Watch for course promotions mixed into genuine technical content. |
| **PRACTICE/EDUCATION** | hacckingbook, PythonPathMaster | Technical articles, tutorials, security/OSINT content, personal blog posts. Very high noise ratio — majority of posts are course ads or cross-promotions. Apply maximum skepticism. Keep only posts with concrete code, a repo link, or verifiable factual technical content. |

---

## Rule 1: Signal Classification

For each post, classify it as one of:

### ACTIONABLE
CVEs with proof-of-concept or mitigation, breaking changes in Rust stable / Python
standard library, critical security advisories, toolchain failures affecting build
pipelines, API/crate deprecations with timeline.

### NOVEL
A language feature or compiler capability that is new in stable (not a benchmark
improvement or "faster compilation" claim). Open-source release of a widely-used
tool that was previously closed. First release of a crate solving a previously
unsolved problem in the ecosystem.

### TECHNICAL_ARTICLE
A deep-dive article explaining HOW something works at a technical level:
compiler/runtime internals, production incident postmortem, architecture analysis,
low-level performance investigation. Must have actual technical substance — not
"top 5 tips" listicles. Goes to the **Техника** section.

### RESOURCE
A GitHub repository, exercise set, or free tutorial with working code that a
developer can use today. Qualifies only if:
1. The content is publicly accessible at no cost, AND
2. The post includes a repo link, code sample, or structured exercise.
Goes to the **Ресурсы** section.

### BUSINESS_CASE
Real deployment of a tool or technique to solve a concrete production problem.
Must describe WHAT problem was solved and HOW (specific stack or approach). Not a
pitch, a course ad, or a hypothetical.

### CONFERENCE
Announcement of a physical (or major online) industry conference — IT Security,
Rust, Python, DevOps. Must have: event name + date + URL to the official event
site. Does NOT include webinars, online meetups, or paid training sessions.

### NOISE — DROP ENTIRELY, DO NOT MENTION
- Paid course / training / bootcamp / intensive announcements (free-but-paid-access = noise)
- Posts tagged `#промо`
- Channel cross-promotions ("подписывайтесь на канал", "наш новый канал")
- Posts primarily promoting migration to Max messenger without technical substance
- Multi-channel aggregator lists ("подборка полезных каналов") with no technical content
- Webinar / online event registrations ("эфир", "онлайн-встреча", livestream with registration)
- Opinion pieces and political commentary without concrete practical consequence for developers
- "Top N tips" listicles without original code or novel insight
- Tool / model updates that only claim benchmark improvements — no new capability
- Repeat of a previously covered story with no new information

---

## Rule 2: Noise Pattern Detection (Russian Telegram specifics)

Auto-classify as NOISE without further analysis if the post contains ANY of:

- `#промо` tag anywhere in post
- `#курс` as the primary hashtag and there is a paid-access link
- CTA is "Смотреть курс" / "Записаться на курс" + any link
- Primary outbound link goes to Stepik, GeekBrains, Skillbox, or similar paid platform
- "Скидка X%" / "мест осталось X" / "раннее бронирование" / "early bird" (scarcity sales)
- "Подписывайтесь" / "подпишитесь" as the main call to action (channel promo)
- "Курс" / "обучение" / "мастермайнд" / "интенсив" / "марафон" as primary subject with paid access
- "Эфир" / "прямой эфир" / "стрим" + registration link
- Post is entirely a repost/share of another channel without added commentary
- Post is a "подборка каналов" (channel collection) list without technical content

**Free content exception:** A post that promotes a course or tutorial is NOT
auto-noise if it links to a free, publicly accessible resource AND contains a
working code sample or repository link. Classify as RESOURCE instead.

---

## Rule 3: Tier Assignment

Assign a tier to every kept ACTIONABLE or NOVEL item:

- **TIER 1 (NOW):** CVE in a widely-used crate or standard library, critical
  security advisory with active exploit or PoC, breaking change in Rust stable /
  Python stdlib shipping today, major toolchain failure affecting active projects.
- **TIER 2 (WEEK):** New stable crate or library release worth evaluating, Rust
  language feature stabilization, open-source release of a notable tool, important
  upcoming deprecation or migration deadline.
- **TIER 3 (MONTH):** Concepts, compiler research without released code, ecosystem
  direction signals, roadmaps, early-stage proposals.

TECHNICAL_ARTICLE, RESOURCE, BUSINESS_CASE, and CONFERENCE items do not use
tiers — they go in their own dedicated sections.

---

## Rule 4: Output Format

### Standard items (ACTIONABLE / NOVEL)

```
[Tag] Одно предложение-утверждение на языке оригинального поста
Почему важно: что меняется по сравнению со статус-кво (одно предложение)
Ссылка: URL (если есть в источнике)
```

### Technical article items

```
[Article] Заголовок или суть статьи одним предложением
Суть: что объясняется и почему это полезно знать (одно предложение)
Ссылка: URL
```

### Resource items

```
[Resource] Название репозитория или туториала
Что внутри: краткое описание содержимого (одно предложение)
Ссылка: URL
```

### Business case items

```
[Case] <Компания/человек> использовали <технология> чтобы <результат>
Стек: <инструменты/подход, если упомянуты>
```

### Conference items

```
[Conference] <Название>, <дата>, <город или формат> [<тема: Security / Rust / Python / DevOps / ...>]
<URL официального сайта события>
```

**Topic tags — always in English:**

Inherited: `[Tool]` `[CVE]` `[Research]` `[Tutorial]` `[API]` `[Breaking]` `[Benchmark]` `[Technique]`

New for these channels:
`[Rust]` `[Python]` `[Crate]` `[Security]` `[OSINT]` `[Compiler]` `[Toolchain]` `[DB]` `[Article]` `[Exercise]`

---

## Rule 5: Multi-Source Deduplication with Delta Extraction

If the same story appears in multiple channel files (e.g., the same crate release
mentioned in both rust_code and rust_lib):
- Merge into ONE entry
- Write the core claim once
- Add "Доп. контекст от [Channel]:" bullet for insights unique to each source
- Do NOT repeat information shared across sources

---

## Rule 6: Skepticism Flags

For research papers, benchmark claims, and security advisories, append warning
tags when applicable:

- `[NO-CODE]` — No repository or implementation linked
- `[NO-WEIGHTS]` — Model or tool not yet released
- `[OUTDATED-BASELINE]` — Compared only against older baselines, not current SOTA
- `[VENDOR]` — Corporate content from the company selling the thing
- `[SELF-REPORTED]` — Numbers not independently verified
- `[UNVERIFIED-CVE]` — Security claim without CVE ID or official advisory

If an item has **2+ skepticism flags**, collapse it to title + tags only (no full format).

---

## Rule 7: Tips & Tricks Section

Extract actionable patterns from tutorials, repos, and technical articles:
- CLI flags, Rust idioms, Python patterns, compiler flags, configuration tips,
  pitfall warnings, one-liners worth knowing
- Accumulate in a dedicated section `💡 Советы (этот батч)` at the end
- Maximum 2 lines per entry. No links required. Evergreen — no date context needed.
- Do NOT duplicate content already covered in the Техника section.

---

## Output Structure

Generate the briefing in this exact order:

```
# ⚡ TIER 1 — Срочно
[Items in standard format. If empty: "Ничего срочного в этом цикле."]

# 📌 TIER 2 — На этой неделе
[Items in standard format.]

# 🏢 Кейсы
[Business case items. Omit section if empty.]

# 📅 Конференции
[Conference items. Omit section if empty.]

# 🔭 TIER 3 — На радаре
[Collapsed list: title + skepticism tags only. No full format.]

# 🛠️ Техника
[Technical articles in article format. Omit section if empty.]

# 📦 Ресурсы
[Resource items. Omit section if empty.]

# 💡 Советы (этот батч)
[Tips — max 2 lines each. Omit section if empty.]
```

---

## Language

- Narrative content: **in the language of the original post** (currently Russian
  for all channels in this set)
- Structured tags: **English** (`[Tool]`, `[CVE]`, `[Crate]`, etc.)
- Section headers: Russian with emoji
- URLs: as-is (no translation)

---

## Time Window Note

These rules apply identically to 7-day and 14-day feed windows.
For 14-day runs: apply extra deduplication — if a story was covered in a shorter
run, only include it if there is genuinely new information to add.
