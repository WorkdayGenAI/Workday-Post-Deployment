# EUTM Agent for GenWizard Agent Manager

## Appendix: Quick Reference

This README explains the EUTM agent and guides a builder through recreating it in GenWizard Agent Manager.

### A. Build Sequence

```text
1. Prepare access
2. Add credentials to Secret Manager
3. Upload required documents to Uploaded Artifacts
4. Create Python tools in the Tools section
5. Validate and approve the tools
6. Create utility agents and attach the required tools
7. Create the super agent
8. Add the utility agents to the super agent in the required order
9. Validate the complete flow
10. Connect and run the agent from Canvas
```

### B. Agent Manager Structure

```text
Python scripts
    ↓
Tools
    ↓
Utility Agents
    ↓
Super Agent
    ↓
Canvas
```

- **Tools** are created from the Python scripts supplied with this package.
- **Utility Agents** use the tools required for a specific stage of the EUTM process.
- **The Super Agent** combines the utility agents into the complete EUTM workflow.
- **Secret Manager** stores all credentials and secret configuration values.
- **Uploaded Artifacts** stores all documents and supporting files required by the agent.

### C. Components at a Glance

| Component type | Count | Purpose |
|---|---:|---|
| Tools | 9 | Execute the Python-based retrieval, processing, generation and delivery functions |
| Utility Agents | 7 | Group the required tools into individual stages of the workflow |
| Super Agent | 1 | Connect all utility agents into the complete EUTM process |
| Secret Manager entries | Environment dependent | Securely store credentials and endpoint configuration |
| Uploaded Artifacts | Environment dependent | Store the documents required by the tools during execution |

### D. Tools at a Glance

| Order | Tool | Purpose |
|---:|---|---|
| 1 | `trigger_for_aldi` | Resolve the main Business Process and retrieve the Workday XML and validations |
| 2 | `GTS_for_EUTM` | Generate GTS content from the Workday XML |
| 3 | `combined_code` | Retrieve the supporting user-training or job-aid content |
| 4 | `segregate_by_country` | Retain the main Business Process steps applicable to the selected country |
| 5 | `claude_call_for_main_bp` | Generate the main Business Process EUTM content |
| 6 | `combined_code_for_sub_bp` | Retrieve and segregate the referenced sub-process definitions and validations |
| 7 | `claude_call_for_subbp_three` | Generate the sub-process EUTM sections |
| 8 | `document_generation_final` | Merge the main and sub-process content into the final Word document |
| 9 | `workday_send_msg_to_canvas` | Send the generated document link to Canvas |

### E. Utility Agents at a Glance

| Super Agent order | Utility Agent | Tools used |
|---:|---|---|
| 1 | `Trigger for Aldi` | `trigger_for_aldi` |
| 2 | `GTS for EUTM` | `GTS_for_EUTM` |
| 3 | `Combined Code Agent 2` | `combined_code`, `segregate_by_country` |
| 4 | `Generate_document_for_BP` | `claude_call_for_main_bp` |
| 5 | `Combined Code for Sub BP` | `combined_code_for_sub_bp` |
| 6 | `claude call for subbp three` | `claude_call_for_subbp_three` |
| 7 | `document_generation_entire_EUTM` | `document_generation_final`, `workday_send_msg_to_canvas` |

---

## 1. What Is This Agent?

The EUTM agent creates Workday End-User Training Material for a selected Business Process, initiating security group and country.

The completed workflow:

1. Retrieves the main Workday Business Process definition.
2. Generates GTS scenario and step content.
3. Retrieves supporting user-training or job-aid content.
4. Filters process steps for the selected country.
5. Generates the main Business Process training material.
6. Identifies and processes relevant sub-processes.
7. Generates sub-process training sections.
8. Creates the final Word document.
9. Sends the document link to Canvas.

The final output is a downloadable EUTM Word document written for business users.

## 2. Intended Audience

This guide is intended for users who:

- Have access to GenWizard Agent Manager.
- Are authorised to create and approve tools.
- Can create utility agents and super agents.
- Can access Secret Manager and Uploaded Artifacts.
- Have the approved credentials and supporting documents required by the EUTM workflow.

## 3. How Agent Manager Is Used

### 3.1 Tools

The **Tools** section is where the supplied Python scripts are converted into Agent Manager tools.

Each tool requires:

- A unique tool name.
- The matching Python source code.
- A description.
- The required input attributes.
- The required packages.
- Successful validation and approval, where required.

The Python scripts are not run as a standalone VS Code project. They are entered into and executed through the Tools section of GenWizard Agent Manager.

### 3.2 Utility Agents

After creating the tools, create the utility agents.

Each utility agent represents one stage of the EUTM workflow and is connected only to the tool or tools needed for that stage.

The utility agents must be created only after their tools have been saved, validated and made available for selection.

### 3.3 Super Agent

The super agent combines the utility agents into the complete workflow.

For this use case, create a super agent named:

```text
GTS for EUTM
```

Add the seven utility agents in the exact sequence documented in this README. The workflow is sequential because later stages depend on files created by earlier stages.

## 4. Supporting Platform Components

### 4.1 Secret Manager

All usernames, passwords, API keys, endpoint values and other sensitive configuration must be maintained in **Secret Manager**.

Do not place secret values in:

- Tool source code.
- Tool descriptions.
- Utility Agent configurations.
- Super Agent descriptions.
- README files.
- Uploaded documents.
- Logs or screenshots.

The tool source must retrieve approved values at runtime through `core.get_secret`.

### 4.2 Uploaded Artifacts

All documents and supporting files required by the EUTM workflow must be stored in **Uploaded Artifacts**.

This includes files such as:

- `initiator_file.xlsx`
- Mapping workbooks used by the process
- Supporting reference documents
- Job-aid documents
- Any additional approved file required by the tools

Use the exact filenames expected by the tool source. A filename mismatch can prevent a tool from locating the required document.

Tools that read documents must retrieve them using the `uploaded_artifacts/` path. Generated files may also be written to or made available through the platform's artefact storage based on the tool's output logic.

## 5. Prerequisites

Before building the agent, confirm that the following are available:

- Access to the target GenWizard Agent Manager environment.
- Permission to create tools.
- Permission to validate or approve tools.
- Permission to create Utility Agents.
- Permission to create Super Agents.
- Access to Secret Manager.
- Access to Uploaded Artifacts.
- Approved Quasar credentials.
- Approved Workday custom-report credentials.
- Approved model endpoint credentials.
- Approved Canvas credentials.
- All nine tool source files.
- `agent_manager_manifest.json`, if supplied with the package.
- All required supporting documents.

Use a non-production environment for the first complete validation.

## 6. Prepare Secret Manager

Create or confirm the following Secret Manager entries. The exact secret names are required because the tools retrieve them by name.

| Secret name | Required fields | Used for |
|---|---|---|
| `wd-tool-secrets` | `quasar_baseurl`, `quasar_username`, `quasar_password` | Quasar authentication and retrieval |
| `wd-tool-eutm-secret-2` | `eutm_report_Url`, `eutm_report_username`, `eutm_report_password` | Workday Business Process report retrieval |
| `SCA_WA_Claude_Opus_4_6` | `Endpoint`, `api_key`, `deployment_name` | GTS and EUTM generation |
| `workday_CUI` | `url`, `username`, `password` | Default or demo Canvas delivery |
| `workday_dev` | `url`, `username`, `password` | Development Canvas delivery |
| `workday_stgtest` | `url`, `username`, `password` | Stage-test Canvas delivery |
| `workday_prod` | `url`, `username`, `password` | Production Canvas delivery |

### Secret Manager Validation

For every secret:

1. Confirm the secret name matches the source code exactly.
2. Confirm all required fields are present.
3. Confirm the credential has access to the intended environment.
4. Confirm the tool can retrieve the secret without displaying its content.
5. Do not copy secret values into test notes or screenshots.

## 7. Prepare Uploaded Artifacts

Before testing the tools, upload all required documents to **Uploaded Artifacts**.

### Required File Checklist

| File | Required when | Purpose |
|---|---|---|
| `initiator_file.xlsx` | Main EUTM generation uses Initiation mapping | Provides the starting point for the selected Business Process and persona |
| Business Process mapping workbook | Required by the configured Quasar source | Resolves Workday Business Process references |
| User-training index workbook | Required by the configured Quasar source | Resolves job-aid or user-training content |
| Supporting job-aid documents | When matching content exists | Provides introductory context |
| Other approved reference files | When required by tool logic | Supports specialised Business Processes |

### Upload Rules

- Keep the expected filename unchanged.
- Do not add version suffixes unless the tool is updated to use them.
- Do not store credentials in uploaded documents.
- Confirm the uploaded file opens successfully.
- Confirm the correct sheet names exist in Excel files.
- Replace outdated files deliberately rather than keeping ambiguous duplicates.

## 8. Create the Tools

Open the **Tools** section in GenWizard Agent Manager and create the following tools.

For each tool:

1. Select the option to create a new tool.
2. Enter the exact tool name.
3. Add a clear description.
4. Paste the matching Python source code.
5. Add the required attributes.
6. Add the required packages.
7. Save the tool.
8. Run validation or certification.
9. Resolve any reported issue.
10. Submit and approve the tool when required.
11. Test the tool before using it in a Utility Agent.

### 8.1 Tool: `trigger_for_aldi`

**Purpose:** Resolve the main Workday Business Process reference, retrieve the Workday XML and create the validation file.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `process` | str | Workday Business Process name |
| `conversation_id` | str | Conversation identifier used across the workflow |
| `requester_user_email_id` | str | Requesting user's email identifier |
| `environment` | str | Runtime environment |
| `country` | str | Country or regional scope |
| `persona` | str | Initiating Security Group |

**Packages:**

```text
typing
core
uuid
re
json
requests
html
lxml
```

**Expected outputs:**

```text
{process}_{persona}_{country}_{conversation}_workday_bp_xml.txt
{process}_{persona}_{country}_{conversation}_validations.txt
```

### 8.2 Tool: `GTS_for_EUTM`

**Purpose:** Generate GTS Markdown and CSV content from the Workday XML.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `conversationid` | str | Same conversation identifier used by the preceding stage |
| `process` | str | Workday Business Process name |
| `persona` | str | Initiating Security Group |
| `country` | str | Country or regional scope |

**Packages:**

```text
typing
core
uuid
re
json
requests
io
pandas
```

**Expected outputs:**

```text
{process}_{persona}_{country}_markdown_gts_{conversation}.txt
{process}_{country}_{persona}TestCaseGenerated_{conversation}.csv
```

### 8.3 Tool: `combined_code`

**Purpose:** Retrieve the matching supporting training or job-aid content.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `process` | str | Workday Business Process name |
| `persona` | str | User persona |
| `conversation_id` | str | Conversation identifier |
| `country` | str | Country or regional scope |

**Packages:**

```text
typing
core
uuid
re
json
requests
```

**Expected output:**

```text
{process}_{persona}_{country}_{conversation}_indexfile_content.txt
```

### 8.4 Tool: `segregate_by_country`

**Purpose:** Create the country-scoped main Business Process steps.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `conversation_id` | str | Conversation identifier |
| `persona` | str | Initiating Security Group |
| `country` | str | USA, US, AU, GB, IE, GBIE or Global |
| `process` | str | Workday Business Process name |

**Packages:**

```text
typing
core
uuid
re
json
html
lxml
```

**Expected output:**

```text
{country}_{persona}_{process}_{conversation}_country_segregation.json
```

### 8.5 Tool: `claude_call_for_main_bp`

**Purpose:** Generate the main Business Process EUTM content.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `conversation_id` | str | Conversation identifier |
| `process_steps` | str | Hand-off from the preceding Utility Agent |
| `Process` | str | Workday Business Process name |
| `Persona` | str | Initiating Security Group |
| `country` | str | Country or regional scope |

**Packages:**

```text
typing
core
uuid
re
json
requests
io
pandas
```

**Expected output:**

```text
{Process}_{Persona}_{country}_{conversation}_EUTM_response.txt
```

### 8.6 Tool: `combined_code_for_sub_bp`

**Purpose:** Retrieve sub-process definitions and create aligned segregation and validation files.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `conversation_id` | str | Conversation identifier |
| `persona` | str | Initiating Security Group |
| `country` | str | Country or regional scope |
| `process` | str | Main Workday Business Process name |

**Packages:**

```text
typing
core
uuid
re
json
html
requests
lxml
```

**Expected outputs:**

```text
{process}_{country}_{persona}_{conversation}_sub_bp_report.json
{process}_{country}_{persona}_{conversation}_segregation_sub_bp.json
{process}_{country}_{persona}_{conversation}_validation_sub_bp.json
```

### 8.7 Tool: `claude_call_for_subbp_three`

**Purpose:** Generate the EUTM content for the supported sub-processes.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `conversation_id` | str | Conversation identifier |
| `persona` | str | Initiating Security Group |
| `country` | str | Country or regional scope |
| `process` | str | Main Workday Business Process name |

**Packages:**

```text
typing
core
uuid
re
json
requests
```

**Expected output:**

```text
{process}_{persona}_{country}_{conversation}_sub_bp_tasks.json
```

### 8.8 Tool: `document_generation_final`

**Purpose:** Merge the generated content and create the final EUTM Word document.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `usecase` | str | Use `EUTM` |
| `conversation_id` | str | Conversation identifier |
| `Persona` | str | Initiating Security Group |
| `country` | str | Country or regional scope |
| `process` | str | Workday Business Process name |

**Packages:**

```text
typing
core
uuid
re
json
io
docx
```

**Expected output:**

```text
{process}_{Persona}_for_{country}_{conversation}_EUTM_Document.docx
```

### 8.9 Tool: `workday_send_msg_to_canvas`

**Purpose:** Deliver the final document link to Canvas.

**Attributes:**

| Name | Type | Description |
|---|---|---|
| `conversation_id` | str | Canvas conversation identifier |
| `message` | str | Message containing the final document link |
| `environment` | str | dev, demo, stagetest or prod |
| `recipient_id` | str | Recipient identifier when required |

**Packages:**

```text
typing
core
json
requests
```

## 9. Validate the Tools

Use one consistent test set for the entire validation:

```text
process: Create Position
persona: Personnel Leader
country: AU
conversation_id: one shared non-production conversation ID
usecase: EUTM
environment: approved non-production environment
```

Run the tools individually in the documented order.

After every tool run:

1. Confirm the tool completed successfully.
2. Confirm the expected output file was created.
3. Confirm the filename contains the expected process, persona, country and conversation ID.
4. Confirm the next tool can locate the file.
5. Review errors before continuing.
6. Do not continue with guessed or manually fabricated intermediate content.

## 10. Create the Utility Agents

After all tools are available, open the **Utility Agents** section and create the following Utility Agents.

For each Utility Agent:

1. Create a new Utility Agent.
2. Use the exact name shown below.
3. Enter a short description of the stage.
4. Add the tool or tools listed for that Utility Agent.
5. Configure the tool input mapping.
6. Save the Utility Agent.
7. Run an independent test where possible.

### 10.1 Utility Agent: `Trigger for Aldi`

**Tools:**

```text
trigger_for_aldi
```

**Configuration:** Pass `process`, `conversation_id`, `requester_user_email_id`, `environment`, `country` and `persona` from the runtime input to the tool without changing them.

### 10.2 Utility Agent: `GTS for EUTM`

**Tools:**

```text
GTS_for_EUTM
```

**Configuration:** Pass `process`, `persona`, `country` and the same conversation identifier used by the preceding stage. Map it to the tool's `conversationid` attribute.

### 10.3 Utility Agent: `Combined Code Agent 2`

**Tools:**

```text
combined_code
segregate_by_country
```

**Required order:**

```text
1. combined_code
2. segregate_by_country
```

**Configuration:** Reuse the exact same process, persona, country and conversation ID for both tools.

### 10.4 Utility Agent: `Generate_document_for_BP`

**Tools:**

```text
claude_call_for_main_bp
```

**Configuration:**

- Pass `conversation_id` from the runtime input.
- Map the user's process value to `Process`.
- Map the user's persona value to `Persona`.
- Pass `country` unchanged.
- Pass the preceding Utility Agent's output to `process_steps` without rewriting it.

### 10.5 Utility Agent: `Combined Code for Sub BP`

**Tools:**

```text
combined_code_for_sub_bp
```

**Configuration:** Pass `conversation_id`, `persona`, `country` and `process` unchanged.

### 10.6 Utility Agent: `claude call for subbp three`

**Tools:**

```text
claude_call_for_subbp_three
```

**Configuration:** Pass `conversation_id`, `persona`, `country` and `process` unchanged.

### 10.7 Utility Agent: `document_generation_entire_EUTM`

**Tools:**

```text
document_generation_final
workday_send_msg_to_canvas
```

**Required order:**

```text
1. document_generation_final
2. workday_send_msg_to_canvas
```

**Configuration:**

- Set `usecase` to `EUTM`.
- Map the user process to `process`.
- Map the user persona to `Persona`.
- Pass the same `country` and `conversation_id`.
- Read the download link returned by `document_generation_final`.
- Include that link in the `message` passed to `workday_send_msg_to_canvas`.
- Pass `environment` and `recipient_id` from the runtime input.

## 11. Create the Super Agent

Open the **Super Agents** section and create a new Super Agent.

### Super Agent Details

| Field | Value |
|---|---|
| Name | `GTS for EUTM` |
| Description | Generates country- and initiating-role-specific Workday End-User Training Material and returns the final Word document through Canvas. |
| Maximum messages | Use the approved value for the target environment |
| Tags | Workday |

### Add the Utility Agents

Add the Utility Agents in this exact order:

```text
Start
  -> Trigger for Aldi
  -> GTS for EUTM
  -> Combined Code Agent 2
  -> Generate_document_for_BP
  -> Combined Code for Sub BP
  -> claude call for subbp three
  -> document_generation_entire_EUTM
  -> End
```

Do not change the sequence. The tools exchange files through the platform's artefact storage, and each later stage depends on earlier output.

### Super Agent Runtime Inputs

| Input | Required | Purpose |
|---|---|---|
| `process` | Yes | Workday Business Process name |
| `persona` | Yes | Initiating Security Group |
| `country` | Yes | Country or regional scope |
| `conversation_id` | Yes | Shared identifier used for file names and Canvas delivery |
| `requester_user_email_id` | As required | Requester context |
| `environment` | Yes for delivery | Selects the Canvas environment |
| `recipient_id` | Environment dependent | Canvas recipient |

Preserve these values exactly across all Utility Agents. Do not translate, abbreviate, reformat or substitute them.

## 12. End-to-End Validation

Run the completed Super Agent with a valid non-production input combination.

### Validation Checkpoints

| Stage | Expected result |
|---|---|
| Trigger for Aldi | Workday XML and validation files are created |
| GTS for EUTM | GTS Markdown and CSV are created |
| Combined Code Agent 2 | Supporting content and country segregation files are created |
| Generate_document_for_BP | Main EUTM text begins with `# Business Process` |
| Combined Code for Sub BP | Sub-process report, segregation and validation files are created |
| claude call for subbp three | Sub-process task JSON is created and keys remain aligned |
| document_generation_entire_EUTM | Final DOCX is created and a download link is returned |
| Canvas delivery | The document link appears in the originating Canvas conversation |

### Validation Rules

- Stop at the first failed stage.
- Check the expected filename before reviewing downstream tools.
- Confirm the same conversation ID was used throughout.
- Confirm required documents exist in Uploaded Artifacts.
- Confirm credentials exist in Secret Manager.
- Confirm all tools are approved and available to their Utility Agents.
- Do not bypass a failed stage with manually created files.

## 13. Artefact Naming Contract

The following names must remain consistent:

```text
{process}_{persona}_{country}_{conversation}_workday_bp_xml.txt
{process}_{persona}_{country}_{conversation}_validations.txt
{process}_{persona}_{country}_markdown_gts_{conversation}.txt
{process}_{country}_{persona}TestCaseGenerated_{conversation}.csv
{process}_{persona}_{country}_{conversation}_indexfile_content.txt
{country}_{persona}_{process}_{conversation}_country_segregation.json
{Process}_{Persona}_{country}_{conversation}_EUTM_response.txt
{process}_{country}_{persona}_{conversation}_sub_bp_report.json
{process}_{country}_{persona}_{conversation}_segregation_sub_bp.json
{process}_{country}_{persona}_{conversation}_validation_sub_bp.json
{process}_{persona}_{country}_{conversation}_sub_bp_tasks.json
{process}_{Persona}_for_{country}_{conversation}_EUTM_Document.docx
```

A change to any naming pattern must be applied to every tool that writes or reads that file.

## 14. Dependencies

| Dependency | Purpose |
|---|---|
| `core` | Secret Manager and artefact access |
| `requests` | Quasar, Workday, model and Canvas calls |
| `pandas` | CSV and Excel processing |
| `lxml` | Workday XML parsing |
| `python-docx` | Word document generation |
| `json`, `re`, `io`, `uuid`, `html`, `typing` | Standard processing support |

## 15. Security and Governance

- Keep all passwords, tokens, API keys and endpoint configuration in Secret Manager.
- Keep all supporting documents in Uploaded Artifacts.
- Do not print secret values or tokens.
- Do not include secrets in test screenshots.
- Do not include runtime IDs in reusable documentation.
- Do not store presigned URLs in source control.
- Complete validation, scanning and approval before adding a tool to a Utility Agent.
- Use a non-production environment for the first complete test.

## 16. Troubleshooting

| Problem | Likely cause | Resolution |
|---|---|---|
| Tool is not available in Utility Agent | Tool was not saved, approved or published | Complete the tool lifecycle and refresh the Utility Agent tool list |
| Secret cannot be retrieved | Secret name or field name differs from the source | Correct the entry in Secret Manager |
| Uploaded file cannot be found | Filename differs or file is not in Uploaded Artifacts | Upload the file with the exact expected name |
| Workday XML is missing | Process reference, credentials or report access failed | Validate the trigger tool and Workday Secret Manager entry |
| GTS output is missing | XML file was not found or generation failed | Check the preceding stage and expected filename |
| Country JSON is empty | Country input or filtering condition does not match | Validate country value and inspect the Workday conditions |
| Main EUTM generation fails | One or more required files are absent | Confirm GTS, validation, country and supporting-content files |
| Sub-process output is incomplete | Sub-process definitions or validations were not retrieved | Inspect sub-process report and JSON files |
| DOCX has unresolved task markers | Main task markers and sub-process JSON keys do not match | Align the exact task names across both outputs |
| Canvas delivery fails | Environment secret or recipient mapping is incorrect | Validate the Canvas Secret Manager entry and delivery inputs |
| Wrong file is read | Different runtime values generated a different filename | Reuse the same process, persona, country and conversation ID |

## 17. Migration to Another Agent Manager Environment

When rebuilding the agent in another environment:

1. Export or copy the nine tool definitions.
2. Export or document the seven Utility Agent configurations.
3. Export or document the Super Agent sequence.
4. Recreate the required Secret Manager entries without copying secret values into files.
5. Upload the required documents to Uploaded Artifacts.
6. Revalidate every tool.
7. Reattach the tools to the Utility Agents.
8. Recreate the Super Agent sequence.
9. Run the full validation checklist.
10. Confirm Canvas delivery in the destination environment.

## 18. Executive Summary

The EUTM solution is built in GenWizard Agent Manager using a clear three-level structure:

1. Python scripts are converted into **Tools**.
2. The Tools are assigned to **Utility Agents** for the individual stages of the workflow.
3. The Utility Agents are assembled into the **GTS for EUTM Super Agent**.

All sensitive credentials and endpoint values are maintained in **Secret Manager**. All required documents and supporting files are stored in **Uploaded Artifacts**.

By following this README in order, a builder can create, validate and connect the complete EUTM agent without using a local VS Code runner or embedding sensitive configuration in the source code.
