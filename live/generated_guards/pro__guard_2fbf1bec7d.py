def guard(features: dict, prediction: str) -> str:
    """Guard against trades at Bollinger Band extremes with high volatility - potential reversals."""
    bb_pos = features.get("bb_position", 0.5)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.0)
    
    # Reject trades when price is at extreme BB position AND volatility is elevated
    # This catches potential reversal setups rather than continuation trades
    at_extreme = bb_pos > 0.92 or bb_pos < 0.08
    high_volatility = atr_ratio > 1.3
    
    if at_extreme and high_volatility:
        return "skip"
    
    # Also reject when BB is contracted (low width) with extreme position - consolidation break trap
    contracted = bb_width < 0.5
    if at_extreme and contracted:
        return "skip"
    
    return prediction