import logging
import sys
from math import sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import msgspec
import numpy as np
from numpy.random import default_rng

from mendelian_randomisation.estimate import ivw_estimate
from mendelian_randomisation.simulate import run_simulation

logger = logging.getLogger(__name__)


class RunSimulationConfig(msgspec.Struct):
    """Parameters passed to run_simulation()."""

    exposure_heritability: float
    exposure_num_causal_variants: int
    num_instrumental_variables: int
    exposure_sample_size: int
    outcome_sample_size: int
    percent_outcome_variance_explained_by_exposure: float
    af_lower: float = 0.01
    af_upper: float = 0.99
    minus_log10_p_threshold: float = 0.0


class SimulationConfig(msgspec.Struct):
    """Top-level configuration for the simulation script."""

    run_simulation: RunSimulationConfig
    num_repetitions: int
    output_tsv: str
    beta_histogram_png: str
    p_value_histogram_png: str
    seed: int | None = None


def main(config_path: str) -> None:
    """
    Run repeated simulations and IVW estimations from a JSON config.

    Parameters
    ----------
    config_path : str
        Path to the JSON configuration file.
    """
    with open(config_path, "rb") as f:
        config = msgspec.json.decode(f.read(), type=SimulationConfig)

    sim_params = msgspec.structs.asdict(config.run_simulation)
    num_repetitions = config.num_repetitions
    output_tsv = Path(config.output_tsv)
    beta_histogram_png = Path(config.beta_histogram_png)
    p_value_histogram_png = Path(config.p_value_histogram_png)

    rng = default_rng(config.seed)
    true_beta_xy = sqrt(config.run_simulation.percent_outcome_variance_explained_by_exposure / 100.0)

    betas = np.empty(num_repetitions)
    standard_errors = np.empty(num_repetitions)
    minus_log10_p_values = np.empty(num_repetitions)
    num_instruments_arr = np.empty(num_repetitions, dtype=int)

    for i in range(num_repetitions):
        sim_result = run_simulation(**sim_params, rng=rng)

        result = ivw_estimate(
            sim_result["beta_gx"],
            sim_result["beta_gy"],
            sim_result["standard_error_beta_gy"],
        )

        betas[i] = result.beta
        standard_errors[i] = result.standard_error
        minus_log10_p_values[i] = result.minus_log10_p_value
        num_instruments_arr[i] = result.num_instruments

    _write_tsv(output_tsv, num_instruments_arr, betas, standard_errors, minus_log10_p_values)
    logger.info(f"Wrote {num_repetitions} results to {output_tsv}")

    _plot_beta_histogram(beta_histogram_png, betas, true_beta_xy)
    logger.info(f"Wrote beta histogram to {beta_histogram_png}")

    p_values = 10.0 ** (-minus_log10_p_values)
    _plot_p_value_histogram(p_value_histogram_png, p_values)
    logger.info(f"Wrote p-value histogram to {p_value_histogram_png}")


def _write_tsv(
    path: Path,
    num_instruments: np.ndarray,
    betas: np.ndarray,
    standard_errors: np.ndarray,
    minus_log10_p_values: np.ndarray,
) -> None:
    """
    Write simulation results to a TSV file.

    Parameters
    ----------
    path : Path
        Output file path.
    num_instruments : numpy.ndarray
        Number of instruments per repetition.
    betas : numpy.ndarray
        IVW beta estimates.
    standard_errors : numpy.ndarray
        Standard errors of IVW estimates.
    minus_log10_p_values : numpy.ndarray
        Negative log10 p-values of IVW estimates.
    """
    with open(path, "w") as f:
        f.write("num_instruments\tbeta\tstandard_error\tminus_log10_p_value\n")
        for i in range(len(betas)):
            f.write(f"{num_instruments[i]}\t{betas[i]}\t{standard_errors[i]}\t{minus_log10_p_values[i]}\n")


def _plot_beta_histogram(path: Path, betas: np.ndarray, true_beta_xy: float) -> None:
    """
    Plot a histogram of IVW beta estimates with a reference line at the true value.

    Parameters
    ----------
    path : Path
        Output PNG path.
    betas : numpy.ndarray
        IVW beta estimates.
    true_beta_xy : float
        True causal effect for the reference line.
    """
    fig, ax = plt.subplots()
    ax.hist(betas, bins="auto", edgecolor="black")
    mean = np.mean(betas)
    se = np.std(betas, ddof=1) / np.sqrt(len(betas))
    ax.axvline(true_beta_xy, color="red", linestyle="--", label=f"True β = {true_beta_xy:.4f}")
    ax.axvline(mean, color="blue", linestyle="-", label=f"Mean = {mean:.4f} (SE = {se:.4f})")
    ax.set_xlabel("IVW beta estimate")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of IVW beta estimates")
    ax.legend()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_p_value_histogram(path: Path, p_values: np.ndarray) -> None:
    """
    Plot a histogram of p-values with a reference line at p = 0.05.

    Parameters
    ----------
    path : Path
        Output PNG path.
    p_values : numpy.ndarray
        P-values from IVW estimates.
    """
    fig, ax = plt.subplots()
    ax.hist(p_values, bins="auto", edgecolor="black")
    mean = np.mean(p_values)
    se = np.std(p_values, ddof=1) / np.sqrt(len(p_values))
    ax.axvline(0.05, color="red", linestyle="--", label="p = 0.05")
    ax.axvline(mean, color="blue", linestyle="-", label=f"Mean = {mean:.4f} (SE = {se:.4f})")
    ax.set_xlabel("P-value")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of IVW p-values")
    ax.legend()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    if len(sys.argv) != 2:
        logger.error(f"Usage: {sys.argv[0]} <config.json>")
        sys.exit(1)
    main(sys.argv[1])
