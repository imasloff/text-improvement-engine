import spacy
from sentence_transformers import SentenceTransformer

from suggestions import generate_suggestions


def main():
  nlp = spacy.load("en_core_web_lg")
  
  input_text_fname, st_terms_fname = "src/input_text.txt", "src/st_terms.csv"
  with open(input_text_fname, "r") as input_text_file:
    input_text = input_text_file.read()
  with open(st_terms_fname, "r") as st_terms_file:
    st_terms = [line.strip() for line in st_terms_file]

  model = SentenceTransformer(
      'paraphrase-MiniLM-L6-v2')  # Choose a suitable pre-trained model
  suggestions = generate_suggestions(input_text, st_terms, model, nlp)

  print("\nSuggestions:")
  for suggestion in suggestions:
    print(f"""Original: '{suggestion['original_phrase']}'
              Recommended: '{suggestion['recommended_replacement']}'
              Similarity: {suggestion['similarity_score']:.4f}""")


if __name__ == "__main__":
  main()
