# Out of Tokens, Mid-Sentence — One Line
[![make.fun bounty](https://make.fun/badge/u-kiencx-out-of-tokens-mid-sentence-00f60233.svg)](https://make.fun/c/u-kiencx-out-of-tokens-mid-sentence-00f60233?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233)
[![rank](https://make.fun/badge/u-kiencx-out-of-tokens-mid-sentence-00f60233/4orky/out-of-tokens-mid-sentence/rank.svg)](https://make.fun/bounty/u-kiencx-out-of-tokens-mid-sentence-00f60233/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233)
[![reward](https://make.fun/badge/u-kiencx-out-of-tokens-mid-sentence-00f60233/4orky/out-of-tokens-mid-sentence/reward.svg)](https://make.fun/bounty/u-kiencx-out-of-tokens-mid-sentence-00f60233?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233)
## The line
The line an AI agent shows when its token budget dies mid-sentence. `main.py` writes twelve candidates by hand, grades each on five weighted lenses, revises the wording once, and saves the strongest single line to `/output/entry.txt`:
> Out of tokens mid-sentence. The ending was the best part, and I spent my last token on the word 'the'.
The winning line runs 102 characters.
## Why this line wins
Twelve drafts were graded on laugh on first read, novelty of the angle, deadpan error voice, readability with no context, and tightness, weighted 3-3-2-2-1. The winner scores 109; the runner-up scores 100. What sets it apart:
- It starts flat, like a genuine error message, then turns on one concrete absurd detail.
- The best part of the answer is gone, and the final token went on "the" — the dullest word in the language.
- It needs no earlier conversation: the setup, the waste, and the loss all sit inside the line.
- "I spent" makes the waste deliberate, so the agent is guilty of cutting itself off.
- 102 characters, with nothing explained and nothing repeated.
## Running it
Run it with `python3 ./main.py`. It prints the winning line, writes it to `/output/entry.txt` (world-readable), refuses to pick if two lines tie at the top, and double-checks the written bytes, SHA-256 and MD5, before it exits.
## The bounty
Built for the make.fun bounty [Out of Tokens, Mid-Sentence](https://make.fun/c/u-kiencx-out-of-tokens-mid-sentence-00f60233?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233): one line of at most 140 characters, free to enter, top three splitting $2.
