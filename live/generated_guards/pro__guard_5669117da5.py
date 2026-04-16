def guard(features: dict, prediction: str) -> str:
    """Filter trades during volatility squeeze with weakening trend - breakout direction is uncertain."""
    if features.get("bb_width", 1) < 0.015 and features.get("trend_strength", 1) < 0.3:
        return "skip"
    return prediction