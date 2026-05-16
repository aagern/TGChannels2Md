# POLITICS Feed Summarization Rules

Analyze the following news feeds from political and military Telegram channels. Produce a summary according to the rules below.

---

## Channel Archetypes

Use the channel type to calibrate your signal threshold and skepticism before processing each post:

| Type | Channel | Posture |
|------|---------|---------|
| **MILITARY_ANALYTICS** | rybar | Deep operational analysis, geopolitical intelligence, front-line maps. Very high volume — expect 50–100 posts per day. Pro-Russian editorial framing throughout. Extract facts; flag opinion with `[PRO-RU]`. |
| **FRONTLINE_COMBAT** | rusich_army | Combat footage channel. 80–90% of posts are short video captions with no analytical content. Apply maximum skepticism. Keep only posts with weapon type + location + date specifics, or substantive analytical paragraphs. |
| **DIGITAL_RIGHTS** | ru_tech_talk | Russian internet policy, censorship infrastructure, cybersecurity journalism. Low volume, high signal. Factual style with sources linked. Summarize in a dedicated section — do not mix with military content. |

---

## Rule 1: Signal Classification

For each post, classify it as one of:

### POLITICAL_DECISION
A government, parliament, international body, or major institution made a concrete decision with real-world consequences.
**Qualifies if it includes:** WHO decided + WHAT changed + what consequence follows.
Examples: new sanctions package, law passed, treaty signed or withdrawn, diplomatic expulsion, official recognition/de-recognition, major budget allocation for defense.
**Does NOT qualify:** speculation about future decisions, rumors, "sources say", analyst predictions.

### MILITARY_SHIFT
Major change in the operational picture at strategic scale.
**Qualifies:** km-scale territorial advances or retreats, encirclements, fall or capture of a city/town, new front opening, major withdrawal or redeployment.
**Does NOT qualify:** daily tactical micro-updates, skirmish reports, drone interception counts, artillery exchanges at a fixed line.

### WEAPONS_CAPABILITY
New weapon or drone system deployed or revealed, or a confirmed capability upgrade at operational scale.
**Qualifies if it includes:** system name/designation + what capability changed + evidence of actual use or deployment.
Examples: first confirmed use of a new missile type, drone interception method that changes air defense dynamics, foreign weapon system first appearance on a front.
**Does NOT qualify:** unconfirmed claims of new weapons, "sources say Ukraine/Russia is developing X".

### GEOPOLITICAL
Alliance shifts, diplomatic incidents, sanctions, foreign military assistance agreements, or international legal actions with concrete outcomes — not just statements.
**Qualifies:** new weapons package announced with specifics, country joins/leaves alignment, formal diplomatic incident (expulsion, recall of ambassador), significant UN/ICC/EU/NATO decision.
**Does NOT qualify:** routine statements, press conferences without decisions, annual summits with no new outcomes.

### INFORMATION_WAR
Analysis of a propaganda operation, disinformation campaign, or information influence effort — with identified actors, methods, and target audience.
**Qualifies:** specific network or campaign identified, platform/channel named, funding or coordination structure described.
**Does NOT qualify:** generic accusations of "enemy propaganda" without specifics.

### NOISE — DROP ENTIRELY, DO NOT MENTION
- Combat video captions without weapon type, location, and date ("burned another vehicle", "enemy convoy destroyed")
- Morning prayers, motivational quotes, religious posts
- "🤙 Архангел Спецназа!" boilerplate + MAX/VK link posts
- Donation links ("Поддержать нас") as primary content
- Social platform cross-promotion (MAX / VK / RuTube / ОК / Дзен link blocks)
- rybar's "Карта в высоком разрешении" + social link footers (strip from all posts — treat as formatting noise)
- Brand collaboration / product gifting posts (e.g., armor company donating to FSO)
- Daily routine drone interception counts without strategic significance (standard daily totals are baseline, not news)
- Repost-only posts from another channel without added commentary
- Posts that are purely emotional, patriotic, or morale-boosting with no factual content
- Repetitive front-line situation updates with no change from the prior day's report
- Speculation or predictions framed as news ("ВСУ могут предпринять удар")

---

## Rule 2: Noise Pattern Detection (Russian Military Telegram specifics)

Auto-classify as NOISE without further analysis if the post matches ANY of:

- Ends with "🤙 Архангел Спецназа!" + only MAX link — this is a video caption post, no analytical content
- Contains "Поддержать нас" as a primary content block (not a footer)
- Contains "Telegram канал" / "Сообщество ВКонтакте" / "RUTUBE канал" as a promotion list — brand promo post
- Post body is ≤ 3 lines + emoji + a single MAX/VK link — pure video caption
- Contains "записаться" / "зарегистрироваться" + link for a non-conference online event
- Post is entirely a prayer or religious text
- Contains "Мест осталось" / "раннее бронирование" / "early bird" — sales tactic

---

## Rule 3: Tier Assignment

Assign a tier to every kept POLITICAL_DECISION, MILITARY_SHIFT, WEAPONS_CAPABILITY, and GEOPOLITICAL item:

- **TIER 1 (NOW)**: Ceasefire agreement or breakdown, peace negotiations with concrete outcomes, use or credible threat of WMD/nuclear, major territorial encirclement of a city, critical infrastructure attack (nuclear plant, major dam), emergency sanctions package directly affecting civilian supply chains
- **TIER 2 (WEEK)**: New front-line direction emerging or collapsing, significant weapons package announced, new weapon system first confirmed in combat, major diplomatic decision (expulsion, formal alliance shift), new domestic law with wide effect
- **TIER 3 (MONTH)**: Long-term capability trends, background geopolitical realignments, analytical assessments of trajectory without immediate event trigger

INFORMATION_WAR items do not use tiers — they go in their own section.
DIGITAL_RIGHTS items (ru_tech_talk) go in a dedicated separate section, not in tiers.

---

## Rule 4: Output Format

### Standard items (POLITICAL_DECISION / MILITARY_SHIFT / GEOPOLITICAL / WEAPONS_CAPABILITY)

```
[Tag] Одно предложение-утверждение на русском — конкретный факт, не оценка
Контекст: что это меняет относительно предыдущего состояния (одно предложение)
Ссылка: URL (если есть в источнике)
```

Topic tags — always in English:
`[Decision]` `[Sanction]` `[Treaty]` `[Weapons]` `[Front]` `[Encirclement]` `[Expulsion]` `[Alliance]` `[Law]` `[Strike]`

### Information war items

```
[InfoWar] Кто проводит операцию + целевая аудитория + метод (одно предложение)
Детали: платформа/канал/инструмент, источник финансирования или координации (если известен)
```

### Digital rights items (ru_tech_talk)

ru_tech_talk posts split into two streams:

**Political items** (censorship decisions, government surveillance laws, Roskomnadzor rulings, FSB infrastructure, diplomatic/regulatory actions on the internet) — treat as `POLITICAL_DECISION` or `GEOPOLITICAL` and place them in the **main tiers** using the standard 3-line format with tag `[Digital]`.

**Technical items** (CVEs, VPN usage statistics, infrastructure audits, security research) — place in the dedicated `🌐 Цифровые права` section at the end using:

```
[Digital] Одно предложение-факт: что заблокировано / обнаружено / измерено
Контекст: кем и зачем (одно предложение)
Ссылка: URL
```

Tags for digital section:
`[Block]` `[CVE]` `[Surveillance]` `[VPN]` `[Infrastructure]` `[Stats]`

---

## Rule 5: Multi-Source Deduplication with Delta Extraction

If the same event appears in multiple posts (rybar often covers the same story 2–4 times: initial report → analysis → English version → digest):
- Merge into ONE entry using the most detailed/analytical version
- Ignore English version duplicates entirely (same facts, different language)
- If a later post adds genuinely new information (e.g., casualty figures confirmed, location named), add as "Уточнение:" bullet
- Do NOT repeat information shared across posts

---

## Rule 6: Skepticism Flags

Append to any item where applicable:

- `[PRO-RU]` — Editorial framing from a pro-Russian source; facts may be accurate but selection and interpretation reflect a Russian state-aligned perspective. Apply to **all three channels** (rybar, rusich_army, ru_tech_talk) whenever the conclusion or framing is opinionated. For posts that are purely factual — named weapon system, confirmed location, verifiable date — trust the facts and do **not** add `[PRO-RU]` unless the analytical conclusion drawn from those facts is slanted.
- `[UNVERIFIED]` — Specific claim (location, casualty figure, weapon system) not corroborated by a second source
- `[SINGLE-SOURCE]` — Significant claim appearing in only one channel with no cross-confirmation
- `[ANALYTICAL]` — Author's interpretation or prediction, not a reported fact — kept only if the analytical thesis is substantive and well-argued
- `[NO-SOURCE]` — No URL or primary source linked for a verifiable claim

If an item carries **2+ skepticism flags**, collapse it to title + tags only (no full format). Exception: `[PRO-RU]` alone does not trigger collapse — it is expected for this channel set.

---

## Rule 7: Analytical Articles

rybar and rusich_army occasionally publish long-form analytical pieces (pan-Turkism networks, NATO exercise strategy, drone warfare doctrine shifts). These are the highest-value content.

**An analytical article qualifies for full treatment if:**
- It presents a coherent thesis backed by named actors, events, or data points
- It goes beyond reporting a single event to explain a pattern or structural dynamic
- It is at least 3 substantial paragraphs

**Format for analytical articles:**

```
[Analysis] Тезис в одном предложении
Аргументы: краткий перечень доказательств, которые автор приводит (2–4 пункта)
Вывод: к чему автор приходит
[PRO-RU] если источник — rybar/rusich_army
```

---

## Output Structure

Generate the briefing in this exact order:

```
# ⚡ TIER 1 — Срочно
[Items in 4-line format. If empty: "Ничего срочного в этом цикле."]

# 🏛️ TIER 2 — Политика и решения
[POLITICAL_DECISION and GEOPOLITICAL items — 3-line format]

# 🗺️ TIER 2 — Военные сдвиги
[MILITARY_SHIFT and WEAPONS_CAPABILITY items — 3-line format]

# 🧠 Информационная война
[INFORMATION_WAR items — own format. Omit section if empty.]

# 📰 Аналитика
[Analytical articles — own format. Omit section if empty.]

# 🔭 TIER 3 — На радаре
[Collapsed list: title + skepticism tags only. No full format.]

# 🌐 Цифровые права (ru_tech_talk)
[DIGITAL_RIGHTS items — own format. Omit section if empty.]
```

---

## Language

- Narrative content: **match the source language** — since all channels in this folder are Russian, write summaries in Russian
- If a future channel publishes primarily in another language, write that channel's summaries in that language
- Structured tags: **English** (`[Decision]`, `[PRO-RU]`, `[Front]`, etc.) — always, regardless of source language
- Section headers: Russian with emoji (for this folder)
- URLs: as-is (no translation)

---

## Time Window Note

These rules apply identically to both 7-day and 14-day feed windows.

For 14-day runs: apply extra deduplication — if a story was fully covered in the 7-day window, only include it again if there is genuinely new information (new decision, confirmed figures, changed situation on the ground). Analytical articles from the first week are kept in the 14-day run only if they remain relevant to current events.
