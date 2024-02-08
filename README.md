# Text Improvement Engine

## Overview

This tool analyzes input text and suggests improvements based on semantic similarity to a list of standard phrases. It provides both a command-line interface (CLI) and a simple web-based user interface (UI).

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
3. Input the text in the provided textarea and upload the standard terms file (in TXT or CSV format).

## Results Analysis

The results are saved in the output directory. For CLI, it prints suggestions on the console. For the UI, it both generates a JSON file (suggestions.json) containing replacement suggestions with their similarity scores and prints them in UI form.
