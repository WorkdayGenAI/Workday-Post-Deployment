import re,pandas as pd
from .clients import Claude
from .common import get,put,path,safe
def run(process,persona,country,conversation_id,**kwargs):
 sid=safe(conversation_id); xml=get(f'{process}_{persona}_{country}_{sid}_workday_bp_xml.txt'); prompt='Generate Workday test cases from this XML only. Country='+country+'; Initiating Security Group='+persona+'. First line: INFERRED_BP: <name>. Then output only an 8-column Markdown table: Test Case ID | Test Scenario | Security Role | Test Data / Inputs | Test Case Description | Step Number | Test Steps | Expected Result. Use British English and one row per process step.\nXML:\n'+xml; md=Claude().complete(prompt); mdname=f'{process}_{persona}_{country}_markdown_gts_{sid}.txt'; put(mdname,md); lines=[x.strip() for x in md.splitlines() if x.strip().startswith('|') and x.strip().endswith('|') and not re.fullmatch(r'\|[\s:|-]+\|',x.strip())]; rows=[[c.strip() for c in x.strip('|').split('|')] for x in lines]
 if len(rows)<2: raise RuntimeError('Invalid GTS Markdown table')
 df=pd.DataFrame(rows[1:],columns=rows[0]); bp=next((x.split(':',1)[1].strip() for x in md.splitlines() if x.upper().startswith('INFERRED_BP:')),'Unknown BP'); df.insert(0,'Inferred_BP',bp); csv=f'{process}_{country}_{persona}TestCaseGenerated_{sid}.csv'; df.to_csv(path(csv),index=False,encoding='utf-8-sig'); return {'markdown':mdname,'csv':csv,'rows':len(df)}
