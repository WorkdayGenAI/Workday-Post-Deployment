import requests
from .common import env
class Quasar:
 def __init__(self): self.base=env('QUASAR_BASE_URL').rstrip('/'); self.auth=(env('QUASAR_USERNAME'),env('QUASAR_PASSWORD')); self.token=''
 def post(self,path,payload):
  if not self.token:
   r=requests.post(self.base+'/atr-gateway/identity-management/api/v1/auth/short-token?useDeflate=true',json={'username':self.auth[0],'password':self.auth[1]},timeout=60); r.raise_for_status(); self.token=r.json()['token']
  r=requests.post(self.base+path,json=payload,headers={'apiToken':self.token,'content-type':'application/json'},timeout=120); r.raise_for_status(); return r
class Workday:
 def get_xml(self,ref):
  r=requests.get(env('WORKDAY_REPORT_BASE_URL').rstrip('/')+'/ccx/service/customreport2/aldi3/mvangara-impl/Genwiz_Business_Process_Definition_Details',params={'Business_Process_Definition!Business_Process_Definition_ID':ref},auth=(env('WORKDAY_REPORT_USERNAME'),env('WORKDAY_REPORT_PASSWORD')),timeout=120); r.raise_for_status(); return r.text
class Claude:
 def complete(self,prompt,max_tokens=30000):
  endpoint=env('CLAUDE_ENDPOINT').rstrip('/'); url=endpoint if endpoint.endswith('/anthropic/v1/messages') else endpoint+'/anthropic/v1/messages'; messages=[{'role':'user','content':prompt}]; out=[]
  while True:
   r=requests.post(url,headers={'x-api-key':env('CLAUDE_API_KEY'),'anthropic-version':'2023-06-01','content-type':'application/json'},json={'model':env('CLAUDE_MODEL'),'max_tokens':max_tokens,'temperature':0.2,'messages':messages},timeout=(10,300)); r.raise_for_status(); d=r.json(); chunk=''.join(x.get('text','') for x in d.get('content',[])); out.append(chunk)
   if d.get('stop_reason')!='max_tokens': return ''.join(out)
   messages += [{'role':'assistant','content':chunk},{'role':'user','content':'Continue exactly where you stopped. Do not repeat.'}]
