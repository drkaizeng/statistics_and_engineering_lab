import logging
from math import log, sqrt
from pathlib import Path

import click
import numpy as np
from numpy.random import Generator, default_rng
from scipy.stats import norm

logger = logging.getLogger(__name__)

SimulationResult = np.ndarray


def expected_genotype_variance(af_lower: float, af_upper: float) -> float:
    """
    Compute the expected variance of a genotype under Hardy-Weinberg equilibrium,
    where allele frequencies are drawn from a distribution proportional to 1/p.

    Parameters
    ----------
    af_lower : float
        Lower bound of the allele frequency range, in (0, 1).
    af_upper : float
        Upper bound of the allele frequency range, in (0, 1).

    Returns
    -------
    float
        The expected genotype variance E[2p(1-p)] under the 1/p prior.

    Raises
    ------
    ValueError
        If bounds are invalid (not 0 < af_lower < af_upper < 1).
    """
    if not (0.0 < af_lower < af_upper < 1.0):
        raise ValueError(f"Require 0 < af_lower < af_upper < 1, got af_lower={af_lower}, af_upper={af_upper}")
    numerator = 2.0 * (af_upper - af_lower) - (af_upper**2 - af_lower**2)
    denominator = log(af_upper) - log(af_lower)
    return numerator / denominator


def run_simulation(
    exposure_heritability: float,
    exposure_num_causal_variants: int,
    num_instrumental_variables: int,
    exposure_sample_size: int,
    outcome_sample_size: int,
    percent_outcome_variance_explained_by_exposure: float,
    af_lower: float = 0.01,
    af_upper: float = 0.99,
    minus_log10_p_threshold: float = 0.0,
    rng: Generator | None = None,
) -> SimulationResult:
    """
    Simulate GWAS summary statistics for Mendelian Randomisation.

    Parameters
    ----------
    exposure_heritability : float
        Heritability of the exposure (h²_X), in (0, 1].
    exposure_num_causal_variants : int
        Number of causal variants influencing the exposure (L_X).
    num_instrumental_variables : int
        Number of instrumental variables to generate (L_IV).
    exposure_sample_size : int
        Sample size for the exposure GWAS (n_X).
    outcome_sample_size : int
        Sample size for the outcome GWAS (n_Y).
    percent_outcome_variance_explained_by_exposure : float
        Percentage of outcome variance explained by the exposure, in [0, 100].
    af_lower : float, optional
        Lower bound of allele frequency range. The default is 0.01.
    af_upper : float, optional
        Upper bound of allele frequency range. The default is 0.99.
    minus_log10_p_threshold : float, optional
        Negative log10 of the p-value threshold for IV selection. 0 means no
        filtering (p_threshold = 1). The default is 0.0.
    rng : numpy.random.Generator or None, optional
        Random number generator. If None, a new default generator is created.

    Returns
    -------
    numpy.ndarray
        Structured array with fields: ``effect_allele_frequency``,
        ``true_beta_gx``, ``true_beta_gy``, ``beta_gx``, ``beta_gy``,
        ``standard_error_beta_gx``, ``standard_error_beta_gy``,
        ``minus_log10_p_value_beta_gx``, ``minus_log10_p_value_beta_gy``.

    Raises
    ------
    ValueError
        If any input parameter is out of valid range.
    """
    _validate_inputs(
        exposure_heritability,
        exposure_num_causal_variants,
        num_instrumental_variables,
        exposure_sample_size,
        outcome_sample_size,
        percent_outcome_variance_explained_by_exposure,
        af_lower,
        af_upper,
        minus_log10_p_threshold,
    )

    if rng is None:
        rng = default_rng()
    e_var_g = expected_genotype_variance(af_lower, af_upper)
    sigma2_gx = exposure_heritability / (exposure_num_causal_variants * e_var_g)
    beta_xy = sqrt(percent_outcome_variance_explained_by_exposure / 100.0)
    filtering = minus_log10_p_threshold > 0.0
    collected = _simulate_batch(
        rng,
        num_instrumental_variables,
        sigma2_gx,
        beta_xy,
        exposure_sample_size,
        outcome_sample_size,
        af_lower,
        af_upper,
        minus_log10_p_threshold,
        filtering,
    )
    return collected


_RESULT_DTYPE = np.dtype(
    [
        ("effect_allele_frequency", np.float64),
        ("true_beta_gx", np.float64),
        ("true_beta_gy", np.float64),
        ("beta_gx", np.float64),
        ("beta_gy", np.float64),
        ("standard_error_beta_gx", np.float64),
        ("standard_error_beta_gy", np.float64),
        ("minus_log10_p_value_beta_gx", np.float64),
        ("minus_log10_p_value_beta_gy", np.float64),
    ]
)


def _simulate_batch(
    rng: Generator,
    n_needed: int,
    sigma2_gx: float,
    beta_xy: float,
    n_x: int,
    n_y: int,
    af_lower: float,
    af_upper: float,
    minus_log10_p_threshold: float,
    filtering: bool,
) -> SimulationResult:
    """
    Generate simulated variants in vectorized batches until n_needed pass filtering.

    Parameters
    ----------
    rng : numpy.random.Generator
        Random number generator.
    n_needed : int
        Number of instrumental variables required.
    sigma2_gx : float
        Variance of the effect size distribution for the exposure.
    beta_xy : float
        True causal effect of exposure on outcome.
    n_x : int
        Exposure GWAS sample size.
    n_y : int
        Outcome GWAS sample size.
    af_lower : float
        Lower bound of allele frequency range.
    af_upper : float
        Upper bound of allele frequency range.
    minus_log10_p_threshold : float
        log10(P-value) threshold for filtering (log10(1.0)=0 means no filtering).
    filtering : bool
        Whether p-value filtering is active.

    Returns
    -------
    numpy.ndarray
        Structured array of shape (n_needed,) with the simulation results.
    """
    collected = np.empty(0, dtype=_RESULT_DTYPE)
    batch_size = n_needed * 4 if filtering else n_needed

    while len(collected) < n_needed:
        allele_freq = _sample_allele_frequencies(rng, batch_size, af_lower, af_upper)
        genotype_var = 2.0 * allele_freq * (1.0 - allele_freq)

        true_beta_gx = rng.normal(0.0, sqrt(sigma2_gx), size=batch_size)
        true_beta_gy = true_beta_gx * beta_xy

        se_gx = 1.0 / np.sqrt(n_x * genotype_var)
        se_gy = 1.0 / np.sqrt(n_y * genotype_var)

        beta_gx_hat = rng.normal(true_beta_gx, se_gx)
        beta_gy_hat = rng.normal(true_beta_gy, se_gy)

        abs_z_gx = np.abs(beta_gx_hat / se_gx)
        abs_z_gy = np.abs(beta_gy_hat / se_gy)
        minus_log10_p_gx = -((np.log(2) + norm.logsf(abs_z_gx)) / np.log(10))
        minus_log10_p_gy = -((np.log(2) + norm.logsf(abs_z_gy)) / np.log(10))

        batch = np.empty(batch_size, dtype=_RESULT_DTYPE)
        batch["effect_allele_frequency"] = allele_freq
        batch["true_beta_gx"] = true_beta_gx
        batch["true_beta_gy"] = true_beta_gy
        batch["beta_gx"] = beta_gx_hat
        batch["beta_gy"] = beta_gy_hat
        batch["standard_error_beta_gx"] = se_gx
        batch["standard_error_beta_gy"] = se_gy
        batch["minus_log10_p_value_beta_gx"] = minus_log10_p_gx
        batch["minus_log10_p_value_beta_gy"] = minus_log10_p_gy

        if filtering:
            batch = batch[minus_log10_p_gx >= minus_log10_p_threshold]

        collected = np.concatenate([collected, batch]) if len(collected) > 0 else batch

    return collected[:n_needed]


def _sample_allele_frequencies(rng: Generator, n: int, af_lower: float, af_upper: float) -> np.ndarray:
    """
    Sample allele frequencies from a distribution proportional to 1/p on [af_lower, af_upper].

    Uses inverse CDF: p = af_lower * (af_upper / af_lower)^u, where u ~ Uniform(0, 1).

    Parameters
    ----------
    rng : numpy.random.Generator
        Random number generator.
    n : int
        Number of samples.
    af_lower : float
        Lower bound of allele frequency range.
    af_upper : float
        Upper bound of allele frequency range.

    Returns
    -------
    numpy.ndarray
        Array of sampled allele frequencies.
    """
    u = rng.uniform(0.0, 1.0, size=n)
    return af_lower * (af_upper / af_lower) ** u


def _validate_inputs(
    exposure_heritability: float,
    exposure_num_causal_variants: int,
    num_instrumental_variables: int,
    exposure_sample_size: int,
    outcome_sample_size: int,
    percent_variance: float,
    af_lower: float,
    af_upper: float,
    minus_log10_p: float,
) -> None:
    """
    Validate simulation input parameters.

    Parameters
    ----------
    exposure_heritability : float
        Must be in (0, 1].
    exposure_num_causal_variants : int
        Must be positive.
    num_instrumental_variables : int
        Must be positive.
    exposure_sample_size : int
        Must be positive.
    outcome_sample_size : int
        Must be positive.
    percent_variance : float
        Must be in (0, 100].
    af_lower : float
        Must be in (0, 1).
    af_upper : float
        Must be in (0, 1) and greater than af_lower.
    minus_log10_p : float
        Must be non-negative.

    Raises
    ------
    ValueError
        If any parameter is out of range.
    """
    if not (0.0 < exposure_heritability <= 1.0):
        raise ValueError(f"exposure_heritability must be in (0, 1], got {exposure_heritability}")
    if exposure_num_causal_variants < 1:
        raise ValueError(f"exposure_num_causal_variants must be >= 1, got {exposure_num_causal_variants}")
    if num_instrumental_variables < 1:
        raise ValueError(f"num_instrumental_variables must be >= 1, got {num_instrumental_variables}")
    if exposure_sample_size < 1:
        raise ValueError(f"exposure_sample_size must be >= 1, got {exposure_sample_size}")
    if outcome_sample_size < 1:
        raise ValueError(f"outcome_sample_size must be >= 1, got {outcome_sample_size}")
    if not (0.0 <= percent_variance <= 100.0):
        raise ValueError(f"percent_outcome_variance_explained_by_exposure must be in [0, 100], got {percent_variance}")
    if not (0.0 < af_lower < af_upper < 1.0):
        raise ValueError(f"Require 0 < af_lower < af_upper < 1, got af_lower={af_lower}, af_upper={af_upper}")
    if minus_log10_p < 0.0:
        raise ValueError(f"minus_log10_p_value_threshold must be >= 0, got {minus_log10_p}")


@click.command()
@click.option("--exposure-heritability", required=True, type=float, help="Heritability of the exposure (h²_X).")
@click.option(
    "--exposure-num-causal-variants", required=True, type=int, help="Number of causal variants for the exposure (L_X)."
)
@click.option(
    "--num-instrumental-variables", required=True, type=int, help="Number of instrumental variables to simulate (L_IV)."
)
@click.option("--exposure-sample-size", required=True, type=int, help="Sample size for the exposure GWAS (n_X).")
@click.option("--outcome-sample-size", required=True, type=int, help="Sample size for the outcome GWAS (n_Y).")
@click.option(
    "--percent-outcome-variance-explained-by-exposure",
    required=True,
    type=float,
    help="Percentage of outcome variance explained by the exposure.",
)
@click.option(
    "--causal-variant-allele-frequency-lower-bound",
    type=float,
    default=0.01,
    show_default=True,
    help="Lower bound of allele frequency range.",
)
@click.option(
    "--causal-variant-allele-frequency-upper-bound",
    type=float,
    default=0.99,
    show_default=True,
    help="Upper bound of allele frequency range.",
)
@click.option(
    "--minus-log10-p-value-threshold",
    type=float,
    default=0.0,
    show_default=True,
    help="Negative log10 of the p-value threshold for IV selection. 0 means no filtering.",
)
@click.option(
    "--output-tsv",
    required=True,
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    help="Path to the output TSV file.",
)
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility.")
def simulate(
    exposure_heritability: float,
    exposure_num_causal_variants: int,
    num_instrumental_variables: int,
    exposure_sample_size: int,
    outcome_sample_size: int,
    percent_outcome_variance_explained_by_exposure: float,
    causal_variant_allele_frequency_lower_bound: float,
    causal_variant_allele_frequency_upper_bound: float,
    minus_log10_p_value_threshold: float,
    output_tsv: Path,
    seed: int | None,
) -> None:
    """Simulate GWAS summary statistics for Mendelian Randomisation."""
    rng = default_rng(seed)
    result = run_simulation(
        exposure_heritability=exposure_heritability,
        exposure_num_causal_variants=exposure_num_causal_variants,
        num_instrumental_variables=num_instrumental_variables,
        exposure_sample_size=exposure_sample_size,
        outcome_sample_size=outcome_sample_size,
        percent_outcome_variance_explained_by_exposure=percent_outcome_variance_explained_by_exposure,
        af_lower=causal_variant_allele_frequency_lower_bound,
        af_upper=causal_variant_allele_frequency_upper_bound,
        minus_log10_p_threshold=minus_log10_p_value_threshold,
        rng=rng,
    )

    _write_tsv(result, output_tsv)
    click.echo(f"Wrote {len(result)} instrumental variables to {output_tsv}")


def _write_tsv(result: SimulationResult, output_path: Path) -> None:
    """
    Write simulation results to a TSV file.

    Parameters
    ----------
    result : numpy.ndarray
        Structured array from run_simulation.
    output_path : Path
        Output file path.
    """
    columns = list(result.dtype.names)  # type: ignore[arg-type]
    with open(output_path, "w") as f:
        f.write("\t".join(columns) + "\n")
        for row in result:
            f.write("\t".join(str(row[col]) for col in columns) + "\n")


if __name__ == "__main__":
    simulate()
