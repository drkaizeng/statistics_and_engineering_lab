# Linear regression (in prog)
My first Rust project. I chose to implement simple linear regression to focus on learning Rust's syntax, ownership system, and tooling without the overhead of complex matrix operations. The following sections outline the implementation. The mathematical treatment follows Rencher and Schaalje (2008).

## The model
Consider the model
$$
y = \beta_0 + \beta_1 x + \epsilon
$$
where $\epsilon \sim N(0, \sigma^2)$.



!!! note "References"
Rencher, A. C., & Schaalje, G. B. (2008). Linear models in statistics. John Wiley & Sons.