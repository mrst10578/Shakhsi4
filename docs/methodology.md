# Shakhsi4 methodological and execution notes

## Scope and source integrity
Two separate panels from private Gmail attachments, received 2026-09-30:
- AI: 30 countries × 2016–2024, dependent high-tech exports (percentage share) and unemployment (rate); investment and AI patent counts are log1p-transformed. Interpreting log1p coefficients as pure elasticities is incorrect, especially near zero.
- Digital: 47 countries × 2005–2022, dependent annual GDP growth in percentage points and ln(productivity); Internet, broadband, ICT exports plus unemployment, inflation and R&D controls.

Both workbooks are balanced and contain no nulls or duplicate ISO3-year combinations. This does NOT guarantee reliable original measurements. Iran is absent in both.

## Pre-estimation checklist
Panel ID/time validation; descriptive statistics, suspicious ranges and outliers; within/pooled VIF and correlation; persistence and common shocks; pre-registration of instrument restrictions; panel unit-root tests when their assumptions/power justify use. T=9 makes IPS/LLC conclusions especially fragile, and cross-section dependence can invalidate first-generation tests. Unit-root testing is not a mandatory GMM gate and stationarity testing alone does not establish cointegration.

## GMM checklist
Stata 18 do-files use xtabond2 and deliberately collapse narrow instrument lags. Log dynamic FE is a comparison only, since lagged FE has Nickell bias. System GMM requires credible exogeneity restrictions and additional initial-condition moments, not merely a command. Audit robust Hansen J, AR(1), AR(2), difference-in-Hansen for level moments when reported, and number of instruments relative to groups. A non-rejected Hansen is not proof of validity, and a near-one p-value may reflect instrument proliferation. Sargan differs from robust Hansen.

With 47 countries and 18 years, full year dummies can proliferate instruments; if instruments approach N, results should be marked unsuitable rather than reported as reliable. Check a reduced instrument design and compare alternative panel estimators.

## Iran peers
Neither panel contains Iranian observations. Scientific peer matching needs external Iranian GDP per capita (PPP), structure, digital adoption, inflation, institutions etc for a common pre-treatment period and documented distance rule. A very small peer-only sample is inappropriate for large-N GMM. Full 30/47-country models are reference baselines; subsets are sensitivity analyses, not an exercise in selecting significant p-values.

## Different paper
The accompanying 2026 paper investigates money demand in Iran using an ARDL time-series model (1994–2024). Its bounds/CUSUM and other ARDL tests are unrelated to verification of these panel GMM equations.

## Execution evidence
The Excel files have been analyzed locally for coverage, missingness and multicollinearity. Stata binaries are not accessible here, so NO actual xtabond2, valid Hansen, Arellano-Bond or Difference-in-Hansen test outcome is claimed. To finish: use licensed Stata 18, install xtabond2, run each do-file, inspect logs and reject failed diagnostic specifications.
