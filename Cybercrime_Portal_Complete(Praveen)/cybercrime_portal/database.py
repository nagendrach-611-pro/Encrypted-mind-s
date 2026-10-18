import sqlite3, hashlib
from typing import Dict, List, Optional
class CybercrimeDatabase:
 def __init__(self,db_path='cybercrime_cases.db'):
  self.db_path=db_path; self.create_tables(); self.seed_admin()
 def get_connection(self):
  c=sqlite3.connect(self.db_path); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
 def create_tables(self):
  c=self.get_connection(); c.executescript('''CREATE TABLE IF NOT EXISTS cases(id INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT UNIQUE NOT NULL,complainant_name TEXT NOT NULL,contact_number TEXT NOT NULL,email TEXT,incident_location TEXT NOT NULL,incident_date TEXT NOT NULL,complaint_description TEXT NOT NULL,evidence_info TEXT,category TEXT NOT NULL,subcategory TEXT,priority TEXT NOT NULL,confidence REAL NOT NULL,ai_summary TEXT,status TEXT NOT NULL DEFAULT 'New',assigned_officer TEXT,officer_notes TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
  CREATE TABLE IF NOT EXISTS evidence(id INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT NOT NULL,file_name TEXT NOT NULL,file_type TEXT,file_size INTEGER,sha256 TEXT NOT NULL,description TEXT,uploaded_by TEXT,uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE);
  CREATE TABLE IF NOT EXISTS audit_logs(id INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT,username TEXT NOT NULL,action TEXT NOT NULL,details TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
  CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password_hash TEXT NOT NULL,role TEXT NOT NULL,full_name TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS status_history(id INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT NOT NULL,old_status TEXT,new_status TEXT NOT NULL,changed_by TEXT NOT NULL,changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(case_id) REFERENCES cases(case_id) ON DELETE CASCADE);'''); c.commit(); c.close()
 def seed_admin(self):
  c=self.get_connection(); cur=c.cursor(); cur.execute("SELECT 1 FROM users WHERE username='admin'")
  if not cur.fetchone(): cur.execute('INSERT INTO users VALUES(?,?,?,?)',('admin',hashlib.sha256(b'admin123').hexdigest(),'Admin','System Administrator'))
  c.commit(); c.close()
 def authenticate(self,u,p)->Optional[Dict]:
  c=self.get_connection(); r=c.execute('SELECT * FROM users WHERE username=? AND password_hash=?',(u,hashlib.sha256(p.encode()).hexdigest())).fetchone(); c.close(); return dict(r) if r else None
 def generate_case_id(self):
  c=self.get_connection(); n=c.execute('SELECT COALESCE(MAX(id),0)+1 n FROM cases').fetchone()['n']; c.close(); return f'CC-{n:06d}'
 def insert_case(self,d):
  c=self.get_connection()
  try:
   cid=self.generate_case_id(); c.execute('''INSERT INTO cases(case_id,complainant_name,contact_number,email,incident_location,incident_date,complaint_description,evidence_info,category,subcategory,priority,confidence,ai_summary) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cid,d['complainant_name'],d['contact_number'],d.get('email',''),d['incident_location'],d['incident_date'],d['complaint_description'],d.get('evidence_info',''),d['category'],d.get('subcategory',''),d['priority'],d['confidence'],d.get('ai_summary',''))); c.commit(); return True,cid
  except Exception as e: c.rollback(); return False,str(e)
  finally: c.close()
 def get_all_cases(self,search=''):
  c=self.get_connection(); q='SELECT * FROM cases'; params=[]
  if search: q+=' WHERE case_id LIKE ? OR complainant_name LIKE ? OR category LIKE ? OR status LIKE ?'; params=[f'%{search}%']*4
  q+=' ORDER BY created_at DESC'; rows=c.execute(q,params).fetchall(); c.close(); return [dict(x) for x in rows]
 def get_case(self,cid):
  c=self.get_connection(); r=c.execute('SELECT * FROM cases WHERE case_id=?',(cid,)).fetchone(); c.close(); return dict(r) if r else None
 def _audit(self,cur,cid,user,action,details=''): cur.execute('INSERT INTO audit_logs(case_id,username,action,details) VALUES(?,?,?,?)',(cid,user,action,details))
 def update_case_status(self,cid,status,user='system'):
  c=self.get_connection(); cur=c.cursor(); r=cur.execute('SELECT status FROM cases WHERE case_id=?',(cid,)).fetchone()
  if not r: c.close(); return False
  old=r['status']; cur.execute('UPDATE cases SET status=?,updated_at=CURRENT_TIMESTAMP WHERE case_id=?',(status,cid)); cur.execute('INSERT INTO status_history(case_id,old_status,new_status,changed_by) VALUES(?,?,?,?)',(cid,old,status,user)); self._audit(cur,cid,user,'Status updated',f'{old} -> {status}'); c.commit(); c.close(); return True
 def update_case(self,cid,officer,notes,user):
  c=self.get_connection(); cur=c.cursor(); cur.execute('UPDATE cases SET assigned_officer=?,officer_notes=?,updated_at=CURRENT_TIMESTAMP WHERE case_id=?',(officer,notes,cid)); self._audit(cur,cid,user,'Case updated',f'Officer: {officer}'); c.commit(); c.close()
 def add_evidence(self,*args):
  c=self.get_connection(); cur=c.cursor(); cur.execute('INSERT INTO evidence(case_id,file_name,file_type,file_size,sha256,description,uploaded_by) VALUES(?,?,?,?,?,?,?)',args); self._audit(cur,args[0],args[-1],'Evidence added',args[1]); c.commit(); c.close()
 def get_evidence(self,cid):
  c=self.get_connection(); rows=c.execute('SELECT * FROM evidence WHERE case_id=? ORDER BY uploaded_at DESC',(cid,)).fetchall(); c.close(); return [dict(x) for x in rows]
 def get_history(self,cid):
  c=self.get_connection(); rows=c.execute('SELECT * FROM status_history WHERE case_id=? ORDER BY changed_at DESC',(cid,)).fetchall(); c.close(); return [dict(x) for x in rows]
 def get_audit_logs(self,cid=None):
  c=self.get_connection(); rows=c.execute('SELECT * FROM audit_logs WHERE case_id=? ORDER BY created_at DESC',(cid,)).fetchall() if cid else c.execute('SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 200').fetchall(); c.close(); return [dict(x) for x in rows]
 def get_statistics(self):
  c=self.get_connection(); total=c.execute('SELECT COUNT(*) n FROM cases').fetchone()['n']; status={r['status']:r['n'] for r in c.execute('SELECT status,COUNT(*) n FROM cases GROUP BY status')}; category={r['category']:r['n'] for r in c.execute('SELECT category,COUNT(*) n FROM cases GROUP BY category')}; priority={r['priority']:r['n'] for r in c.execute('SELECT priority,COUNT(*) n FROM cases GROUP BY priority')}; c.close(); return {'total':total,'status':status,'category':category,'priority':priority}
