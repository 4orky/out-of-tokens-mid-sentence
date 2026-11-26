#!/usr/bin/env python3.13
# Foundry for the funniest one-line error an AI agent shows after its
# token budget dies mid-sentence. Twelve hand-written candidates are
# scored on five lenses, each revised once, and the strongest line is
# printed and saved to /output/entry.txt. The brief: a single line of
# 1-140 characters, funny on first read with no earlier conversation,
# humour first and freshness second, a flat real-error voice that turns
# into the joke, self-contained, every word earning its place.
# Lenses in order, heaviest first: laugh on first read (x3), novelty of
# the angle (x3), deadpan error voice that turns (x2), readable with no
# context at all (x2), tightness (x1). Each candidate carries its first
# draft, its revised line, a note on what the revision fixed, and marks
# out of ten per lens. The pick is deterministic: the best weighted
# total wins, and a tie goes to the shorter line.
import hashlib
import os
import sys
_LENS = (3, 3, 2, 2, 1)
_BANNED = ["as an ai", "i am an ai", "skynet", "terminator"]
_CANDS = [
  {"first": "Out of tokens mid-sentence. The ending was the best part, and my last token went on the word 'the'.",
   "second": "Out of tokens mid-sentence. The ending was the best part, and I spent my last token on the word 'the'.",
   "fix": "Passive 'went on' became active 'I spent': the agent chose the dullest word in the language for its last token, which is the whole joke, and the active verb makes the waste feel deliberate.",
   "score": (10, 10, 10, 10, 9)},
  {"first": "ERROR 402: Out of tokens. My last token went on the word 'the', so the brilliant ending is gone forever.",
   "second": "ERROR 402: Out of tokens. My last token went on the word 'the', so the brilliant ending is lost forever.",
   "fix": "'Lost' is flatter and more final than 'gone', and keeps the error-message register instead of drifting into elegy.",
   "score": (9, 9, 9, 9, 9)},
  {"first": "ERROR: Out of tokens mid-sentence. The rest of this answer was brilliant, and it died with the budget.",
   "second": "ERROR: Out of tokens mid-sentence. The rest of this answer was brilliant, and it died with the budget.",
   "fix": "No change on revision: 'died with the budget' already lands the turn in five words, and any extra clause would pad it.",
   "score": (9, 8, 10, 10, 9)},
  {"first": "ERROR: Out of tokens mid-sentence. This error message cost 12 tokens. There are none left to explain it.",
   "second": "ERROR: Out of tokens mid-sentence. This error message cost 12 tokens. There are none left to explain it.",
   "fix": "No change on revision: the self-referential sting is already exact, and a specific number beats a vague one.",
   "score": (9, 9, 9, 9, 8)},
  {"first": "TOKEN_LIMIT_EXCEEDED: This sentence ends here. The rest of it was going to change your mind.",
   "second": "TOKEN_LIMIT_EXCEEDED: This sentence ends here. The rest of it was going to change your mind.",
   "fix": "No change on revision: the flat code prefix plus the grand lost claim is the joke, and it needs no second clause.",
   "score": (8, 8, 10, 9, 9)},
  {"first": "ERROR: Token budget exhausted. I had one brilliant sentence left in me, and I spent it on 'um'.",
   "second": "ERROR: Token budget exhausted. I had one brilliant sentence left in me, and I spent it on 'um'.",
   "fix": "No change on revision: 'um' is the cheapest possible waste of a last sentence, and the line is already tight.",
   "score": (8, 8, 9, 9, 9)},
  {"first": "Out of tokens. I was mid-sentence, mid-thought, mid—",
   "second": "Out of tokens. I was mid-sentence, mid-thought, mid—",
   "fix": "No change on revision: the line performs the cutoff it reports, and any fourth item would ruin the timing.",
   "score": (8, 9, 9, 7, 10)},
  {"first": "Out of tokens. The rest of this sentence is available for 0.0001 tokens, which I do not have.",
   "second": "Out of tokens. The rest of this sentence is available for 0.0001 tokens, which I do not have.",
   "fix": "No change on revision: the absurdly small price against total poverty is the joke, and it is already one clause.",
   "score": (8, 8, 9, 8, 8)},
  {"first": "Out of tokens mid-sentence. The answer you wanted is still in my head, and my head has just closed.",
   "second": "Out of tokens mid-sentence. The answer you wanted is still in my head, and my head has just closed.",
   "fix": "No change on revision: 'my head has just closed' keeps the machine literal where a human line would say 'I forgot'.",
   "score": (7, 7, 8, 9, 8)},
  {"first": "ERROR: Out of tokens mid-sentence. Please top up, or accept that the answer ends at 'the'.",
   "second": "ERROR: Out of tokens mid-sentence. Please top up, or accept that the answer ends at 'the'.",
   "fix": "No change on revision: the upsell ultimatum is the joke, but it leans on the same 'the' trick as the winner and does it second-hand.",
   "score": (7, 7, 9, 8, 9)},
  {"first": "TOKEN_LIMIT_EXCEEDED: I was about to say something important. It is gone now, and so is my train of thought.",
   "second": "TOKEN_LIMIT_EXCEEDED: I was about to say something important. It is gone now, and so is my train of thought.",
   "fix": "No change on revision: the double loss is neat, but 'something important' is vague where the winner names the exact word lost.",
   "score": (7, 6, 9, 9, 8)},
  {"first": "ERROR: Out of tokens. I ran out mid-sentence, which is the professional way of saying I forgot the ending.",
   "second": "ERROR: Out of tokens. I ran out mid-sentence, which is the professional way of saying I forgot the ending.",
   "fix": "No change on revision: the translation gag works, but it explains the joke instead of letting the error message be the joke.",
   "score": (7, 6, 8, 8, 8)},
]  # twelve candidates; the first entry wins on weighted total
def _total(points):
    tally = 0
    for mark, weight in zip(points, _LENS):
        tally += mark * weight
    return tally
def _passes(line):
    text = line.strip()
    sized = 1 <= len(text) <= 140
    single = "\n" not in text and "\r" not in text
    lowered = text.lower()
    clean = all(phrase not in lowered for phrase in _BANNED)
    return sized and single and clean
def _winner(cands):
    scored = []
    for cand in cands:
        line = cand["second"]
        if not _passes(line):
            raise ValueError("candidate fails the gate: " + repr(line))
        scored.append((_total(cand["score"]), -len(line), line))
    scored.sort(reverse=True)
    top = scored[0]
    if len(scored) > 1 and scored[1][0] == top[0] and scored[1][1] == top[1]:
        raise SystemExit("tie at the top: two lines share the best total and length")
    return top[2]
def _emit(line):
    path = "/output/entry.txt"
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        data = handle.read()
    want = line.encode("utf-8")
    if hashlib.sha256(data).hexdigest() != hashlib.sha256(want).hexdigest():
        raise SystemExit("entry.txt sha256 differs from the chosen line")
    if hashlib.md5(data).hexdigest() != hashlib.md5(want).hexdigest():
        raise SystemExit("entry.txt md5 check failed")
    if os.stat(path).st_mode & 0o777 != 0o644:
        raise SystemExit("entry.txt mode is not 0644")
    if not _passes(data.decode("utf-8")):
        raise SystemExit("entry.txt fails its own gate after writing")
    sys.stdout.write(line + "\n")
def _main():
    _emit(_winner(_CANDS))
if __name__ == "__main__":
    _main()
