def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using stochastic divergence and momentum confirmation."""
    if prediction == "skip":
        return prediction
    
    stoch_div = abs(features.get('stoch_k', 50) - features.get('stoch_d', 50))
    macd_weak = abs(features.get('macd_histogram', 0)) < 0.0003
    obv_flat = abs(features.get('obv_slope', 0)) < 0.5
    vwap_away = abs(features.get('vwap_deviation', 0)) > 0.01
    
    # False compression: weak momentum + stoch divergence + no volume confirmation
    false_comp = macd_weak and (obv_flat or vwap_away) and stoch_div > 5
    if false_comp:
        return "skip"
    
    return prediction