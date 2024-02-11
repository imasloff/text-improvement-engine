import os
import spacy
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from typing import Dict, Tuple
from sentence_transformers import SentenceTransformer

from suggestions import generate_suggestions
from utils import load_file, allowed_file


DEFAULT_STANDARD_TERMS_PATH = os.path.join('src', "standard_terms.csv")
DEFAULT_INPUT_TEXT_PATH = os.path.join('src', "input_text.txt")

app = Flask(__name__)


def main(input_text: str = "", standard_terms_path: str = DEFAULT_STANDARD_TERMS_PATH) -> Dict[str, Tuple[str, float]]:
    nlp = spacy.load("en_core_web_md")

    standard_terms = load_file(standard_terms_path).split('\n')

    model = SentenceTransformer('all-mpnet-base-v2')
    suggestions = generate_suggestions(input_text, standard_terms, model, nlp)
    suggestions = dict(
        sorted(suggestions.items(), key=lambda x: x[1][1], reverse=True))
    return suggestions


@app.route("/", methods=["GET", "POST"])
def index():
    standard_terms_path = DEFAULT_STANDARD_TERMS_PATH
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        standard_terms_file = request.files.get("file_upload")
        if standard_terms_file and allowed_file(standard_terms_file.filename):
            fname = secure_filename(standard_terms_file.filename)
            fname, postfix = fname.split('.')
            standard_terms_path = os.path.join('src', secure_filename(
                f"{fname}_{str(datetime.now().date())}.{postfix}"))
            standard_terms_file.save(standard_terms_path)
        return redirect(url_for("result", input_text=input_text, standard_terms_path=standard_terms_path))
    return render_template("index.html")


@app.route("/result")
def result():
    input_text, standard_terms_path = request.args.get(
        "input_text"), request.args.get("standard_terms_path")
    suggestions = main(input_text, standard_terms_path)
    if not suggestions:
        suggestions = "No suggestions found. Please check input text and standard terms files."
    if not isinstance(suggestions, dict):
        fname = 'error.txt'
        output_path = os.path.join('output', fname)
        output_file = open(output_path, "w").write(suggestions)
    else:
        fname = 'suggestions.json'
        output_path = os.path.join('output', fname)
        output_file = json.dump(suggestions, open(output_path, "w", encoding="utf-8"), indent=4)
    return render_template("result.html", suggestions=suggestions, filename=fname)


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    return send_from_directory('output', filename)


if __name__ == "__main__":
    app.run()
