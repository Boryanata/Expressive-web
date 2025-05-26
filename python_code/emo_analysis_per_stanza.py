"""
Detailed emotion analysis with EmoRoBERTa (28 Go-Emotions labels)

Prereqs:
  • transformers ≥ 4.28
  • torch (CPU or CUDA)
  • huggingface-hub token cached locally
  • EmoRoBERTa repo access approved once in the browser
"""

from transformers import pipeline, AutoTokenizer
import json, torch

# ── configuration ─────────────────────────────────────────────────────────
MODEL_NAME = "Sindhu/emo_roberta"    # 28-label gated model
MAX_LEN    = 512                     # model context window
DEVICE     = 0 if torch.cuda.is_available() else -1   # GPU if present

# ── helper: split by *token* count ───────────────────────────────────────
tok = AutoTokenizer.from_pretrained(MODEL_NAME)

# ── build the classification pipeline ────────────────────────────────────
emo = pipeline(
    "text-classification",
    model=MODEL_NAME,
    device=DEVICE
)

# ── your poem (replace with any text) ────────────────────────────────────
poem_text = """
No man is an island,
Entire of itself;
Every man is a piece of the continent,
A part of the main.

If a clod be washed away by the sea,
Europe is the less,
As well as if a promontory were:
As well as if a manor of thy friend's
Or of thine own were.

Any man's death diminishes me,
Because I am involved in mankind.
And therefore never send to know for whom the bell tolls;
It tolls for thee.
"""

# Split the poem into stanzas (stanzas are separated by blank lines)
stanzas = poem_text.strip().split("\n\n")

# Prepare a list to store results for the entire poem
results_data = []

# Process each stanza individually
for idx, stanza in enumerate(stanzas, 1):
    if stanza.strip():  # Skip empty stanzas
        result = emo(stanza, truncation=True, return_all_scores=True)  # Ensure all scores are returned
        
        # Debugging: Print the result to inspect its structure
        print(f"Result for stanza {idx}: {result}")
        
        # Store the results in a structured format
        stanza_data = {
            "stanza_number": idx,
            "text": stanza,
            "emotions": [
                {"label": emotion["label"], "score": emotion["score"]}
                for emotion in sorted(result[0], key=lambda x: x["score"], reverse=True)  # Sort by score
            ]
        }
        results_data.append(stanza_data)

# Export all results to a single JSON file
output_file = "/Users/boryana/Desktop/Creative-Computing/python/emotion_results_stanzas.json"
with open(output_file, "w") as f:
    json.dump(results_data, f, indent=4)

print(f"Emotion analysis results for the entire poem saved to {output_file}")