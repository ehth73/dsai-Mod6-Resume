import os
from datetime import datetime

import pandas as pd


def save_candidate_report(df: pd.DataFrame, skill_query: str, output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(output_dir, f"candidate_matching_report_{timestamp}.xlsx")

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        summary = pd.DataFrame({
            "Field": ["Required Skillsets", "Generated At", "Number of Candidates"],
            "Value": [skill_query, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), len(df)]
        })
        summary.to_excel(writer, sheet_name="Summary", index=False)
        df.to_excel(writer, sheet_name="Top Candidates", index=False)

    return path
