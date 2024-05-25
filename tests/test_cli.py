from unittest.mock import patch

from click.testing import CliRunner

import teufa.cli


@patch("teufa.server.Application.run")
def test_cli_server(mock_run):
    runner = CliRunner()

    result = runner.invoke(teufa.cli.server)
    assert result.exit_code == 0

    mock_run.assert_called_once_with()


@patch("teufa.server.Application")
def test_cli_server_dev(MockApplication):
    runner = CliRunner()

    result = runner.invoke(teufa.cli.server, ["--dev"])
    assert result.exit_code == 0

    MockApplication.assert_called_once_with(
        {
            "bind": "0.0.0.0:8000",
            "reload": True,
        }
    )
    MockApplication.return_value.run.assert_called_once_with()
