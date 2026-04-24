---
title: Resume Matching Chatbot
emoji: 📄
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

# Resume Matching Chatbot for Hugging Face Spaces

This project is a GitHub-ready and Hugging Face-ready resume chatbot that allows employers to enter required skillsets and receive recommended candidates from uploaded resumes.

## Features

- Employer skillset chatbot
- Guardrails to reject non-skillset questions
- Admin resume upload flow
- PDF, DOCX, and TXT resume parsing
- Candidate ranking using Sentence Transformers
- Downloadable Excel candidate matching report
- Downloadable market skill report
- GitHub Actions template for syncing to Hugging Face Spaces

## Folder Structure

```text
resume-chatbot-hf-github-ready/
├── app.py
├── requirements.txt
├── README.md
├── DEPLOYMENT_GUIDE.md
├── resumes/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── utils/
│   ├── __init__.py
│   ├── guardrails.py
│   ├── market_report.py
│   ├── ranker.py
│   ├── report_generator.py
│   └── resume_loader.py
└── .github/
    └── workflows/
        └── sync-to-huggingface.yml
```

## Local Run

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Hugging Face Deployment

1. Create a new Hugging Face Space.
2. Select Gradio as the SDK.
3. Upload this project or connect it through GitHub.
4. Add resumes through the Admin Resume Upload tab.
5. Use the Employer Skillset Chatbot tab to search candidates.

## Sample Employer Prompt

```text
Python, SQL, machine learning, data analysis, Power BI
```

## Guardrail Behaviour

The chatbot only answers skillset-based employer queries. For non-skillset prompts, it returns:

```text
The bot does not have the answer to your query. Please enter job skillsets only.
```
