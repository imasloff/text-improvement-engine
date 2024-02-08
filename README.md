# Text Improvement Engine

## Overview

This tool analyzes input text and suggests improvements based on semantic similarity to a list of standard phrases. It provides both a command-line interface (CLI) and a simple web-based user interface (UI).

## Technologies Used

1. **Spacy**: Utilized for natural language processing (NLP) tasks, including tokenization and syntactic analysis.
2. **Sentence Transformers**: Employed for generating contextualized embeddings of phrases, enabling semantic similarity calculations.
3. **Flask**: Integrated into a lightweight web application for user-friendly interaction through a web interface.

## Rationale Behind Design Decisions

### Choice of NLP Model (Spacy)

Spacy was chosen for its efficiency in tokenization and syntactic analysis. Its pre-trained English model, "en_core_web_md", provides accurate tokenization and dependency parsing, contributing to the semantic understanding required for the Text Improvement Engine. The version of the model can be replaced with "en_core_web_lg" for slightly better accuracy or with "en_core_web_sm" for slightly better performance.

### Embeddings for Similarity Calculation (Sentence Transformers)

The Sentence Transformers library was selected to encode input phrases and standard terms into embeddings. This choice was motivated by its ability to capture contextual information, enhancing the semantic similarity calculations crucial for suggesting suitable replacements.

### User Interface (Flask)

Flask, a micro web framework, was chosen for its simplicity and ease of integration. The lightweight nature of Flask allows for quick development and deployment of a user interface.

### Threshold Setting and Suggestions Ranking

The threshold for similarity (set at 0.45) was chosen empirically to balance precision and recall. Suggestions are ranked based on similarity scores, allowing users to focus on the most relevant replacements first.

### Command-Line Interface (CLI) for Quick Assessment

The CLI provides a straightforward way to assess the Text Improvement Engine quickly. Users can run the CLI script, input file names, and receive instant suggestions and similarity scores.

## Project Structure

```plaintext
/text_improvement_engine
|-- output
|   |-- suggestions.json
|-- src
|   |-- input_text.txt
|   |-- standard_terms.csv
|-- templates
|   |-- index.html
|-- cli.py
|-- README.md
|-- requirements.txt
|-- suggestions.py
|-- ui.py
|-- utils.py
```

## Setup

1. Clone this repository:

```bash
git clone https://github.com/imasloff/text-improvement-engine.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface (CLI)

Run the CLI script:

```bash
python cli.py
```

Follow the instructions to input the standard terms and the file containing the input text or skip them to use the default files.

### User Interface (UI)

1. Run the UI script:

```bash
python ui.py
```

2. Open your web browser and go to http://127.0.0.1:5000/.
3. Input the text in the provided textarea and upload the standard terms file (in TXT or CSV format), you can skip file upload to use default standard terms.

## Results Analysis

The results are saved in the output directory. For CLI, it prints suggestions on the console. For the UI, it both generates a JSON file (suggestions.json) containing replacement suggestions with their similarity scores and prints them in UI form.
