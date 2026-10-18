from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def generate_report(case):
 return '\n'.join([f"CYBERCRIME INCIDENT REPORT",f"Case ID: {case.get('case_id','')}",f"Status: {case.get('status','')}",f"Complainant: {case.get('complainant_name','')}",f"Category: {case.get('category','')}",f"Priority: {case.get('priority','')}",f"\nDescription:\n{case.get('complaint_description','')}",f"\nAI Summary:\n{case.get('ai_summary','')}",f"\nOfficer Notes:\n{case.get('officer_notes','')}"])

def generate_pdf(case,evidence=None,history=None):
 b=BytesIO(); doc=SimpleDocTemplate(b,pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36); s=getSampleStyleSheet(); title=ParagraphStyle('T',parent=s['Title'],alignment=TA_CENTER); story=[Paragraph('CYBERCRIME INCIDENT REPORT',title),Spacer(1,12)]
 data=[[k,str(case.get(v,''))] for k,v in [('Case ID','case_id'),('Status','status'),('Complainant','complainant_name'),('Contact','contact_number'),('Email','email'),('Location','incident_location'),('Incident Date','incident_date'),('Category','category'),('Subcategory','subcategory'),('Priority','priority'),('AI Confidence','confidence')]]
 t=Table(data,colWidths=[120,390]); t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.grey),('BACKGROUND',(0,0),(0,-1),colors.lightgrey)])); story += [t,Spacer(1,12)]
 for h,k in [('Complaint Description','complaint_description'),('AI Summary','ai_summary'),('Officer Notes','officer_notes')]: story += [Paragraph(h,s['Heading2']),Paragraph(str(case.get(k,'') or 'None'),s['BodyText']),Spacer(1,8)]
 if evidence:
  story += [Paragraph('Evidence',s['Heading2']),Table([['File','SHA-256','Uploaded By']]+[[e['file_name'],e['sha256'],e.get('uploaded_by','')] for e in evidence],colWidths=[160,270,80])]
 if history:
  story += [Spacer(1,10),Paragraph('Status History',s['Heading2'])]+[Paragraph(f"{h['changed_at']} — {h['old_status'] or 'Created'} → {h['new_status']} by {h['changed_by']}",s['BodyText']) for h in history]
 doc.build(story); return b.getvalue()
