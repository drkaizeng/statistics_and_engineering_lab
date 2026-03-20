import dataclasses
import logging
from math import sqrt
from pathlib import Path

import click
import numpy as np
from scipy.stats import norm

logger = logging.getLogger(__name__)

_REQUIRED_COLUMNS = ("beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy")
_P_VALUE_COLUMN = "minus_log10_p_value_beta_gx"


@dataclasses.dataclass(frozen=True)
class IVWResult:
    """Result of an Inverse-Variance Weighted estimation.

    Attributes
    ----------
    beta : float
        The IVW causal effect estimate.
    standard_error : float
        Standard error of the IVW estimate.
    minus_log10_p_value : float
        Negative log10 of the two-sided p-value for the null hypothesis beta = 0.
    num_instruments : int
        Number of instrumental variables used.
    """

    beta: float
    standard_error: float
    minus_log10_p_value: float
    num_instruments: int


def ivw_estimate(beta_gx: np.ndarray, beta_gy: np.ndarray, se_gy: np.ndarray) -> IVWResult:
    """
    Compute the Inverse-Variance Weighted (IVW) estimate of the causal effect.

    Parameters
    ----------
    beta_gx : numpy.ndarray
        Estimated effects of genetic variants on the exposure.
    beta_gy : numpy.ndarray
        Estimated effects of genetic variants on the outcome.
    se_gy : numpy.ndarray
        Standard errors of beta_gy estimates.

    Returns
    -------
    IVWResult
        The IVW estimate, its standard error, minus_log10_p_value, and instrument count.

    Raises
    ------
    ValueError
        If arrays are empty or have mismatched lengths.
    """
    if len(beta_gx) == 0:
        raise ValueError("No instruments provided")
    if not (len(beta_gx) == len(beta_gy) == len(se_gy)):
        raise ValueError(
            f"Array lengths must match: beta_gx={len(beta_gx)}, beta_gy={len(beta_gy)}, se_gy={len(se_gy)}"
        )

    weights = beta_gx**2 / se_gy**2
    beta = np.sum(beta_gx * beta_gy / se_gy**2) / np.sum(weights)
    variance = 1.0 / np.sum(weights)
    se = sqrt(variance)
    minus_log10_p = _compute_minus_log10_p_value(beta, se)

    return IVWResult(
        beta=float(beta),
        standard_error=se,
        minus_log10_p_value=minus_log10_p,
        num_instruments=len(beta_gx),
    )


def _compute_minus_log10_p_value(beta: float, se: float) -> float:
    """
    Compute -log10(p-value) from a z-score using the two-sided normal test.

    Parameters
    ----------
    beta : float
        The estimate.
    se : float
        Standard error of the estimate.

    Returns
    -------
    float
        Negative log10 of the two-sided p-value.
    """
    abs_z = abs(beta / se)
    return float(-(np.log(2) + norm.logsf(abs_z)) / np.log(10))


def _read_input(path: Path, threshold: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Read and validate the input TSV, optionally filtering by p-value threshold.

    Parameters
    ----------
    path : Path
        Path to the input TSV file.
    threshold : float
        Minimum -log10(p-value) for instrument selection. 0 means no filtering.

    Returns
    -------
    tuple of numpy.ndarray
        (beta_gx, beta_gy, se_gy) arrays after filtering.

    Raises
    ------
    ValueError
        If required columns are missing, values are invalid, or no instruments remain.
    """
    with open(path) as f:
        header = f.readline().strip().split("\t")

    for col in _REQUIRED_COLUMNS:
        if col not in header:
            raise ValueError(f"Missing required column: {col}")

    filtering = threshold > 0.0
    if filtering and _P_VALUE_COLUMN not in header:
        raise ValueError(f"Column '{_P_VALUE_COLUMN}' is required when --instrument-minus-log10-p-value-threshold > 0")

    col_indices = {col: header.index(col) for col in _REQUIRED_COLUMNS}
    cols_to_load = [col_indices[c] for c in _REQUIRED_COLUMNS]

    if filtering:
        p_col_idx = header.index(_P_VALUE_COLUMN)
        cols_to_load.append(p_col_idx)

    data = np.loadtxt(path, delimiter="\t", skiprows=1, usecols=cols_to_load)
    if data.ndim == 1:
        data = data.reshape(1, -1)

    beta_gx = data[:, 0]
    beta_gy = data[:, 1]
    se_gx = data[:, 2]
    se_gy = data[:, 3]

    if not np.all(np.isfinite(data)):
        raise ValueError("All values in required columns must be finite")
    if np.any(se_gx <= 0.0):
        raise ValueError("standard_error_beta_gx must be > 0 for all rows")
    if np.any(se_gy <= 0.0):
        raise ValueError("standard_error_beta_gy must be > 0 for all rows")

    if filtering:
        p_values = data[:, 4]
        mask = p_values >= threshold
        beta_gx = beta_gx[mask]
        beta_gy = beta_gy[mask]
        se_gy = se_gy[mask]

    if len(beta_gx) == 0:
        raise ValueError("No instruments remain after filtering")

    return beta_gx, beta_gy, se_gy


@click.command()
@click.option(
    "--input-tsv",
    required=True,
    type=click.Path(exists=True, path_type=Path, file_okay=True, dir_okay=False),
    help="Input TSV file with GWAS summary statistics.",
)
@click.option(
    "--output-tsv",
    required=True,
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    help="Output TSV file with IVW estimation results.",
)
@click.option(
    "--instrument-minus-log10-p-value-threshold",
    type=float,
    default=0.0,
    show_default=True,
    help="Minimum -log10(p-value) for instrument selection. 0 means no filtering.",
)
def estimate(
    input_tsv: Path,
    output_tsv: Path,
    instrument_minus_log10_p_value_threshold: float,
) -> None:
    """Estimate causal effects using the Inverse-Variance Weighted (IVW) estimator."""
    beta_gx, beta_gy, se_gy = _read_input(input_tsv, instrument_minus_log10_p_value_threshold)
    result = ivw_estimate(beta_gx, beta_gy, se_gy)

    columns = [
        "instrument_minus_log10_p_value_threshold",
        "num_instruments",
        "beta",
        "standard_error",
        "minus_log10_p_value",
    ]
    values = [
        str(instrument_minus_log10_p_value_threshold),
        str(result.num_instruments),
        str(result.beta),
        str(result.standard_error),
        str(result.minus_log10_p_value),
    ]
    with open(output_tsv, "w") as f:
        f.write("\t".join(columns) + "\n")
        f.write("\t".join(values) + "\n")

    click.echo(
        f"IVW estimate: beta={result.beta:.6f}, SE={result.standard_error:.6f}, "
        f"-log10(p)={result.minus_log10_p_value:.4f}, n_instruments={result.num_instruments}"
    )


if __name__ == "__main__":
    estimate()
