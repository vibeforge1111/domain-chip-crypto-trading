def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts with divergent structure."""
    # True compression detected
    if features['atr_ratio'] < 0.75 and features['bb_width'] < 0.35:
        # Price at band extreme with stoch divergence
        if features['bb_pct_b'] < 0.12 or features['bb_pct_b'] > 0.88:
            if features['stoch_k'] < 20 or features['stoch_k'] > 80:
                # MACD histogram opposing the move
                if features['macd_histogram'] < -0.0003:
                    return "skip"
                # Weak 2h RSI confirmation
                if features['rsi_2h'] < 40 or features['rsi_2h'] > 60:
                    return "skip"
    return prediction