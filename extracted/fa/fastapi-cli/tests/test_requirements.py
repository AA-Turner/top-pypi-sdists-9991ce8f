from pathlib import Path

import pytest
from typer.testing import CliRunner

from fastapi_cli.discover import get_import_data
from fastapi_cli.exceptions import FastAPICLIException

from .utils import changing_dir

runner = CliRunner()

assets_path = Path(__file__).parent / "assets"


def test_no_uvicorn() -> None:
    import uvicorn

    import fastapi_cli.cli

    fastapi_cli.cli.uvicorn = None  # type: ignore[attr-defined, assignment]

    with changing_dir(assets_path):
        result = runner.invoke(fastapi_cli.cli.app, ["dev", "single_file_app.py"])
        assert result.exit_code == 1
        assert result.exception is not None
        assert (
            "Could not import Uvicorn, try running 'pip install uvicorn'"
            in result.exception.args[0]
        )

    fastapi_cli.cli.uvicorn = uvicorn  # type: ignore[attr-defined]


def test_no_fastapi() -> None:
    from fastapi import FastAPI

    import fastapi_cli.discover

    fastapi_cli.discover.FastAPI = None  # type: ignore[attr-defined, assignment]
    with changing_dir(assets_path):
        with pytest.raises(FastAPICLIException) as exc_info:
            get_import_data(path=Path("single_file_app.py"))
        assert "Could not import FastAPI, try running 'pip install fastapi'" in str(
            exc_info.value
        )

    fastapi_cli.discover.FastAPI = FastAPI  # type: ignore[attr-defined]
