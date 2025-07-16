from datetime import datetime
import os

def save_transcript(lines, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"💾 Transcript saved to {path}")

