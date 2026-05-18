import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names to lowercase with underscores.

    Converts all column names to lowercase and strips leading or trailing
    whitespace. Preserves existing underscores. Returns a copy of the
    DataFrame with renamed columns.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose column names will be standardized.

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with standardized column names.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply project-specific missing value handling decisions.

    Drops duplicate rows and rows missing values in columns that are
    essential for analysis: name, genre, publisher, and year_of_release.
    Review-related columns (critic_score, critic_count, user_score,
    user_count, rating) retain NaN because their missingness is systematic
    and era-driven rather than a data error. Dropping those rows would
    eliminate nearly all pre-2000 titles and bias the dataset toward the
    modern era.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to apply missing value handling to.

    Returns
    -------
    pd.DataFrame
        A cleaned copy with duplicates and essential-field nulls removed.
    """
    df = df.copy()

    df = df.drop_duplicates()
    df = df.dropna(subset=['name', 'genre', 'publisher', 'year_of_release'])
    df = df.reset_index(drop=True)

    return df


def clean_column_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correct column data types after missing value handling.

    Converts year_of_release from float64 to int64. The conversion is safe
    at this point because rows with missing year values have already been
    dropped by handle_missing_values. Column names must be standardized via
    clean_column_names before calling this function.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame with columns to type-correct.

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with year_of_release as int64.
    """
    df = df.copy()
    df['year_of_release'] = df['year_of_release'].astype(int)
    return df
