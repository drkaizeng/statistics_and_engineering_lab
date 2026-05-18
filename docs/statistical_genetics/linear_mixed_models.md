# Linear mixed models (LMMs)

**Project status:** Active

The following exposition of linear mixed models is based on standard textbooks such as Rencher and Schaalje (2008), and references from the field of statistical genetics such as Matti Pirinen's lecture notes (see [here](https://www.mv.helsinki.fi/home/mjxpirin/GWAS_course/)).

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

### Covariance, genetic relationship matrix, and heritability
Let $i$ and $j$ index two individuals, corresponding to rows in the vectors and matrices defined in \eqref{eq:lmm}. Because $\mathbf{X}_i \boldsymbol{\alpha}$ and $\mathbf{X}_j \boldsymbol{\alpha}$ are fixed constants, they do not contribute to the covariance. The covariance between their phenotypes can be expressed as:

$$
\begin{align*}
\text{Cov}(y_i, y_j) &= \text{Cov}(\mathbf{G}_i \boldsymbol{\beta} + \epsilon_i, \mathbf{G}_j \boldsymbol{\beta} + \epsilon_j) \nonumber \\
&= \text{Cov}(\mathbf{G}_i\boldsymbol{\beta}, \mathbf{G}_j\boldsymbol{\beta}) \nonumber \\
&= \text{Cov}\left(\sum_{k=1}^M G_{ik} \beta_k, \sum_{l=1}^M G_{jl} \beta_l\right) \nonumber \\
&= \sum_{k=1}^M \sum_{l=1}^M G_{ik} G_{jl} \text{Cov}(\beta_k, \beta_l) \nonumber \\
&= \sigma_g^2 \sum_{k=1}^M G_{ik} G_{jk}  \\
\end{align*}
$$

The second term on the right-hand side of the last equation is proportional to element $ij$ of the genetic relationship matrix $\mathbf{K} = \mathbf{G}\mathbf{G}^T / M$.

#### The genetic relationship matrix (GRM)
Because the GRM plays a central role in the LMM, we will discuss it in more detail here. The kinship coefficient between two individuals $i$ and $j$, $\phi_{ij}$, is defined as the probability a randomly chosen allele from individual $i$ and a randomly chosen allele from individual $j$ are identical by descent (IBD). It is important to note that this is an expected value over many independent realisations of the evolutionary process at the locus. The observed value may differ from the expected value due to intrinsic biological factors such as de novo mutations and random Mendelian sampling, as well as extrinsic factors such as genotyping errors. 

Consider an autosomal locus with two alleles, arbitrarily labeled 0 and 1. Let $p$ be the frequency of allele 1 in the population. Denote the genotypes of the two individuals at the locus as $G^*_{i} = H_{i1} + H_{i2}$ and $G^*_{j} = H_{j1} + H_{j2}$, respectively, where $H_{ik}$ be an indicator variable that takes the value 1 if haplotype $k$ in individual $i$ carries allele 1, and 0 otherwise. Assuming Hardy-Weinberg equilibrium, the mean and variance are $E(H_{ik}) = E(H_{jl}) = p$ and $\text{Var}(H_{ik}) = \text{Var}(H_{jl}) = p(1-p)$. The genetic relationship between the two individuals can be calculated as:

$$
\begin{align*}
\text{Corr}(G^*_i, G^*_j) &= \text{Corr}(H_{i1} + H_{i2}, H_{j1} + H_{j2}) \nonumber \\
&= \frac{\text{Cov}(H_{i1} + H_{i2}, H_{j1} + H_{j2})}{\sqrt{\text{Var}(H_{i1} + H_{i2}) \text{Var}(H_{j1} + H_{j2})}} \nonumber \\
&= \frac{\text{Cov}(H_{i1}, H_{j1}) + \text{Cov}(H_{i1}, H_{j2}) + \text{Cov}(H_{i2}, H_{j1}) + \text{Cov}(H_{i2}, H_{j2})}{\sqrt{2p(1-p) \cdot 2p(1-p)}} \nonumber \\
&= \frac{4 \text{Cov}(H_{ik}, H_{jl})}{2p(1-p)} \nonumber \\
&= 2 \frac{E(H_{ik} H_{jl}) - E(H_{ik})E(H_{jl})}{p(1-p)} \nonumber \\
&= 2 \frac{\Pr(H_{ik} = 1, H_{jl} = 1) - p^2}{p(1-p)} \\
\end{align*}
$$

We can express $\Pr(H_{ik} = 1, H_{jl} = 1)$ in terms of $\phi_{ij}$ as follows:

$$
\begin{align*}
\Pr(H_{ik} = 1, H_{jl} = 1) = \phi_{ij} p + (1 - \phi_{ij}) p^2
\end{align*}
$$

The first term on the right-hand side corresponds to the case where the two alleles are IBD, in which case they both carry allele 1 with probability $p$. The second term corresponds to the case where the two alleles are not IBD, in which case they both carry allele 1 with probability $p^2$. Substituting this expression into the equation for $\text{Corr}(G^*_i, G^*_j)$ gives:

$$
\begin{align}
\text{Corr}(G^*_i, G^*_j) = 2 \phi_{ij} = r_{ij}
\end{align}
$$

where $r_{ij}$ is the relatedness coefficient. Without inbreeding, $r_{ij}$ can be interpreted as the expected proportion of alleles that are IBD between individuals $i$ and $j$. For example, $r_{ij} = 1$ for monozygotic twins or duplicated samples, $r_{ij} = 0.5$ for first-degree relatives such as parent-offspring pairs and full siblings.

With data from $M$ sites, we can estimate the relatedness coefficient as:

$$
\begin{align*}
\hat{r}_{ij} = \frac{1}{M} \sum_{k=1}^M \frac{(G^*_{ik} - 2\hat{p}_k)(G^*_{jk} - 2\hat{p}_k)}{2\hat{p}_k(1-\hat{p}_k)}
= \frac{1}{M} \sum_{k=1}^M G_{ik} G_{jk}
\end{align*}
$$

where $\hat{p}_k$ is the sample frequency of allele 1 at site $k$, and $G_{ik}$ is the standardised genotype.

It should be noted that the GRM estimator assumes that the samples are drawn from a homogeneous population. If this assumption is violated, the estimator can be biased. Furthermore, the $\hat{p}_k (1 - \hat{p}_k)$ term in the denominator can be small for rare variants, which can lead to large sampling variance in the estimator. It is common practice to exclude rare variants when constructing the GRM for this reason (e.g., rare variants with minor allele frequency less than 5%).

!!! note "References"
Rencher, A. C., & Schaalje, G. B. (2008). Linear models in statistics. John Wiley & Sons.