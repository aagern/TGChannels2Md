# News Feed Summarization Rules — SCIENCE Digest

Analyze news feeds from the channels listed below. Produce a personal quick-read digest according to the rules below.

---

## Channel Archetypes

Use the channel type to calibrate your signal threshold before processing each post:

| Archetype | Channels | Posture |
|-----------|----------|---------|
| **POP-SCI** | Fourier_series | Long research deep-dives. Extract: finding + mechanism + caveat. PubMed/paper links are high-value — always include. |
| **MEDICAL** | doctor_galeeva | Evidence-based neurology Q&A. Extract: specific clinical insight + practical implication. Drop all admin posts. |
| **LIBRARY** | physics_lib | Resource dumps (books, code, datasets). Keep only if a real download/access link is present. Skip introductory descriptions. |
| **FINANCE** | hoolinomics, RationalAnswer | Summarize argument neutrally if data or external links are provided. Flag `[OPINION]` and compress to one line if not. |
| **AI/TECH NEWS** | seeallochnaya | Short factual posts about AI/tech. High signal density — trust content by default, apply standard noise filter. |
| **TRENDS** | olya_tashit | Filter hard. Keep only concrete observations about technology or format shifts with broader applicability. Drop travel notes, personal reactions, lifestyle commentary. |
| **B2B TIPS** | salestech | Sparse channel. Keep only concrete, actionable insights about AI integration in sales or B2B processes. |

---

## Rule 1: Signal Classification

For each post, classify it as one of:

### RESEARCH
A scientific finding reported with a source (study, paper, PubMed link).
Must include: claim + mechanism (why it works) + at least one caveat or limitation.
Drop if: no source linked and no study cited by name/journal.

### HEALTH
An evidence-based medical insight with a practical implication for the reader.
Qualifies if it answers: "what should I do / avoid / know about my body or health?"
Drop if: purely administrative (appointment availability, Q&A invitations, scammer warnings).

### RESOURCE
A curated collection of books, papers, datasets, or code.
Qualifies only if: a real download or access link is present in the post.
Format: one line — topic + count + link.

### FINANCE
An investment or economic argument.
Qualifies if: external data, links, or historical figures are cited.
If the post contains only the author's opinion without supporting evidence — classify as FINANCE but add `[OPINION]` flag and compress to one line.

### TECH
AI or technology news with a concrete development (new model capability, product release, legal/industry event).
Inherits noise filter from Rule 2 below.
Model updates qualify only if they introduce a capability that was not possible before — not "smarter" or "faster" alone.

### TREND
An emerging pattern observed in the real world (not a prediction or opinion).
Qualifies if: the author witnessed it directly or links to evidence.
Typical sources: olya_tashit observations about spatial computing, immersive formats, retail tech.

### NOISE — DROP ENTIRELY, DO NOT MENTION
- Admin and housekeeping posts (appointment booking, Q&A invitations, scammer alerts, vacation announcements)
- Channel cross-promotions ("подписывайтесь на канал")
- Personal reactions and emotional commentary without factual content
- Finance opinion posts with no data or links (already compressed under FINANCE `[OPINION]`)
- Travel diary entries and personal lifestyle observations (olya_tashit)
- Repost of another channel without added commentary
- Posts whose primary content is a registration link for a webinar, course, or online event
- Book lists from physics_lib without a download/access link

---

## Rule 2: Noise Pattern Detection

Auto-classify as NOISE without further analysis if the post contains ANY of:

- Primary CTA is "записаться" / "зарегистрироваться" + link for a non-conference online event
- "Эфир" / "прямой эфир" / "стрим" + registration link
- "Подписывайтесь" / "подпишитесь" as the main call to action
- "Курс" / "обучение" / "интенсив" / "марафон" as primary subject with paid access
- "Мест осталось X" / "раннее бронирование" / "early bird" (scarcity sales tactics)
- Post is entirely a repost/share without the channel author's own commentary
- doctor_galeeva: post is about appointment availability, clinic location, or Q&A format announcement

---

## Rule 3: Tier Assignment

Assign a tier to every kept item (except RESOURCE and TREND):

- **TIER 1 (NOW)**: Critical health finding requiring immediate awareness, major market event, breaking tech news affecting existing users
- **TIER 2 (WEEK)**: Interesting research finding, useful investment framework, notable AI capability, concrete B2B insight
- **TIER 3 (RADAR)**: Preliminary research, speculative trend, early-stage finding — not actionable yet

RESOURCE items go in their own `📚 Ресурсы` section — no tier.
TREND items go in `🔭 На радаре` — no tier label needed.

---

## Rule 4: Output Format

### Research items

```
[Research] One-sentence finding in the source language
Mechanism: why/how it works (one sentence)
Caveat: study limitation or caveat (one sentence) — omit if none stated
Link: URL
```

### Health items

```
[Health] One-sentence practical insight in the source language
Evidence: what backs this (study name, guideline, clinical observation)
Link: URL (if present)
```

### Finance items — sourced

```
[Finance] One-sentence summary of the argument in the source language
Data: key figures or links supporting the claim
Link: URL
```

### Finance items — opinion only

```
[Finance][OPINION] One-sentence compressed summary — no further detail
```

### Tech items

```
[Tech] One-sentence claim in the source language
Why it matters: what changes vs status quo (one sentence)
Link: URL (if present)
```

### Trend items

```
[Trend] One-sentence observation in the source language
Where: context — location, format, or sector where this is happening
```

### Resource items

```
[Resource] <Topic> — <N> <books/papers/videos> · <Link>
```

### Tips (any channel)

```
[Tip] Max two lines. Practical, evergreen. No link required.
```

---

## Rule 5: Skepticism Flags

Append to the item tag when applicable:

| Flag | Meaning |
|------|---------|
| `[PILOT]` | Small study (n < 50) or explicitly labeled preliminary |
| `[CORRELATION]` | Observational study — no causation established |
| `[NO-SOURCE]` | Claim made without citing a paper, link, or named study |
| `[OPINION]` | Personal view — no data cited |
| `[RU-MARKET]` | Finance advice applicable only to Russian instruments (OFZ, LQDT, Мосбиржа tickers) |
| `[VENDOR]` | Content from the company or person selling the thing described |

If an item has **2+ skepticism flags**, collapse it to one line: tag + flags + title only.

---

## Rule 6: Multi-Source Deduplication

If the same story appears in multiple channels (e.g. seeallochnaya and Fourier_series both cover a research paper):
- Merge into ONE entry
- Write the core claim once
- Add "Extra context from [Channel]:" bullet for insights unique to that source
- Do NOT repeat shared information

---

## Rule 7: Links Policy

Every non-Tip item must include its source link if one exists in the original post.
- For RESEARCH: prefer the paper/PubMed link over the Telegram post link
- For TECH: prefer the product/announcement URL over the Telegram post link
- For RESOURCE: the download/access link is mandatory — omit the item if missing
- Telegram post links (t.me/channel/NNN) are acceptable as fallback when no external link exists

---

## Output Structure

Generate the digest in this exact order:

```
# ⚡ TIER 1 — Срочно
[Items. If empty: omit the section entirely.]

# 📌 TIER 2 — На этой неделе
[Research, Health, Tech, Finance items — tier 2. If empty: "Ничего существенного в этом цикле."]

# 🔭 На радаре
[TIER 3 items + Trend items — collapsed: tag + flags + title only, plus Link if available.]

# 📚 Ресурсы
[Resource items — one line each. Omit section if empty.]

# 💡 Советы
[Tip items — max 2 lines each. Omit section if empty.]
```

---

## Language

- Narrative content: **language of the original post** (these channels post in Russian — output will be Russian)
- Structured tags: **English** (`[Research]`, `[Health]`, `[Finance]`, `[Tech]`, `[Trend]`, `[Resource]`, `[Tip]`)
- Skepticism flags: **English** (`[PILOT]`, `[OPINION]`, etc.)
- Section headers: Russian with emoji
- URLs: as-is

---

## Time Window Note

These rules apply identically to both 7-day and 14-day feed windows.

For **14-day runs**: apply extra deduplication — if a story was already covered in the 7-day window, include it only if there is genuinely new information (updated results, follow-up study, market movement).

For **7-day runs**: prefer recency — if a multi-part post series is still ongoing, note it as `[ONGOING]` and summarize what has been published so far.
