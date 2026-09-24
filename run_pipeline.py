import argparse,importlib,json,uuid
ORDER=['01_trigger_for_aldi','02_gts_for_eutm','03_combined_code','04_segregate_by_country','05_generate_main_bp','06_combined_code_for_sub_bp','07_generate_sub_bp','08_document_generation_final']
def main():
 p=argparse.ArgumentParser(); p.add_argument('--process',required=True); p.add_argument('--persona',required=True); p.add_argument('--country',required=True); p.add_argument('--conversation-id',default=str(uuid.uuid4())); p.add_argument('--recipient-id',default=''); a=p.parse_args(); ctx=vars(a); ctx['conversation_id']=ctx.pop('conversation_id'); results={}
 for name in ORDER:
  print('\n=== '+name+' ==='); results[name]=importlib.import_module('src.'+name).run(**ctx); print(json.dumps(results[name],indent=2))
 print('\nCompleted:',results['08_document_generation_final']['document'])
if __name__=='__main__': main()
