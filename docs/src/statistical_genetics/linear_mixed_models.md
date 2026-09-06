# The genetic relationship matrix and the covariance structure of the infinitesimal model

*This note works out why the genetic relationship matrix (GRM) is the covariance structure implied
by the infinitesimal model.*

The exposition is based on standard textbooks such as Rencher and Schaalje (2008), and references from the field of statistical genetics such as Matti Pirinen's lecture notes (see [here](https://www.mv.helsinki.fi/home/mjxpirin/GWAS_course/)).

## The infinitesimal model with additive effects
Consider a sample of $N$ individuals, each of whom has been genotyped at $M$ sites. Assume that each site has two alleles arbitrarily labeled 0 and 1. Let $\mathbf{G}^*$ represent the $N \times M$ genotype matrix, where $G^*_{ik}$ is the genotype of individual $i$ at site $k$, coded as the number of copies of allele 1 (i.e., 0, 1, or 2). The samples have been measured for a trait of interest, as well as $C$ covariates. We use $\mathbf{y}$ to represent the $N \times 1$ vector of phenotypes, $\mathbf{X}$ to represent the $N \times C$ matrix of covariates (including an intercept), and assume that $\mathbf{X}$ is full rank. We are interested in the following linear mixed model (LMM):

$$
\begin{equation}
\label{eq:lmm}
\mathbf{y} = \mathbf{X}\boldsymbol{\alpha} + \mathbf{G}\boldsymbol{\beta} + \boldsymbol{\epsilon}
\end{equation}
$$

where $\mathbf{G}$ is a standardised version of $\mathbf{G}^*$ with mean 0 and variance 1 for each column, $\boldsymbol{\alpha}$ is a $C \times 1$ vector of fixed effects, $\boldsymbol{\beta}$ is an $M \times 1$ vector of random effects with $\boldsymbol{\beta} \sim \mathcal{N}(\mathbf{0}, \sigma_g^2\mathbf{I}_M)$, $\boldsymbol{\epsilon}$ is an $N \times 1$ vector of residuals with $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \sigma_e^2\mathbf{I}_N)$, and $\boldsymbol{\beta}$ and $\boldsymbol{\epsilon}$ are independent. The symbol $\mathbf{I}_X$ represents the $X \times X$ identity matrix.

The assumption $\boldsymbol{\beta} \sim \mathcal{N}(\mathbf{0}, \sigma_g^2\mathbf{I}_M)$ is what makes this the *infinitesimal* model: every one of the $M$ sites is assumed to have a non-zero effect, and all effects are drawn from a single common distribution.

In a fixed effect model, $\boldsymbol{\beta}$ in \eqref{eq:lmm} is treated as a fixed effect, which leads to $M$ parameters to be estimated. When $M$ is large, the number of parameters can exceed the number of samples, leading to overfitting. The LMM addresses this issue by assuming that the effects of the $M$ sites share a common distribution, thereby reducing the number of parameters from $M$ to 1 (i.e., $\sigma_g^2$).

## The covariance structure it implies
Let $i$ and $j$ index two individuals, corresponding to rows in the vectors and matrices defined in \eqref{eq:lmm}. Because $\mathbf{X}_i \boldsymbol{\alpha}$ and $\mathbf{X}_j \boldsymbol{\alpha}$ are fixed constants, they do not contribute to the covariance. For $i \neq j$, the covariance between their phenotypes can be expressed as:

$$
\begin{align*}
\text{Cov}(y_i, y_j) &= \text{Cov}(\mathbf{G}_i \boldsymbol{\beta} + \epsilon_i, \mathbf{G}_j \boldsymbol{\beta} + \epsilon_j) \nonumber \\
&= \text{Cov}(\mathbf{G}_i\boldsymbol{\beta}, \mathbf{G}_j\boldsymbol{\beta}) \nonumber \\
&= \text{Cov}\left(\sum_{k=1}^M G_{ik} \beta_k, \sum_{l=1}^M G_{jl} \beta_l\right) \nonumber \\
&= \sum_{k=1}^M \sum_{l=1}^M G_{ik} G_{jl} \text{Cov}(\beta_k, \beta_l) \nonumber \\
&= \sigma_g^2 \sum_{k=1}^M G_{ik} G_{jk}
\end{align*}
$$

The summation on the right-hand side of the last equation is element $ij$ of $\mathbf{G}\mathbf{G}^T$. Writing the genetic relationship matrix as $\mathbf{K} = \mathbf{G}\mathbf{G}^T / M$, this gives $\text{Cov}(y_i, y_j) = M \sigma_g^2 K_{ij}$.

### The marginal model
Collecting the elementwise result into matrix form, $\text{Cov}(\mathbf{G}\boldsymbol{\beta}) = \sigma_g^2 \mathbf{G}\mathbf{G}^T = M\sigma_g^2 \mathbf{K}$, so marginalising over the random effects gives

$$
\begin{equation}
\label{eq:lmm_marginal}
\mathbf{y} \sim \mathcal{N}\left(\mathbf{X}\boldsymbol{\alpha}, \; M\sigma_g^2\mathbf{K} + \sigma_e^2\mathbf{I}_N\right)
\end{equation}
$$

The above shows that the $M$-vector $\boldsymbol{\beta}$ has been integrated out entirely, and also highlights that the GRM is the sufficient summary of the genotypes for this model.

## Interpreting $\sigma_g^2$ and $h_{\text{SNP}}^2$
Under the parametrisation used above, $\sigma_g^2$ is the per-site prior variance. Averaging $\text{Var}(y_i) = M\sigma_g^2 K_{ii} + \sigma_e^2$ over individuals and using $\overline{K_{ii}} = 1$ (guaranteed by the column standardisation, since $\frac{1}{N}\sum_i G_{ik}^2 = 1$ for every site $k$) gives a mean genetic variance of $M\sigma_g^2$, and hence the SNP heritability (defined with respect to the $M$ genotyped sites rather than all causal variants)

$$
\begin{align*}
h_{\text{SNP}}^2 = \frac{M\sigma_g^2}{M\sigma_g^2 + \sigma_e^2}
\end{align*}
$$

### Two readings of the genetic variance
It should be noted that the genetic variance above can be derived in two ways:

*Conditional on the genotypes* — the reading behind \eqref{eq:lmm_marginal} — $\mathbf{G}$ is the observed sample and the randomness lies in $\boldsymbol{\beta}$, so $\text{Var}(y_i \mid \mathbf{G}) = M\sigma_g^2 K_{ii} + \sigma_e^2$ and the genetic part averages to $M\sigma_g^2$ across the sample.

*Marginally over the genotypes* — closer to what is usually meant by genetic variance — fix the effect vector at $\mathbf{b}$ and let $\mathbf{x} = (x_1, ..., x_M)^T$ be the standardised genotype vector of a randomly drawn individual:

$$
\begin{align*}
\text{Var}(\mathbf{b}^T\mathbf{x}) = \mathbf{b}^T\text{Var}(\mathbf{x})\mathbf{b} = \mathbf{b}^T\mathbf{R}\mathbf{b}
\end{align*}
$$

where $\mathbf{R} = \text{Var}(\mathbf{x}) = \text{Cor}(\mathbf{x})$ is the linkage disequilibrium (LD) matrix, the two coinciding because the genotypes are standardised. Averaging over the prior, using $\text{Cov}(\beta_k, \beta_l) = 0$ for $k \ne l$ and $R_{kk} = 1$:

$$
\begin{align*}
E\left(\boldsymbol{\beta}^T \mathbf{R} \boldsymbol{\beta}\right) = \sum_{k,l} E(\beta_k \beta_l) R_{kl} = \sum_k E(\beta_k^2) R_{kk} = M\sigma_g^2
\end{align*}
$$

For standardised $\mathbf{G}$ the sample LD matrix is $\mathbf{R} = \mathbf{G}^T\mathbf{G} / N$, which leads to the following relationship:

$$
\begin{align*}
M \, \text{tr}(\mathbf{K}) = \text{tr}(\mathbf{G}\mathbf{G}^T) = \text{tr}(\mathbf{G}^T\mathbf{G}) = N \, \text{tr}(\mathbf{R})
\end{align*}
$$

With $\text{tr}(\mathbf{R}) = M$ this gives $\text{tr}(\mathbf{K}) = N$, and hence $\overline{K_{ii}} = 1$. Both routes to the genetic variance are therefore the result of reading along the two dimensions of $\mathbf{G}$.

An important difference between the two is the following: conditional on the genotypes the result is exact; marginally it holds only in expectation, and the genetic variance realised by any single draw of $\boldsymbol{\beta}$ scatters around $M\sigma_g^2$:

$$
\begin{align*}
\text{Var}\left(\boldsymbol{\beta}^T\mathbf{R}\boldsymbol{\beta}\right)
= 2 \sigma_g^4 \, \text{tr}\left(\mathbf{R}^2\right)
\qquad
\text{tr}\left(\mathbf{R}^2\right) = \sum_{k,l} R_{kl} R_{lk} \geq M
\end{align*}
$$

where the first equation follows from Theorem 5.2c in Rencher and Schaalje, and $\sum_{k,l} R_{kl} R_{lk} = M$ if and only if the sites are in linkage equilibrium.

### A note on the factor of $M$
Much of the literature instead sets $\boldsymbol{\beta} \sim \mathcal{N}(\mathbf{0}, (\sigma_g^2 / M)\mathbf{I}_M)$, which absorbs the factor of $M$ into the prior and yields $\text{Cov}(\mathbf{y}) = \sigma_g^2\mathbf{K} + \sigma_e^2\mathbf{I}_N$, with $\sigma_g^2$ reading directly as the total genetic variance and $h_{\text{SNP}}^2 = \sigma_g^2 / (\sigma_g^2 + \sigma_e^2)$. The two are the same model under reparametrisation, but the factor of $M$ is easy to lose track of when comparing formulas across sources.

## The genetic relationship matrix
Because the GRM plays a central role in the LMM, we will discuss it in more detail here. The kinship coefficient between two individuals $i$ and $j$, $\phi_{ij}$, is defined as the probability a randomly chosen allele from individual $i$ and a randomly chosen allele from individual $j$ are identical by descent (IBD). It is important to note that this is an expected value over many independent realisations of the evolutionary process at the locus. The observed value may differ from the expected value due to intrinsic biological factors such as de novo mutations and random Mendelian sampling, as well as extrinsic factors such as genotyping errors.

Consider an autosomal locus with two alleles, arbitrarily labeled 0 and 1. Let $p$ be the frequency of allele 1 in the population. Denote the genotypes of the two individuals at the locus as $G^*_{i} = H_{i1} + H_{i2}$ and $G^*_{j} = H_{j1} + H_{j2}$, respectively, where $H_{ik}$ is an indicator variable that takes the value 1 if haplotype $k$ in individual $i$ carries allele 1, and 0 otherwise. Assuming Hardy-Weinberg equilibrium, the mean and variance are $E(H_{ik}) = E(H_{jl}) = p$ and $\text{Var}(H_{ik}) = \text{Var}(H_{jl}) = p(1-p)$. The genetic relationship between the two individuals can be calculated as:

$$
\begin{align*}
\text{Corr}(G^*_i, G^*_j) &= \text{Corr}(H_{i1} + H_{i2}, H_{j1} + H_{j2}) \nonumber \\
&= \frac{\text{Cov}(H_{i1} + H_{i2}, H_{j1} + H_{j2})}{\sqrt{\text{Var}(H_{i1} + H_{i2}) \text{Var}(H_{j1} + H_{j2})}} \nonumber \\
&= \frac{\text{Cov}(H_{i1}, H_{j1}) + \text{Cov}(H_{i1}, H_{j2}) + \text{Cov}(H_{i2}, H_{j1}) + \text{Cov}(H_{i2}, H_{j2})}{\sqrt{2p(1-p) \cdot 2p(1-p)}} \nonumber \\
&= \frac{4 \text{Cov}(H_{ik}, H_{jl})}{2p(1-p)} \nonumber \\
&= 2 \frac{E(H_{ik} H_{jl}) - E(H_{ik})E(H_{jl})}{p(1-p)} \nonumber \\
&= 2 \frac{\Pr(H_{ik} = 1, H_{jl} = 1) - p^2}{p(1-p)}
\end{align*}
$$

Collapsing the four haplotype-pair covariances into $4\,\text{Cov}(H_{ik}, H_{jl})$ assumes that the two haplotypes within an individual are exchangeable, so that the covariance does not depend on which pair is chosen. This holds in the absence of inbreeding, and is consistent with the definition of $\phi_{ij}$ as an average over the random choice of one allele from each individual.

We can express $\Pr(H_{ik} = 1, H_{jl} = 1)$ in terms of $\phi_{ij}$ as follows:

$$
\begin{align*}
\Pr(H_{ik} = 1, H_{jl} = 1) = \phi_{ij} p + (1 - \phi_{ij}) p^2
\end{align*}
$$

The first term on the right-hand side corresponds to the case where the two alleles are IBD, in which case they both carry allele 1 with probability $p$. The second term corresponds to the case where the two alleles are not IBD, in which case they both carry allele 1 with probability $p^2$. Substituting this expression into the equation for $\text{Corr}(G^*_i, G^*_j)$ gives:

$$
\begin{align*}
\text{Corr}(G^*_i, G^*_j) = 2 \phi_{ij} = r_{ij}
\end{align*}
$$

where $r_{ij}$ is the relatedness coefficient. Without inbreeding, $r_{ij}$ can be interpreted as the expected proportion of alleles that are IBD between individuals $i$ and $j$. For example, $r_{ij} = 1$ for monozygotic twins or duplicated samples, $r_{ij} = 0.5$ for first-degree relatives such as parent-offspring pairs and full siblings. Applying the definition to an individual and themselves gives $\phi_{ii} = 1/2$ without inbreeding, since a random allele is drawn twice with replacement and the same copy is picked half the time. Hence $r_{ii} = 1$, which is the expected value of the diagonal of $\mathbf{K}$.

With data from $M$ sites, we can estimate the relatedness coefficient as:

$$
\begin{align*}
\hat{r}_{ij} = \frac{1}{M} \sum_{k=1}^M \frac{(G^*_{ik} - 2\hat{p}_k)(G^*_{jk} - 2\hat{p}_k)}{2\hat{p}_k(1-\hat{p}_k)}
= \frac{1}{M} \sum_{k=1}^M G_{ik} G_{jk}
\end{align*}
$$

where $\hat{p}_k$ is the sample frequency of allele 1 at site $k$, and $G_{ik}$ is the standardised genotype. This is precisely $K_{ij} = (\mathbf{G}\mathbf{G}^T / M)_{ij}$ from \eqref{eq:lmm_marginal} — the matrix the model's covariance depends on is an estimator of relatedness.

## What the GRM estimator assumes
It should be noted that the GRM estimator assumes that the samples are drawn from a homogeneous population. If this assumption is violated, the estimator can be biased. Furthermore, the $2\hat{p}_k (1 - \hat{p}_k)$ term in the denominator can be small for rare variants, which can lead to large sampling variance in the estimator. It is common practice to exclude low-frequency variants when constructing the GRM for this reason (e.g., variants with minor allele frequency less than 5%).

## Where this leads
With \eqref{eq:lmm_marginal} in hand, three questions follow, none of which are pursued here:

- **Estimating the variance components.** $\sigma_g^2$ and $\sigma_e^2$ are usually estimated by restricted maximum likelihood (REML) rather than ML, which corrects the downward bias ML incurs by not accounting for the degrees of freedom consumed by $\boldsymbol{\alpha}$.

- **Association testing.** Testing a candidate site means adding it as a fixed effect while excluding it, and sites in linkage disequilibrium with it, from the random-effect term. Otherwise the random effects absorb the signal attributable to the candidate — the proximal contamination problem — deflating the test statistic and reducing power. A popular fix is to build the GRM leaving out the candidate's chromosome.

- **Computation.** Evaluating the likelihood naively is slow and infeasible at biobank scale; much of the practical literature is concerned with avoiding it.

!!! note "References"

    Pirinen, M. GWAS course lecture notes. Available at [https://www.mv.helsinki.fi/home/mjxpirin/GWAS_course/](https://www.mv.helsinki.fi/home/mjxpirin/GWAS_course/)

    Rencher, A. C., & Schaalje, G. B. (2008). Linear models in statistics. John Wiley & Sons.
