from .common import get_json,put_json,safe
def run(process,persona,country,conversation_id,**kwargs):
 sid=safe(conversation_id); data=get_json(f'{country}_{persona}_{process}_{sid}_country_segregation.json'); records=data.get(country,data.get(country.upper(),data.get('Global',[]))); tasks=[]
 for item in records:
  t=item.get('Record',{}).get('Task')
  if t and t.lower()!='initiation' and t not in tasks: tasks.append(t)
 seg={t:[{'Record':{'Task':t,'If':'[no condition applied]','Groups':'-'}}] for t in tasks}; val={t:'' for t in tasks}; s=f'{process}_{country}_{persona}_{sid}_segregation_sub_bp.json'; v=f'{process}_{country}_{persona}_{sid}_validation_sub_bp.json'; put_json(s,seg); put_json(v,val); return {'segregation':s,'validations':v,'tasks':tasks}
