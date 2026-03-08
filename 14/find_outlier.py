import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing sentence-transformers...")
    install('sentence-transformers')
    from sentence_transformers import SentenceTransformer

try:
    import numpy as np
except ImportError:
    print("Installing numpy...")
    install('numpy')
    import numpy as np

try:
    from scipy.spatial.distance import cosine
except ImportError:
    print("Installing scipy...")
    install('scipy')
    from scipy.spatial.distance import cosine

headlines = [
    "Open-source language model surpasses proprietary benchmarks on reasoning tasks",
    "Autonomous vehicle startup completes one million miles of driverless testing",
    "Quantum computing breakthrough achieves error correction milestone",
    "Cybersecurity firm discovers critical zero-day vulnerability in popular browser",
    "Mental health app demonstrates effectiveness in reducing anxiety symptoms",
    "Robotics company demonstrates humanoid robot performing warehouse tasks"
]

# Using a standard fast text embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(headlines)

# Compute mean centroid
centroid = np.mean(embeddings, axis=0)

# Calculate cosine distances from centroid
distances = [cosine(emb, centroid) for emb in embeddings]

# Find the semantic outlier (maximum distance)
outlier_idx = np.argmax(distances)

print("="*40)
print(f"The semantic outlier is headline {outlier_idx}:\n{headlines[outlier_idx]}")
print("="*40)
for i, d in enumerate(distances):
    print(f"Headline {i} distance: {d:.4f}")
