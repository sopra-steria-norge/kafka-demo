from importlib.metadata import PackageNotFoundError, version

"""The version string of f1 (PEP 440 / SemVer compatible)."""
__version__: str

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"

"""The decomposed version, split across "``.``."

Use this for version comparison.
"""
version_info: list[str] = __version__.split(".")

__all__ = ["__version__", "version_info"]
