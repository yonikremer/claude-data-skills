# ClinicalTrials.gov Domain Glossary

| Term | Definition | Source | Real Example |
|---|---|---|---|
| NCT ID | Unique ClinicalTrials.gov identifier for a study | API response | `NCT00171717` |
| Protocol section | The part of a study record describing the study plan | API field path | `protocolSection` object |
| Identification module | Sub-module containing NCT ID, title, sponsor | API field path | `protocolSection.identificationModule` |
| Status module | Sub-module with recruitment/completion dates and status | API response | `protocolSection.statusModule.overallStatus: "COMPLETED"` |
| Overall status | Current recruitment/disposition state of the study | API response | `COMPLETED`, `RECRUITING`, `WITHDRAWN` |
| Design module | Sub-module with study design details | API field path | `protocolSection.designModule` |
| Allocation | How participants are assigned to groups | API response | `NON_RANDOMIZED` |
| Intervention model | Structure of treatment groups | API response | `SINGLE_GROUP`, `PARALLEL`, `CROSSOVER` |
| Masking | Who is blinded to assignment | API response | `NONE`, `DOUBLE`, `QUADRUPLE` |
| Phase | Stage of clinical investigation | API response | `PHASE1`, `PHASE2`, `PHASE3`, `PHASE4`, `NA` |
| Arms / interventions | Treatment groups and what is administered | API module | `protocolSection.armsInterventionsModule` |
| Eligibility module | Inclusion/exclusion criteria | API module | `protocolSection.eligibilityModule` |
| Conditions module | Diseases/conditions and keywords | API response | `protocolSection.conditionsModule.conditions: ["Congenital Adrenal Hyperplasia"]` |
| Sponsor collaborators module | Organizations running the study | API module | `protocolSection.sponsorCollaboratorsModule` |
| Next page token | Opaque cursor for paginated results | API response | `nextPageToken: "ZVNj7o2Elu8o3lp3U8mh5unumpOQJJxrYf0"` |
