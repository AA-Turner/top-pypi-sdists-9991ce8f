"""Feature Flags Module.

This module implements a feature flag system for the wandb library to require experimental features
and notify the user when features have been deprecated.

Example:
    import wandb
    wandb.require("wandb-service@beta")
    wandb.require("incremental-artifacts@beta")
"""

from __future__ import annotations

import os
from typing import Iterable

import wandb
from wandb.env import _REQUIRE_LEGACY_SERVICE
from wandb.errors import UnsupportedError
from wandb.sdk import wandb_run


class _Requires:
    """Internal feature class."""

    _features: tuple[str, ...]

    def __init__(self, features: str | Iterable[str]) -> None:
        self._features = (
            tuple([features]) if isinstance(features, str) else tuple(features)
        )

    def require_require(self) -> None:
        pass

    def _require_service(self) -> None:
        wandb.teardown = wandb._teardown  # type: ignore
        wandb.attach = wandb._attach  # type: ignore
        wandb_run.Run.detach = wandb_run.Run._detach  # type: ignore

    def require_service(self) -> None:
        self._require_service()

    def require_core(self) -> None:
        wandb.termwarn(
            "`wandb.require('core')` is redundant as it is now the default behavior."
        )

    def require_legacy_service(self) -> None:
        os.environ[_REQUIRE_LEGACY_SERVICE] = "true"

    def apply(self) -> None:
        """Call require_* method for supported features."""
        last_message: str = ""
        for feature_item in self._features:
            full_feature = feature_item.split("@", 2)[0]
            feature = full_feature.split(":", 2)[0]
            func_str = "require_{}".format(feature.replace("-", "_"))
            func = getattr(self, func_str, None)
            if not func:
                last_message = f"require() unsupported requirement: {feature}"
                wandb.termwarn(last_message)
                continue
            func()

        if last_message:
            wandb.termwarn("Supported requirements are: `legacy-service`, `service`.")
            raise UnsupportedError(last_message)


def require(
    requirement: str | Iterable[str] | None = None,
    experiment: str | Iterable[str] | None = None,
) -> None:
    """Indicate which experimental features are used by the script.

    This should be called before any other `wandb` functions, ideally right
    after importing `wandb`.

    Args:
        requirement: The name of a feature to require or an iterable of
            feature names.
        experiment: An alias for `requirement`.

    Raises:
        wandb.errors.UnsupportedError: If a feature name is unknown.
    """
    features = requirement or experiment
    if not features:
        return

    f = _Requires(features=features)
    f.apply()


def _import_module_hook() -> None:
    """On wandb import, setup anything needed based on parent process require calls."""
    # TODO: optimize by caching which pids this has been done for or use real import hooks
    # TODO: make this more generic, but for now this works
    require("service")
