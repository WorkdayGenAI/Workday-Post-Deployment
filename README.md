# EUTM VS Code pipeline

The scripts follow the workflow order in the supplied Agent Manager JSON. Agent Manager `core` artefacts are replaced with local `artifacts` and `output` folders. Secrets are not embedded.

## Run
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run_pipeline.py --process "Create Position" --persona "Personnel Leader" --country "AU"
```

Fill `.env` with approved development endpoints and credentials and never commit it.

## Order
1. Trigger and Workday XML retrieval
2. GTS creation
3. Job-aid/index retrieval
4. Country segregation
5. Main BP EUTM generation
6. Sub-BP preparation
7. Sub-BP EUTM generation
8. DOCX generation
9. Optional Canvas delivery

## Parity limitation
The original flow depends on internal Quasar, Workday, Claude and Canvas services. Your VS Code machine must have network/VPN access and authorised credentials. Script 06 keeps the same hand-off contract but uses local sub-BP placeholders; add the approved per-sub-BP Quasar and Workday retrieval contract there for production parity.
