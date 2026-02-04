# Mendelian randomisaton (MR)

**Project status:** Active


## Roadmap
- [ ] **Theory**: Document the statistical foundations of Mendelian Randomization (MR), specifically focusing on summary-data genome-wide association studies (GWAS) frameworks.
- [ ] **Development**: Architect and implement a Python package for Inverse-Variance Weighted (IVW) estimation.
- [ ] **Automation**: Configure a CI/CD pipeline for automated testing and deployment to PyPI.

## Theory
Mendelian Randomization (MR) is a method that leverages genetic variants as instrumental variables to infer causal relationships between exposures and outcomes in observational data. The core principle of MR is based on Mendel's laws of inheritance, which suggest that alleles are randomly assorted during gamete formation, thus mimicking the randomization process in randomised controlled trials. There are many reviews on MR, e.g., Lawlor et al. (2008), Davey Smith and Hemani (2014), Sanderson et al. (2022), to name a few. The following notes only cover the bascis to set the stage for implementation.

### Exposures
These are also referred to as modifiable exposures or risk factors. 


!!! note "References"
Davey Smith, G. and Hemani, G., 2014. Mendelian randomization: genetic anchors for causal inference in epidemiological studies. Human molecular genetics, 23(R1), pp.R89-R98.

Lawlor, D.A., Harbord, R.M., Sterne, J.A., Timpson, N. and Davey Smith, G., 2008. Mendelian randomization: using genes as instruments for making causal inferences in epidemiology. Statistics in medicine, 27(8), pp.1133-1163.

Sanderson, E., Glymour, M.M., Holmes, M.V., Kang, H., Morrison, J., Munafò, M.R., Palmer, T., Schooling, C.M., Wallace, C., Zhao, Q. and Davey Smith, G., 2022. Mendelian randomization. Nature reviews Methods primers, 2(1), p.6.