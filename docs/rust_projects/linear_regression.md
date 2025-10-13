# Linear regression (in prog)
My first Rust project. I chose to implement simple linear regression to focus on learning Rust's syntax, ownership system, and tooling without the overhead of complex matrix operations. The following sections outline the implementation. The mathematical treatment follows Rencher and Schaalje (2008).

## The model
Consider the model
$$
y = \beta_0 + \beta_1 x + \epsilon
$$
where $\epsilon \sim N(0, \sigma^2)$. Let the observations be $(x_i, y_i)$ (for $i$ = 1, ..., $n$). The estimates are
$$
\begin{align*}
\widehat{\beta_1} &= \frac{\sum_{i=1}^n x_i y_i - n \bar{x} \bar{y}}{\sum_{i=1}^n x_i^2 - n\bar{x}}
\\[10pt]
\widehat{\beta_0} &= \bar{y} - \widehat{\beta_1} \bar{x}
\\[10pt]
\widehat{\sigma^2} &= \frac{\sum_{i=1}^n (y_i - \widehat{y_i})^2}{n - 2}
\\[10pt]
\text{var}(\widehat{\beta_1}) &= \frac{\widehat{\sigma^2}}{\sum_{i=1}^n (x_i - \bar{x})^2}
\\[10pt]
\text{var}(\widehat{\beta_0}) &= \widehat{\sigma^2} \Big[ \frac{1}{n} + \frac{\bar{x}^2}{\sum_{i=1}^n (x_i - \bar{x})^2} \Big]
\end{align*}
$$

where $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$, $\bar{y} = \frac{1}{n} \sum_{i=1}^n y_i$, and $\widehat{y_i} = \widehat{\beta_0} + \widehat{\beta_1} x_i$.

Under the null hypothesis that $\beta_1 = 0$, the $t$ defined below follows a $t$ distribution with $n - 2$ degrees of freedom:
$$
t = \frac{ \widehat{\beta_1} }{\hat{\sigma} / \sqrt{\sum_i (x_i - \bar{x})^2}}
$$





!!! note "References"
Rencher, A. C., & Schaalje, G. B. (2008). Linear models in statistics. John Wiley & Sons.