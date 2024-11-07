import re

import pandas as pd
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def parse_code():
    df = pd.read_csv("CSV_files/pre-llm-code.csv")

    pre_LLM = {
        "Dec-18": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Jan-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Feb-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Mar-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Apr-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "May-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Jun-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Jul-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Aug-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Sep-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Oct-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Nov-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Dec-19": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Jan-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Feb-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Mar-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Apr-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "May-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Jun-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Jul-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Aug-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
        "Sep-20": {
            "question": [],
            "answer_score": [],
            "answer": [],
            "question_tags": [],
        },
    }

    for index, row in df.iterrows():
        if row.iloc[0] in pre_LLM:
            pre_LLM[row.iloc[0]]["question"].append(row.iloc[2])
            pre_LLM[row.iloc[0]]["answer_score"].append(row.iloc[3])
            pre_LLM[row.iloc[0]]["answer"].append(row.iloc[4])
            pre_LLM[row.iloc[0]]["question_tags"].append(row.iloc[5])
    generate_pdf_report(pre_LLM)


def generate_pdf_report(data_dict):
    doc = SimpleDocTemplate("pre_llm_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    for month, details in data_dict.items():
        story.append(Paragraph(f"<b>Month: {month}</b>", styles["Heading2"]))

        for i in range(len(details["question"])):
            question = sanitize_html(details["question"][i])
            answer_score = details["answer_score"][i]
            answer = sanitize_html(details["answer"][i])
            question_tags = sanitize_html(details["question_tags"][i])

            story.append(Paragraph(f"<b>Question {i + 1}:</b>", styles["BodyText"]))
            story.append(Paragraph(f"<b>Tags:</b> {question_tags}", styles["BodyText"]))
            story.append(Paragraph(f"<b>Question:</b> {question}", styles["BodyText"]))
            story.append(
                Paragraph(f"<b>Answer Score:</b> {answer_score}", styles["BodyText"])
            )
            story.append(Paragraph(f"<b>Answer:</b> {answer}", styles["BodyText"]))
            story.append(Spacer(1, 12))

    doc.build(story)
    print("PDF report generated successfully!")


def sanitize_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for img_tag in soup.find_all("img"):
        img_tag.decompose()

    for sub_tag in soup.find_all("sub"):
        sub_tag.decompose()

    for tag in soup.find_all(True):
        if tag.name == "a":
            unsupported_attrs = ["rel", "title"]
            for attr in unsupported_attrs:
                if attr in tag.attrs:
                    del tag.attrs[attr]

    for br_tag in soup.find_all("br"):
        br_tag.replace_with("\n")

    return str(soup)


if __name__ == "__main__":
    parse_code()
