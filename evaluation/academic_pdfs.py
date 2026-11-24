"""Compile the editable notes, exercises and defense questions to PDF."""
from html import escape
import json
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, KeepTogether


NAVY = colors.HexColor("#112841")
TEAL = colors.HexColor("#006D73")
STYLE = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26, leading=30,
                            textColor=NAVY, spaceAfter=16),
    "head": ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=13, leading=17,
                           textColor=TEAL, spaceAfter=7, spaceBefore=9, keepWithNext=True),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14,
                           textColor=NAVY, spaceAfter=6),
}


def paragraph(text, kind="body"):
    text = escape(text.replace("–","-").replace("—","-"))
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return Paragraph(text, STYLE[kind])


def save(path, title, body):
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(TEAL)
        canvas.drawString(48, 27, "ISTIC  /  MASTER D3S  /  PROJET 4")
        canvas.drawRightString(A4[0]-48, 27, str(doc.page))
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=48, rightMargin=48, topMargin=47,
                      bottomMargin=48, title=title).build(
        [paragraph(title,"title"), *body], onFirstPage=footer, onLaterPages=footer)


def markdown_pdf(source, target, title):
    lines = []
    for line in Path(source).read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("# ") or line.startswith("|---"):
            continue
        if line.startswith("## "):
            lines.append(paragraph(line[3:],"head"))
        elif line.startswith("|"):
            lines.append(paragraph("   /   ".join(cell.strip() for cell in line.strip("|").split("|"))))
        else:
            lines.append(paragraph(line.replace("`","")))
    save(target,title,lines)


def script_pdf(rows, target, title):
    duration = sum(row["duration"] for row in rows)
    lines = [
        paragraph("Version courte", "head"),
        paragraph("Dans chaque série à étapes, montrer le dernier état et expliquer le passage. "
                  "Lire un seul exemple par famille d’articles et garder la démonstration d’incident."),
        paragraph("Version standard", "head"),
        paragraph(f"Durée indicative {duration//60} min {duration%60:02d} s, hors questions et démonstration libre. "
                  "Pour une animation, commenter les premiers états, puis laisser apparaître l’état final."),
    ]
    for row in rows:
        body = [paragraph(f"{row['number']:02d} · {row['title']} · {row['duration']} s","head"),
                paragraph(f"{row['owner']} · {row['oral']}"),
                paragraph(f"À montrer : {row['focus']}   {row['cue']}"),
                paragraph(f"Transition : {row['transition']}")]
        if row.get("source"):
            body.append(paragraph(f"Source : {row['source']}"))
        if row.get("oralGroup"):
            body.append(paragraph(f"Idée à retenir : {row['oralGroup']}"))
        if row.get("frameNotes"):
            states = row["frameNotes"].split("\n")
            body.append(paragraph(f"Repères de lecture. Début : {states[0]} Fin : {states[-1]}"))
        lines.append(KeepTogether(body))
    save(target,title,lines)


def main():
    root = Path("presentation")
    rows = json.loads((root/"slides.json").read_text(encoding="utf-8"))
    script_pdf(rows,root/"Script_Oral_Complet_FR.pdf","Script oral complet")
    for name in ("Nasr","Wajdi","Youssif"):
        script_pdf([row for row in rows if row["owner"].startswith(name)],
                   root/f"Script_{name}_FR.pdf",f"Script oral · {name}")
    markdown_pdf(root/"QUESTIONS.md",root/"Questions_Reponses_Soutenance.pdf","57 questions de soutenance")
    markdown_pdf("docs/MANUAL_EXERCISES.md","docs/EXERCICES_CORRIGES_FINAL.pdf","Exercices corrigés")


if __name__ == "__main__":
    main()
