import sys
from pathlib import Path

# Add the script's directory to the path to allow relative imports
sys.path.insert(0, str(Path(__file__).parent))

import os
import shutil

import gradio as gr
import pandas as pd

from utils.guardrails import guardrail_response, is_skillset_query
from utils.market_report import generate_market_skill_report
from utils.ranker import rank_candidates
from utils.report_generator import save_candidate_report
from utils.resume_loader import load_resumes

RESUME_DIR = Path("resumes")
REPORT_DIR = Path("reports")
RESUME_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


def employer_chatbot(skill_query: str, top_k: int):
    """Employer-facing chatbot flow."""
    if not skill_query or not skill_query.strip():
        return "Please enter the required job skillsets.", pd.DataFrame(), None, None

    if not is_skillset_query(skill_query):
        return guardrail_response(), pd.DataFrame(), None, None

    resumes = load_resumes(str(RESUME_DIR))
    if not resumes:
        return "No resumes are available. Please ask the administrator to upload resumes first.", pd.DataFrame(), None, None

    ranked_df = rank_candidates(skill_query, resumes, top_k=int(top_k))
    candidate_report_path = save_candidate_report(ranked_df, skill_query, str(REPORT_DIR))
    market_report_path = generate_market_skill_report(resumes, str(REPORT_DIR))

    message = (
        f"Found the top {len(ranked_df)} recommended candidate(s) based on the required skillsets. "
        "Download the Excel report for full details."
    )
    return message, ranked_df, candidate_report_path, market_report_path


def admin_upload_resume(files):
    """Admin upload flow for resume files."""
    if not files:
        return "No files selected.", list_uploaded_resumes()

    allowed_ext = {".pdf", ".docx", ".txt"}
    uploaded = []
    rejected = []

    for file in files:
        src = Path(file.name)
        ext = src.suffix.lower()
        if ext not in allowed_ext:
            rejected.append(src.name)
            continue

        target = RESUME_DIR / src.name
        counter = 1
        while target.exists():
            target = RESUME_DIR / f"{src.stem}_{counter}{src.suffix}"
            counter += 1

        shutil.copy(src, target)
        uploaded.append(target.name)

    msg_parts = []
    if uploaded:
        msg_parts.append("Uploaded: " + ", ".join(uploaded))
    if rejected:
        msg_parts.append("Rejected unsupported files: " + ", ".join(rejected))

    return " | ".join(msg_parts) if msg_parts else "No valid files uploaded.", list_uploaded_resumes()


def list_uploaded_resumes():
    rows = []
    for path in sorted(RESUME_DIR.glob("*")):
        if path.is_file() and path.name != ".gitkeep":
            rows.append({
                "File Name": path.name,
                "File Type": path.suffix.lower(),
                "Size KB": round(path.stat().st_size / 1024, 2),
            })
    return pd.DataFrame(rows)


def refresh_resume_table():
    return list_uploaded_resumes()


with gr.Blocks(title="Resume Matching Chatbot") as demo:
    gr.Markdown("# Resume Matching Chatbot")
    gr.Markdown(
        "Employer users can enter job skillsets to find matching candidates. "
        "Admin users can upload resume files for matching."
    )

    with gr.Tab("Employer Skillset Chatbot"):
        skill_query = gr.Textbox(
            label="Required Skillsets",
            placeholder="Example: Python, SQL, machine learning, credit risk, Excel",
            lines=4,
        )
        top_k = gr.Slider(1, 10, value=3, step=1, label="Number of candidates to return")
        search_button = gr.Button("Find Matching Candidates")
        response_text = gr.Textbox(label="Chatbot Response")
        results_table = gr.Dataframe(label="Recommended Candidates")
        candidate_report = gr.File(label="Download Candidate Excel Report")
        market_report = gr.File(label="Download Market Skill Report")

        search_button.click(
            employer_chatbot,
            inputs=[skill_query, top_k],
            outputs=[response_text, results_table, candidate_report, market_report],
        )

    with gr.Tab("Admin Resume Upload"):
        gr.Markdown("Upload PDF, DOCX, or TXT resumes into the resume repository.")
        upload_files = gr.File(label="Upload Resumes", file_count="multiple")
        upload_button = gr.Button("Upload Resume Files")
        upload_status = gr.Textbox(label="Upload Status")
        resume_table = gr.Dataframe(label="Uploaded Resumes", value=list_uploaded_resumes())
        refresh_button = gr.Button("Refresh Resume List")

        upload_button.click(admin_upload_resume, inputs=upload_files, outputs=[upload_status, resume_table])
        refresh_button.click(refresh_resume_table, outputs=resume_table)

if __name__ == "__main__":
    demo.launch()
