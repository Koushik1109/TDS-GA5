# /// script
# requires-python = ">=3.11"
# dependencies = ["sentence-transformers", "Pillow", "numpy"]
# ///

from sentence_transformers import SentenceTransformer, util
from PIL import Image
import os
import glob

TEXT_QUERY = "a red wooden barn standing in a golden wheat field"

def main():
    model = SentenceTransformer('clip-ViT-B-32')
    
    # Load all images
    img_dir = "images"
    if not os.path.exists(img_dir):
        # Fallback if images are in current directory
        img_paths = glob.glob("img_*.jpg")
    else:
        img_paths = glob.glob(os.path.join(img_dir, "img_*.jpg"))
        
    img_paths.sort()
    
    if not img_paths:
        print("No images found.")
        return

    # Compute text embedding
    text_emb = model.encode([TEXT_QUERY])

    # Process images
    images = [Image.open(p) for p in img_paths]
    img_embs = model.encode(images)
    
    # Compute cosine similarity
    cos_scores = util.cos_sim(text_emb, img_embs)[0]
    
    best_idx = cos_scores.argmax().item()
    best_img = os.path.basename(img_paths[best_idx])
    
    print(best_img)

if __name__ == "__main__":
    main()
