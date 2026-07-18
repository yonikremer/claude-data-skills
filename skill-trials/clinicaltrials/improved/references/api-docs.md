# ClinicalTrials.gov API v2 Reference

## Source of truth

- Base URL (verified by probe): `https://clinicaltrials.gov/api/v2`
- Official portal: `https://clinicaltrials.gov/data-api/api` (JS-heavy; rely on live probes for facts)

## Authentication

- None for read access.

## Rate limits

- Not precisely published. Empirical guidance: keep to ~1 request/second and no more than a few hundred requests per minute.
- Watch for HTTP 429 (Too Many Requests) or HTTP 403; back off with exponential retry.

## Pagination

- `pageSize`: max 1000, default 10.
- `nextPageToken`: opaque token returned in the response. Pass it as `pageToken` to fetch the next page.

## Endpoint Verification Matrix

Coverage goal: enumerate the entire public v2 surface. Endpoints marked `UNVERIFIED` are documented but were not safely exercised during validation.

| Method | Path | Purpose | Required params | Verified? | Probe status | Notes |
|---|---|---|---|---|---|---|
| GET | `/studies` | Search studies | `query.term` or `filter.*` | ✅ | 200 | Returns `{studies:[...], nextPageToken}` |
| GET | `/studies/{nctId}` | Single study | `nctId` | ✅ | 200 | Returns study object directly |
| POST | `/studies/download` | Bulk download | `ids` or query + `format` | ❌ | 400 on naive GET | Requires POST with JSON body; not probed to avoid large downloads |
| GET | `/version` | API build/version info | none | ✅ | 200 | Returns version metadata |

## Sample Response Shape (`/studies?query.term=diabetes&pageSize=1`)

```json
{
  "studies": [
    {
      "protocolSection": {
        "identificationModule": {
          "nctId": "NCT00171717",
          "briefTitle": "Conversion From Tacrolimus to Cyclosporine..."
        },
        "statusModule": {
          "overallStatus": "COMPLETED"
        },
        "designModule": {
          "studyType": "INTERVENTIONAL",
          "phases": ["PHASE4"],
          "designInfo": {
            "allocation": "NON_RANDOMIZED",
            "interventionModel": "SINGLE_GROUP",
            "primaryPurpose": "TREATMENT",
            "maskingInfo": { "masking": "NONE" }
          }
        }
      }
    }
  ],
  "nextPageToken": "..."
}
```

## Field Filtering

The `fields` query parameter accepts comma-separated module names. Examples verified by probe:

- `fields=NCTId,BriefTitle`
- `fields=NCTId,BriefTitle,OverallStatus`

Unknown fields are ignored by the server.
