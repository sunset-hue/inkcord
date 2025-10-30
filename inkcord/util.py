"""Helper functions for internal and external purposes."""


# don't modify __version__ it's automatically supplied by the set_semver function
def _set_semver(
    breaking: tuple[int, int],
    non_breaking: tuple[int, int],
    minor: tuple[int, int],
):
    """
    Formats a semver version compatible with the semver specifications.
    The arguments are tuples just to specify order, they stay at the order 0,1,2 for all arguments respectively.
    """
    version = __version__.split(".")
    for i in [breaking, non_breaking, minor]:
        version[i[1]] = str(i[0])

    return "".join(version)


__version__: str = "0.0.0"
