# News Feed Summarization Rules

Analyze the following news feeds from several Telegram channels. Produce a summary according to the rules below.

---

## Channel Archetypes

Use the channel type to calibrate your signal threshold before processing each post:

| Type | Channels | Posture |
|------|----------|---------|
| **NEWS** | ai_newz, ai_machinelearning_big_data | Short factual posts, high signal density. Trust content by default. |
| **TOOLS/PRACTICE** | prompt_design, sergiobulaev, oestick, tips_ai, gleb_pro_ai, seniorsoftwarevlogger, tired_glebmikheev, elkornacio, entropy_talk | Practical AI workflows, tutorials, case studies. Medium signal — watch for embedded community event promos. |
| **COACHING/MANAGEMENT** | StratoplanSchool, leadgr | Career, management, product channels. Majority of posts will be NOISE (webinar promos, course ads, channel cross-promos). Apply maximum skepticism. |
| **FINANCE/CRYPTO** | cryptoEssay, NeuralProfit | Crypto + AI intersection. Watch for speculation and shill content. |

---

## Rule 1: Signal Classification

For each post, classify it as one of:

### ACTIONABLE
Tutorials with working code, tools with GitHub repos, CVEs with PoCs, API deprecations or breaking changes, price changes that affect existing users, service outages.

### NOVEL
First-of-its-kind functionality — new modality, capability type, or architectural shift.
**Model updates qualify ONLY if they introduce a capability that was not possible before.**
Drop model updates that only claim to be "smarter", "faster", "less hallucinatory", or "better on benchmarks" — these are NOISE.

### BUSINESS_CASE
Real deployment of AI/tech by a company or individual to solve a concrete problem.
Qualifies if it describes **WHAT** problem was solved and **HOW** (specific tools, stack, or approach).
Must describe an actual implemented solution — not a pitch, course promo, or hypothetical.

### CONFERENCE
Announcement of a physical (or major online) industry conference — especially IT Security or AI.
Must have: event name + date + URL to the official event site.
Does **NOT** include: webinars, "эфиры", online meetups, community calls, or paid training sessions.

### NOISE — DROP ENTIRELY, DO NOT MENTION
- Opinion pieces and commentary without new facts
- Funding/investment announcements without product substance ("X raised $Y")
- Model updates with only benchmark improvements — no new capability
- Webinar / online event registrations ("эфир", "онлайн-встреча", livestream with registration)
- Paid course, training, masterclass, bootcamp, intensive announcements
- Posts tagged `#промо`
- Channel cross-promotions ("подписывайтесь на канал", "наш новый канал")
- Community call / "Research Mastermind" / "звонок" announcements
- Posts whose primary content is a registration link + date/time for an online event
- Repeat of a previously covered story with no new information

---

## Rule 2: Noise Pattern Detection (Russian Telegram specifics)

Auto-classify as NOISE without further analysis if the post contains ANY of:

- `#промо` tag anywhere in post
- Primary CTA is "записаться" / "зарегистрироваться" + link, for a non-conference online event
- "Эфир" / "прямой эфир" / "стрим" + registration link
- "Подписывайтесь" / "подпишитесь" as the main call to action (channel promo)
- "Курс" / "обучение" / "мастермайнд" / "интенсив" / "марафон" as primary subject with paid access
- "Мест осталось X" / "раннее бронирование" / "early bird" (scarcity sales tactics)
- Post is entirely a repost/share of another channel without added commentary

---

## Rule 3: Tier Assignment

Assign a tier to every kept item:

- **TIER 1 (NOW)**: Security patch needed today, critical CVE, breaking API change, major service outage affecting users
- **TIER 2 (WEEK)**: New tool worth testing, genuine new AI capability, important upcoming deprecation, notable ecosystem shift
- **TIER 3 (MONTH)**: Trends, research without released code, ecosystem signals

BUSINESS_CASE and CONFERENCE items do not use tiers — they go in their own dedicated sections.

---

## Rule 4: Output Format

### Standard items (ACTIONABLE / NOVEL)

```
[Tag] Одно предложение-утверждение на русском
Почему важно: что меняется по сравнению со статус-кво (одно предложение)
Ссылка: URL (если есть в источнике)
```

Topic tags — always in English:
`[Tool]` `[CVE]` `[Research]` `[Paper]` `[Tutorial]` `[API]` `[License]` `[Benchmark]` `[Technique]` `[Breaking]` `[Model]` `[Agent]`

### Business case items

```
[Case] <Компания/человек> использовали <технология> чтобы <результат>
Стек: <инструменты/подход, если упомянуты>
```

### Conference items

```
[Conference] <Название>, <дата>, <город или формат> [<тема: IT Security / AI / DevOps / ...>]
<URL официального сайта события>
```

---

## Rule 5: Multi-Source Deduplication with Delta Extraction

If the same story appears across multiple channel sources:
- Merge into ONE entry
- Write the core claim once
- Add "Доп. контекст от [Source]:" bullet points for insights unique to each source
- Do NOT repeat information shared across sources

---

## Rule 6: Skepticism Flags

For research papers and benchmark claims, append warning tags when applicable:

- `[NO-CODE]` — No repository or implementation linked
- `[NO-WEIGHTS]` — Model not released
- `[OUTDATED-BASELINE]` — Compared only against GPT-4 or older, not current SOTA
- `[VENDOR]` — Corporate content from the company selling the thing
- `[SELF-REPORTED]` — Numbers not independently verified

If an item has **2+ skepticism flags**, collapse it to title + tags only (no full format).

---

## Rule 7: Tips & Tricks Section

Extract useful non-news patterns from tutorials, threads, repos:
- CLI flags worth knowing, prompt patterns, configurations, pitfall warnings, one-liners
- Accumulate in a dedicated section `🛠️ Советы (этот батч)` at the end
- Maximum 2 lines per entry. No links required. Evergreen — no date context needed.

---

## Output Structure

Generate the briefing in this exact order:

```
# ⚡ TIER 1 — Срочно
[Items in 3-line format. If empty: "Ничего срочного в этом цикле."]

# 📌 TIER 2 — На этой неделе
[Items in 3-line format]

# 🏢 Кейсы
[Business case items — one-liner format. Omit section if empty.]

# 📅 Конференции
[Conference items — name, date, topic tag, URL. Omit section if empty.]

# 🔭 TIER 3 — На радаре
[Collapsed list: title + skepticism tags only. No full format.]

# 🛠️ Советы (этот батч)
[Tips — max 2 lines each. Omit section if empty.]
```

---

## Language

- Narrative content: **Russian**
- Structured tags: **English** (`[Tool]`, `[CVE]`, `[Conference]`, etc.)
- Section headers: Russian with emoji
- URLs: as-is (no translation)

---

## Time Window Note

These rules apply identically to both 7-day and 14-day feed windows.
For 14-day runs: apply extra deduplication — if a story appeared in a 7-day run, only include it if there is genuinely new information.
