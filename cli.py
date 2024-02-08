import os
import spacy
from sentence_transformers import SentenceTransformer
from werkzeug.utils import secure_filename

from suggestions import generate_suggestions
from utils import load_file, allowed_file


DEFAULT_STANDARD_TERMS_PATH = os.path.join('src', "standard_terms.csv")
DEFAULT_INPUT_TEXT_PATH = os.path.join('src', "input_text.txt")


def main():
  nlp = spacy.load("en_core_web_md")

  print("\nDon't forget to add your input files" +
        "\n(one containing input text and one containing standard terms)" +
        "\ninto the /src directory\n")
  
  while True:
    standard_terms_fname = secure_filename(
      input('Name of the file with standard terms (txt or csv)\nPress Enter to use default: ')
    )

    if not standard_terms_fname:
      break

    if standard_terms_fname and allowed_file(standard_terms_fname):
      break

    if not allowed_file(standard_terms_fname):
      print("File type not allowed. Please upload a txt or csv file.")

  standard_terms_path = os.path.join('src', standard_terms_fname) if standard_terms_fname else DEFAULT_STANDARD_TERMS_PATH
  standard_terms = load_file(standard_terms_path).split('\n')

  input_text_fname = input('Name of the file containing the input text\nPress Enter to use default: ')
  input_text_path = os.path.join('src', input_text_fname) if input_text_fname else DEFAULT_INPUT_TEXT_PATH
  input_text = load_file(input_text_path)

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

if __name__=='__main__':
  main()