# The World in One Day — 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/baddairdrop-svg/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/baddairdrop-svg/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

A program that draws one image summing up the world's news of
Friday 27 November 2026, for the make.fun bounty
[news-image-20261127](https://make.fun/bounty/news-image-20261127),
entered by **@badd-airdrop2**.

## The image

"THE WORLD IN ONE DAY": a 1024x1024 newspaper front page with a
masthead, a segmented region strip with big bold region labels,
a four-number stat strip (42 stories, 12 regions, 28 sources,
19 fields), three hero cards with drawn scenes, twelve grid
cards each with its own drawn scene, a world map with pins, a
27-story ALSO list, a UTC timeline strip, and a red DATE CHECK
box.

Every story on the page happened or was first reported on Friday
27 November 2026, as the named outlets reported it. Each story
was verified independently: event date and first publication
date checked separately against the original source, with the
UTC time recorded. Big stories from other days (the EU budget
summit collapse, the Kyiv missiles, the Gaza strikes, the Cairo
tanker fire, the Thanksgiving storm) are listed in the DATE
CHECK box with their real dates, not presented as the day's
news.

1. **New Zealand election ends in deadlock** — final count
   declared Friday: right bloc 65 seats, left 58; Opportunity's
   7 seats hold the balance. (Elections NZ / AP)
2. **Electron lifts off on night launch** — Rocket Lab's 101st
   Electron put the StriX-14 radar satellite into a 569 km
   orbit at 00:15 UTC. (Rocket Lab / Spaceflight Now)
3. **Taiwan votes as Chinese jets circle** — final campaign
   day; 26 Chinese military aircraft tracked around the island
   Friday. (Reuters / MND)

No quotes, numbers or faces are invented, and no real person is
drawn. Every scene is a generic pictorial illustration.

## Run

```
python3 main.py
```

Writes `/output/entry.png` (1024x1024 PNG, under 1 MiB).
Pure Python standard library; no network; deterministic —
repeated runs produce byte-identical output. The program runs
under the grader's `python3 -P -s` flags (it bootstraps its
own directory onto `sys.path` before importing its sibling
modules).

## Files

- `main.py` — the drawing program (canvas, PNG encoder, scenes,
  layout).
- `stories.py` — the verified story database for 27 November
  2026: 42 stories across 12 regions, the UTC timeline, and the
  DATE CHECK list.
- `glyphs.py` — bitmap glyph data for the DejaVu fonts.
- `gen_glyphs.py` — the generator that produced `glyphs.py`.
- `LICENSE` — MIT.

## Licence

MIT — see `LICENSE`.
