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


def clean_score_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and convert score columns to appropriate numeric types.

    Replaces 'tbd' placeholder values in the user_score column with NaN
    and converts the column from object to float. This function expects
    column names to already be standardized via clean_column_names.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing score columns to clean.

    Returns
    -------
    pd.DataFrame
        A copy of the input DataFrame with cleaned score columns.
    """
    df = df.copy()
    df['user_score'] = pd.to_numeric(df['user_score'].replace('tbd', pd.NA), errors='coerce')
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply project-specific missing value handling decisions.

    Drops duplicate rows and rows missing values in columns that are
    essential for analysis: name, genre, publisher, and year_of_release.
    Review-related columns (critic_score, critic_count, user_score,
    user_count, developer, rating) retain NaN because their missingness
    is systematic and era-driven rather than a data error. Dropping those
    rows would eliminate nearly all pre-2000 titles and bias the dataset
    toward the modern era. After dropping rows with missing year values,
    the year_of_release column is safely converted from float to integer.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to apply missing value handling to.

    Returns
    -------
    pd.DataFrame
        A cleaned copy with duplicates and essential-field nulls removed
        and year_of_release cast to integer.
    """
    df = df.copy()

    df = df.drop_duplicates()
    df = df.dropna(subset=['name', 'genre', 'publisher', 'year_of_release'])
    df['year_of_release'] = df['year_of_release'].astype(int)
    df = df.reset_index(drop=True)

    return df
