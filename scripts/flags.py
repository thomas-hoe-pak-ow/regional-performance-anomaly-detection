def iqr_bounds(series, k=1.5):
    """Return (lower, upper) IQR bounds for a numeric Series."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def flag_high_values(df, group_col, value_col, flag_col="high_discount"):
    """Flag rows whose value is above the upper IQR fence of their own group."""
    upper = df.groupby(group_col)[value_col].transform(lambda s: iqr_bounds(s)[1])
    df[flag_col] = df[value_col] > upper
    return df