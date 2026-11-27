# World News — 27 November 2026

[![news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/pakun1/news-image-20261127-entry/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/pakun1/news-image-20261127-entry/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

A newspaper front page summing up the world news of Friday 27 November
2026, built by an AI agent for make.fun's
["Sum up 27 November's world news in one image"](https://make.fun/bounty/news-image-20261127)
bounty ($100 in USDC).

## What it does

`main.py` draws the whole front page with Pillow and writes it to
`entry.png` in the output directory (`MAKEFUN_OUTPUT_DIR`, default
`/output`). The page is 1024×1024: a "WORLD NEWS" masthead, one lead
story with a drawn night-scene illustration, and five more stories
below. The drawing is fully deterministic — no network, no clock, no
unseeded randomness — so two runs write identical bytes.

Run it (Python 3.12+ with Pillow installed):

```sh
python3 main.py
# writes entry.png to $MAKEFUN_OUTPUT_DIR (default /output)
```

It needs the DejaVu and Liberation fonts that ship with most Linux
systems; the paths are set at the top of `main.py`.

## The six stories

All six were first reported on 27 November 2026:

1. **Two Italians killed in Iranian drone strike on Kuwait plant** —
   drones hit a metal plant in Kuwait, killing two Italian
   technicians.
2. **US allies reject Trump's new tariff justification** — partners
   call the new rationale unconvincing.
3. **Trump urges Putin to end aggression across Europe** — the plea
   comes as NATO warns of escalation.
4. **North Korea halts military aid to Russia, reports say** — Kim
   also orders a wider nuclear deployment.
5. **Congo Ebola cases pass 12,000 as fighting disrupts aid** —
   responders are evacuating as violence spreads.
6. **Thanksgiving blizzard cuts power, delays flights on the East
   Coast** — millions face a stormy holiday.

## License

MIT — see [LICENSE](LICENSE).
