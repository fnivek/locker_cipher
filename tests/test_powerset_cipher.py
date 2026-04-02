from click.testing import CliRunner

from locker_cipher.cli.powerset_cipher import main


def test_powerset_cli() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["f3", "1", "2", "3"])

    assert result.exit_code == 0
    assert "F3: 1 --> 111" in result.output
    assert "F3: 2 --> 117" in result.output
    assert "F3: 3 --> 115" in result.output
    assert "F3: 1+2 (3) --> 115" in result.output
    assert "F3: 1+3 (4) --> 101" in result.output
    assert "F3: 2+3 (5) --> 97" in result.output
    assert "F3: 1+2+3 (6) --> 105" in result.output
