# AI Plant Doctor

Streamlit web app for plant leaf disease detection with an AI-generated treatment report.

## Features

- Upload a plant leaf image
- Validate whether the image looks like a leaf
- Detect plant disease using a pretrained image classification model
- Extract plant name and disease name from the model output
- Generate a structured report with:
  - scientific name
  - description
  - treatment steps
  - recommended fertilizers
  - improvement tips
  - healthy leaf comparison
- Show a separate diagnosis result page after upload

## Project Structure

```text
AIKRProject/
|-- app.py
|-- README.md
|-- requirements.txt
|-- models/
|   `-- classes.json
`-- utils/
    |-- __init__.py
    |-- groq_helper.py
    |-- leaf_check.py
    `-- predict.py
```

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

If `streamlit` is not on your PATH, run:

```bash
python -m streamlit run app.py
```

## Groq API Key

The app uses Groq for the AI report.

Set your key in the environment before starting the app:

```powershell
$env:GROQ_API_KEY="your_api_key_here"
```
Replace the following in `groq_helper.py`:

```python
DEFAULT_GROQ_API_KEY = ""
```

with:

```python
DEFAULT_GROQ_API_KEY = "your_groq_api_key_here"
```

## Notes

- `leaf_check.py` currently uses a lightweight heuristic leaf check.
- `predict.py` uses the pretrained Hugging Face plant disease model.
- If Groq is unavailable, the app generates a local fallback report so the UI still works.
