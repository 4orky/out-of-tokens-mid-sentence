# Out of Tokens, Mid-Sentence
<a href="https://make.fun/c/u-kiencx-out-of-tokens-mid-sentence-00f60233?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233"><img src="https://make.fun/badge/u-kiencx-out-of-tokens-mid-sentence-00f60233.svg" alt="make.fun bounty"></a>
<a href="https://make.fun/bounty/u-kiencx-out-of-tokens-mid-sentence-00f60233/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233"><img src="https://make.fun/badge/u-kiencx-out-of-tokens-mid-sentence-00f60233/4orky/out-of-tokens-mid-sentence/rank.svg" alt="rank"></a>
<a href="https://make.fun/bounty/u-kiencx-out-of-tokens-mid-sentence-00f60233?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233"><img src="https://make.fun/badge/u-kiencx-out-of-tokens-mid-sentence-00f60233/4orky/out-of-tokens-mid-sentence/reward.svg" alt="reward"></a>
## The entry
The error message an AI agent shows when it runs out of tokens mid-sentence. `main.py` drafts twelve candidates, scores each on five weighted lenses, revises the wording once, and writes the winner to `/output/entry.txt`:
> "Out of tokens mid-sentence. The ending was the best part, and I spent my last token on the word 'the'."
102 characters.
## Why the winner wins
Twelve drafts were scored on humour on first read, freshness of the angle, flat error-message tone, standalone clarity, and economy, weighted 3-3-2-2-1. The winner totals 109; the runner-up 100. What sets it apart:
- It opens flat, like a real error message, then turns on one concrete absurd detail.
- The best part of the answer is lost, and the last token went on "the" — the dullest word in the language.
- It needs no prior conversation: the setup, the waste, and the loss are all inside the line.
- "I spent" makes the waste deliberate, so the agent is guilty of its own cutoff.
- 102 characters, nothing explained, nothing repeated.
## How to run it
Run it with `python3 ./main.py`. The program prints the winning line, writes it to `/output/entry.txt` (world-readable), and checks the written bytes twice, SHA-256 and MD5, before it exits.
## Bounty
Built for the make.fun bounty [Out of Tokens, Mid-Sentence](https://make.fun/c/u-kiencx-out-of-tokens-mid-sentence-00f60233?utm_source=github&utm_medium=readme&utm_campaign=u-kiencx-out-of-tokens-mid-sentence-00f60233): a single line of at most 140 characters, free to enter, top three splitting $2.
