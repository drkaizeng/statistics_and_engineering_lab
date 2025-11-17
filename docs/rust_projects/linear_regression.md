# Linear regression (in prog)
My first Rust project. I chose to implement simple linear regression to focus on learning Rust's syntax, ownership system, and tooling without the overhead of complex matrix operations. By the same token, the standard library was used, except for calculations involving the t-distribution. The mathematical treatment follows Rencher and Schaalje (2008).

## The model
Consider the model
$$
y = \beta_0 + \beta_1 x + \epsilon
$$
where $\epsilon \sim N(0, \sigma^2)$. Let the independent observations be $(x_i, y_i)$ (for $i$ = 1, ..., $n$). The estimates are
$$
\widehat{\beta_1} = \frac{\sum_{i=1}^n x_i y_i - n \bar{x} \bar{y}}{\sum_{i=1}^n x_i^2 - n\bar{x}^2}
$$
$$
\widehat{\beta_0} = \bar{y} - \widehat{\beta_1} \bar{x}
$$
$$
\widehat{\sigma^2} = \frac{\sum_{i=1}^n (y_i - \widehat{y_i})^2}{n - 2}
$$
$$
\text{var}(\widehat{\beta_1}) = \frac{\widehat{\sigma^2}}{\sum_{i=1}^n (x_i - \bar{x})^2}
$$
$$
\text{var}(\widehat{\beta_0}) = \widehat{\sigma^2} \Big[ \frac{1}{n} + \frac{\bar{x}^2}{\sum_{i=1}^n (x_i - \bar{x})^2} \Big]
$$

where $\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i$, $\bar{y} = \frac{1}{n} \sum_{i=1}^n y_i$, and $\widehat{y_i} = \widehat{\beta_0} + \widehat{\beta_1} x_i$. The coefficient of determination is given by
$$
r^2 = \frac{\sum_i (\widehat{y_i} - \bar{y})^2}{\sum_i (y - \bar{y})^2}
$$


Under the null hypothesis that $\beta_j = 0$ ($j$ = 0, 1), the $t$ defined below follows a $t$ distribution with $n - 2$ degrees of freedom:
$$
t_j = \frac{ \widehat{\beta_j} }{\sqrt{\text{var}(\widehat{\beta_j})}}
$$


## The implementation
### Input
The input is a header-less TSV file with two columns. Each row defines an observation $(x_i, y_i)$. Any missing or irregular data will cause the program to exit.

## Output
A TSV file with informative row labels.





!!! note "References"
Rencher, A. C., & Schaalje, G. B. (2008). Linear models in statistics. John Wiley & Sons.