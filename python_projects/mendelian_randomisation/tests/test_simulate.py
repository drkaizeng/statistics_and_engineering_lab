from math import log, sqrt
from pathlib import Path

import numpy as np
import pytest
from click.testing import CliRunner

from mendelian_randomisation.simulate import (
    expected_genotype_variance,
    run_simulation,
    simulate,
)

SEED = 42


class TestExpectedGenotypeVariance:
    def test_default_bounds(self) -> None:
        result = expected_genotype_variance(0.01, 0.99)
        assert result == pytest.approx(0.2133, abs=1e-4)

    def test_symmetric_bounds(self) -> None:
        a, b = 0.1, 0.9
        expected = (2.0 * (b - a) - (b**2 - a**2)) / (log(b) - log(a))
        assert expected_genotype_variance(a, b) == pytest.approx(expected, rel=1e-10)

    def test_narrow_range(self) -> None:
        a, b = 0.49, 0.51
        result = expected_genotype_variance(a, b)
        assert 0.0 < result < 0.5

    def test_invalid_bounds_lower_ge_upper(self) -> None:
        with pytest.raises(ValueError, match="af_lower"):
            expected_genotype_variance(0.5, 0.5)

    def test_invalid_bounds_zero(self) -> None:
        with pytest.raises(ValueError, match="af_lower"):
            expected_genotype_variance(0.0, 0.5)

    def test_invalid_bounds_one(self) -> None:
        with pytest.raises(ValueError, match="af_lower"):
            expected_genotype_variance(0.01, 1.0)


class TestRunSimulation:
    def test_output_shape_no_filtering(self) -> None:
        result = run_simulation(
            exposure_heritability=0.5,
            exposure_num_causal_variants=1000,
            num_instrumental_variables=50,
            exposure_sample_size=10000,
            outcome_sample_size=10000,
            percent_outcome_variance_explained_by_exposure=10.0,
            seed=SEED,
        )
        assert len(result) == 50

    def test_output_columns(self) -> None:
        result = run_simulation(
            exposure_heritability=0.5,
            exposure_num_causal_variants=1000,
            num_instrumental_variables=10,
            exposure_sample_size=10000,
            outcome_sample_size=10000,
            percent_outcome_variance_explained_by_exposure=10.0,
            seed=SEED,
        )
        expected_columns = [
            "effect_allele_frequency",
            "true_beta_gx",
            "true_beta_gy",
            "beta_gx",
            "beta_gy",
            "standard_error_beta_gx",
            "standard_error_beta_gy",
            "minus_log10_p_value_beta_gx",
            "minus_log10_p_value_beta_gy",
        ]
        assert list(result.dtype.names) == expected_columns

    def test_concrete_example_sigma2_gx(self) -> None:
        e_var = expected_genotype_variance(0.01, 0.99)
        sigma2_gx = 0.5 / (1000 * e_var)
        assert sigma2_gx == pytest.approx(0.002344, abs=1e-4)

    def test_concrete_example_beta_xy(self) -> None:
        beta_xy = sqrt(10.0 / 100.0)
        assert beta_xy == pytest.approx(0.3162, abs=1e-4)

    def test_allele_frequencies_within_bounds(self) -> None:
        result = run_simulation(
            exposure_heritability=0.5,
            exposure_num_causal_variants=1000,
            num_instrumental_variables=500,
            exposure_sample_size=10000,
            outcome_sample_size=10000,
            percent_outcome_variance_explained_by_exposure=10.0,
            af_lower=0.05,
            af_upper=0.95,
            seed=SEED,
        )
        assert np.all(result["effect_allele_frequency"] >= 0.05)
        assert np.all(result["effect_allele_frequency"] <= 0.95)

    def test_p_value_filtering(self) -> None:
        result = run_simulation(
            exposure_heritability=0.5,
            exposure_num_causal_variants=1000,
            num_instrumental_variables=20,
            exposure_sample_size=100000,
            outcome_sample_size=100000,
            percent_outcome_variance_explained_by_exposure=10.0,
            minus_log10_p_threshold=5.0,
            seed=SEED,
        )
        assert len(result) == 20
        assert np.all(result["minus_log10_p_value_beta_gx"] >= 5.0)

    def test_p_values_in_valid_range(self) -> None:
        result = run_simulation(
            exposure_heritability=0.5,
            exposure_num_causal_variants=1000,
            num_instrumental_variables=100,
            exposure_sample_size=10000,
            outcome_sample_size=10000,
            percent_outcome_variance_explained_by_exposure=10.0,
            seed=SEED,
        )
        assert np.all(result["minus_log10_p_value_beta_gx"] >= 0.0)
        assert np.all(result["minus_log10_p_value_beta_gy"] >= 0.0)

    def test_reproducibility_with_seed(self) -> None:
        kwargs = {
            "exposure_heritability": 0.5,
            "exposure_num_causal_variants": 1000,
            "num_instrumental_variables": 50,
            "exposure_sample_size": 10000,
            "outcome_sample_size": 5000,
            "percent_outcome_variance_explained_by_exposure": 10.0,
            "seed": 123,
        }
        r1 = run_simulation(**kwargs)
        r2 = run_simulation(**kwargs)
        np.testing.assert_array_equal(r1["beta_gx"], r2["beta_gx"])

    def test_invalid_heritability(self) -> None:
        with pytest.raises(ValueError, match="exposure_heritability"):
            run_simulation(
                exposure_heritability=0.0,
                exposure_num_causal_variants=100,
                num_instrumental_variables=10,
                exposure_sample_size=1000,
                outcome_sample_size=1000,
                percent_outcome_variance_explained_by_exposure=10.0,
            )

    def test_invalid_percent_variance(self) -> None:
        with pytest.raises(ValueError, match="percent_outcome"):
            run_simulation(
                exposure_heritability=0.5,
                exposure_num_causal_variants=100,
                num_instrumental_variables=10,
                exposure_sample_size=1000,
                outcome_sample_size=1000,
                percent_outcome_variance_explained_by_exposure=0.0,
            )


class TestSimulateCli:
    def test_basic_invocation(self, tmp_path: Path) -> None:
        output = tmp_path / "output.tsv"
        runner = CliRunner()
        result = runner.invoke(
            simulate,
            [
                "--exposure-heritability",
                "0.5",
                "--exposure-num-causal-variants",
                "1000",
                "--num-instrumental-variables",
                "50",
                "--exposure-sample-size",
                "10000",
                "--outcome-sample-size",
                "10000",
                "--percent-outcome-variance-explained-by-exposure",
                "10",
                "--output-tsv",
                str(output),
                "--seed",
                "42",
            ],
        )
        assert result.exit_code == 0
        assert output.exists()
        lines = output.read_text().strip().split("\n")
        assert len(lines) == 51  # header + 50 data rows
        assert lines[0].split("\t")[0] == "effect_allele_frequency"

    def test_missing_required_flag(self) -> None:
        runner = CliRunner()
        result = runner.invoke(simulate, ["--exposure-heritability", "0.5"])
        assert result.exit_code != 0
