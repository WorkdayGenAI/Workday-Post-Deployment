import json
from .clients import Claude
from .common import get_json,put_json,safe
def run(process,persona,country,conversation_id,**kwargs):
 sid=safe(conversation_id); seg=get_json(f'{process}_{country}_{persona}_{sid}_segregation_sub_bp.json'); val=get_json(f'{process}_{country}_{persona}_{sid}_validation_sub_bp.json'); out={}
 for key,steps in seg.items():
  if not steps and not val.get(key): out[key]=''; continue
  prompt=f'Write only Initiation and Process Steps for Workday sub-process {key}, in British English, for {persona}, {country}. Use only supplied evidence. Return Markdown wrapped in #--- markers. Include owner, conditions, actionable steps and supported cross-role notes. Steps={json.dumps(steps)} Validations={val.get(key,"")}'; out[key]=Claude().complete(prompt,12000)
 name=f'{process}_{persona}_{country}_{sid}_sub_bp_tasks.json'; put_json(name,out); return {'sub_bp':name}
