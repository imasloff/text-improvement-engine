import numpy as np
from sentence_transformers import util, SentenceTransformer
from typing import List, Dict, Tuple
from spacy.tokens import Doc


def calculate_similarity(input_phrases: List[str], standard_terms: List[str], model: SentenceTransformer) -> Tuple[str, float]:
    """
    Calculates the cosine similarity between input_phrases and standard_terms.

    Returns a tuple of the most similar standard term and its score.
    """
    input_embeddings = model.encode(input_phrases, convert_to_tensor=True)
    standard_embeddings = model.encode(standard_terms, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(input_embeddings, standard_embeddings).cpu().numpy()
    return similarity_scores


def generate_suggestions(
    input_text: str,
    standard_terms: List[str],
    model: SentenceTransformer,
    nlp: Doc,
    threshold: float = 0.45
) -> Dict[str, Tuple[str, float]]:
    """
    Generates replacement suggestions for input_text 
    based on the similarity between certain phrases in this text and standard_terms.

    Returns a dictionary with the keys of the input phrases proposed for replacement 
    and the values of the most similar standard terms with their ratings.
    """
    doc = nlp(input_text)

    input_phrases = set()
    for token in doc:
        subtree_text = ' '.join(n.text.lower() for n in token.subtree)
        input_phrases.add(token.text.lower())
        input_phrases.add(subtree_text)

    standard_terms = [term.lower() for term in standard_terms]

    similarity_scores = calculate_similarity(list(input_phrases), standard_terms, model)
    
    suggestions = {}
    for input_phrase, scores in zip(input_phrases, similarity_scores):
        above_threshold = np.where(scores > threshold)[0]
        for index in above_threshold:
            best_term = standard_terms[index]
            best_suggestion = (best_term, round(np.float64(scores[index]), 4))
            suggestions[input_phrase] = max(
                suggestions.get(input_phrase, best_suggestion),
                best_suggestion,
                key=lambda x: x[1]
            )

    return suggestions
