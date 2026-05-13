# Linear mixed models (LMMs)

**Project status:** Active

Consider a sample of $N$ individuals, each of whom has been genotyped at $M$ sites. Assume that the each site has two alleles arbitrarily labeled 0 and 1. Let $\mathbf{G}$ represent the $N \times M$ genotype matrix, where $G_{ij}$ is the genotype of individual $i$ at site $j$, coded as the number of copies of allele 1 (i.e., 0, 1, or 2). The samples have been measured for a trait of interest, as well as $C$ covariates. We use $\mathbf{y}$ to represent the $N \times 1$ vector of phenotypes, $\mathbf{X}$ to represent the $N \times C$ matrix of covariates (including an intercept), and assume that $\mathbf{X}$ is full rank. We are interested in the following linear mixed model (LMM):

$$
\begin{equation}
\mathbf{y} = \mathbf{X}\boldsymbol{\alpha} + \mathbf{G}_S\boldsymbol{\beta} + \boldsymbol{\epsilon}
\end{equation}
$$

where $\mathbf{G}_S$ is a standardised version of $\mathbf{G}$ with mean 0 and variance 1 for each column, $\boldsymbol{\alpha}$ is a $C \times 1$ vector of fixed effects, $\boldsymbol{\beta}$ is a $M \times 1$ vector of random effects with $\boldsymbol{\beta} \sim \mathcal{N}(\mathbf{0}, \sigma_g^2\mathbf{I}_M)$, and $\boldsymbol{\epsilon}$ is a $N \times 1$ vector of residuals with $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \sigma_e^2\mathbf{I}_N)$. The symbol $\mathbf{I}_X$ represents the $X \times X$ identity matrix.

