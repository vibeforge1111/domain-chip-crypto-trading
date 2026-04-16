def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    
    Focus: Detect true vs false compression using atr_ratio + bb_width + new features
    """
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    macd_histogram = features.get('macd_histogram', 0.0)
    
    # False compression: high volatility but tight bands = reject
    if atr_ratio > 1.2 and bb_width < 0.15:
        return "skip"
    
    # Extreme stochastic readings suggest exhaustion
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    # 2h RSI overbought/oversold with compression = likely reversal trap
    if bb_width < 0.15 and (rsi_2h > 70 or rsi_2h < 30):
        return "skip"
    
    return prediction