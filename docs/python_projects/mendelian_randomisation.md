# Mendelian randomisaton (MR)

**Project status:** Active


## Roadmap
- [ ] **Theory**: Document the statistical foundations of Mendelian Randomization (MR), specifically focusing on estimators that use summary statistics from genome-wide association studies (GWAS).
- [ ] **Development**: Architect and implement a Python package for Inverse-Variance Weighted (IVW) estimation.
- [ ] **Automation**: Configure a CI/CD pipeline for automated testing and deployment to PyPI.

## Theory
Mendelian Randomization is a method that leverages genetic variants as instrumental variables (IV) to infer causal relationships between exposures and outcomes in observational data. The core principle of MR is based on Mendel's laws of inheritance, which suggest that alleles are randomly assorted during gamete formation, thus mimicking the randomization process in randomised controlled trials (RCTs). There are many reviews on MR, e.g., Lawlor et al. (2008), Davey Smith and Hemani (2014), Sanderson et al. (2022), to name a few. The following notes only cover the bascis to set the stage for implementation.

### Exposures
These are also referred to as modifiable exposures or risk factors. In the context MR, exposures are the variables that we are interested in studying for their potential causal effect on an outcome. It is essential that the exposure of interest is determined by genetic variants that can be used as IV. For example, if we are interested in studying the causal effect of body mass index (BMI) on cardiovascular disease, BMI would be the exposure.

### Outcomes
In MR, outcomes are typically health-related traits or diseases that may be influenced by the exposure. For example, if we are studying the causal effect of BMI on cardiovascular disease, cardiovascular disease would be the outcome.

### Comparison with Randomized Controlled Trials (RCTs)
MR shares some similarities with RCTs in that both methods aim to infer causal relationships between exposures and outcomes. However, unlike RCTs, which involve the random assignment of participants to treatment or control groups, MR relies on the natural random assortment of genetic variants. That is, the chance that an individual inherits a particular genetic variant is random and independent of confounding factors. Thus, if the genetic variant at a locus is associated with the exposure, and if the exposure is causally related to the outcome, then the genetic variant should also be associated with the outcome. As a concrete example, imagine a locus with alleles A and a, where allele A is associated with higher BMI, such that the average BMI of individuals with the AA genotype is higher than those with the Aa genotype, which in turn is higher than those with the aa genotype. If BMI is causally related to cardiovascular disease, then we would expect to see a similar pattern of association between the genotypes and the risk of cardiovascular disease. 

A significant advantage of MR over RCTs is that MR can be conducted using existing observational data, which is often more readily available and less expensive than conducting a new RCT. Additionally, MR can provide insights into the long-term effects of exposures, which may not be feasible in RCTs due to time constraints.

### Instrumental Variables (IV)
IVs are genetic variants that are associated with the exposure. This name comes from the statistical method of instrumental variable analysis.

### Mathematical principles of MR
Let $X$ be the exposure, $Y$ be the outcome. The question of interest is whether $X$ has a causal effect on $Y$. This can be represented using a directed acyclic graph (DAG) as follows:

```kroki-graphviz
digraph MR {
    rankdir=TB;
    node [shape=box, style="rounded,filled", fillcolor="#e8e8ff", fontname="Helvetica"];
    edge [fontname="Helvetica", fontsize=10];

    X [label="X (Exposure)"];
    Y [label="Y (Outcome)"];

    { rank=same; X; Y; }

    X -> Y [label="        "];
}
```

Establishing causality from $X$ to $Y$ is challenging. For instance, although it is easy to test whether $X$ and $Y$ are correlated, correlation does not imply causation. Another common issue is confounding, where a third variable $U$ influences both $X$ and $Y$, leading to a spurious association between $X$ and $Y$. An example of this is the relationship between smoking and lung cancer, where socioeconomic status could be a confounder. In this case, individuals with lower socioeconomic status may be more likely to smoke and also have a higher risk of lung cancer due to factors such as limited access to healthcare and increased exposure to environmental pollutants. This may in turn lead to higher rates of lung cancer among smokers, even if we were to assume smoking itself is not the direct cause of lung cancer (despite the fact that it is). This can be represented in a DAG as follows, where a question mark is used to indicate that the causal relationship between $X$ and $Y$ is uncertain:

```kroki-graphviz
digraph MR {
    rankdir=TB;
    node [shape=box, style="rounded,filled", fillcolor="#e8e8ff", fontname="Helvetica"];
    edge [fontname="Helvetica", fontsize=10];

    U [label="U (Confounder)"];
    X [label="X (Exposure)"];
    Y [label="Y (Outcome)"];

    { rank=same; X; Y; }

    U -> X [style=dashed];
    U -> Y [style=dashed];
    X -> Y [label="   ?    "];
}
```

The key idea of MR is to use genetic variants (G) as IVs. If G is associated with X, but has no direct effect on Y. Then, if we observe an association between G and Y, we can infer that X has a causal effect on Y. This can be represented in a DAG as follows:

```kroki-graphviz
digraph MR {
    rankdir=TB;
    node [shape=box, style="rounded,filled", fillcolor="#e8e8ff", fontname="Helvetica"];
    edge [fontname="Helvetica", fontsize=10];

    U [label="U (Confounder)"];
    G [label="G (Genetic variant as IV)"];
    X [label="X (Exposure)"];
    Y [label="Y (Outcome)"];

    { rank=same; G; X; Y; }

    U -> X [style=dashed];
    U -> Y [style=dashed];
    G -> X [label="        "];
    X -> Y [label="        "];
}
```

The confounder U is not a problem in this case because G is independent of U (due to the random assortment of alleles during reproduction). This is analogous to the randomization process in RCTs, where assignment to treatment or control groups is independent of confounding factors, and the outcome is only influenced by the treatment assignment. 


## Theory: The Inverse-Variance Weighted (IVW) Estimator Using GWAS Summary Statistics





!!! note "References"
Davey Smith, G. and Hemani, G., 2014. Mendelian randomization: genetic anchors for causal inference in epidemiological studies. Human molecular genetics, 23(R1), pp.R89-R98.

Lawlor, D.A., Harbord, R.M., Sterne, J.A., Timpson, N. and Davey Smith, G., 2008. Mendelian randomization: using genes as instruments for making causal inferences in epidemiology. Statistics in medicine, 27(8), pp.1133-1163.

Sanderson, E., Glymour, M.M., Holmes, M.V., Kang, H., Morrison, J., Munafò, M.R., Palmer, T., Schooling, C.M., Wallace, C., Zhao, Q. and Davey Smith, G., 2022. Mendelian randomization. Nature reviews Methods primers, 2(1), p.6.