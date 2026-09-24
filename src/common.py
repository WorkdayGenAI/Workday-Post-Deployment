import json,os,re,uuid
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(); ROOT=Path(__file__).resolve().parents[1]; ARTIFACTS=ROOT/'artifacts'; OUTPUT=ROOT/'output'
def safe(v): return re.sub(r'[^A-Za-z0-9_-]','_',str(v or '').strip()) or uuid.uuid4().hex
def path(name): return ARTIFACTS/re.sub(r'[\[\](){}]','',name)
def put(name,data):
 p=path(name); p.write_bytes(data if isinstance(data,bytes) else str(data).encode()); return p
def get(name): return path(name).read_text(encoding='utf-8')
def put_json(name,data): return put(name,json.dumps(data,indent=2,ensure_ascii=False))
def get_json(name): return json.loads(get(name))
def env(key,optional=False):
 v=os.getenv(key,'').strip()
 if not v and not optional: raise RuntimeError(f'Missing environment variable: {key}')
 return v
