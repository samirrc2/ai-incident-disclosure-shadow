# Data availability and reproducibility

## Production-approved article statement

> The original contributions presented in the study are included in the article/Supplementary material; further inquiries can be directed to the corresponding author. Incident data were obtained from the AI Incident Database (AIID) snapshot of 27 July 2026 (https://incidentdatabase.ai/research/snapshots/), which is licensed under CC BY-SA 4.0 (McGregor, 2021). Supplementary files containing AIID-derived records are distributed under the same CC BY-SA 4.0 license. SEC filings were obtained from SEC EDGAR and are in the public domain.

## Supporting computational materials

- **Public study repository:** https://github.com/samirrc2/ai-incident-disclosure-shadow. This contains the documented, frozen incident-to-issuer mappings, per-incident coding records, analytical scripts and SHA-256 manifests.
- **Previously archived Code Ocean computational artifact:** https://doi.org/10.24433/CO.2340354.v3. This is a **separate research artifact DOI**, not the peer-reviewed article DOI.
- **Journal article:** https://doi.org/10.3389/frai.2026.1969275. Cite this DOI for the peer-reviewed research findings.

The repository's `reproduce.sh` regenerates the analytical outputs from frozen inputs without calling external AI APIs. It does not re-run historical SEC EDGAR web retrieval or recreate the upstream AIID incident database. Source data and derivative records must be reused in accordance with the applicable upstream terms.

The AIID source snapshot was dated 27 July 2026. The source material's CC BY-SA 4.0 terms apply to AIID-derived records, alongside attribution to the AI Incident Database and McGregor (2021). SEC EDGAR filings are public-domain sources. See [LICENSE](LICENSE) for the separate software and data provisions.

The research concerns whether records are identifiable in specified filings, not whether a corporation complied with securities law. No named company's legal disclosure obligations are adjudicated.
