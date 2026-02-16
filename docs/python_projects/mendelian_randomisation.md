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

For simplicity, assume that both $X$ and $Y$ are quantitative traits and can be modelled using standard linear models:
$$
X = \alpha + \beta_{GX} G + \epsilon_X \\
Y = \gamma^* + \beta_{XY} X + \epsilon_Y^*
$$
where $\alpha$ and $\gamma^*$ are intercepts, $\beta_{GX}$ is the effect of the genetic variant on the exposure, $\beta_{XY}$ is the causal effect of the exposure on the outcome, and $\epsilon_X$ and $\epsilon_Y^*$ are error terms, where $E(\epsilon_X) = E(\epsilon_Y^*) = 0$.

Because $G$ has no direct effect on $Y$ (i.e., it only affects $Y$ through $X$), we can derive the following relationship:

$$
\begin{aligned}
Y &= \gamma^* + \beta_{XY} (\alpha + \beta_{GX} G + \epsilon_X) + \epsilon_Y^* \\
&= \gamma^* + \beta_{XY} \alpha + \beta_{XY} \beta_{GX} G + \beta_{XY} \epsilon_X + \epsilon_Y^*
\end{aligned}
$$

Defining $\gamma = \gamma^* + \beta_{XY} \alpha$, $\epsilon_Y = \beta_{XY} \epsilon_X + \epsilon_Y^*$, and $\beta_{GY} = \beta_{XY} \beta_{GX}$, we can rewrite the equation for $Y$ as:

$$
Y = \gamma + \beta_{GY} G + \epsilon_Y
$$

Thus, if we have estimates $\widehat{\beta}_{GX}$ and $\widehat{\beta}_{GY}$, we can estimate the causal effect $\beta_{XY}$ as
$$
\widehat{\beta}_{XY} = \frac{\widehat{\beta}_{GY}}{\widehat{\beta}_{GX}}
$$

Genome-wide association studies (GWAS) allow for the quantification of associations between a genetic variant and traits $X$ and $Y$, yielding the estimates $\widehat{\beta}_{GX}$ and $\widehat{\beta}_{GY}$. When data from multiple unlinked genetic variants are available, the above equation suggests that the data points $(\widehat{\beta}_{GX}^{(1)}, \widehat{\beta}_{GY}^{(1)})$, $(\widehat{\beta}_{GX}^{(2)}, \widehat{\beta}_{GY}^{(2)})$, ..., $(\widehat{\beta}_{GX}^{(n)}, \widehat{\beta}_{GY}^{(L)})$ should lie on a line with slope $\widehat{\beta}_{XY}$, where the superscript denotes the index of the genetic variant. This means that, with GWAS summary statistics widely available, we can combine data from multiple variants from multiple GWASs to obtain a more precise estimate of $\widehat{\beta}_{XY}$, so long as these different studies are from comparable populations, such that if we were able to test for association between the genetic variants and the traits of interest across all these studies, the causal effect estimates are the same across the studies (bar differences caused by differences in sample sizes). One common method for combining multiple estimates this is the Inverse-Variance Weighted (IVW) estimator, detailed below.

#### The Inverse-Variance Weighted (IVW) estimator
The causal effect estimates obtained from different genetic variants vary in precision due to differences in sample sizes and allele frequencies. The IVW estimator is a method for combining these estimates that gives more weight to those with higher precision (i.e., lower variance). Let $\sigma_{GX}^{(i)}$ and $\sigma_{GY}^{(i)}$ be the standard errors of $\widehat{\beta}_{GX}^{(i)}$ and $\widehat{\beta}_{GY}^{(i)}$, respectively. For notational clarity, we will drop the superscript $(i)$ in the following. The variance of the ratio estimator $\widehat{\beta}_{XY} = \widehat{\beta}_{GY} / \widehat{\beta}_{GX}$ can be approximated using the delta method as follows:

$$
\begin{aligned}
\text{Var}(\widehat{\beta}_{XY})
&\approx \frac{\sigma_{GY}^2}{\widehat{\beta}_{GX}^2} + \frac{\widehat{\beta}_{GY}^2 \sigma_{GX}^2}{\widehat{\beta}_{GX}^4} - 2 \frac{\widehat{\beta}_{GY} \text{Cov}(\widehat{\beta}_{GX}, \widehat{\beta}_{GY})}{\widehat{\beta}_{GX}^3}
\end{aligned}
$$

When the estimates $\widehat{\beta}_{GX}$ and $\widehat{\beta}_{GY}$ are obtained from independent samples, the covariance term is zero. Further, the estimate $\widehat{\beta}_{GX}$ is often much more precise than $\widehat{\beta}_{GY}$ (i.e., $\sigma_{GX}^2$ is much smaller than $\sigma_{GY}^2$). When these two conditions hold, we have

$$
\text{Var}(\widehat{\beta}_{XY}) \approx \frac{\sigma_{GY}^2}{\widehat{\beta}_{GX}^2}
$$

Weighting each estimate $\widehat{\beta}_{XY}^{(i)}$ by the inverse of its variance, we can obtain the IVW estimator as follows (Burgess et al., 2013):

$$
\widehat{\beta}_{XY}^{(\text{IVW})} = \frac{\sum_{i=1}^L \widehat{\beta}_{GX}^{(i)} \widehat{\beta}_{GY}^{(i)} / \sigma_{GY}^{(i)2}}{\sum_{i=1}^L \widehat{\beta}_{GX}^{(i)2} / \sigma_{GY}^{(i)2}}
$$

where $L$ is the number of genetic variants used as IVs. The variance of the IVW estimator can be estimated as follows:
$$
\text{Var}(\widehat{\beta}_{XY}^{(\text{IVW})}) = \frac{1}{\sum_{i=1}^L \widehat{\beta}_{GX}^{(i)2} / \sigma_{GY}^{(i)2}}
$$

Let $z = \widehat{\beta}_{XY}^{(\text{IVW})} / \sqrt{\text{Var}(\widehat{\beta}_{XY}^{(\text{IVW})})}$ be the test statistic for testing the null hypothesis that $X$ has no causal effect on $Y$ (i.e., $\beta_{XY} = 0$). Under the null hypothesis, $z^2$ follows a chi-squared distribution with 1 degree of freedom, which can be used to obtain a p-value for the test.




!!! note "References"

Burgess, S., Butterworth, A. and Thompson, S.G., 2013. Mendelian randomization analysis with multiple genetic variants using summarized data. Genetic epidemiology, 37(7), pp.658-665.

Davey Smith, G. and Hemani, G., 2014. Mendelian randomization: genetic anchors for causal inference in epidemiological studies. Human molecular genetics, 23(R1), pp.R89-R98.

Lawlor, D.A., Harbord, R.M., Sterne, J.A., Timpson, N. and Davey Smith, G., 2008. Mendelian randomization: using genes as instruments for making causal inferences in epidemiology. Statistics in medicine, 27(8), pp.1133-1163.

Sanderson, E., Glymour, M.M., Holmes, M.V., Kang, H., Morrison, J., Munafò, M.R., Palmer, T., Schooling, C.M., Wallace, C., Zhao, Q. and Davey Smith, G., 2022. Mendelian randomization. Nature reviews Methods primers, 2(1), p.6.