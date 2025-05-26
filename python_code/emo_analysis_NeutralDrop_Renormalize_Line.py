"""
Detailed emotion analysis with EmoRoBERTa (28 Go‑Emotions labels)
Neutral is removed and the remaining probabilities are renormalised.

Prereqs:
  • transformers ≥ 4.28
  • torch (CPU or CUDA)
  • huggingface‑hub token cached locally
"""

from transformers import pipeline, AutoTokenizer
import json, torch, os

# ── configuration ──────────────────────────────────────────────────
MODEL_NAME = "Sindhu/emo_roberta"      # 28‑label gated model
DEVICE     = 0 if torch.cuda.is_available() else -1   # GPU if present
MAX_LEN    = 512                       # model context window
OUTPUT_FILE = os.path.expanduser("~/emotion_results_lines.json")

# ── helper: split by lines ─────────────────────────────────────────
def split_into_lines(text):
    return [line.strip() for line in text.strip().split("\n") if line.strip()]

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
He lives—still lives! High on the Balkan crest,
blood-soaked, he sprawls and gasps for mortal breath:
a hero, manly, young, a wound deep-pressed
wide in his chest now wrestles him toward death.

His rifle flung to one side in the mud,
his sabre shattered, useless, on the ground;
his darkening eyes reel back beneath the blood,
and cursing lips damn all the world around.

The hero lies there, while above his head
the sullen sun stands still and scorches on;
afar a reaper’s field-song ripples red,
and faster yet his streaming blood is drawn.

It is the harvest… sing, enslaved wives, sing
those sorrowed songs! Shine too, relentless sun,
upon this shackled earth. This youth will bring
his life to end—but hush, wild heart, be done!

For he who falls for freedom’s sacred breath
can never die: the grieving earth and sky,
the beast, the forest, mourn his noble death,
and poets weave his name so none may die.

By day an eagle spreads its shade above,
a wolf with gentle tongue will lick the wound;
a falcon—hero’s bird and brother’s love—
stands guard, a silent watcher overground.

At dusk the crescent moon ascends the blue,
and starlight floods the arch of heaven’s hall;
the forest murmurs, winds awaken, too—
the Balkan lifts a rebel battle-call!

Then woodland nymphs in shining linen white,
wondrous, ethereal, begin their song;
soft through the moonlit grass they steal by night
and round the hero form a magic throng.

One binds his wound with herbs of mountain birth,
one sprinkles icy water on his brow,
a third lands swift a kiss of living worth—
he gazes, dazzled by her beauty’s vow.

“Tell me, O sister, where does Karadzha lie?
Where is my band, my faithful comrades brave?
Tell me—and take my soul—for here I’ll die;
here on this slope I seek my final grave.”

They clap their hands; they clasp, a shining host,
and singing, rise toward the vaulted height—
they soar through midnight, searching for the ghost
of Karadzha, singing through the night…

But dawn arrives! And on the Balkan side
the hero bleeds; his lifeblood drains away.
A wolf still licks the savage wound he hides,
and still the sun beats down its ruthless ray.
"""

lines = split_into_lines(poem_text)

# ── analyse & post‑process ────────────────────────────────────────
results_data = []

for idx, line in enumerate(lines, 1):
    out = emo(line)[0]                    # list[dict(label, score)]

    # 1. drop neutral
    non_neutral = [r for r in out if r["label"] != "neutral"]

    # 2. renormalise
    denom = sum(r["score"] for r in non_neutral) or 1.0
    for r in non_neutral:
        r["rel_score"] = r["score"] / denom

    # 3. store sorted by relative salience
    line_data = {
        "line_number": idx,
        "text": line,
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
    results_data.append(line_data)

# ── write JSON ────────────────────────────────────────────────────
output_file = "/Users/boryana/Desktop/Creative-Computing/python/emotion_results_NoNeutral_HadjiDimitarBG_lines.json"

# Add metadata for the poem
poem_metadata = {
    "title": "Hadji Dimitar",
    "author": "Hristo Botev",
    "lines_analysis": results_data  # Add the line-by-line analysis here
}

# Write the JSON file
with open(output_file, "w", encoding="utf-8") as f:  # Ensure UTF-8 encoding
    json.dump(poem_metadata, f, indent=4, ensure_ascii=False)  # Save the metadata
print(f"Emotion analysis saved to {output_file}")