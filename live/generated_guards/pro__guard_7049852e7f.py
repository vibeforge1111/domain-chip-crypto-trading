def guard(features: dict, prediction: str) -> str:
    # Detect false compression: low volatility but building momentum
    is_compressed = features['atr_ratio'] < 0.7 and features['bb_width'] < 0.15
    if is_compressed:
        # False break risk: momentum heating up in compression
        if features['stoch_k'] > 80 or features['macd_histogram'] > 0.001:
            return "skip"
        # Unstable position: far from VWAP in compression
        if abs(features['vwap_deviation']) > 0.02:
            return "skip"
        # Wider timeframe overbought/oversold
        if features['rsi_2h'] > 70 or features['rsi_2h'] < 30:
            return "skip"
    return prediction