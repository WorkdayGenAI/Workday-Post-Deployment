from .clients import Quasar,Workday
from .common import put,safe
OVERRIDES={}
def run(process,persona,country,conversation_id,**kwargs):
 q=Quasar(); payload={'output':'<Reference ID>','query':f'@content: <Business Process>=={process} @metadata:BusinessProcessMapping.xlsx','index':'wd_TSEndUserTrainingMaterials_idx','search_limit':'200'}; refs=q.post('/api/v2/acnopenai/searchvectors',payload).json(); expected=process.upper().replace(' ','_')+'_DEFAULT_DEFINITION'; ref=refs[0] if len(refs)==1 else expected if expected in refs else OVERRIDES.get(process,expected); xml=Workday().get_xml(ref); name=f'{process}_{persona}_{country}_{safe(conversation_id)}_workday_bp_xml.txt'; put(name,xml); return {'reference_id':ref,'xml':name}
