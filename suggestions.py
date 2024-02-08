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
    similarity_scores = util.pytorch_cos_sim(
        input_embeddings, standard_embeddings).flatten()
    most_similar_index = similarity_scores.argmax()
    return standard_terms[most_similar_index], round(similarity_scores[most_similar_index].item(), 4)


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

    suggestions = {}
    for token in doc:
        subtree_text = ' '.join(n.text for n in token.subtree)
        phrases_to_check = set([token.text, subtree_text])
        for input_phrase in phrases_to_check:
            best_term, similarity_score = calculate_similarity(
                [input_phrase], standard_terms, model)
            if similarity_score > threshold:
                if input_phrase in suggestions:
                    suggestions[input_phrase] = max(
                        suggestions[input_phrase], (best_term, similarity_score), key=lambda x: x[1])
                else:
                    suggestions[input_phrase] = (best_term, similarity_score)

    return suggestions
