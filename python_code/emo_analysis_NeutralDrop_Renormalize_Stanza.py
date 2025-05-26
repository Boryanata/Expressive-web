"""
Detailed emotion analysis with EmoRoBERTa (28 Go‑Emotions labels)
Neutral is removed and the remaining probabilities are renormalised.

Prereqs:
  • transformers ≥ 4.28
  • torch (CPU or CUDA)
  • huggingface‑hub token cached locally
"""

from transformers import pipeline, AutoTokenizer
import json, torch, textwrap, os

# ── configuration ──────────────────────────────────────────────────
MODEL_NAME = "Sindhu/emo_roberta"      # 28‑label gated model
DEVICE     = 0 if torch.cuda.is_available() else -1   # GPU if present
MAX_LEN    = 512                       # model context window
OUTPUT_FILE = os.path.expanduser("~/emotion_results_stanzas.json")

# ── helper: split by *token* count (keeps stanzas <512 tokens) ──
tok = AutoTokenizer.from_pretrained(MODEL_NAME)

def split_into_stanzas(text, max_len=MAX_LEN):
    raw = text.strip().split("\n\n")
    chunks = []
    for stanza in raw:
        # If a stanza is too long, break it further on sentence ends
        tokens = tok(stanza)["input_ids"]
        if len(tokens) <= max_len:
            chunks.append(stanza.strip())
        else:
            # crude sentence split → wrap & regroup until < max_len
            for sent in textwrap.wrap(stanza.replace("\n", " "), width=200):
                chunks.append(sent.strip())
    return [c for c in chunks if c]

# ── build pipeline ────────────────────────────────────────────────
emo = pipeline(
    "text-classification",
    model=MODEL_NAME,
    device=DEVICE,
    return_all_scores=True,
    truncation=True
)

# ── your poem (replace with any text) ─────────────────────────────
poem_text = """
This being human is a guest house.
Every morning a new arrival.
A joy, a depression, a meanness,
some momentary awareness comes
as an unexpected visitor.
Welcome and entertain them all!
Even if they are a crowd of sorrows,
who violently sweep your house
empty of its furniture,
still, treat each guest honorably.
He may be clearing you out
for some new delight.
The dark thought, the shame, the malice.
meet them at the door laughing and invite them in.
Be grateful for whatever comes.
because each has been sent
as a guide from beyond.
"""

stanzas = split_into_stanzas(poem_text)

# ── analyse & post‑process ────────────────────────────────────────
results_data = []

for idx, stanza in enumerate(stanzas, 1):
    out = emo(stanza)[0]                    # list[dict(label, score)]

    # 1. drop neutral
    non_neutral = [r for r in out if r["label"] != "neutral"]

    # 2. renormalise
    denom = sum(r["score"] for r in non_neutral) or 1.0
    for r in non_neutral:
        r["rel_score"] = r["score"] / denom

    # 3. store sorted by relative salience
    stanza_data = {
        "stanza_number": idx,
        "text": stanza,
        "emotions": sorted(
            [
                {"label": r["label"],
                 "raw_score": round(r["score"], 6),
                 "rel_score": round(r["rel_score"], 6)}
                for r in non_neutral
            ],
            key=lambda x: x["rel_score"],
            reverse=True
        )
    }
    results_data.append(stanza_data)

# ── write JSON ────────────────────────────────────────────────────
output_file = "/Users/boryana/Desktop/Creative-Computing/python/emotion_results_NoNeutral_stanzas.json"
with open(output_file, "w") as f:  # Use `output_file` here
    json.dump(results_data, f, indent=4)
print(f"Emotion analysis saved to {output_file}")