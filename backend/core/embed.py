import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = None


def reset_vectorizer():
    """Resets TF-IDF so each PDF is independent."""
    global vectorizer
    vectorizer = TfidfVectorizer(stop_words="english")


def embed_texts(texts):
    global vectorizer

    if not texts:
        return []

    if vectorizer is None:
        reset_vectorizer()

    vectorizer.fit(texts)

    vectors = vectorizer.transform(texts).toarray()

    if vectors.shape[1] < 384:
        vectors = np.pad(vectors, ((0, 0), (0, 384 - vectors.shape[1])))
    else:
        vectors = vectors[:, :384]

    return vectors
