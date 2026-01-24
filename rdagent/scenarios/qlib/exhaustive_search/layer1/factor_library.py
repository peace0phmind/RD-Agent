"""
Factor library for Layer 1 exhaustive search
"""
import json
from pathlib import Path
from typing import Dict, List


class FactorLibrary:
    """Manage factor definitions from multiple sources"""

    def __init__(self):
        """Initialize factor library"""
        self._factors = None
        self.load_all_factors()

    def load_all_factors(self):
        """Load factors from all sources"""
        all_factors = []

        # Source 1: Alpha158 baseline
        all_factors.extend(self.get_alpha158_factors())

        # Source 2: Custom research factors
        all_factors.extend(self.get_custom_research_factors())

        # Remove duplicates by name
        seen = set()
        unique_factors = []
        for factor in all_factors:
            if factor["name"] not in seen:
                seen.add(factor["name"])
                unique_factors.append(factor)

        self._factors = unique_factors

    def get_alpha158_factors(self) -> List[Dict]:
        """
        Get Alpha158 baseline factors (20 factors)

        These are the baseline factors used in RD-Agent
        Reference: rdagent/scenarios/qlib/factor_template/conf_baseline.yaml
        """
        # Alpha158 baseline factors
        factors = [
            # Price momentum factors
            {
                "name": "RESI5",
                "description": "5-day price residual",
                "formula": "RESI(close, 5)",
                "category": "momentum"
            },
            {
                "name": "RESI10",
                "description": "10-day price residual",
                "formula": "RESI(close, 10)",
                "category": "momentum"
            },
            {
                "name": "ROC60",
                "description": "60-day rate of change",
                "formula": "ROC(close, 60)",
                "category": "momentum"
            },

            # Volatility factors
            {
                "name": "STD5",
                "description": "5-day standard deviation",
                "formula": "STDDEV(returns, 5)",
                "category": "volatility"
            },
            {
                "name": "VSTD5",
                "description": "5-day volume standard deviation",
                "formula": "STDDEV(volume, 5)",
                "category": "volatility"
            },

            # Correlation factors
            {
                "name": "CORR5",
                "description": "5-day correlation",
                "formula": "CORR(close, volume, 5)",
                "category": "correlation"
            },
            {
                "name": "CORR10",
                "description": "10-day correlation",
                "formula": "CORR(close, volume, 10)",
                "category": "correlation"
            },
            {
                "name": "CORR20",
                "description": "20-day correlation",
                "formula": "CORR(close, volume, 20)",
                "category": "correlation"
            },
            {
                "name": "CORR60",
                "description": "60-day correlation",
                "formula": "CORR(close, volume, 60)",
                "category": "correlation"
            },

            # R-squared factors
            {
                "name": "RSQR5",
                "description": "5-day R-squared",
                "formula": "RSQR(close, 5)",
                "category": "r_squared"
            },
            {
                "name": "RSQR10",
                "description": "10-day R-squared",
                "formula": "RSQR(close, 10)",
                "category": "r_squared"
            },
            {
                "name": "RSQR20",
                "description": "20-day R-squared",
                "formula": "RSQR(close, 20)",
                "category": "r_squared"
            },
            {
                "name": "RSQR60",
                "description": "60-day R-squared",
                "formula": "RSQR(close, 60)",
                "category": "r_squared"
            },

            # Volume-price factors
            {
                "name": "KLEN",
                "description": "K-line length",
                "formula": "high - low",
                "category": "volume_price"
            },
            {
                "name": "KLOW",
                "description": "K-line low position",
                "formula": "(close - low) / (high - low)",
                "category": "volume_price"
            },
            {
                "name": "CORD5",
                "description": "5-day correlation delta",
                "formula": "CORR(close, volume, 5) - CORR(REF(close,1), REF(volume,1), 5)",
                "category": "volume_price"
            },
            {
                "name": "CORD10",
                "description": "10-day correlation delta",
                "formula": "CORR(close, volume, 10) - CORR(REF(close,1), REF(volume,1), 10)",
                "category": "volume_price"
            },
            {
                "name": "CORD60",
                "description": "60-day correlation delta",
                "formula": "CORR(close, volume, 60) - CORR(REF(close,1), REF(volume,1), 60)",
                "category": "volume_price"
            },
            {
                "name": "WVMA5",
                "description": "5-day volume-weighted MA",
                "formula": "WMA(close, volume, 5)",
                "category": "volume_price"
            },
            {
                "name": "WVMA60",
                "description": "60-day volume-weighted MA",
                "formula": "WMA(close, volume, 60)",
                "category": "volume_price"
            },
        ]

        return factors

    def get_custom_research_factors(self) -> List[Dict]:
        """
        Get custom research factors from previous experiments

        These factors showed promising results in our experiments
        """
        factors = [
            # Best factor from experiments
            {
                "name": "Price_Distance_Z_5D",
                "description": "5-day price distance Z-score",
                "formula": "(close - SMA(close, 5)) / (STDDEV(close, 5) + 1e-10)",
                "category": "statistical",
                "source": "experiment_20260123",
                "best_ic": 0.102156
            },
            {
                "name": "Price_Distance_Z_10D",
                "description": "10-day price distance Z-score",
                "formula": "(close - SMA(close, 10)) / (STDDEV(close, 10) + 1e-10)",
                "category": "statistical",
                "source": "experiment_20260123",
                "best_ic": 0.100
            },
            {
                "name": "Price_Distance_Z_20D",
                "description": "20-day price distance Z-score",
                "formula": "(close - SMA(close, 20)) / (STDDEV(close, 20) + 1e-10)",
                "category": "statistical",
                "source": "experiment_20260123",
                "best_ic": 0.098
            },

            # Volume-price trend factors
            {
                "name": "VPT_5D",
                "description": "5-day volume price trend",
                "formula": "SUM((close - REF(close,1))/REF(close,1) * volume, 5)",
                "category": "volume_momentum",
                "source": "experiment_20260123",
                "best_ic": 0.095
            },
            {
                "name": "VPT_10D",
                "description": "10-day volume price trend",
                "formula": "SUM((close - REF(close,1))/REF(close,1) * volume, 10)",
                "category": "volume_momentum",
                "source": "experiment_20260123",
                "best_ic": 0.094
            },

            # On-balance volume
            {
                "name": "OBV_5D",
                "description": "5-day on-balance volume",
                "formula": "SUM(SIGN(close - REF(close,1)) * volume, 5)",
                "category": "volume_momentum",
                "source": "experiment_20260123",
                "best_ic": 0.095
            },
            {
                "name": "OBV_10D",
                "description": "10-day on-balance volume",
                "formula": "SUM(SIGN(close - REF(close,1)) * volume, 10)",
                "category": "volume_momentum",
                "source": "experiment_20260123",
                "best_ic": 0.094
            },

            # Classic momentum factors
            {
                "name": "Momentum_5D",
                "description": "5-day momentum",
                "formula": "close / REF(close, 5) - 1",
                "category": "momentum",
                "source": "baseline"
            },
            {
                "name": "Momentum_10D",
                "description": "10-day momentum",
                "formula": "close / REF(close, 10) - 1",
                "category": "momentum",
                "source": "baseline"
            },
            {
                "name": "Momentum_20D",
                "description": "20-day momentum",
                "formula": "close / REF(close, 20) - 1",
                "category": "momentum",
                "source": "baseline"
            },

            # Rate of change
            {
                "name": "ROC_5D",
                "description": "5-day rate of change",
                "formula": "(close - REF(close, 5)) / REF(close, 5)",
                "category": "momentum",
                "source": "baseline"
            },
            {
                "name": "ROC_10D",
                "description": "10-day rate of change",
                "formula": "(close - REF(close, 10)) / REF(close, 10)",
                "category": "momentum",
                "source": "baseline"
            },
            {
                "name": "ROC_20D",
                "description": "20-day rate of change",
                "formula": "(close - REF(close, 20)) / REF(close, 20)",
                "category": "momentum",
                "source": "baseline"
            },

            # Volatility factors
            {
                "name": "Volatility_5D",
                "description": "5-day volatility",
                "formula": "STDDEV(close / REF(close, 1) - 1, 5)",
                "category": "volatility",
                "source": "baseline"
            },
            {
                "name": "Volatility_10D",
                "description": "10-day volatility",
                "formula": "STDDEV(close / REF(close, 1) - 1, 10)",
                "category": "volatility",
                "source": "baseline"
            },
            {
                "name": "Volatility_20D",
                "description": "20-day volatility",
                "formula": "STDDEV(close / REF(close, 1) - 1, 20)",
                "category": "volatility",
                "source": "baseline"
            },

            # Volume ratio
            {
                "name": "Volume_Ratio_5D",
                "description": "5-day volume ratio",
                "formula": "volume / SMA(volume, 5)",
                "category": "volume",
                "source": "baseline"
            },
            {
                "name": "Volume_Ratio_20D",
                "description": "20-day volume ratio",
                "formula": "volume / SMA(volume, 20)",
                "category": "volume",
                "source": "baseline"
            },

            # ATR (Average True Range)
            {
                "name": "ATR_5D",
                "description": "5-day average true range",
                "formula": "SMA(MAX(high - low, ABS(high - REF(close,1)), ABS(low - REF(close,1))), 5)",
                "category": "volatility",
                "source": "baseline"
            },
            {
                "name": "ATR_10D",
                "description": "10-day average true range",
                "formula": "SMA(MAX(high - low, ABS(high - REF(close,1)), ABS(low - REF(close,1))), 10)",
                "category": "volatility",
                "source": "baseline"
            },
            {
                "name": "ATR_20D",
                "description": "20-day average true range",
                "formula": "SMA(MAX(high - low, ABS(high - REF(close,1)), ABS(low - REF(close,1))), 20)",
                "category": "volatility",
                "source": "baseline"
            },
        ]

        return factors

    def get_all_factors(self) -> List[Dict]:
        """Get all unique factors from all sources"""
        return self._factors

    def get_factors_by_category(self, category: str) -> List[Dict]:
        """Get factors filtered by category"""
        return [f for f in self._factors if f.get("category") == category]
