# Local audit: real source files analyzed, 2026-10-08
| | AI panel | Digital panel |
|---|---:|---:|
| Countries | 30 | 47 |
| Years | 2016–2024 | 2005–2022 |
| Observations | 270 | 846 |
| Missing values | 0 | 0 |
| Duplicate ISO3-year | 0 | 0 |
| Iran included | No | No |
| Balanced | Yes | Yes |

### Multicollinearity
- AI pooled VIF: Investment 1.0288; Patents 1.0437; GDP Growth 1.0173.
- AI within-country VIF: Investment 1.0000; Patents 1.0017; GDP Growth 1.0018.
- Digital pooled VIF: Internet 4.0387; Broadband 4.7626; ICT Exports 1.2308; Unemployment 1.0950; Inflation 1.2233; RnD 1.8268.
- Digital within-country VIF: Internet 3.4185; Broadband 3.8607; ICT Exports 1.5139; Unemployment 1.0863; Inflation 1.0302; RnD 1.3990.
- Digital pooled correlation Internet/Broadband r = 0.8645. High correlation is an interpretability caution, not grounds to automatically drop variables.

### Verify source anomalies, do not silently change data
- AI patents fell sharply from 2023 to 2024 in AUS (2024/2023=0.135), DNK (0.179), IND (0.182). Potential reporting lag/coding changes are *not verified*.
- AI investment includes five zeros, so log1p is required for logarithm-based specification.
- Digital growth minimum is -54.4021 percentage points, requiring source/outlier review.

### Outstanding
No Stata 18 runtime here. IPS, Hansen, AR1/AR2, Difference-in-Hansen, instrument count and estimated System GMM coefficients remain **unexecuted**. No p-values fabricated. Raw email source files remain private and are not committed to this public GitHub repository.
