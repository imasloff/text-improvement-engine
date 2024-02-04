import spacy
import string
from sentence_transformers import util


def calculate_similarity(phrase1, phrase2, model):
  embeddings1 = model.encode(phrase1, convert_to_tensor=True)
  embeddings2 = model.encode(phrase2, convert_to_tensor=True)
  similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
  return similarity_score


def generate_suggestions(input_text,
                         standardized_terms,
                         model,
                         nlp,
                         threshold=0.7):

  doc = nlp(input_text)
  cleared_tokens = [
      token.text.lower() for token in doc
      if not token.is_stop and token.is_alpha
  ]
  suggestions = []
  for i in range(len(cleared_tokens)):
    for chunk_size in range(1, min(5, len(cleared_tokens) - i)):
      # Form a chunk with varying lengths
      input_phrase = ' '.join(cleared_tokens[j]
                              for j in range(i, i + chunk_size))

      for standardized_term in standardized_terms:
        similarity_score = calculate_similarity([input_phrase],
                                                [standardized_term], model)
        if similarity_score > threshold:
          suggestions.append({
              "original_phrase": input_phrase,
              "recommended_replacement": standardized_term,
              "similarity_score": similarity_score
          })
          break

  return suggestions
