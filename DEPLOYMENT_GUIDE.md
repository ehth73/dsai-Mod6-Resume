# Hugging Face Deployment Guide

## 1. Create the Hugging Face Space

1. Go to Hugging Face.
2. Click **New Space**.
3. Set the SDK to **Gradio**.
4. Choose CPU Basic for initial testing.
5. Create the Space.

## 2. Upload Files Manually

Upload the following files and folders into the Space:

```text
app.py
requirements.txt
README.md
utils/
resumes/
reports/
```

The Space will install dependencies from `requirements.txt` and launch `app.py`.

## 3. Deploy Through GitHub

Create a GitHub repository and upload this project.

Add these GitHub repository secrets:

```text
HF_TOKEN = your Hugging Face access token
HF_USERNAME = your Hugging Face username
HF_SPACE_NAME = your Hugging Face Space name
```

Then enable the included GitHub Actions workflow:

```text
.github/workflows/sync-to-huggingface.yml
```

## 4. Upload Resumes

Use the **Admin Resume Upload** tab in the app.

Supported formats:

```text
.pdf
.docx
.txt
```

## 5. Employer Usage

Use the **Employer Skillset Chatbot** tab and enter required skillsets only.

Example:

```text
Python, SQL, credit risk, compliance, Power BI
```

The app returns:

- Top matching candidates
- Match score
- Matched terms or reason
- Resume path
- Downloadable candidate report
- Downloadable market skill report

## 6. Production Notes

For production use, consider:

- Private Hugging Face Space
- Persistent storage
- Admin authentication
- Personal data handling and PDPA review
- Resume deletion workflow
- Audit logging
- Malware scanning for uploaded files
- Role-based access control
