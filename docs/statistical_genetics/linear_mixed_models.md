# Linear mixed models (LMMs)

**Project status:** Active

## The standard infinitesimal model with additive effects
Consider a sample of $N$ individuals, each of whom has been genotyped at $M$ sites. Assume that the each site has two alleles arbitrarily labeled 0 and 1. Let $\mathbf{G}^*$ represent the $N \times M$ genotype matrix, where $G^*_{ij}$ is the genotype of individual $i$ at site $j$, coded as the number of copies of allele 1 (i.e., 0, 1, or 2). The samples have been measured for a trait of interest, as well as $C$ covariates. We use $\mathbf{y}$ to represent the $N \times 1$ vector of phenotypes, $\mathbf{X}$ to represent the $N \times C$ matrix of covariates (including an intercept), and assume that $\mathbf{X}$ is full rank. We are interested in the following linear mixed model (LMM):

$$
\begin{equation}
\label{eq:lmm}
\mathbf{y} = \mathbf{X}\boldsymbol{\alpha} + \mathbf{G}\boldsymbol{\beta} + \boldsymbol{\epsilon}
\end{equation}
$$

where $\mathbf{G}$ is a standardised version of $\mathbf{G}^*$ with mean 0 and variance 1 for each column, $\boldsymbol{\alpha}$ is a $C \times 1$ vector of fixed effects, $\boldsymbol{\beta}$ is a $M \times 1$ vector of random effects with $\boldsymbol{\beta} \sim \mathcal{N}(\mathbf{0}, \sigma_g^2\mathbf{I}_M)$, and $\boldsymbol{\epsilon}$ is a $N \times 1$ vector of residuals with $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \sigma_e^2\mathbf{I}_N)$. The symbol $\mathbf{I}_X$ represents the $X \times X$ identity matrix.

In a fixed effect model where $\boldsymbol{\beta}$ in \eqref{eq:lmm} is treated as a fixed effect, which leads to $M$ parameters to be estimated. When $M$ is large, the number of parameters can exceed the number of samples, leading to overfitting. The LMM addresses this issue by assuming that the effects of the $M$ sites share a common distribution thereby reducing the number of parameters from $M$ to 1 (i.e., $\sigma_g^2$).

### Covariance and heritability
Let $i$ and $j$ index two individuals, corresponding to rows in the vectors and matrices defined in \eqref{eq:lmm}. Because $\mathbf{X}_i \boldsymbol{\alpha}$ and $\mathbf{X}_j \boldsymbol{\alpha}$ are fixed constants, they do not contribute to the covariance. The covariance between their phenotypes can be expressed as:

$$
\begin{align}
\label{eq:cov}
\text{Cov}(y_i, y_j) &= \text{Cov}(\mathbf{G}_i \boldsymbol{\beta} + \epsilon_i, \mathbf{G}_j \boldsymbol{\beta} + \epsilon_j) \nonumber \\
&= \text{Cov}(\mathbf{G}_i\boldsymbol{\beta}, \mathbf{G}_j\boldsymbol{\beta}) \nonumber \\
&= \text{Cov}\left(\sum_{k=1}^M G_{ik} \beta_k, \sum_{l=1}^M G_{jl} \beta_l\right) \nonumber \\
&= \sum_{k=1}^M \sum_{l=1}^M G_{ik} G_{jl} \text{Cov}(\beta_k, \beta_l) \nonumber \\
&= \sigma_g^2 \sum_{k=1}^M G_{ik} G_{jk}  \\
\end{align}
$$

The second term in \eqref{eq:cov} is proportional to element $ij$ of the genetic relationship matrix (GRM) $\mathbf{K} = \mathbf{G}\mathbf{G}^T / M$. 

