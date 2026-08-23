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
- [] **Automation**: Configure a CI/CD pipeline for automated testing and deployment to PyPI.


## Theory
The goal of this section is to understand the SuSiE model (Wang et al., 2020) and its extension, SuSiE-RSS (Zou et al., 2022). Formulas from the original papers are reproduced, and where necessary, derivations are provided.

### The model
Let $\mathbf{y}$ be an $n$-vector of mean-centred phenotypes, and let $\mathbf{X}$ be an $n \times p$ matrix of mean-centered genotypes, where $n$ is the number of individuals and $p$ is the number of variants. The following linear model is assumed, with the mean-centring ensuring the intercept is zero:

$$
\begin{equation}
\label{eq:standard_linear_model}
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
Instead of attempting to finding causal variants using \eqref{eq:standard_linear_model} directly, a more tractable alternative where the regression coefficients $\mathbf{b}$ are expressed as a sum of single-effect vectors is used:

$$
\begin{equation}
\mathbf{b} = \sum_{l=1}^{L} \mathbf{b}_l
\end{equation}
$$

where $L$ is a user-supplied hyper-parameter that specifies the maximum number of causal variants, and $\mathbf{b}^{(l)}$ is a $p$-vector of regression coefficients in which exactly one element is non-zero. Thus, the target model becomes

$$
\begin{align}
\mathbf{y} &= \sum_{l=1}^{L} \mathbf{X}\mathbf{b}_l + \mathbf{e} \label{eq:susie_model_start} \\
\mathbf{e} &\sim N_n(0, \sigma^2 I_n) \\
\mathbf{b}_l &= \vec{\gamma}_l b_l \\
\vec{\gamma}_l &\sim \text{Multinomial}(1, \vec{\pi}) \\
b_l &\sim N_1(0, \sigma_{0l}^2) \label{eq:susie_model_end}
\end{align}
$$

Thus, $\vec{\gamma}_l$ is a $p$-vector of indicator variables that specifies which variant is causal for the $l$-th single-effect, $\vec{\pi}$ is a $p$-vector of prior probabilities for each variant being causal, and $\sigma_{0l}^2 > 0$ is the prior variance of the non-zero regression coefficients.

Put together, the SuSiE model has the following hierarchical structure:

- Hyper (user-supplied) parameters: $L$, $\sigma^2$, $\vec{\pi}$, $\vec{\sigma}_0^2 = (\sigma_{01}^2, \ldots, \sigma_{0L}^2)$
- Latent variables: $\mathbf{b}^{(1)}, \ldots, \mathbf{b}^{(L)}$

When $L \ll p$, the SuSiE model is approximately equal to the model \eqref{eq:standard_linear_model} in which $L$ randomly-chosen variables have non-zero effects. It should nonetheless be noted that the two models are different. In particular, there is nothing in the SuSiE model that prevents two or more of the $\mathbf{b}^{(l)}$ vectors from having non-zero elements in the same position, although this is unlikely to occur in practice.

### Inferences using the SuSiE model

#### Single-effect regression (SER) model
The first step towards understanding how to make inferences using the SuSiE model is to derive properties of its constituents, the single-effect regression (SER) model, which can be obtained by setting $L = 1$ in \eqref{eq:susie_model_start} - \eqref{eq:susie_model_end}. The subscript $l$ is dropped for clarity.

The first quantity of interest is the posterior probability that variant $j$ is causal: 

$$
\begin{align}
\alpha_j &:= \Pr(\gamma_j = 1 | \mathbf{y}, \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi}) \\
&= \frac{\Pr(\gamma_j = 1, \mathbf{y} | \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi})}{\Pr(\mathbf{y} | \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi})}  \\
&= \frac{\Pr(\gamma_j = 1 | \sigma^2, \sigma_0^2, \vec{\pi}) \Pr(\mathbf{y} | \mathbf{X}, \gamma_j = 1, \sigma^2, \sigma_0^2, \vec{\pi}) }{\sum_{j'=1}^{p} \Pr(\gamma_{j'} = 1 | \sigma^2, \sigma_0^2, \vec{\pi}) \Pr(\mathbf{y} | \gamma_{j'} = 1, \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi}) } \\
&= \frac{\pi_j \Pr(\mathbf{y} | \gamma_j = 1, \mathbf{X}, \sigma^2, \sigma_0^2)}{\sum_{j'=1}^{p} \pi_{j'} \Pr(\mathbf{y} | \gamma_{j'} = 1, \mathbf{X}, \sigma^2, \sigma_0^2)}
\end{align}
$$

To finish the derivation, we note that, given $\gamma_j = 1$, only the $j$-th variant has a non-zero effect, and only the $j$-th column of $\mathbf{X}$, denoted by $\mathbf{x}_j$, is relevant. Thus, we can write

$$
\begin{align}
\Pr(\mathbf{y} | \gamma_j = 1, \mathbf{X}, \sigma^2, \sigma_0^2) &= \Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, \sigma_0^2) \\
&= \frac{\Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, \sigma_0^2)}{\Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, b_j = 0)} \Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, b_j = 0)
\end{align}
$$



!!! note "References"

    Wang, G., Sarkar, A., Carbonetto, P. and Stephens, M., 2020. A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society Series B: Statistical Methodology, 82(5), pp.1273-1300.

    Zou, Y., Carbonetto, P., Wang, G. and Stephens, M., 2022. Fine-mapping from summary data with the “Sum of Single Effects” model. PLoS genetics, 18(7), p.e1010299.