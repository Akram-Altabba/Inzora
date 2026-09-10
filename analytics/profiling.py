"""
analytics/profiling.py

Dataset profiling: produces a structural summary of a CSV dataset —
row/column counts, per-column dtypes, missing values, duplicates, and
unique value counts.

Scope note: this module describes what a dataset IS. It does not judge
whether those numbers are good or bad (that's quality.py) and it does
not generate findings (that's insights.py). Keeping this boundary clean
keeps each module simple and independently testable.
"""

from pathlib import Path
from typing import Union

import pandas as pd


class ProfilingError(Exception):
    """Raised when a dataset cannot be loaded or profiled. Message is
    written to be shown directly to a user, not just logged."""
    pass


def load_csv(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame with basic validation.

    Raises ProfilingError with a user-facing message on failure, so the
    API layer can return it directly without translation.
    """
    path = Path(filepath)

    if not path.exists():
        raise ProfilingError(f"File not found: {filepath}")
    if path.suffix.lower() != ".csv":
        raise ProfilingError(f"Expected a .csv file, got: '{path.suffix}'")

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ProfilingError("The CSV file is empty.")
    except pd.errors.ParserError as e:
        raise ProfilingError(f"Could not parse CSV file: {e}")
    except UnicodeDecodeError:
        raise ProfilingError(
            "Could not read file encoding. Please save the file as UTF-8 and try again."
        )

    if df.shape[1] == 0:
        raise ProfilingError("The CSV file has no columns.")
    if df.shape[0] == 0:
        raise ProfilingError("The CSV file has no data rows.")

    return df


def profile_dataset(df: pd.DataFrame) -> dict:
    """
    Generate a structural profile of a DataFrame.

    Returns a dict with dataset-level stats and a per-column breakdown.
    Takes a DataFrame directly (not a filepath) so this function can be
    unit-tested with in-memory data, independent of file I/O.
    """
    n_rows, n_cols = df.shape

    column_profiles = {col: _profile_column(df[col]) for col in df.columns}
    duplicate_count = int(df.duplicated().sum())

    return {
        "n_rows": n_rows,
        "n_columns": n_cols,
        "column_names": list(df.columns),
        "duplicate_rows": duplicate_count,
        "duplicate_row_pct": _pct(duplicate_count, n_rows),
        "columns": column_profiles,
    }


def profile_csv(filepath: Union[str, Path]) -> dict:
    """Convenience wrapper: load a CSV and profile it in one call."""
    df = load_csv(filepath)
    return profile_dataset(df)


def _profile_column(series: pd.Series) -> dict:
    """Generate a structural profile for a single column."""
    n = len(series)
    missing = int(series.isna().sum())
    unique = int(series.nunique(dropna=True))

    return {
        "dtype": _classify_dtype(series),
        "pandas_dtype": str(series.dtype),
        "missing_count": missing,
        "missing_pct": _pct(missing, n),
        "unique_count": unique,
        "unique_pct": _pct(unique, n),
    }


def _classify_dtype(series: pd.Series) -> str:
    """
    Classify a column into a simplified type category used by downstream
    modules (chart recommendation, insight generation): 'numeric',
    'boolean', 'datetime', or 'categorical'.

    Known limitation: pandas does NOT auto-detect date-like strings on a
    raw CSV read — a date column will land here as 'categorical' unless
    it was explicitly parsed as a date beforehand. Auto-sniffing date
    formats is deliberately out of scope for now (format/locale
    ambiguity, false positives on numeric strings); this is a candidate
    enhancement once the insight engine's trend detection needs it.
    """
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    return "categorical"


def _pct(count: int, total: int) -> float:
    """Safe percentage helper — avoids division by zero, rounds to 2dp."""
    return round(count / total * 100, 2) if total else 0.0