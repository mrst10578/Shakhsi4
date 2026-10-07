version 18.0
clear all
set more off
* Source workbook is private; this do-file belongs only to Shakhsi4.
capture mkdir results
capture log close _all
log using "results/digital_stata.log", text replace
capture confirm file "data/Balanced_Panel_Data.xlsx"
if _rc {
 display as error "Place Balanced_Panel_Data.xlsx inside data/ first."
 log close
 exit 601
}
import excel using "data/Balanced_Panel_Data.xlsx", firstrow clear
isid ISO3 Year
assert inrange(Year,2005,2022)
assert Productivity>0
encode ISO3, gen(country_id)
xtset country_id Year
xtdescribe
misstable summarize
gen double ln_productivity = ln(Productivity)
foreach x in Growth ln_productivity Internet Broadband ICT_Exports Unemployment Inflation RnD {
 display as text "Panel IPS unit-root test: `x'"
 capture noisily xtunitroot ips `x', lags(1)
 if _rc display as error "IPS unavailable for `x'; no inference."
}
pwcorr Internet Broadband ICT_Exports Unemployment Inflation RnD, sig
regress Growth Internet Broadband ICT_Exports Unemployment Inflation RnD i.Year
estat vif
regress ln_productivity Internet Broadband ICT_Exports Unemployment Inflation RnD i.Year
estat vif
* Benchmarks; FE lagged dependent model may be biased.
xtreg Growth L.Growth Internet Broadband ICT_Exports Unemployment Inflation RnD i.Year, fe vce(cluster country_id)
xtreg ln_productivity L.ln_productivity Internet Broadband ICT_Exports Unemployment Inflation RnD i.Year, fe vce(cluster country_id)
capture which xtabond2
if _rc {
 display as error "Install xtabond2 inside Stata: ssc install xtabond2"
 log close
 exit 499
}
tab Year, gen(yr_)
drop yr_1
unab year_dummies: yr_*
* T=18 vs N=47: high instrument proliferation risk with 17 year dummies.
foreach y in Growth ln_productivity {
 display as result "EXPERIMENTAL System GMM: `y'"
 capture noisily xtabond2 `y' L.`y' Internet Broadband ICT_Exports Unemployment Inflation RnD `year_dummies', ///
    gmmstyle(L.`y' Internet Broadband ICT_Exports, lag(1 1) collapse) ///
    ivstyle(Unemployment Inflation RnD `year_dummies', equation(both)) ///
    twostep robust small
 if _rc display as error "GMM failed: no validated estimate for `y'."
 else display as error "NOT VALIDATED: check instrument count vs 47 groups, Hansen, AR(1), AR(2), difference-in-Hansen and sensitivity."
}
log close
