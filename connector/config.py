from pathlib import Path

# TODO dynamically save and extract if missing
GLOVEVERSION = "glove.42B.300d"
DIMENSIONS = 300
GLOVEURL = f"https://nlp.stanford.edu/data/{GLOVEVERSION}.zip"
# EMBEDDINGPATH = f"data/{GLOVEVERSION}.txt"
EMBEDDINGPATH = Path(__file__).parent / "../data/testembeddings.txt"
