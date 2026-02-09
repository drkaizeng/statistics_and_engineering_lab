# Mendelian randomisaton (MR)

**Project status:** Active


## Roadmap
- [ ] **Theory**: Document the statistical foundations of Mendelian Randomization (MR), specifically focusing on estimators that use summary statistics from genome-wide association studies (GWAS).
- [ ] **Development**: Architect and implement a Python package for Inverse-Variance Weighted (IVW) estimation.
- [ ] **Automation**: Configure a CI/CD pipeline for automated testing and deployment to PyPI.

## Theory: General overview of Mendelian Randomization (MR)
Mendelian Randomization (MR) is a method that leverages genetic variants as instrumental variables (IV) to infer causal relationships between exposures and outcomes in observational data. The core principle of MR is based on Mendel's laws of inheritance, which suggest that alleles are randomly assorted during gamete formation, thus mimicking the randomization process in randomised controlled trials (RCTs). There are many reviews on MR, e.g., Lawlor et al. (2008), Davey Smith and Hemani (2014), Sanderson et al. (2022), to name a few. The following notes only cover the bascis to set the stage for implementation.

### Exposures
These are also referred to as modifiable exposures or risk factors. In the context MR, exposures are the variables that we are interested in studying for their potential causal effect on an outcome. It is essential that the exposure of interest is determined by genetic variants that can be used as instrumental variables (IV). For example, if we are interested in studying the causal effect of body mass index (BMI) on cardiovascular disease, BMI would be the exposure.

### Outcomes
In MR, outcomes are typically health-related traits or diseases that may be influenced by the exposure. For example, if we are studying the causal effect of BMI on cardiovascular disease, cardiovascular disease would be the outcome.

### Comparison with Randomized Controlled Trials (RCTs)
Mendelian Randomization (MR) shares some similarities with RCTs in that both methods aim to infer causal relationships between exposures and outcomes. However, unlike RCTs, which involve the random assignment of participants to treatment or control groups, MR relies on the natural random assortment of genetic variants. That is, the chance that an individual inherits a particular genetic variant is random and independent of confounding factors. Thus, if the genetic variant at a locus is associated with the exposure, and if the exposure is causally related to the outcome, then the genetic variant should also be associated with the outcome. As a concrete example, image a locus with alleles A and a, where allele A is associated with higher BMI, such that the average BMI of individuals with the AA genotype is higher than those with the Aa genotype, which in turn is higher than those with the aa genotype. If BMI is causally related to cardiovascular disease, then we would expect to see a similar pattern of association between the genotypes and the risk of cardiovascular disease. 

A significant advantage of MR over RCTs is that MR can be conducted using existing observational data, which is often more readily available and less expensive than conducting a new RCT. Additionally, MR can provide insights into the long-term effects of exposures, which may not be feasible in RCTs due to time constraints.

### Instrumental Variables (IV)
Instrumental variables are genetic variants that are associated with the exposure. This name comes from the statistical method of instrumental variable analysis.

### Assumptions of MR

### Example violation of MR assumptions


## Theory: The Inverse-Variance Weighted (IVW) Estimator Using GWAS Summary Statistics





!!! note "References"
Davey Smith, G. and Hemani, G., 2014. Mendelian randomization: genetic anchors for causal inference in epidemiological studies. Human molecular genetics, 23(R1), pp.R89-R98.

Lawlor, D.A., Harbord, R.M., Sterne, J.A., Timpson, N. and Davey Smith, G., 2008. Mendelian randomization: using genes as instruments for making causal inferences in epidemiology. Statistics in medicine, 27(8), pp.1133-1163.

Sanderson, E., Glymour, M.M., Holmes, M.V., Kang, H., Morrison, J., Munafò, M.R., Palmer, T., Schooling, C.M., Wallace, C., Zhao, Q. and Davey Smith, G., 2022. Mendelian randomization. Nature reviews Methods primers, 2(1), p.6.