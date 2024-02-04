import spacy
from typing import Any
from sentence_transformers import SentenceTransformer

from suggestions import generate_suggestions


def load_file(fname: str) -> Any:
  """
  Loads the file from src directiry, 
  reads and return its contents,
  deals with exceptions.
  """
  try:
    with open('src/' + fname, "r") as file:
      content = file.read()
    return content
  except FileNotFoundError:
    print(f"Error: File not found at {fname}. Please check the file path.")
    exit(1)
  except Exception as e:
    print(f"Error loading file at {fname}: {e}")
    exit(1)

def main():
  nlp = spacy.load("en_core_web_md")

  print("\nDon't forget to add your input files" +
        "\n(one containing input text and one containing standard terms)" +
        "\ninto the /src directory\n")
  
  input_text_fname = input('File with input text (e.g. input_text.txt): ')
  standard_terms_fname = input('File with standard terms (e.g. standard_terms.csv): ')

  input_text = load_file(input_text_fname)
  standard_terms = load_file(standard_terms_fname).split('\n')

  model = SentenceTransformer('all-mpnet-base-v2')
  suggestions = generate_suggestions(input_text, standard_terms, model, nlp)

  print("\nSuggestions:")
  for input_phrase, suggestion in sorted(
    suggestions.items(),
    key=lambda x: x[1][1],
    reverse=True
  ):
    print(
      f"\nOriginal: '{input_phrase}'\n" +
      f"Recommended: '{suggestion[0]}'\n" +
      f"Similarity: {suggestion[1]:.4f}"
    )


if __name__ == "__main__":
  main()
