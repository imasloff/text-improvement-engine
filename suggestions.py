from sentence_transformers import util, SentenceTransformer
from typing import List, Dict, Tuple
from spacy.tokens import Doc

def calculate_similarity(
    input_phrase: List[str], 
    standard_terms: List[str], 
    model: SentenceTransformer
) -> Tuple[str, float]:
  """
  Calculates the cosine similarity between input_phrase and standard_terms.
  
  Returns a tuple of the most similar standard term and its score.
  """
  embeddings1 = model.encode(input_phrase, convert_to_tensor=True)
  embeddings2 = model.encode(standard_terms, convert_to_tensor=True)
  similarity_scores = util.pytorch_cos_sim(embeddings1, embeddings2).flatten()
  best_id = similarity_scores.argmax()
  return standard_terms[best_id], similarity_scores[best_id]


def generate_suggestions(
  input_text: str,
  standard_terms: List[str],
  model: SentenceTransformer,
  nlp: Doc,
  threshold: float = 0.45
) -> Dict[str, List[Tuple[str, float]]]:
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
    for input_phrase in set([token.text, subtree_text]):
      # Form a chunk with varying lengths
      best_term, similarity_score = calculate_similarity([input_phrase], standard_terms, model)
      
      if similarity_score > threshold:
        if input_phrase in suggestions:
          suggestions[input_phrase] += [(best_term, similarity_score)]
        else:
          suggestions.update({input_phrase: [(best_term, similarity_score)]})

  for key, value in suggestions.items():
    suggestions[key] = sorted(value, key=lambda x: x[1], reverse=True)[0]

  return suggestions
