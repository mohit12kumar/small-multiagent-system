import os
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.config import settings

def generate_pdf_report(candidate_name: str, session_id: int, overall_score: float, feedbacks: list, missing_skills: list, pdf_filename: str = None) -> str:
    """
    Generates a styled ReportLab PDF report and saves to backend/uploads/reports/
    """
    import datetime
    
    try:
        if not pdf_filename:
            pdf_filename = f"report_session_{session_id}_{uuid.uuid4().hex[:8]}.pdf"
            
        target_dir = getattr(settings, 'REPORT_DIR', os.path.join("uploads", "reports"))
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, pdf_filename)
        
        doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=12
        )
        story.append(Paragraph("Interview Preparation Performance Report", title_style))
        story.append(Spacer(1, 10))
        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Metadata Table
        data_meta = [
            ["Candidate Name:", candidate_name or "Candidate", "Session ID:", str(session_id)],
            ["Overall Score:", f"{float(overall_score):.1f} / 100", "Generated Date:", current_date]
        ]
        t_meta = Table(data_meta, colWidths=[110, 160, 100, 160])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#0f172a")),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1"))
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 15))
        
        # Skill Gap & Recommendations
        story.append(Paragraph("Identified Skill Gaps & Recommended Topics", styles['Heading2']))
        skills_text = ", ".join(missing_skills) if missing_skills else "No major skill gaps identified!"
        story.append(Paragraph(f"<b>Missing Target Skills:</b> {skills_text}", styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Evaluation Scores Table
        story.append(Paragraph("Question Performance & Score Breakdown", styles['Heading2']))
        table_data = [["#", "Grammar", "Technical", "Comm", "Confidence", "Completeness", "Score"]]
        
        for idx, f in enumerate(feedbacks or [], 1):
            if isinstance(f, dict):
                table_data.append([
                    str(idx),
                    f"{float(f.get('grammar_score', 0)):.0f}%",
                    f"{float(f.get('technical_score', 0)):.0f}%",
                    f"{float(f.get('communication_score', 0)):.0f}%",
                    f"{float(f.get('confidence_score', 0)):.0f}%",
                    f"{float(f.get('completeness_score', 0)):.0f}%",
                    f"{float(f.get('overall_score', 0)):.1f}%"
                ])
            
        t_scores = Table(table_data, colWidths=[30, 80, 80, 80, 80, 90, 80])
        t_scores.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563eb")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))
        ]))
        story.append(t_scores)
        
        doc.build(story)
        return file_path
    except Exception as e:
        print(f"[PDF Service Error]: Failed to generate PDF report: {e}")
        fallback_path = os.path.join("uploads", "reports", f"fallback_report_{session_id}.txt")
        os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
        with open(fallback_path, "w", encoding="utf-8") as f:
            f.write(f"Interview Report for Candidate: {candidate_name}\nSession ID: {session_id}\nOverall Score: {overall_score}\nSkills: {missing_skills}\n")
        return fallback_path
