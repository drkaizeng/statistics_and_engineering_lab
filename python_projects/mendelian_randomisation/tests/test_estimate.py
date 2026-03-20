from math import sqrt
from pathlib import Path

import numpy as np
import pytest
from click.testing import CliRunner

from mendelian_randomisation.estimate import estimate, ivw_estimate


def _write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with open(path, "w") as f:
        f.write("\t".join(header) + "\n")
        for row in rows:
            f.write("\t".join(row) + "\n")


class TestIVWEstimate:
    def test_single_variant(self) -> None:
        beta_gx = np.array([0.5])
        beta_gy = np.array([0.15])
        se_gy = np.array([0.1])
        result = ivw_estimate(beta_gx, beta_gy, se_gy)
        assert result.beta == pytest.approx(0.15 / 0.5, rel=1e-10)
        assert result.num_instruments == 1

    def test_known_values(self) -> None:
        beta_gx = np.array([0.3, 0.5, 0.4])
        beta_gy = np.array([0.09, 0.16, 0.13])
        se_gy = np.array([0.05, 0.08, 0.06])

        weights = beta_gx**2 / se_gy**2
        expected_beta = np.sum(beta_gx * beta_gy / se_gy**2) / np.sum(weights)
        expected_se = sqrt(1.0 / np.sum(weights))

        result = ivw_estimate(beta_gx, beta_gy, se_gy)
        assert result.beta == pytest.approx(expected_beta, rel=1e-10)
        assert result.standard_error == pytest.approx(expected_se, rel=1e-10)
        assert result.num_instruments == 3
        assert result.minus_log10_p_value > 0.0

    def test_empty_arrays(self) -> None:
        with pytest.raises(ValueError, match="No instruments"):
            ivw_estimate(np.array([]), np.array([]), np.array([]))

    def test_mismatched_lengths(self) -> None:
        with pytest.raises(ValueError, match="lengths must match"):
            ivw_estimate(np.array([0.1, 0.2]), np.array([0.1]), np.array([0.1]))


class TestReadInputAndCli:
    def test_basic_cli(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(
            input_path,
            ["beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy"],
            [["0.3", "0.09", "0.01", "0.05"], ["0.5", "0.16", "0.01", "0.08"]],
        )
        runner = CliRunner()
        result = runner.invoke(estimate, ["--input-tsv", str(input_path), "--output-tsv", str(output_path)])
        assert result.exit_code == 0
        lines = output_path.read_text().strip().split("\n")
        assert len(lines) == 2
        header = lines[0].split("\t")
        assert header == [
            "instrument_minus_log10_p_value_threshold",
            "num_instruments",
            "beta",
            "standard_error",
            "minus_log10_p_value",
        ]
        values = lines[1].split("\t")
        assert values[0] == "0.0"
        assert values[1] == "2"

    def test_p_value_filtering(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(
            input_path,
            ["beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy", "minus_log10_p_value_beta_gx"],
            [
                ["0.3", "0.09", "0.01", "0.05", "10.0"],
                ["0.5", "0.16", "0.01", "0.08", "2.0"],
                ["0.4", "0.13", "0.01", "0.06", "8.0"],
            ],
        )
        runner = CliRunner()
        result = runner.invoke(
            estimate,
            [
                "--input-tsv",
                str(input_path),
                "--output-tsv",
                str(output_path),
                "--instrument-minus-log10-p-value-threshold",
                "5.0",
            ],
        )
        assert result.exit_code == 0
        lines = output_path.read_text().strip().split("\n")
        values = lines[1].split("\t")
        assert values[0] == "5.0"
        assert values[1] == "2"

    def test_missing_column(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(input_path, ["beta_gx", "beta_gy"], [["0.3", "0.09"]])
        runner = CliRunner()
        result = runner.invoke(estimate, ["--input-tsv", str(input_path), "--output-tsv", str(output_path)])
        assert result.exit_code != 0

    def test_threshold_without_p_column(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(
            input_path,
            ["beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy"],
            [["0.3", "0.09", "0.01", "0.05"]],
        )
        runner = CliRunner()
        result = runner.invoke(
            estimate,
            [
                "--input-tsv",
                str(input_path),
                "--output-tsv",
                str(output_path),
                "--instrument-minus-log10-p-value-threshold",
                "5.0",
            ],
        )
        assert result.exit_code != 0

    def test_no_instruments_after_filtering(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(
            input_path,
            ["beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy", "minus_log10_p_value_beta_gx"],
            [["0.3", "0.09", "0.01", "0.05", "1.0"]],
        )
        runner = CliRunner()
        result = runner.invoke(
            estimate,
            [
                "--input-tsv",
                str(input_path),
                "--output-tsv",
                str(output_path),
                "--instrument-minus-log10-p-value-threshold",
                "5.0",
            ],
        )
        assert result.exit_code != 0

    def test_negative_standard_error(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(
            input_path,
            ["beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy"],
            [["0.3", "0.09", "0.01", "-0.05"]],
        )
        runner = CliRunner()
        result = runner.invoke(estimate, ["--input-tsv", str(input_path), "--output-tsv", str(output_path)])
        assert result.exit_code != 0

    def test_extra_columns_ignored(self, tmp_path: Path) -> None:
        input_path = tmp_path / "input.tsv"
        output_path = tmp_path / "output.tsv"
        _write_tsv(
            input_path,
            ["extra_col", "beta_gx", "beta_gy", "standard_error_beta_gx", "standard_error_beta_gy", "another"],
            [["999", "0.3", "0.09", "0.01", "0.05", "abc"]],
        )
        runner = CliRunner()
        result = runner.invoke(estimate, ["--input-tsv", str(input_path), "--output-tsv", str(output_path)])
        assert result.exit_code == 0
