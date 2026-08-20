# Fine-mapping with SuSiE

**Project status:** Active

## Roadmap
- [] **Theory**:
  - [] Learn the variational empirical Bayes approach by deriving the SuSiE model.
  - [] Understand the SuSiE-RSS model for fine-mapping with summary statistics.
- [] **Implementation**: Implement the SuSiE-RSS model in Python.
- [] **Simulation**:
  - [] Simulate data to test the SuSiE-RSS model.
  - [] Understand the cause of some commonly observed issues with the SuSiE-RSS model, such as non-significant variants being assigned high PIPs, highly correlated variants being assigned high PIPs, and the model failing to converge.
- [x] **Automation**: Configure a CI/CD pipeline for automated testing and deployment to PyPI.


## Theory
The goal of this section is to understand the SuSiE model (Wang et al., 2020) and its extension, SuSiE-RSS (Zou et al., 2022). Formulas from the original papers are reproduced, and where necessary, derivations are provided.

### The model
Let $\mathbf{y}$ be an $n$-vector of mean-centred phenotypes, and let $\mathbf{X}$ be an $n \times p$ matrix of mean-centered genotypes, where $n$ is the number of individuals and $p$ is the number of variants. The following linear model is assumed, with the mean-centring ensuring the intercept is zero:

$$
\begin{equation}
\mathbf{y} = \mathbf{X}\mathbf{b} + \mathbf{e}
\end{equation}
$$

where $\mathbf{b}$ is a $p$-vector of regression coefficients, and $\mathbf{e} \sim N_n(0, \sigma^2 I_n)$ is an $n$ vector of error terms, $\sigma^2 > 0$ is the residual variance, $I_n$ is the $n \times n$ identity matrix.

The goal of fine-mapping is to identify the non-zero elements of $\mathbf{b}$, which correspond to the causal variants. Two frequently-used concepts in this context are the posterior inclusion probability (PIP) and credible sets. The PIP for variant $j$ is defined as

$$
\begin{equation}
\text{PIP} = \Pr(b_j \neq 0 | \mathbf{y}, \mathbf{X})
\end{equation}
$$

A level-$\rho$ credible set is defined as a set of variants that contains at least one causal variant with probability $\rho$ or greater. 

### The sum of single-effects (SuSiE) regression model
Instead of attempting to finding causal variants using (1) directly, 

!!! note "References"

    Wang, G., Sarkar, A., Carbonetto, P. and Stephens, M., 2020. A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society Series B: Statistical Methodology, 82(5), pp.1273-1300.

    Zou, Y., Carbonetto, P., Wang, G. and Stephens, M., 2022. Fine-mapping from summary data with the “Sum of Single Effects” model. PLoS genetics, 18(7), p.e1010299.