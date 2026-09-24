import requests
from .common import env
def run(conversation_id,message,recipient_id='',**kwargs):
 base=env('CANVAS_BASE_URL',True)
 if not base:return {'status':'skipped'}
 r=requests.post(base.rstrip('/')+'/atr-gateway/identity-management/api/v1/auth/short-token',json={'username':env('CANVAS_USERNAME'),'password':env('CANVAS_PASSWORD')},timeout=60); r.raise_for_status(); body={'conversation_id':conversation_id,'content':message,'type':'assistant','metadata':{'external_system_name':'agent_manager','external_system_be_replied':False,'external_system_message_type':'text','external_system_response_id':'','external_configs':{}}};
 if recipient_id: body['recipient_id']=recipient_id
 r=requests.post(base.rstrip('/')+'/atr-gateway/genai/messages',json=body,headers={'apiToken':r.json()['token']},timeout=60); r.raise_for_status(); return {'status':'sent'}
