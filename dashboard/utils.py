import pandas as pd


def format_currency(value):
    """Format large currency values into readable Indian-Rupee shorthand."""

    if pd.isna(value):
        return "₹ 0.00"

    value = float(value)
    sign = "-" if value < 0 else ""
    value = abs(value)

    if value >= 1_000_000_000_000:
        return f"{sign}₹ {value/1_000_000_000_000:.2f} T"
    elif value >= 1_000_000_000:
        return f"{sign}₹ {value/1_000_000_000:.2f} B"
    elif value >= 1_000_000:
        return f"{sign}₹ {value/1_000_000:.2f} M"
    elif value >= 1_000:
        return f"{sign}₹ {value/1_000:.2f} K"

    return f"{sign}₹ {value:.2f}"


def format_number(value):
    """Format large plain counts into readable shorthand (1.2K, 3.4M, ...)."""

    if pd.isna(value):
        return "0"

    value = float(value)

    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value/1_000:.2f}K"

    return f"{value:,.0f}"


def safe_ratio(numerator, denominator):
    """Return a percentage, guarding against division by zero."""

    if not denominator:
        return 0.0

    return (numerator / denominator) * 100