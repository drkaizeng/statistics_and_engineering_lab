# The Frisch-Waugh-Lovell Theorem

Consider the following multiple linear regression model:

$$
\begin{align}
\label{eq:mulreg}
\mathbf{y} = \mathbf{X}\boldsymbol{\beta}  +  \mathbf{C} \boldsymbol{\alpha}+ \boldsymbol{\epsilon}
\end{align}
$$

where $\mathbf{y}$ is the response variable, $\mathbf{X}$  ($n$ by $p$) and $\mathbf{C}$ ($n$ by $q$) are matrices of predictors and covariates, $\boldsymbol{\beta}$ and $\boldsymbol{\alpha}$ are vectors of the effect sizes of the predictors and covariates, and $\boldsymbol{\epsilon}$ is the residual error with $\text{Cov}(\boldsymbol{\epsilon}) = \sigma^2 \mathbf{I}$. Note that the intercept can be viewed as part of the covariate matrix $\mathbf{C}$.

We define $\mathbf{H} = \mathbf{C} (\mathbf{C}^\top \mathbf{C})^{-1} \mathbf{C}^\top$ as the hat matrix, and multiply both sides of \eqref{eq:mulreg} by $(\mathbf{I} - \mathbf{H})$, where $\mathbf{I}$ is the identity matrix. This leads to

$$
\begin{align}
(\mathbf{I} - \mathbf{H}) \mathbf{y} &= (\mathbf{I} - \mathbf{H}) \mathbf{X}\boldsymbol{\beta}  +  (\mathbf{I} - \mathbf{H}) \mathbf{C} \boldsymbol{\alpha}+ (\mathbf{I} - \mathbf{H})\boldsymbol{\epsilon} \\
&= (\mathbf{I} - \mathbf{H}) \mathbf{X}\boldsymbol{\beta}  +  (\mathbf{I} - \mathbf{H})\boldsymbol{\epsilon}
\end{align}
$$

Note that $\hat{\mathbf{y}} := \mathbf{Hy}$ are the predicted values from the least-squares estimator for the model $\mathbf{y} = \mathbf{C} \mathbf{b} + \mathbf{e}$, and $\tilde{\mathbf{y}} = (\mathbf{I} - \mathbf{H}) \mathbf{y}$ are the residual errors (Rencher and Schaalje 2008). Similarly, we can define $\tilde{\mathbf{X}} = (\mathbf{I} - \mathbf{H}) \mathbf{X}$ as the residuals obtained by regressing $\mathbf{X}$ on the covariates $\mathbf{C}$. Thus, we arrive at the Frisch-Waugh-Lovell theorem, which states that the coefficient vector $\boldsymbol{\beta}$ can be obtained from the following model:

$$
\begin{align}
\label{eq:fwl}
\tilde{\mathbf{y}} = \tilde{\mathbf{X}} \boldsymbol{\beta} + \tilde{\boldsymbol{\epsilon}}
\end{align}
$$

The Frisch-Waugh-Lovell theorem proves that the residual errors from the above procedure are identical to the residual errors obtained from fitting the full model \eqref{eq:mulreg}. Thus, it is important that when fitting the above model, the residuals are interpreted correctly and that the standard errors are estimated by using the correct degrees of freedom $n - p - q$.

# Numerical considerations
When fitting $\mathbf{y} = \mathbf{C}\mathbf{b} + \mathbf{e}$ (and similarly, when regressing $\mathbf{X}$ on $\mathbf{C}$), it is important to consider the numerical stability. First, it is useful to transform the columns of $\mathbf{C}$ so that they are on a comparable scale as follows. Define

$$
\mathbf{N} = \text{diag}\left(\|\mathbf{c}_1\|, \|\mathbf{c}_2\|, \dots, \|\mathbf{c}_q\|\right),
$$

where $\mathbf{c}_j$ is the $j$-th column of $\mathbf{C}$, and $\|\cdot\|$ denotes the Euclidean norm. Then, we can scale the columns of $\mathbf{C}$ by defining

$$
\begin{align}
\mathbf{D} = \mathbf{C} \mathbf{N}^{-1}.
\end{align}
$$

Secondly, directly computing $\mathbf{H}$ by performing matrix inversion is numerically unstable for ill-conditioned matrices, because forming $\mathbf{C}^\top \mathbf{C}$ squares the condition number, $\kappa(\mathbf{C}^\top \mathbf{C}) = \kappa(\mathbf{C})^2$, halving the number of accurate digits available; working from a decomposition of $\mathbf{D}$ instead keeps the error growth proportional to $\kappa(\mathbf{D})$ rather than its square. Therefore, we perform the SVD (singular value decomposition) on the scaled matrix $\mathbf{D}$:

$$
\begin{align}
\mathbf{D} &= \mathbf{U} \mathbf{\Sigma} \mathbf{V}^\top
\end{align}
$$

where  $\mathbf{U}$ ($n$ by $q$) and $\mathbf{V}$ ($q$ by $q$) are matrices with orthonormal columns, and $\mathbf{\Sigma}$ is a diagonal matrix containing the singular values of $\mathbf{D}$. Specifically, the columns of $\mathbf{U}$ are the eigenvectors of $\mathbf{D} \mathbf{D}^\top$, and $\mathbf{\Sigma}$ contains the square roots of the corresponding eigenvalues:

$$
\begin{align}
\mathbf{D} \mathbf{D}^\top \mathbf{u}_k = \mathbf{D} \mathbf{D}^\top s_k^{-1} \mathbf{D} \mathbf{v}_k = s_k \mathbf{D} \mathbf{v}_k = s_k^2 \mathbf{u}_k
\end{align}
$$

where $\mathbf{u}_k = s_k^{-1} \mathbf{D} \mathbf{v}_k$ is the $k$-th column of $\mathbf{U}$, $\mathbf{v}_k$ is the $k$-th column of $\mathbf{V}$ and is also the $k$-th eigenvector of $\mathbf{D}^\top \mathbf{D}$, and $s_k$ is the $k$-th singular value of $\mathbf{D}$ which corresponds to the square root of the $k$-th eigenvalue of either $\mathbf{D} \mathbf{D}^\top$ or $\mathbf{D}^\top \mathbf{D}$ (Jolliffe 2002).

Note that

$$
\begin{align}
\mathbf{C} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^\top \mathbf{N}
\end{align}
$$

Define $\mathbf{R} = \mathbf{\Sigma} \mathbf{V}^\top \mathbf{N}$. Because $\mathbf{C}$ is a full rank matrix, $\mathbf{\Sigma}$ is invertible, $\mathbf{V}$ is an invertible square orthogonal matrix, and $\mathbf{N}$ is also invertible because no column of $\mathbf{C}$ is zero. Thus, $\mathbf{R}$ is also invertible, and we can write

$$
\begin{align}
\mathbf{C} (\mathbf{C}^\top \mathbf{C})^{-1} \mathbf{C}^\top
= \mathbf{UR} (\mathbf{R}^\top \mathbf{U}^\top \mathbf{UR})^{-1} \mathbf{R}^\top \mathbf{U}^\top 
= \mathbf{U} \mathbf{U}^\top
\end{align}
$$

Therefore, we can use SVD to compute the residuals

$$
\begin{align}
\tilde{\mathbf{y}} = \mathbf{y} - \mathbf{C} (\mathbf{C}^\top \mathbf{C})^{-1} \mathbf{C}^\top \mathbf{y} = \mathbf{y} - \mathbf{U} \mathbf{U}^\top \mathbf{y}
\end{align}
$$
