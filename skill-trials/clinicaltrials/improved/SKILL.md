---
name: clinicaltrials-gov-v2
description: Use when you need to search or fetch clinical-study records from ClinicalTrials.gov using the public REST API v2.
---

# ClinicalTrials.gov API v2

## Mandatory Pre-flight

- No API key is required, but the API is rate-limited. Keep requests sparse (≈1 request/second) and watch for HTTP 429.
- Base URL: `https://clinicaltrials.gov/api/v2`.
- Python examples below use the standard library only (`urllib.request`, `json`).

## Domain Fundamentals

ClinicalTrials.gov is the US registry of clinical research studies. Each study has a unique **NCT ID** (e.g., `NCT00000102`).
The API returns studies as deeply nested JSON under modules such as `protocolSection`, `resultsSection`, and `derivedSection`.
Key concepts:

- **Protocol**: the plan of the study (title, design, eligibility, locations).
- **Arms / Interventions**: treatment groups and what is being administered.
- **Eligibility**: inclusion/exclusion criteria for participants.
- **Status**: recruitment state (`RECRUITING`, `COMPLETED`, `WITHDRAWN`, etc.).
- **Phase**: stage of drug development (`PHASE1`, `PHASE2`, `PHASE3`, `PHASE4`, `NA`).

See `references/glossary.md` for the full jargon list.

## Core Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /studies` | Search studies. Use `query.term`, `pageSize`, `filter.*`, `fields`. |
| `GET /studies/{nctId}` | Fetch a single study by NCT ID. |
| `POST /studies/download` | Bulk download studies by IDs or query. |
| `GET /version` | API build/version metadata. |

## Minimal Example

```python
import urllib.request, json, urllib.parse

base = "https://clinicaltrials.gov/api/v2"
params = urllib.parse.urlencode({"query.term": "diabetes", "pageSize": "5"})
url = f"{base}/studies?{params}"

with urllib.request.urlopen(url, timeout=30) as resp:
    data = json.load(resp)

for study in data["studies"]:
    mod = study["protocolSection"]["identificationModule"]
    print(mod["nctId"], "-", mod.get("briefTitle", "(no title)"))
```

## Idiomatic Example: Paginated Search

```python
import urllib.request, json, urllib.parse, time

base = "https://clinicaltrials.gov/api/v2"
params = {"query.term": "type 2 diabetes", "pageSize": "100", "fields": "NCTId,BriefTitle,OverallStatus"}

token = None
while True:
    if token:
        params["pageToken"] = token
    url = f"{base}/studies?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        page = json.load(resp)
    for s in page.get("studies", []):
        ident = s["protocolSection"]["identificationModule"]
        status = s["protocolSection"]["statusModule"]["overallStatus"]
        print(ident["nctId"], status, ident.get("briefTitle"))
    token = page.get("nextPageToken")
    if not token:
        break
    time.sleep(1.0)  # be polite
```

## Wall of Shame

- **Field names are case-sensitive and path-heavy.** The NCT ID lives at `protocolSection.identificationModule.nctId`, not `nct_id`.
- **`fields` reduces payload size, but values must be exact module names** (e.g., `NCTId`, `BriefTitle`). Unknown fields are silently ignored.
- **Pagination uses `nextPageToken`, not page numbers.** Stop when the token is absent.
- **`/studies/{nctId}` returns a single study object, not a list.** Do not index into `data["studies"]`.
- **Rate-limit behavior is not officially published.** If you receive 429 or 403, back off and retry with exponential delay.

## Reference Pointers

- Full endpoint details: `references/api-docs.md`
- Domain terminology: `references/glossary.md`
