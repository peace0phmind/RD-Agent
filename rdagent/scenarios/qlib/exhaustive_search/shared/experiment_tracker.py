"""
Experiment tracking system for exhaustive search
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ExperimentTracker:
    """Track all experiments in SQLite database"""

    def __init__(self, db_path: str = "results/experiments.db"):
        """
        Initialize experiment tracker

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.db = sqlite3.connect(str(self.db_path))
        self.db.row_factory = sqlite3.Row  # Enable column access by name
        self.init_schema()

    def init_schema(self):
        """Create database schema if not exists"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                layer TEXT,

                -- Input information
                factors TEXT,
                factor_formulas TEXT,
                model TEXT,
                hyperparameters TEXT,

                -- Output metrics
                ic REAL,
                ir REAL,
                rank_ic REAL,
                annual_return REAL,
                max_drawdown REAL,
                sharpe_ratio REAL,

                -- Intermediate results
                training_time REAL,

                -- Metadata
                status TEXT,
                config_hash TEXT,

                UNIQUE(config_hash)
            )
        """)

        self.db.commit()

    def record_experiment(
        self,
        factors: List[str],
        factor_formulas: Dict[str, str],
        model: str,
        hyperparameters: Dict[str, Any],
        ic: float,
        ir: float,
        rank_ic: float,
        annual_return: float,
        max_drawdown: float,
        sharpe_ratio: float,
        training_time: float,
        status: str = "completed",
        layer: str = "layer1"
    ) -> int:
        """
        Record a single experiment

        Returns:
            experiment_id: ID of the inserted experiment
        """
        # Create config hash for deduplication
        config_str = json.dumps({
            "factors": sorted(factors),
            "model": model,
            "hyperparameters": hyperparameters
        }, sort_keys=True)
        config_hash = hash(config_str)

        try:
            cursor = self.db.execute("""
                INSERT INTO experiments (
                    layer, factors, factor_formulas, model, hyperparameters,
                    ic, ir, rank_ic, annual_return, max_drawdown, sharpe_ratio,
                    training_time, status, config_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                layer,
                json.dumps(factors),
                json.dumps(factor_formulas),
                model,
                json.dumps(hyperparameters),
                ic, ir, rank_ic, annual_return, max_drawdown, sharpe_ratio,
                training_time, status, str(config_hash)
            ))

            self.db.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            # Duplicate experiment (same config_hash)
            return -1

    def get_all_experiments(self) -> List[Dict]:
        """Get all experiments as list of dicts"""
        cursor = self.db.execute("SELECT * FROM experiments ORDER BY ic DESC")
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def get_best_ic(self, layer: str = "layer1") -> Optional[Dict]:
        """Get experiment with best IC"""
        cursor = self.db.execute("""
            SELECT * FROM experiments
            WHERE layer = ?
            ORDER BY ic DESC
            LIMIT 1
        """, (layer,))

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_experiments_by_factor(self, factor_name: str) -> List[Dict]:
        """Get all experiments containing a specific factor"""
        cursor = self.db.execute("""
            SELECT * FROM experiments
            WHERE factors LIKE ?
            ORDER BY ic DESC
        """, (f'%{factor_name}%',))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self):
        """Close database connection"""
        self.db.close()
