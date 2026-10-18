import hashlib
from datetime import date
from pathlib import Path
import pandas as pd
import streamlit as st
from database import CybercrimeDatabase
from categories import CYBERCRIME_CATEGORIES, CASE_STATUS
from ai_classifier import classify_incident
from report_generator import generate_pdf

st.set_page_config(page_title='Cybercrime Incident Portal', page_icon='🛡️', layout='wide')
DB=CybercrimeDatabase(); UPLOAD_DIR=Path('evidence_store'); UPLOAD_DIR.mkdir(exist_ok=True)

def login():
 st.title('🛡️ Cybercrime Incident Portal'); st.caption('Incident reporting • AI triage • evidence • investigation')
 with st.form('login'):
  u=st.text_input('Username',value='admin'); p=st.text_input('Password',type='password',value='admin123')
  if st.form_submit_button('Sign in',use_container_width=True):
   user=DB.authenticate(u,p)
   if user: st.session_state.user=user; st.rerun()
   else: st.error('Invalid credentials')
 st.info('Demo login: admin / admin123. Change it before deployment.')

def dashboard():
 st.header('📊 Officer Dashboard'); s=DB.get_statistics()
 cols=st.columns(5)
 for c,(a,b) in zip(cols,[('Total',s['total']),('New',s['status'].get('New',0)),('Investigating',s['status'].get('Investigating',0)),('Critical',s['priority'].get('Critical',0)),('Resolved',s['status'].get('Resolved',0))]): c.metric(a,b)
 c1,c2=st.columns(2)
 with c1: st.subheader('Cases by category'); st.bar_chart(pd.Series(s['category'],name='Cases'))
 with c2: st.subheader('Cases by status'); st.bar_chart(pd.Series(s['status'],name='Cases'))
 rows=DB.get_all_cases(); st.subheader('Recent cases')
 st.dataframe(pd.DataFrame(rows)[['case_id','complainant_name','category','priority','status','created_at']] if rows else pd.DataFrame(),use_container_width=True,hide_index=True)

def report_case():
 st.header('📝 Report Cybercrime')
 with st.form('complaint',clear_on_submit=True):
  a,b=st.columns(2); name=a.text_input('Complainant name *'); phone=b.text_input('Contact number *'); email=a.text_input('Email'); loc=b.text_input('Incident location *')
  d=a.date_input('Incident date',date.today()); known=b.selectbox('Known category',['Auto-detect']+list(CYBERCRIME_CATEGORIES)); desc=st.text_area('Describe the incident *',height=180); einfo=st.text_area('Evidence description')
  submit=st.form_submit_button('🔎 Analyze & Submit',use_container_width=True)
 if submit:
  if not all([name,phone,loc,desc]): st.error('Fill all required fields.'); return
  ai=classify_incident(desc)
  if known!='Auto-detect': ai['category']=known; ai['subcategory']=CYBERCRIME_CATEGORIES[known]['subcategories'][0]
  ok,res=DB.insert_case({'complainant_name':name,'contact_number':phone,'email':email,'incident_location':loc,'incident_date':str(d),'complaint_description':desc,'evidence_info':einfo,'category':ai['category'],'subcategory':ai['subcategory'],'priority':ai['priority'],'confidence':ai['confidence'],'ai_summary':ai['summary']})
  if ok: st.success(f'Complaint submitted. Case ID: {res}'); st.info(f"{ai['category']} → {ai['subcategory']} | {ai['priority']} | {ai['confidence']*100:.0f}%")
  else: st.error(res)

def case_management():
 st.header('🔍 Case Management'); search=st.text_input('Search case ID, complainant, category or status'); rows=DB.get_all_cases(search)
 if not rows: st.info('No cases found.'); return
 selected=st.selectbox('Select case',[r['case_id'] for r in rows]); case=DB.get_case(selected); ev=DB.get_evidence(selected); hist=DB.get_history(selected)
 l,r=st.columns([1.5,1])
 with l:
  st.subheader(f"{case['case_id']} — {case['category']}"); st.write(case['complaint_description']); st.write(f"Priority: **{case['priority']}** | AI confidence: **{case['confidence']*100:.0f}%**"); st.info(case['ai_summary'])
  st.subheader('Evidence')
  for e in ev: st.code(f"{e['file_name']}\nSHA-256: {e['sha256']}")
  with st.form('evidence'):
   up=st.file_uploader('Upload evidence',type=['png','jpg','jpeg','pdf','txt','csv','zip','docx'],key=selected); ed=st.text_input('Evidence description')
   if st.form_submit_button('Add evidence') and up:
    raw=up.getvalue(); digest=hashlib.sha256(raw).hexdigest(); path=UPLOAD_DIR/f'{selected}_{digest[:12]}_{Path(up.name).name}'; path.write_bytes(raw); DB.add_evidence(selected,up.name,up.type,len(raw),digest,ed,st.session_state.user['username']); st.success('Evidence stored and SHA-256 recorded.'); st.rerun()
 with r:
  st.subheader('Investigation'); status=st.selectbox('Status',CASE_STATUS,index=CASE_STATUS.index(case['status'])); officer=st.text_input('Assigned officer',case.get('assigned_officer') or ''); notes=st.text_area('Officer notes',case.get('officer_notes') or '',height=160)
  if st.button('Save updates',use_container_width=True):
   if status!=case['status']: DB.update_case_status(selected,status,st.session_state.user['username'])
   DB.update_case(selected,officer,notes,st.session_state.user['username']); st.success('Updated'); st.rerun()
  st.download_button('📄 Download PDF report',generate_pdf(case,ev,hist),file_name=f'{selected}_report.pdf',mime='application/pdf',use_container_width=True)
  st.subheader('Timeline')
  for h in hist: st.write(f"{h['changed_at']} — {h['old_status'] or 'Created'} → {h['new_status']} ({h['changed_by']})")

def main():
 if 'user' not in st.session_state: login(); return
 with st.sidebar:
  st.success(st.session_state.user['full_name']); page=st.radio('Navigation',['Dashboard','Report Cybercrime','Case Management','Audit Logs'])
  if st.button('Logout'): st.session_state.pop('user'); st.rerun()
 if page=='Dashboard': dashboard()
 elif page=='Report Cybercrime': report_case()
 elif page=='Case Management': case_management()
 else: st.header('🧾 Audit Logs'); st.dataframe(pd.DataFrame(DB.get_audit_logs()),use_container_width=True,hide_index=True)
main()
