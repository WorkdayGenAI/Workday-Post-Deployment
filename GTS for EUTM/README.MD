## EUTM Agent (End-User Training Material Generator)

### Appendix (Quick Reference)

This appendix sits at the top on purpose so technical and non-technical readers can understand the agent before reviewing the detailed documentation.

#### A. Table of Contents
- [What Is This Agent?](#what-is-this-agent)
- [Quick Summary](#quick-summary)
- [Business Value — Time Savings](#business-value--time-savings)
- [Key Features](#key-features)
- [How the Agent Works](#how-the-agent-works)
- [Architecture Diagram](#architecture-diagram)
- [Architecture Explanation](#architecture-explanation)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Environment Variables](#environment-variables)
- [Running the Agent](#running-the-agent)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)
- [APIs and Integrations](#apis-and-integrations)
- [Security and Authentication](#security-and-authentication)
- [Monitoring and Logging](#monitoring-and-logging)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Assumptions, Risks and Gaps](#assumptions-risks-and-gaps)
- [Business Value](#business-value)
- [Executive Summary](#executive-summary)

#### B. Glossary (plain English)

| Term | What it means |
|---|---|
| **Agent** | A connected set of Agent Manager tools that automates the EUTM workflow |
| **BP (Business Process)** | A Workday workflow such as Hire, Change Job or Create Position |
| **EUTM** | End-User Training Material written for Workday business users |
| **GTS** | Scenario and process-step content used as the primary procedural source |
| **Initiating Security Group** | The role or persona that starts the Workday process |
| **Quasar** | The search service used to retrieve mappings and training content |
| **Workday** | The source system that provides the Business Process definition XML |
| **Claude** | The AI model used to generate GTS and training content |
| **Canvas** | The chat interface where the user requests and receives the result |
| **Artefact** | An intermediate or final file stored by the Agent Manager platform |
| **Presigned URL** | A temporary private link for downloading a generated artefact |
| **Sub-process** | A downstream Business Process referenced by the main process |

#### C. Tools at a glance

| Tool file | Path | Role | Key inputs | Output |
|---|---|---|---|---|
| `trigger_for_aldi` | Main BP retrieval | Resolve the BP reference and retrieve Workday XML and validations | process, conversation_id, country, persona | XML and validation artefacts |
| `GTS_for_EUTM` | GTS generation | Generate scenario and process-step content | conversationid, process, persona, country | Markdown and CSV artefacts |
| `combined_code` | Supporting content | Retrieve matching user-training or job-aid content | process, persona, conversation_id, country | Text artefact |
| `segregate_by_country` | Country processing | Retain process steps applicable to the selected country | conversation_id, persona, country, process | Country JSON |
| `claude_call_for_main_bp` | Main EUTM generation | Generate the main BP training content | conversation_id, process_steps, Process, Persona, country | EUTM Markdown |
| `combined_code_for_sub_bp` | Sub-BP extraction | Retrieve sub-process definitions and validations | conversation_id, persona, country, process | Sub-process JSON files |
| `claude_call_for_subbp_three` | Sub-BP generation | Generate sub-process training sections | conversation_id, persona, country, process | Sub-process task JSON |
| `document_generation_final` | Document generation | Merge all content into Word | usecase, conversation_id, Persona, country, process | DOCX and URL |
| `workday_send_msg_to_canvas` | Delivery | Send the final result to Canvas | conversation_id, message, environment, recipient_id | Delivery confirmation |

#### D. Key facts and constants

| Item | Value |
|---|---|
| Language | Python 3 |
| Runtime | Agent Manager platform tools |
| Platform SDK | `core` |
| Core libraries | requests, pandas, lxml, python-docx |
| Quasar secret | `wd-tool-secrets` |
| Workday secret | `wd-tool-eutm-secret-2` |
| Claude secret | `SCA_WA_Claude_Opus_4_6` |
| Quasar index | `wd_TSEndUserTrainingMaterials_idx` |
| Main output | EUTM Word document |
| Storage | `artifacts/` and `uploaded_artifacts/` |
| Tool format | Extensionless Python modules |

#### E. Reference Key
- ✅ **Fact** — taken from the supplied EUTM tool code and workflow.
- ⚠️ **Assumption** — inferred and clearly labelled.
- ❓ **Unable to determine** — not present in the supplied files and not guessed.

### What Is This Agent?

The **EUTM agent** generates Workday End-User Training Material for a selected Business Process, country and initiating security group. It runs as a connected set of tools inside Agent Manager.

The agent retrieves the Workday process definition, generates scenario-based source content, filters the process for the selected country, creates the main training content, adds supported sub-process instructions, builds a Word document and returns the download link through Canvas.

**Why it exists:** Creating EUTM manually requires analysts to inspect process definitions, identify role- and country-specific paths, rewrite technical process information into training language and assemble a consistently formatted document.

**Who should use it:**
- Workday training-content teams
- Workday functional consultants
- Business Process analysts
- Teams preparing country- and persona-specific training material

### Quick Summary

| Item | Details |
|---|---|
| **Purpose** | Generate Workday EUTM documents for a selected process, country and initiating role |
| **Runtime** | Agent Manager platform tools |
| **Inputs** | Process, persona, country, conversation ID and Canvas delivery parameters |
| **Final output** | Downloadable Word document |
| **Intermediate outputs** | XML, validation text, GTS Markdown, GTS CSV, country JSON, main EUTM text and sub-process JSON |
| **External systems** | Quasar, Workday, Claude and Canvas |
| **Storage** | Agent Manager artefacts through the `core` SDK |

### Business Value — Time Savings

The agent automates work that otherwise requires manual retrieval, analysis, writing and document assembly. This includes obtaining process definitions, determining country applicability, producing role-aware instructions, documenting sub-processes and creating the final Word document.

No measured duration or percentage saving appears in the supplied source, so this README does not claim a specific time-saving figure.

### Key Features

#### 1. Retrieve the live Workday process definition
`trigger_for_aldi` resolves the Business Process reference, calls the Workday custom report, stores the XML and extracts initiation validations.

#### 2. Generate GTS content
`GTS_for_EUTM` converts the Workday XML into scenario-driven source content and produces both Markdown and CSV outputs.

#### 3. Apply country-specific processing
`segregate_by_country` supports USA, US, AU, GB, IE, GBIE and Global. Generic steps and applicable regional steps are retained according to the tool logic.

#### 4. Generate the main EUTM content
`claude_call_for_main_bp` uses GTS as the primary procedural source, country steps for metadata, validations for a separate section, initiation data for navigation and job-aid content for introductory context.

#### 5. Generate sub-process training sections
`combined_code_for_sub_bp` retrieves referenced sub-process definitions and validations. `claude_call_for_subbp_three` converts them into business-user content while preserving the input keys.

#### 6. Create the final Word document
`document_generation_final` replaces task markers with generated sub-process content, removes unresolved markers, converts Markdown headings and tables into Word elements and creates the final DOCX artefact.

#### 7. Deliver the result to Canvas
`workday_send_msg_to_canvas` authenticates to the selected Canvas environment and sends the final document link to the original conversation.

#### 8. Handle long model responses
The Claude helpers continue when the response reaches the token limit, preventing a partial response from being treated as complete.

### How the Agent Works

1. The user supplies the process, persona, country and conversation information through Canvas.
2. `trigger_for_aldi` resolves the main process and retrieves Workday XML and validations.
3. `GTS_for_EUTM` reads the XML and creates GTS Markdown and CSV artefacts.
4. `combined_code` retrieves matching supporting content from Quasar.
5. `segregate_by_country` creates the country-scoped process-step JSON.
6. `claude_call_for_main_bp` generates the main EUTM Markdown.
7. `combined_code_for_sub_bp` retrieves and segregates downstream sub-process definitions.
8. `claude_call_for_subbp_three` generates sub-process training sections.
9. `document_generation_final` creates the final Word document.
10. `workday_send_msg_to_canvas` sends the download link to Canvas.

### Architecture Diagram

```text
Canvas request
    |
    v
trigger_for_aldi
    |---- Workday XML
    |---- validations
    v
GTS_for_EUTM
    |---- GTS Markdown / CSV
    v
combined_code ---- Quasar supporting content
    |
    v
segregate_by_country
    |---- country-scoped steps
    v
claude_call_for_main_bp
    |---- main EUTM Markdown
    v
combined_code_for_sub_bp
    |---- sub-process steps and validations
    v
claude_call_for_subbp_three
    |---- sub-process training JSON
    v
document_generation_final
    |---- EUTM DOCX and download URL
    v
workday_send_msg_to_canvas
    |
    v
Canvas response
```

### Architecture Explanation

| Component | Purpose | Inputs | Outputs | Dependencies |
|---|---|---|---|---|
| **Canvas** | User interaction and delivery | User request | Parameters and displayed result | Canvas APIs |
| **Agent Manager** | Runs the connected tools | Tool prompts and attributes | Ordered execution | Host platform |
| **core SDK** | Supplies platform services | Secret and artefact names | Secrets, files and URLs | Host platform |
| **Quasar** | Retrieves mappings and content | Token and query payload | Reference IDs and indexed text | Quasar APIs |
| **Workday** | Supplies process definitions | Reference ID and credentials | Business Process XML | Workday custom report |
| **Claude** | Generates structured content | Supported source content | GTS and EUTM Markdown | Anthropic-compatible API |
| **Word generator** | Builds the final document | Main EUTM and sub-process JSON | DOCX artefact | python-docx |

### Project Structure

```text
EUTM_Agent_Manager_Tools/
├── trigger_for_aldi
├── GTS_for_EUTM
├── combined_code
├── segregate_by_country
├── claude_call_for_main_bp
├── combined_code_for_sub_bp
├── claude_call_for_subbp_three
├── document_generation_final
├── workday_send_msg_to_canvas
├── agent_manager_manifest.json
└── README.md
```

The tool files have no `.py` extension, but contain Python source. Each file exposes a public function whose name matches the tool name.

### Technology Stack

| Technology | Where used | Purpose |
|---|---|---|
| Python | All tools | Implementation language |
| `core` | All tools | Secrets, artefacts and presigned URLs |
| requests | Integration tools | HTTP calls to Quasar, Workday, Claude and Canvas |
| pandas | GTS and initiation processing | CSV and Excel handling |
| lxml | XML tools | Workday XML parsing |
| python-docx | Final generation | Word-document creation |
| JSON | Tool hand-offs | Structured intermediate data |
| Markdown | Generation tools | Main and sub-process content |

### Prerequisites

- Agent Manager environment that provides the `core` SDK.
- Network access to the configured Quasar, Workday, Claude and Canvas endpoints.
- Required secrets registered in Agent Manager.
- Required Python packages enabled for each tool.
- `initiator_file.xlsx` available in artefact storage when initiation mapping is required.
- Tool attributes configured as listed in `agent_manager_manifest.json`.

### Installation Guide

These files are Agent Manager tools, not a standalone application.

1. Create the nine tools in Agent Manager.
2. Copy each extensionless source file into the corresponding tool.
3. Configure each tool's attributes from `agent_manager_manifest.json`.
4. Add the packages required by the imports.
5. Register the named secrets in Agent Manager's secret store.
6. Create the agents that invoke the tools.
7. Connect the workflow in the documented order.
8. Upload `initiator_file.xlsx` when required.
9. Validate each artefact hand-off with the same process, persona, country and conversation ID.
10. Run an end-to-end test from Canvas.

### Environment Variables

The tools do not use a local `.env` file. They use named secrets through `core.get_secret`.

| Secret name | Required fields | Used by |
|---|---|---|
| `wd-tool-secrets` | `quasar_baseurl`, `quasar_username`, `quasar_password` | Quasar tools |
| `wd-tool-eutm-secret-2` | `eutm_report_Url`, `eutm_report_username`, `eutm_report_password` | Workday retrieval tools |
| `SCA_WA_Claude_Opus_4_6` | `Endpoint`, `api_key`, `deployment_name` | Generation tools |
| `workday_prod` | `url`, `username`, `password` | Production Canvas delivery |
| `workday_CUI` | `url`, `username`, `password` | Demo or default Canvas delivery |
| `workday_stgtest` | `url`, `username`, `password` | Stage-test Canvas delivery |
| `workday_dev` | `url`, `username`, `password` | Development Canvas delivery |

Actual secret values are intentionally excluded.

### Running the Agent

These are platform functions invoked by Agent Manager, not command-line programs.

```python
trigger_for_aldi(
    process="Create Position",
    conversation_id="<conversation-id>",
    requester_user_email_id="<requester-email>",
    environment="demo",
    country="AU",
    persona="Personnel Leader"
)
```

```python
GTS_for_EUTM(
    conversationid="<conversation-id>",
    process="Create Position",
    persona="Personnel Leader",
    country="AU"
)
```

```python
document_generation_final(
    usecase="EUTM",
    conversation_id="<conversation-id>",
    Persona="Personnel Leader",
    country="AU",
    process="Create Position"
)
```

The same conversation ID must be used throughout the workflow so each tool can locate the files generated by the preceding tools.

### Usage Examples

#### Example A — Generate AU training material for Create Position
- **Input:** Process = Create Position, Persona = Personnel Leader, Country = AU.
- **Processing:** The agent retrieves the process definition, generates GTS, retains AU and generic steps, creates main and sub-process content and builds the Word document.
- **Output:** A downloadable EUTM Word document delivered through Canvas.

#### Example B — Generate GBIE training material
- **Input:** A supported process, selected persona and Country = GBIE.
- **Processing:** Country segregation retains GB, IE, GBIE and generic steps according to the specified regional logic.
- **Output:** A GBIE-scoped EUTM document.

#### Example C — Generate Global training material
- **Input:** A supported process, selected persona and Country = Global.
- **Processing:** The main country-segregation tool includes all main-process steps. Content generation remains limited to the supplied evidence.
- **Output:** A Global EUTM document.

### Dependencies

| Dependency | Purpose | Criticality |
|---|---|---|
| `core` | Secrets, artefacts and URLs | Critical |
| requests | External HTTP calls | Critical |
| pandas | GTS CSV and initiator workbook handling | Critical for relevant tools |
| lxml | Workday XML parsing | Critical for XML tools |
| python-docx | Final Word document generation | Critical for document generation |
| json, re, io, uuid, html | Parsing, buffers, sanitisation and IDs | Supporting |

Exact dependency versions are not specified in the supplied files.

### APIs and Integrations

| Integration | Endpoint type | Authentication | Use |
|---|---|---|---|
| Quasar | Short-token endpoint | Username and password | Obtain API token |
| Quasar | Search and generation endpoints | `apiToken` header | Retrieve references and content |
| Workday | Custom report | HTTP Basic authentication | Retrieve process-definition XML |
| Claude | Messages endpoint | `x-api-key` header | Generate GTS and EUTM content |
| Canvas | Messaging endpoint | Short token in `apiToken` header | Deliver the document link |

Endpoint base URLs are read from Agent Manager secrets and are not included in this README.

### Security and Authentication

- Credentials are retrieved at runtime through `core.get_secret`.
- Secret values are not embedded in the tool files or README.
- Tokens, passwords, API keys and raw secret objects should not be logged.
- Network calls use explicit timeouts.
- XML parsing disables network access and external entity resolution where configured.
- Artefact filenames are sanitised before reading or writing.
- Presigned URLs should not be stored in source control.

### Monitoring and Logging

The tools return structured success or error dictionaries. Agent Manager can capture returned values and standard output for troubleshooting.

No dedicated metrics platform, health-check endpoint or monitoring configuration is included in the supplied package.

### Testing

No automated test suite is included. Validate the flow inside Agent Manager:

1. Run `trigger_for_aldi` and confirm XML and validation artefacts.
2. Run `GTS_for_EUTM` and confirm Markdown and CSV outputs.
3. Run `combined_code` and confirm the supporting-content artefact.
4. Run `segregate_by_country` for USA, AU, GB, IE, GBIE and Global.
5. Run `claude_call_for_main_bp` and confirm the output begins with `# Business Process`.
6. Run both sub-process tools and confirm their JSON keys remain aligned.
7. Run `document_generation_final` and open the generated Word document.
8. Run `workday_send_msg_to_canvas` and confirm delivery.

### Troubleshooting

| Issue | Symptoms | Likely cause | Resolution |
|---|---|---|---|
| Missing input | Required-input error | Attribute was not supplied | Check the manifest attribute mapping |
| Quasar authentication failure | Token or search call fails | Secret, network or service issue | Validate `wd-tool-secrets` without exposing values |
| Workday retrieval failure | XML artefact is not created | Secret, reference ID or report access issue | Validate the Workday secret and report permissions |
| Claude generation failure | Generation tool returns an error | Secret, endpoint or model issue | Validate the Claude secret fields and network access |
| Missing artefact | A later tool cannot read a file | Earlier tool failed or parameters changed | Keep process, persona, country and conversation ID consistent |
| Invalid GTS table | CSV generation fails | Model output did not match the table contract | Inspect the Markdown artefact and correct the input or prompt |
| Empty sub-process output | Empty values in sub-process JSON | No supported steps or validations were retrieved | Inspect the sub-process report and extraction artefacts |
| Document URL failure | DOCX exists but no link is returned | Artefact path or platform storage issue | Confirm the file exists under `uploaded_artifacts/` |
| Canvas delivery failure | Document generated but not posted | Environment, recipient ID or Canvas secret issue | Validate the selected Canvas secret and recipient ID |

### Assumptions, Risks and Gaps

**Facts:**
- The solution contains nine Agent Manager tools.
- The tools use `core` for secrets and artefacts.
- Tool hand-offs depend on conversation-scoped filenames.
- The final output is a Word document.
- No local runner or `.env` file is required.

**Assumptions:**
- Agent Manager registers each extensionless file as a Python tool.
- Workspace-specific agent, node, edge and tool IDs are created in the target environment.

**Risks and gaps:**
- No automated tests are included.
- Dependency versions are not pinned.
- Parameter naming and capitalisation vary between tools, including `conversationid` versus `conversation_id` and uppercase `Process`/`Persona` versus lowercase values.
- Artefact naming is tightly coupled between sequential tools.
- The workflow depends on configured Quasar metadata and Workday report paths.
- Large responses may still be affected by platform limits even though continuation is supported.

### Business Value

The EUTM agent standardises training-document generation across Business Processes, roles and supported countries. It combines source process evidence with controlled generation rules so the final document reads as business-user training material rather than technical or test documentation.

The workflow also provides repeatable artefact naming, traceable intermediate outputs and delivery through the same Canvas conversation used to initiate the request.

### Executive Summary

The **EUTM Agent** is an Agent Manager workflow that creates Workday End-User Training Material for a selected process, country and initiating role. It retrieves the live process definition, generates structured scenario content, filters relevant steps, produces the main training material, adds supported sub-process instructions and creates a downloadable Word document.

The solution consists of nine extensionless Python tool modules and an Agent Manager manifest. It uses the platform `core` SDK for secrets and artefacts, integrates with Quasar, Workday, Claude and Canvas, and passes data between tools through conversation-scoped files.

The package is designed specifically for Agent Manager. It does not require a VS Code runner, local environment file, web server or standalone deployment process.

