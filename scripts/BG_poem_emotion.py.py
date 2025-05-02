"""
Detailed emotion analysis with EmoRoBERTa (28 Go-Emotions labels)

Prereqs:
  • transformers ≥ 4.28
  • torch (CPU or CUDA)
  • huggingface-hub token cached locally
  • EmoRoBERTa repo access approved once in the browser
"""

from transformers import pipeline, AutoTokenizer
import math, torch

# ── configuration ─────────────────────────────────────────────────────────
MODEL_NAME = "Sindhu/emo_roberta"    # 28-label gated model
MAX_LEN    = 512                         # model context window
DEVICE     = 0 if torch.cuda.is_available() else -1   # GPU if present

# ── helper: split by *token* count ───────────────────────────────────────
tok = AutoTokenizer.from_pretrained(MODEL_NAME)

def split_by_tokens(text, max_len=MAX_LEN):
    ids = tok(text, add_special_tokens=False)["input_ids"]
    return [
        tok.decode(ids[i : i + max_len])
        for i in range(0, len(ids), max_len)
    ]

# ── build the classification pipeline ────────────────────────────────────
emo = pipeline(
    "text-classification",
    model=MODEL_NAME,
    top_k=None,          # full probability vector (replaces return_all_scores)
    device=DEVICE

)

# ── your poem (replace with any text) ────────────────────────────────────
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

import json

# Split the poem into lines
lines = poem_text.strip().split("\n")

# Prepare a list to store results
results_data = []

# Process each line individually
for idx, line in enumerate(lines, 1):
    if line.strip():  # Skip empty lines
        result = emo(line, truncation=True)
        
        # Debugging: Print the result to inspect its structure
        print(f"Result for line {idx}: {result}")
        
        # Store the results in a structured format
        line_data = {
            "line_number": idx,
            "text": line,
            "emotions": sorted(result[0], key=lambda x: x["score"], reverse=True)
        }
        results_data.append(line_data)

# Export results to a JSON file
output_file = "/Users/boryana/Desktop/Creative-Computing/python/emotion_results.json"
with open(output_file, "w") as f:
    json.dump(results_data, f, indent=4)

print(f"Emotion analysis results saved to {output_file}")











