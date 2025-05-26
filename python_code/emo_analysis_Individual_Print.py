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
This being human is a guest house—
every dawn a new arrival.
Welcome whatever comes:
joy, sadness, meanness, a sudden clarity,
the dark thought, the shame, the malice—
meet them at the door laughing, and invite them in.
Even if a crowd of sorrows
sweeps your house bare of its furniture,
still, treat each guest honorably;
they may be clearing you out
for some new delight.
The sorrow, the grief, the hate—
greet them at the threshold; thank them,
for each has been sent
as a guide from beyond.
"""

import json

# Split the poem into lines
lines = poem_text.strip().split("\n")

# Prepare a list to store results for the entire poem
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

# Export all results to a single JSON file
output_file = "/Users/boryana/Desktop/Creative-Computing/python/emotion_results_poem.json"
with open(output_file, "w") as f:
    json.dump(results_data, f, indent=4)

print(f"Emotion analysis results for the entire poem saved to {output_file}")