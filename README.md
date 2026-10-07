# Shakhsi4 | Independent AI & Digital Economy Econometrics

**Isolated project.** GitHub repository mrst10578/Shakhsi4 and a separate Linear project. It does not depend on Shakhsi2 or Shakhsi3.

Two independent country-panel research studies:
- **AI and labor/high-tech exports:** 30 countries (2016–2024); 270 country-years; Iran absent.
- **Digital economy and growth/productivity:** 47 countries (2005–2022); 846 country-years; Iran absent.

## What has been done
- Read both Gmail messages, study specifications, data dictionaries, and reference ARDL paper.
- Analyzed original Excel files locally: complete, balanced, no duplicated ISO3-year keys and no missing values.
- Computed pooled and within-country VIF and correlation audits. See results/PRELIMINARY_AUDIT.md.
- Prepared separate Stata 18 dynamic-panel GMM and pre/post-test programs, with uncertainty clearly labeled.

## Local usage
1. Use the privately emailed original spreadsheets. They are **not committed to this public repository**.
2. Copy them under data/ retaining exact names: AI_Balanced_Panel (1).xlsx and Balanced_Panel_Data.xlsx.
3. Run: python scripts/audit_panels.py --ai "data/AI_Balanced_Panel (1).xlsx" --digital "data/Balanced_Panel_Data.xlsx" --out results/audit.json
4. In licensed Stata 18, run ssc install xtabond2 if missing. From repo root run:
   - do stata/01_ai_system_gmm.do
   - do stata/02_digital_system_gmm.do
5. Review produced logs for valid estimation, instrument count vs groups, robust Hansen and difference-in-Hansen (when offered), AR(1)/AR(2), specification stability.

**Not yet completed:** GMM estimation and panel unit-root test results. Stata 18 was not accessible to the present agent; no numerical GMM p-values have been invented. Particularly with the 47x18 panel, instrument proliferation makes System GMM an experimental candidate, not an automatic endorsement.

See docs/methodology.md for specific scientific limitations. The sent Iran ARDL money-demand paper addresses a different model and cannot validate the panel-GMM analyses.

[Draft PR #1](https://github.com/mrst10578/Shakhsi4/pull/1)
