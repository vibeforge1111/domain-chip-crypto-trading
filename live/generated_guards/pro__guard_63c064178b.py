def guard(features: dict, prediction: str) -> str:
    """Skip trades when both BB and Stochastic confirm overbought/oversold extremes."""
    # Overbought: price near upper BB + stoch confirming (reversal risk for longs)
    if features['bb_pct_b'] > 0.85 and features['stoch_k'] > 80:
        return "skip"
    # Oversold: price near lower BB + stoch confirming (reversal risk for shorts)
    if features['bb_pct_b'] < 0.15 and features['stoch_k'] < 20:
        return "skip"
    return prediction