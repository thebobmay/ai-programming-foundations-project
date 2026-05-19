import pandas as pd


def summarize_game_market(df: pd.DataFrame) -> dict:
    """
    Return grouped summaries for genre, platform, sales, and rating patterns.

    Computes game counts, total and mean global sales by genre and platform,
    and mean critic and user scores by genre and platform for reviewed titles
    only. Score summaries exclude rows where either critic_score or user_score
    is missing so that averages reflect the same pool of games across both
    metrics.

    Parameters
    ----------
    df : pd.DataFrame
        A cleaned game market DataFrame with columns including name, genre,
        platform, global_sales, critic_score, and user_score.

    Returns
    -------
    dict
        A dictionary with four keys:
        - 'genre_counts'    : game count, total and mean global sales by genre
        - 'platform_counts' : game count, total and mean global sales by platform
        - 'genre_scores'    : mean critic and user scores by genre
        - 'platform_scores' : mean critic and user scores by platform
    """
    genre_counts = (
        df.groupby('genre')
        .agg(
            game_count=('name', 'count'),
            total_global_sales=('global_sales', 'sum'),
            mean_global_sales=('global_sales', 'mean'),
        )
        .round(2)
        .sort_values('game_count', ascending=False)
    )

    platform_counts = (
        df.groupby('platform')
        .agg(
            game_count=('name', 'count'),
            total_global_sales=('global_sales', 'sum'),
            mean_global_sales=('global_sales', 'mean'),
        )
        .round(2)
        .sort_values('game_count', ascending=False)
    )

    reviewed = df.dropna(subset=['critic_score', 'user_score'])

    genre_scores = (
        reviewed.groupby('genre')
        .agg(
            mean_critic_score=('critic_score', 'mean'),
            mean_user_score=('user_score', 'mean'),
            reviewed_game_count=('name', 'count'),
        )
        .round(2)
        .sort_values('mean_critic_score', ascending=False)
    )

    platform_scores = (
        reviewed.groupby('platform')
        .agg(
            mean_critic_score=('critic_score', 'mean'),
            mean_user_score=('user_score', 'mean'),
            reviewed_game_count=('name', 'count'),
        )
        .round(2)
        .sort_values('mean_critic_score', ascending=False)
    )

    return {
        'genre_counts': genre_counts,
        'platform_counts': platform_counts,
        'genre_scores': genre_scores,
        'platform_scores': platform_scores,
    }
