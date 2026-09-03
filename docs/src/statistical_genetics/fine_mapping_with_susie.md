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
b_l &\sim N_1(0, \sigma_{0,l}^2) \label{eq:susie_model_end}
\end{align}
$$

Thus, $\vec{\gamma}_l$ is a $p$-vector of indicator variables that specifies which variant is causal for the $l$-th single-effect, $\vec{\pi}$ is a $p$-vector of prior probabilities for each variant being causal, and $\sigma_{0,l}^2 > 0$ is the prior variance of the non-zero regression coefficients.

Put together, the SuSiE model has the following hierarchical structure:

- Hyper (user-supplied) parameters: $L$, $\sigma^2$, $\vec{\pi}$, $\vec{\sigma}_0^2 = (\sigma_{0,1}^2, \ldots, \sigma_{0,L}^2)$
- Latent variables: $\mathbf{b}_1, \ldots, \mathbf{b}_L$

When $L \ll p$, the SuSiE model is approximately equal to the model \eqref{eq:standard_linear_model} in which $L$ randomly-chosen variables have non-zero effects. It should nonetheless be noted that the two models are different. In particular, there is nothing in the SuSiE model that prevents two or more of the $\mathbf{b}^{(l)}$ vectors from having non-zero elements in the same position, although this is unlikely to occur in practice.

### Inferences using the SuSiE model

#### Single-effect regression (SER) model
The first step towards understanding how to make inferences using the SuSiE model is to derive properties of its constituents, the single-effect regression (SER) model, which can be obtained by setting $L = 1$ in \eqref{eq:susie_model_start} - \eqref{eq:susie_model_end}. In other words, the SER model assumes that exactly one variant has a non-zero effect.

The first quantity of interest is the posterior probability that variant $j$ is causal (the subscript $l$ is dropped for clarity): 

$$
\begin{align}
\alpha_j &:= \Pr(\gamma_j = 1 | \mathbf{y}, \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi}) \\
&= \frac{\Pr(\gamma_j = 1, \mathbf{y} | \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi})}{\Pr(\mathbf{y} | \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi})}  \\
&= \frac{\Pr(\gamma_j = 1 | \sigma^2, \sigma_0^2, \vec{\pi}) \Pr(\mathbf{y} | \mathbf{X}, \gamma_j = 1, \sigma^2, \sigma_0^2, \vec{\pi}) }{\sum_{j'=1}^{p} \Pr(\gamma_{j'} = 1 | \sigma^2, \sigma_0^2, \vec{\pi}) \Pr(\mathbf{y} | \gamma_{j'} = 1, \mathbf{X}, \sigma^2, \sigma_0^2, \vec{\pi}) } \\
&= \frac{\pi_j \Pr(\mathbf{y} | \gamma_j = 1, \mathbf{X}, \sigma^2, \sigma_0^2)}{\sum_{j'=1}^{p} \pi_{j'} \Pr(\mathbf{y} | \gamma_{j'} = 1, \mathbf{X}, \sigma^2, \sigma_0^2)}
\end{align}
$$

Note that, given $\gamma_j = 1$, only the $j$-th variant has a non-zero effect. Therefore, the phenotypes $\mathbf{y}$ depends solely on the $j$-th column of $\mathbf{X}$, denoted by $\mathbf{x}_j$:

$$
\begin{align}
\Pr(\mathbf{y} | \gamma_j = 1, \mathbf{X}, \sigma^2, \sigma_0^2) &= \Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, \sigma_0^2) \\
&= \frac{\Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, \sigma_0^2)}{\Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, b_j = 0)} \Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, b_j = 0)
\end{align}
$$

The first term in the last equation is the Bayes factor (BF) and can be calculated in the same manner as described in Wakefield (2009) but using the specific residual variance $\sigma^2$ and prior variance $\sigma_0^2$:

$$
\begin{align} 
\label{eq:ser_bf}
\text{BF}_j := \frac{\Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, \sigma_0^2)}{\Pr(\mathbf{y} | \mathbf{x}_j, \sigma^2, b_j = 0)}
= \sqrt{\frac{s^2}{s_j^2 + \sigma_0^2}} \exp\bigg(
\frac{z_j^2}{2} \frac{\sigma_0^2}{s_j^2 + \sigma_0^2}
\bigg)
\end{align}
$$

where 

$$
\begin{align}
s_j^2 &= \frac{\sigma^2}{\mathbf{x}_j^T \mathbf{x}_j} \\
\hat{b}_j &= (\mathbf{x}_j^T \mathbf{x}_j)^{-1} \mathbf{x}_j^T \mathbf{y} \\
z_j &= \frac{\hat{b}_j}{s_j}
\end{align}
$$

We can now calculate the posterior probability $\alpha_j$ as:

$$
\begin{align}
\alpha_j &= \frac{\pi_j \text{BF}_j}{\sum_{j'=1}^{p} \pi_{j'} \text{BF}_{j'}}
\end{align}
$$

which is in the same form as the result derived by Maller et al. (2012). Given that the $j$-th variant is causal, the posterior distribution of the causal effect size $b$ is given by

$$
\begin{align}
b | \mathbf{y}, \gamma_j = 1, \mathbf{X}, \sigma^2, \sigma_0^2 \sim N_1(\mu_1, \sigma_1^2)
\end{align}
$$

where

$$
\begin{align}
\sigma_1^2 &= \left(\frac{1}{s_j^2} + \frac{1}{\sigma_0^2}\right)^{-1} \\
\mu_1 &= \sigma_1^2 \frac{\hat{b}_j}{s_j^2}
\end{align}
$$

As in the original paper, we write

$$
\begin{align}
\text{SER}(\mathbf{X}, \mathbf{y}; \sigma^2, \sigma_0^2) := (\vec{\alpha}, \vec{\mu}_1, \vec{\sigma}_1^2)
\end{align}
$$

where $\vec{\alpha} = (\alpha_1, \ldots, \alpha_p)$, $\vec{\mu}_1 = (\mu_{1,1}, \ldots, \mu_{1,p})$, and $\vec{\sigma}_1^2 = (\sigma_{1,1}^2, \ldots, \sigma_{1,p}^2)$.


#### The iterative Bayesian stepwise selection (IBSS) algorithm

```python
def ibss(X: np.ndarray, y: np.ndarray, pi: np.ndarray, sigma_sq: float, L: int, sigma0_sq: np.ndarray):
    """Python-like pseudocode for the IBSS algorithm

    Parameters
    ----------
    X : numpy.ndarray
        An n-by-p matrix of mean-centred genotypes where n is the number of individuals and p is the number of variants.
    y : numpy.ndarray
        An n-vector of mean-centred phenotypes
    pi : numpy.ndarray
        A p-vector of prior probabilities for each variant being causal. The elements must be non-negative and sum up to 1.
    sigma_sq : float
        The residual variance.
    L : int
        The maximum number of causal variants.
    sigma0_sq : np.ndarray
        A L-vector of prior variances for the effect sizes of each of the L causal variants.

    Returns
    -------
    """

```



!!! note "References"

    Maller, J.B., McVean, G., Byrnes, J., Vukcevic, D., Palin, K., Su, Z., Howson, J.M., Auton, A., Myers, S., Morris, A. and Pirinen, M., 2012. Bayesian refinement of association signals for 14 loci in 3 common diseases. Nature genetics, 44(12), pp.1294-1301.

    Wakefield, J., 2009. Bayes factors for genome‐wide association studies: comparison with P‐values. Genetic Epidemiology: The Official Publication of the International Genetic Epidemiology Society, 33(1), pp.79-86.

    Wang, G., Sarkar, A., Carbonetto, P. and Stephens, M., 2020. A simple new approach to variable selection in regression, with application to genetic fine mapping. Journal of the Royal Statistical Society Series B: Statistical Methodology, 82(5), pp.1273-1300.

    Zou, Y., Carbonetto, P., Wang, G. and Stephens, M., 2022. Fine-mapping from summary data with the “Sum of Single Effects” model. PLoS genetics, 18(7), p.e1010299.