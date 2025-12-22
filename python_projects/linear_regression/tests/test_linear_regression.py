from click.testing import CliRunner

from linear_regression.linear_regression import linear_regression


def test_simple_case(tmp_path):
    input_tsv = tmp_path / "input.tsv"
    with open(input_tsv, "w") as f:
        f.write("1\t2\n2\t3\n3\t4\n")

    output_tsv = tmp_path / "output.tsv"

    runner = CliRunner()
    result = runner.invoke(
        linear_regression,
        [f"--input-tsv={input_tsv.resolve()}", f"--output-tsv={output_tsv.resolve()}"],
    )
    assert result.exit_code == 0
    assert output_tsv.is_file()
    expected_output = [
        "beta_1\t1.0\n",
        "var_beta_1\t0.0\n",
        "beta_1_conf_low\t1.0\n",
        "beta_1_conf_high\t1.0\n",
        "beta_1_p_value\t0.0\n",
        "beta_0\t1.0\n",
        "var_beta_0\t0.0\n",
        "beta_0_conf_low\t1.0\n",
        "beta_0_conf_high\t1.0\n",
        "beta_0_p_value\t0.0\n",
        "r_squared\t1.0\n",
    ]
    with open(output_tsv) as f:
        lines = f.readlines()
        for e in expected_output:
            assert e in lines
