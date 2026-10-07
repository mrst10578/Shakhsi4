version 18.0
clear all
set more off
* Source workbook is private; this do-file belongs only to Shakhsi4.
capture mkdir results
capture log close _all
log using "results/ai_stata.log", text replace
capture confirm file "data/AI_Balanced_Panel (1).xlsx"
if _rc {
 display as error "Place AI_Balanced_Panel (1).xlsx inside data/ first."
 log close
 exit 601
}
import excel using "data/AI_Balanced_Panel (1).xlsx", firstrow clear
isid ISO3 Year
assert inrange(Year,2016,2024)
assert AI_Investment>=0 & AI_Patents>=0
encode ISO3, gen(country_id)
xtset country_id Year
xtdescribe
misstable summarize
gen double ln_ai_inv = ln(1+AI_Investment)
gen double ln_ai_pat = ln(1+AI_Patents)
foreach x in HighTech_Exports Unemployment ln_ai_inv ln_ai_pat GDP_Growth {
 display as text "Panel IPS unit-root test, low power T=9: `x'"
 capture noisily xtunitroot ips `x', lags(1)
 if _rc display as error "IPS unavailable for `x': no test inference."
}
pwcorr ln_ai_inv ln_ai_pat GDP_Growth, sig
regress HighTech_Exports ln_ai_inv ln_ai_pat GDP_Growth i.Year
estat vif
regress Unemployment ln_ai_inv ln_ai_pat GDP_Growth i.Year
estat vif
* FE with L.y is only a potentially Nickell-biased benchmark.
xtreg HighTech_Exports L.HighTech_Exports ln_ai_inv ln_ai_pat GDP_Growth i.Year, fe vce(cluster country_id)
xtreg Unemployment L.Unemployment ln_ai_inv ln_ai_pat GDP_Growth i.Year, fe vce(cluster country_id)
capture which xtabond2
if _rc {
 display as error "Install xtabond2 inside Stata: ssc install xtabond2"
 log close
 exit 499
}
tab Year, gen(yr_)
drop yr_1
unab year_dummies: yr_*
foreach y in HighTech_Exports Unemployment {
 display as result "System GMM equation: `y'"
 capture noisily xtabond2 `y' L.`y' ln_ai_inv ln_ai_pat GDP_Growth `year_dummies', ///
    gmmstyle(L.`y' ln_ai_inv ln_ai_pat, lag(1 2) collapse) ///
    ivstyle(GDP_Growth `year_dummies', equation(both)) ///
    twostep robust small
 if _rc display as error "GMM failed for `y'; do not present any results."
 else display as text "MANDATORY AUDIT: Hansen, AR(1), AR(2), instruments/groups and available difference-in-Hansen."
}
log close
