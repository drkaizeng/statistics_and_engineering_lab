# Simulations

Run repeated simulations to validate the IVW estimator.

## Usage

```bash
uv run --group simulations python simulations/do_simulations.py config.json
```

## Config JSON schema

```json
{
  "run_simulation": {
    "exposure_heritability": 0.5,
    "exposure_num_causal_variants": 1000,
    "num_instrumental_variables": 50,
    "exposure_sample_size": 10000,
    "outcome_sample_size": 10000,
    "percent_outcome_variance_explained_by_exposure": 10.0,
    "af_lower": 0.01,
    "af_upper": 0.99,
    "minus_log10_p_threshold": 0.0
  },
  "num_repetitions": 100,
  "seed": 42,
  "output_tsv": "simulations/results.tsv",
  "beta_histogram_png": "simulations/beta_histogram.png",
  "p_value_histogram_png": "simulations/p_value_histogram.png"
}
```

### `run_simulation` (required)

Parameters passed directly to `run_simulation()`.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `exposure_heritability` | float | Yes | — | Heritability of the exposure (h²_X) |
| `exposure_num_causal_variants` | int | Yes | — | Number of causal variants (L_X) |
| `num_instrumental_variables` | int | Yes | — | Number of instrumental variables (L_IV) |
| `exposure_sample_size` | int | Yes | — | Exposure GWAS sample size (n_X) |
| `outcome_sample_size` | int | Yes | — | Outcome GWAS sample size (n_Y) |
| `percent_outcome_variance_explained_by_exposure` | float | Yes | — | % of outcome variance explained by exposure |
| `af_lower` | float | No | 0.01 | Lower bound of allele frequency range |
| `af_upper` | float | No | 0.99 | Upper bound of allele frequency range |
| `minus_log10_p_threshold` | float | No | 0.0 | IV filtering threshold during simulation. 0 = no filtering |

### Top-level fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `num_repetitions` | int | Yes | — | Number of simulation repetitions |
| `seed` | int | No | None | Random seed for reproducibility |
| `output_tsv` | string | Yes | — | Path to output TSV file |
| `beta_histogram_png` | string | Yes | — | Path to beta estimate histogram PNG |
| `p_value_histogram_png` | string | Yes | — | Path to p-value histogram PNG |

## Output

- **TSV**: One row per repetition with columns `num_instruments`, `beta`, `standard_error`, `minus_log10_p_value`.
- **Beta histogram**: Distribution of IVW beta estimates with a vertical line at the true causal effect.
- **P-value histogram**: Distribution of p-values with a vertical line at p = 0.05.
