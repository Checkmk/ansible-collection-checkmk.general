# Noxfile for the checkmk.general collection.
#
# The session configuration lives in antsibull-nox.toml. At the moment only the
# execution environment check is wired up here; the remaining test matrices are
# still driven by the workflows in .github/workflows/.

# /// script
# dependencies = ["nox>=2025.02.09", "antsibull-nox"]
# ///

import sys

import nox  # type: ignore[import-not-found]

try:
    import antsibull_nox  # type: ignore[import-not-found]
except ImportError:
    print("You need to install antsibull-nox in the same Python environment as nox.")
    sys.exit(1)


antsibull_nox.load_antsibull_nox_toml()


# Allow to run the noxfile with `python noxfile.py`, `pipx run noxfile.py`, or similar.
# Requires nox >= 2025.02.09
if __name__ == "__main__":
    nox.main()
