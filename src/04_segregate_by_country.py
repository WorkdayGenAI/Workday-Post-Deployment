import html
from lxml import etree
from .common import get,put_json,safe
TOKENS={'USA':['USA','US','United States'],'AU':['AU','Australia'],'GB':['GB','Great Britain','GBIE'],'IE':['IE','Ireland','GBIE'],'GBIE':['GB','IE','GBIE','Great Britain','Ireland']}
def run(process,persona,country,conversation_id,**kwargs):
 sid=safe(conversation_id); root=etree.fromstring(html.unescape(get(f'{process}_{persona}_{country}_{sid}_workday_bp_xml.txt')).encode(),etree.XMLParser(recover=True)); ns={'wd':'urn:com.workday.report/Genwiz_Business_Process_Definition_Details'}; cc='USA' if country.upper()=='US' else country.upper(); selected=[]
 for g in root.xpath('.//wd:Business_Process_Steps_group',namespaces=ns):
  d=lambda t:g.xpath(f'./wd:{t}/@wd:Descriptor',namespaces=ns); st=(d('Step_Type') or [''])[0]; task=(d('Task') or [st or '-'])[0]; cond='; '.join(d('Entry_Conditions_from_Workflow_Step_and_Allowed_Action')) or '[no condition applied]'; groups='; '.join(d('Security_Groups')) or '-'; country_specific=any(t.lower() in cond.lower() for values in TOKENS.values() for t in values); applies=cc=='GLOBAL' or not country_specific or any(t.lower() in cond.lower() for t in TOKENS.get(cc,[]));
  if applies: selected.append({'Record':{'Task':task,'If':cond,'Groups':groups}})
 label='Global' if cc=='GLOBAL' else cc; name=f'{country}_{persona}_{process}_{sid}_country_segregation.json'; put_json(name,{label:selected}); return {'country_steps':name,'count':len(selected)}
