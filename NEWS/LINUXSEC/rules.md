# LINUXSEC News Feed Summarization Rules

Analyze the following news feeds from LINUXSEC Telegram channels. Produce a summary according to the rules below.

---

## Channel Archetypes

Use the channel type to calibrate your signal threshold before processing each post:

| Type | Channels | Posture |
|------|----------|---------|
| **ANALYST** | alukatsky | Long-form essays (800–1500 words) with explicit author opinion. Very high signal. Use extended 4-5 line format. |
| **NEWS** | SecLabNews, itsec_news | Short factual posts, high volume. Trust content by default. Watch for political commentary without security angle (NOISE). |
| **DEVTOOLS** | devsecops_weekly, k8security | Practical tools, CVEs, Kubernetes/DevSecOps features. High signal density. Trust by default. |
| **COMMUNITY** | linuxkalii | Mixed signal: incidents, AI-security research, opinion pieces. Apply standard classification — drop opinion without new facts. |
| **EDUCATION** | linuxacademiya, cyberyozh_official | Tutorials and Linux tips are valuable → extract to Советы section. Posts where the primary call to action is a paid course link → NOISE (extract any embedded tip first). |
| **REGULATION** | zlonov_security | Russian security legislation and compliance reviews. Niche but high-value. Use REGULATORY classification. |

---

## Rule 1: Signal Classification

For each post, classify it as one of:

### ACTIONABLE
Tutorials with working commands or code, tools with GitHub repos, CVEs with PoC or active exploitation, API breaking changes, service outages affecting users, security patches needed now.

### NOVEL
First-of-its-kind attack primitive, new exploit technique, new security architectural shift.
**Model/tool updates qualify ONLY if they introduce a capability that was not possible before.**
Drop updates that only claim to be "faster" or "better" without a concrete new attack or defense surface.

### INCIDENT
Confirmed security breach with verifiable detail: affected company, nature of compromise, scope, known or suspected attack vector.
Must be confirmed — not rumor, not speculation.
Qualifies even if investigation is ongoing, as long as the breach itself is confirmed.

### BUSINESS_CASE
Real deployment of security tooling or technique by a company or individual to solve a concrete problem.
Must describe WHAT problem was solved and HOW (specific tools, stack, approach).
Not a pitch, course promo, or hypothetical.

### REGULATORY
Russian security legislation or policy change with direct implications for security practitioners.
Must change what a practitioner, vendor, or organization must do or avoid.
Pure political commentary without actionable security angle → NOISE.

### CONFERENCE
Announcement of a physical (or major online) industry security conference.
Must have: event name + date + URL to official event site.
**Does NOT include:** webinars, "эфиры", online meetups, community calls, paid training sessions.

**[CFP] sub-type:** Call for Papers for a confirmed physical security conference.
Must have: event name + submission deadline + URL.
Place in the Конференции section with `[CFP]` tag.

### NOISE — DROP ENTIRELY, DO NOT MENTION
- Opinion pieces and commentary without new facts
- Funding/investment announcements without product substance
- Posts whose entire substance is a registration link for a webinar or online event
- Paid course, training, masterclass, bootcamp, intensive announcements
- Posts tagged `#промо`
- Channel cross-promotions ("подписывайтесь на канал")
- Conference preparation updates: schedule drafts, sticker packs, partner announcements, merch — NOT the conference itself
- Humor posts and fictional narrative vignettes (even if security-themed)
- Russian internet outage or connectivity commentary without a direct security angle
- Repost of another channel's content without added commentary
- Tutorial posts where the primary call to action is a paid course link — extract any useful command/tip to Советы, then drop the post

---

## Rule 2: Noise Pattern Detection (Russian Telegram specifics)

Auto-classify as NOISE without further analysis if the post contains ANY of:

- `#промо` tag anywhere in post
- Primary CTA is "записаться" / "зарегистрироваться" + link for a non-conference online event
- "Эфир" / "прямой эфир" / "стрим" + registration link
- "Подписывайтесь" / "подпишитесь" as the main call to action (channel promo)
- "Курс" / "обучение" / "мастермайнд" / "интенсив" / "марафон" as primary subject with paid access
- "Мест осталось X" / "раннее бронирование" / "early bird" (scarcity sales tactics)
- Post is entirely a repost/share of another channel without added commentary
- Conference logistics update: "стикерпак готовится", "расписание верстается", "партнеры подписываются"

**Exception for EDUCATION channels:** if a paid-course post contains a standalone useful command, config, or technique, extract it as a Советы entry before discarding the post.

---

## Rule 3: Tier Assignment

Assign a tier to every kept ACTIONABLE or NOVEL item:

- **TIER 1 (NOW):** Active exploitation of a CVE in the wild, critical zero-day with no patch, confirmed supply chain compromise, major security service outage affecting users, breaking API change requiring immediate action
- **TIER 2 (WEEK):** New security tool with GitHub repo worth testing, important K8s/Linux security feature, notable new attack technique with PoC, upcoming deprecation or compliance deadline
- **TIER 3 (MONTH):** Security research without released code or PoC, ecosystem trend signals, threat intelligence reports without immediate IOCs

INCIDENT, BUSINESS_CASE, REGULATORY, and CONFERENCE items do not use tiers — they go in their own dedicated sections.

---

## Rule 4: Output Format

### Standard items (ACTIONABLE / NOVEL) — 3 lines

```
[Tag] Одно предложение-утверждение на русском
Почему важно: что меняется по сравнению со статус-кво (одно предложение)
Ссылка: URL (если есть в источнике)
```

### Extended analyst format — 4-5 lines
Use for posts from @alukatsky (long-form essays with explicit author analytical opinion):

```
[Tag] Одно предложение-утверждение на русском
Почему важно: что меняется по сравнению со статус-кво (одно предложение)
Мнение автора: ключевой аналитический вывод автора (1-2 предложения)
Ссылка: URL (если есть в источнике)
```

### Incident items

```
[Incident] <Компания/система>: краткое описание инцидента
Подтверждено: что именно известно (вектор, масштаб, затронутые продукты — если раскрыто)
Статус: что предпринято / что остаётся неизвестным
Ссылка: URL
```

### Regulatory items

```
[Regulatory] Одно предложение: суть изменения
Что меняется для практика: конкретное требование или ограничение
Ссылка: URL
```

### Business case items

```
[Case] <Компания/человек> использовали <технология> чтобы <результат>
Стек: <инструменты/подход, если упомянуты>
```

### Conference items

```
[Conference] <Название>, <дата>, <город или формат> [<тема: IT Security / DevSecOps / ...>]
<URL официального сайта события>
```

### CFP items

```
[CFP] <Название конференции>, <дата события>, <город> — заявки до <дедлайн>
<URL страницы подачи>
```

---

### Topic tags — always in English

**Inherited from reference:**
`[Tool]` `[Research]` `[Paper]` `[Tutorial]` `[API]` `[License]` `[Benchmark]` `[Technique]` `[Breaking]` `[Model]` `[Agent]`

**Security-specific additions:**
`[CVE]` `[Exploit]` `[Incident]` `[Supply-Chain]` `[Bug-Bounty]` `[K8s]` `[Linux]` `[AI-Attack]` `[AI-Defense]` `[Regulatory]` `[Threat-Intel]` `[CFP]` `[Conference]` `[Case]`

---

## Rule 5: Multi-Source Deduplication with Delta Extraction

If the same story appears across multiple channel sources (e.g., Rockstar hack in SecLabNews and linuxkalii):
- Merge into ONE entry
- Write the core claim once
- Add "Доп. контекст от [Source]:" bullet points for insights unique to each source
- Do NOT repeat information shared across sources

---

## Rule 6: Skepticism Flags

For research papers, AI-security experiments, and vendor benchmark claims, append warning tags when applicable:

- `[NO-CODE]` — No repository or implementation linked
- `[NO-WEIGHTS]` — Model not released
- `[OUTDATED-BASELINE]` — Compared only against older systems, not current SOTA
- `[VENDOR]` — Corporate content from the company selling the thing
- `[SELF-REPORTED]` — Numbers not independently verified
- `[LAB-ONLY]` — Results obtained only in controlled/sandboxed environment, not validated in real-world conditions

If an item has **2+ skepticism flags**, collapse it to title + tags only (no full format).

---

## Rule 7: Tips & Tricks (Советы)

Extract useful non-news patterns from tutorials, Linux tips, DevSecOps threads, repos:
- CLI commands worth knowing, config patterns, strace/debugging one-liners, pitfall warnings, security hardening steps
- **For EDUCATION channel posts with paid CTAs:** extract the technique or command, discard the rest of the post
- Accumulate in a dedicated section `🛠️ Советы (этот батч)` at the end
- Maximum 2 lines per entry. No links required. Evergreen — no date context needed.

---

## Output Structure

Generate the briefing in this exact order:

```
# ⚡ TIER 1 — Срочно
[Items in standard or extended format. If empty: "Ничего срочного в этом цикле."]

# 📌 TIER 2 — На этой неделе
[Items in standard or extended format]

# 🏛️ Регулирование
[Regulatory items. Omit section if empty.]

# 🏢 Кейсы
[Business case items. Omit section if empty.]

# 📅 Конференции
[Conference and CFP items — name, date, topic tag, URL. Omit section if empty.]

# 🔭 TIER 3 — На радаре
[Collapsed list: title + skepticism tags only. No full format.]

# 🛠️ Советы (этот батч)
[Tips — max 2 lines each. Omit section if empty.]
```

---

## Language

- Narrative content: **Russian** (the language of the original posts)
- Structured tags: **English** (`[Tool]`, `[CVE]`, `[Incident]`, `[Conference]`, etc.)
- Section headers: Russian with emoji
- URLs: as-is (no translation)

---

## Time Window Note

These rules apply identically to 7-day and 14-day feed windows.
For 14-day runs: apply extra deduplication — if a story appeared in a 7-day run, only include it if there is genuinely new information.
