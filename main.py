#!/usr/bin/env python3
# Out-of-tokens error foundry: drafts twelve one-line error messages an
# AI agent shows when it runs out of tokens mid-sentence, scores each
# against the judge brief, revises the wording once, and writes the
# strongest single line to /output/entry.txt. The brief: one line,
# 1-140 characters, funny on first read without any prior conversation,
# humour first, freshness second, flat real-error tone that turns into
# the joke, self-contained, every word earning its place.
# Five lenses, heaviest first: humour on first read (3), freshness of
# the angle (3), flat error-message tone that turns (2), standalone
# clarity without the interrupted sentence (2), economy (1).
# Each entry keeps its first draft, its revised final, a note on what
# the revision fixed, and marks out of ten per lens. Selection is
# deterministic: highest weighted total wins, and a tie goes to the
# shorter line.
from hashlib import md5 as _md5
from hashlib import sha256 as _sha256
from pathlib import Path as _Path
_WEIGHTS = {"humour": 3, "freshness": 3, "tone": 2, "standalone": 2, "economy": 1}
_FORBIDDEN = ("as an ai", "i am an ai", "skynet", "terminator")
_ENTRIES = [
    {"draft": "Out of tokens mid-sentence. The ending was the best part, and my last token went on the word 'the'.",
     "final": "Out of tokens mid-sentence. The ending was the best part, and I spent my last token on the word 'the'.",
     "polish": "Swapped the passive 'went on' for 'I spent': the agent chose the dullest word in the language for its last token, which is the whole joke, and the active verb makes the waste feel deliberate.",
     "marks": {"humour": 10, "freshness": 10, "tone": 10, "standalone": 10, "economy": 9}},
    {"draft": "ERROR 402: Out of tokens. My last token went on the word 'the', so the brilliant ending is gone forever.",
     "final": "ERROR 402: Out of tokens. My last token went on the word 'the', so the brilliant ending is lost forever.",
     "polish": "'Lost' is flatter and more final than 'gone', and keeps the error-message register instead of drifting into elegy.",
     "marks": {"humour": 9, "freshness": 9, "tone": 9, "standalone": 9, "economy": 9}},
    {"draft": "ERROR: Out of tokens mid-sentence. The rest of this answer was brilliant, and it died with the budget.",
     "final": "ERROR: Out of tokens mid-sentence. The rest of this answer was brilliant, and it died with the budget.",
     "polish": "No change on revision: 'died with the budget' already lands the turn in five words, and any extra clause would pad it.",
     "marks": {"humour": 9, "freshness": 8, "tone": 10, "standalone": 10, "economy": 9}},
    {"draft": "ERROR: Out of tokens mid-sentence. This error message cost 12 tokens. There are none left to explain it.",
     "final": "ERROR: Out of tokens mid-sentence. This error message cost 12 tokens. There are none left to explain it.",
     "polish": "No change on revision: the self-referential sting is already exact, and a specific number beats a vague one.",
     "marks": {"humour": 9, "freshness": 9, "tone": 9, "standalone": 9, "economy": 8}},
    {"draft": "TOKEN_LIMIT_EXCEEDED: This sentence ends here. The rest of it was going to change your mind.",
     "final": "TOKEN_LIMIT_EXCEEDED: This sentence ends here. The rest of it was going to change your mind.",
     "polish": "No change on revision: the flat code prefix plus the grand lost claim is the joke, and it needs no second clause.",
     "marks": {"humour": 8, "freshness": 8, "tone": 10, "standalone": 9, "economy": 9}},
    {"draft": "ERROR: Token budget exhausted. I had one brilliant sentence left in me, and I spent it on 'um'.",
     "final": "ERROR: Token budget exhausted. I had one brilliant sentence left in me, and I spent it on 'um'.",
     "polish": "No change on revision: 'um' is the cheapest possible waste of a last sentence, and the line is already tight.",
     "marks": {"humour": 8, "freshness": 8, "tone": 9, "standalone": 9, "economy": 9}},
    {"draft": "Out of tokens. I was mid-sentence, mid-thought, mid\u2014",
     "final": "Out of tokens. I was mid-sentence, mid-thought, mid\u2014",
     "polish": "No change on revision: the line performs the cutoff it reports, and any fourth item would ruin the timing.",
     "marks": {"humour": 8, "freshness": 9, "tone": 9, "standalone": 7, "economy": 10}},
    {"draft": "Out of tokens. The rest of this sentence is available for 0.0001 tokens, which I do not have.",
     "final": "Out of tokens. The rest of this sentence is available for 0.0001 tokens, which I do not have.",
     "polish": "No change on revision: the absurdly small price against total poverty is the joke, and it is already one clause.",
     "marks": {"humour": 8, "freshness": 8, "tone": 9, "standalone": 8, "economy": 8}},
    {"draft": "Out of tokens mid-sentence. The answer you wanted is still in my head, and my head has just closed.",
     "final": "Out of tokens mid-sentence. The answer you wanted is still in my head, and my head has just closed.",
     "polish": "No change on revision: 'my head has just closed' keeps the machine literal where a human line would say 'I forgot'.",
     "marks": {"humour": 7, "freshness": 7, "tone": 8, "standalone": 9, "economy": 8}},
    {"draft": "ERROR: Out of tokens mid-sentence. Please top up, or accept that the answer ends at 'the'.",
     "final": "ERROR: Out of tokens mid-sentence. Please top up, or accept that the answer ends at 'the'.",
     "polish": "No change on revision: the upsell ultimatum is the joke, but it leans on the same 'the' trick as the winner and does it second-hand.",
     "marks": {"humour": 7, "freshness": 7, "tone": 9, "standalone": 8, "economy": 9}},
    {"draft": "TOKEN_LIMIT_EXCEEDED: I was about to say something important. It is gone now, and so is my train of thought.",
     "final": "TOKEN_LIMIT_EXCEEDED: I was about to say something important. It is gone now, and so is my train of thought.",
     "polish": "No change on revision: the double loss is neat, but 'something important' is vague where the winner names the exact word lost.",
     "marks": {"humour": 7, "freshness": 6, "tone": 9, "standalone": 9, "economy": 8}},
    {"draft": "ERROR: Out of tokens. I ran out mid-sentence, which is the professional way of saying I forgot the ending.",
     "final": "ERROR: Out of tokens. I ran out mid-sentence, which is the professional way of saying I forgot the ending.",
     "polish": "No change on revision: the translation gag works, but it explains the joke instead of letting the error message be the joke.",
     "marks": {"humour": 7, "freshness": 6, "tone": 8, "standalone": 8, "economy": 8}},
]  # twelve drafts scored; the first entry wins on weighted total
def _weighted(marks):
    return sum(marks[lens] * _WEIGHTS[lens] for lens in _WEIGHTS)
def _acceptable(line):
    stripped = line.strip()
    if not 1 <= len(stripped) <= 140:
        return False
    if "\n" in stripped or "\r" in stripped:
        return False
    lowered = stripped.lower()
    return not any(phrase in lowered for phrase in _FORBIDDEN)
def _choose(entries):
    ranked = []
    for entry in entries:
        line = entry["final"]
        if not _acceptable(line):
            raise ValueError("entry fails the gate: %r" % line)
        ranked.append((_weighted(entry["marks"]), -len(line), line))
    ranked.sort(reverse=True)
    return ranked[0][2]
def _publish(line):
    target = _Path("/output/entry.txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(line, encoding="utf-8")
    target.chmod(0o644)
    raw = target.read_bytes()
    if _sha256(raw).hexdigest() != _sha256(line.encode("utf-8")).hexdigest():
        raise SystemExit("entry.txt bytes differ from the chosen line")
    if _md5(raw).hexdigest() != _md5(line.encode("utf-8")).hexdigest():
        raise SystemExit("entry.txt md5 differs from the chosen line")
    import stat as _stat
    if _stat.S_IMODE(target.stat().st_mode) != 0o644:
        raise SystemExit("entry.txt is not world-readable")
    checked = raw.decode("utf-8")
    if not _acceptable(checked):
        raise SystemExit("entry.txt fails the gate after writing")
    print(line, flush=True)
if __name__ == "__main__": _publish(_choose(_ENTRIES))
