"""Helper functions for internal and external purposes."""

# don't modify __version__ it's automatically supplied by the set_semver function


def _set_semver(
    breaking: int | None,
    non_breaking: int | None,
    minor: int | None,
    specifier: int | None,
):
    version = ""
    if all([breaking is None, non_breaking is None, minor is None]):
        raise ValueError(
            f"_set_semver(): reported failure due to all supplied arguments being None. version is unchanged and stays at {__version__}"
        )


__version__ = _set_semver()
