import re

import pandas as pd
import spacy
from bs4 import BeautifulSoup
from reportlab.lib import colors, fonts
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def parse_code():
    df = pd.read_csv("CSV_files/pre-llm-code.csv")

    pre_LLM = {
        "Dec-18": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Jan-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Feb-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Mar-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Apr-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "May-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Jun-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Jul-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Aug-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Sep-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Oct-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Nov-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Dec-19": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Jan-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Feb-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Mar-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Apr-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "May-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Jun-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Jul-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Aug-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
        "Sep-20": {
            "question": [],
            "answer_score": [],
            "so_answer": [],
            "question_tags": [],
            "gpt_answer": [],
            "copilot_answer": [],
            "so_answer_adj": [],
            "so_answer_verb": [],
            "gpt_answer_adj": [],
            "gpt_answer_verb": [],
            "copilot_answer_adj": [],
            "copilot_answer_verb": [],
        },
    }

    for index, row in df.iterrows():
        if row.iloc[0] in pre_LLM:
            pre_LLM[row.iloc[0]]["question"].append(row.iloc[2])
            pre_LLM[row.iloc[0]]["answer_score"].append(row.iloc[3])
            pre_LLM[row.iloc[0]]["so_answer"].append(row.iloc[4])
            pre_LLM[row.iloc[0]]["question_tags"].append(row.iloc[5])
            pre_LLM[row.iloc[0]]["gpt_answer"].append(row.iloc[6])
            pre_LLM[row.iloc[0]]["copilot_answer"].append(row.iloc[7])
            # Possibly consider the idea of counting the number of words or verbs used in each response.
    generate_pdf_report(pre_LLM)


def generate_pdf_report(data_dict):
    doc = SimpleDocTemplate("pre_llm_Q&A_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()

    highlighted_code_style = ParagraphStyle(
        "CodeStyle",
        fontName="Courier",
        fontSize=10,
        backColor=colors.yellow,
    )

    body_text_style = ParagraphStyle(
        "BodyText",
        parent=styles["BodyText"],
        allowWidows=1,
        allowOrphans=1,
        fontName="Helvetica",
        fontSize=10,
        leading=12,
        textColor=colors.black,
    )

    story = []

    for month, details in data_dict.items():
        story.append(Paragraph(f"<b>Month: {month}</b>", styles["Heading2"]))

        for i in range(len(details["question"])):
            question = process_text(details["question"][i])
            answer_score = details["answer_score"][i]
            so_answer = process_text(details["so_answer"][i])
            gpt_answer = process_text(details["gpt_answer"][i])
            copilot_answer = process_text(details["copilot_answer"][i])
            question_tags = process_text(details["question_tags"][i])
            so_info = count_adjectives_and_verbs(so_answer)
            so_answer_adj = details["so_answer_adj"] = so_info["adjectives"]
            so_answer_verb = details["so_answer_verb"] = so_info["verbs"]
            gpt_info = count_adjectives_and_verbs(gpt_answer)
            gpt_answer_adj = details["gpt_answer_adj"] = gpt_info["adjectives"]
            gpt_answer_verb = details["gpt_answer_verb"] = gpt_info["verbs"]
            copilot_info = count_adjectives_and_verbs(copilot_answer)
            copilot_answer_adj = details["copilot_answer_adj"] = copilot_info[
                "adjectives"
            ]
            copilot_answer_verb = details["copilot_answer_verb"] = copilot_info["verbs"]

            story.append(Paragraph(f"<b>Question {i + 1}:</b>", styles["BodyText"]))
            story.append(Paragraph(f"<b>Tags:</b> {question_tags}", styles["BodyText"]))
            story.append(Paragraph(f"<b>Question:</b> {question}", body_text_style))
            story.append(
                Paragraph(f"<b>Answer Score:</b> {answer_score}", styles["BodyText"])
            )
            story.append(
                Paragraph(
                    f"<b>Stack Overflow answer, Verb Count:</b> {so_answer_verb} , <b>Adjective Count:</b> {so_answer_adj}",
                    styles["BodyText"],
                )
            )
            story.append(
                Paragraph(f"<b>Stack Overflow Answer:</b> {so_answer}", body_text_style)
            )
            story.append(
                Paragraph(
                    f"<b>GPT answer, Verb Count:</b> {gpt_answer_verb} , <b>Adjective Count:</b> {gpt_answer_adj}",
                    styles["BodyText"],
                )
            )
            story.append(
                Paragraph(f"<b>GPT-4o Answer:</b> {gpt_answer}", body_text_style)
            )
            story.append(
                Paragraph(
                    f"<b>Co-Pilot, Verb Count:</b> {copilot_answer_verb} , <b>Adjective Count:</b> {copilot_answer_adj}",
                    styles["BodyText"],
                )
            )
            story.append(
                Paragraph(f"<b>Co-Pilot Answer:</b> {copilot_answer}", body_text_style)
            )
            story.append(Spacer(1, 12))

    doc.build(story)
    print("PDF report generated successfully!")


def count_verbs(text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    verbs = [token for token in doc if token.pos_ == "VERB"]
    return len(verbs)


def count_adjectives(text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    adjectives = [token for token in doc if token.pos_ == "ADJ"]
    return len(adjectives)


def count_adjectives_and_verbs(text: str):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    counts = {"adjectives": 0, "verbs": 0}

    for token in doc:
        if token.pos_ == "ADJ":
            counts["adjectives"] += 1
        elif token.pos_ == "VERB":
            counts["verbs"] += 1

    return counts


def process_text(text):
    """
    Processes the input HTML text to:
    - Replace <code> tags with <font> tags to change the font.
    - Remove all other HTML tags.
    """
    soup = BeautifulSoup(text, "html.parser")

    for code in soup.find_all("code"):
        code_text = code.string if code.string is not None else code.get_text()
        new_tag = soup.new_tag("font", face="Courier", color="blue")
        new_tag.string = code_text
        code.replace_with(new_tag)

    for tag in soup.find_all():
        if tag.name != "font":
            tag.unwrap()

    clean_text = str(soup)

    return clean_text


if __name__ == "__main__":
    parse_code()
