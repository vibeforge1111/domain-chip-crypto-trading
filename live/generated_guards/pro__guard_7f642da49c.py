def guard(features: dict, prediction: str) -> str:
    # Detect false compression: tight bands but extreme conditions suggest failed breakout
    if features['atr_ratio'] < 0.7 and features['bb_width'] < 0.15:
        # Stochastic extreme at BB edge indicates reversal likely
        if (features['stoch_k'] > 80 and features['bb_pct_b'] > 0.9) or \
           (features['stoch_k'] < 20 and features['bb_pct_b'] < 0.1):
            return "skip"
        # Momentum divergence during compression signals false move
        if features['macd_histogram'] * (1 if prediction == "long" else -1) < -0.0005:
            return "skip"
    return prediction