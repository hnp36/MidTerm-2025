"""
History Manager Module

This module utilizes Pandas to manage the calculation history, providing
functionality to load, save, filter, and analyze calculation records.
"""
import os
import logging
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any
import pandas as pd
from calculator.calculation import Calculation

class HistoryManager:
    """Manages calculation history using Pandas DataFrame for efficient storage and analysis."""

    def __init__(self, history_file: str = "calculation_history.csv"):
        """Initialize the history manager with the specified history file."""
        self.history_file = history_file
        self.df = pd.DataFrame(columns=['timestamp', 'value1', 'value2', 'operation', 'result'])
        self.logger = logging.getLogger(__name__)

    def add_calculation(self, calculation: Calculation) -> None:
        """Add a calculation to the history DataFrame."""
        try:
            new_record = {
                'timestamp': datetime.now().isoformat(),
                'value1': str(calculation.value1),
                'value2': str(calculation.value2),
                'operation': calculation.operation.__name__,
                'result': str(calculation.perform())
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
            self.logger.info("Added calculation to history: %s(%s, %s)",
                             calculation.operation.__name__, calculation.value1, calculation.value2)
        except Exception as e:
            self.logger.error("Failed to add calculation to history: %s", e)
            raise

    def save_history(self) -> bool:
        """Save the calculation history to a CSV file."""
        try:
            self.df.to_csv(self.history_file, index=False)
            self.logger.info("Saved %d history records to %s", len(self.df), self.history_file)
            return True
        except (IOError, pd.errors.EmptyDataError) as e:
            self.logger.error("Failed to save history: %s", e)
            return False

    def load_history(self) -> bool:
        """Load calculation history from the CSV file."""
        try:
            if os.path.exists(self.history_file):
                self.df = pd.read_csv(self.history_file)
                self.logger.info("Loaded %d history "
                "records from %s", len(self.df), self.history_file)
                return True
            self.logger.warning("History file %s not found", self.history_file)
            return False
        except (IOError, pd.errors.ParserError) as e:
            self.logger.error("Failed to load history: %s", e)
            return False

    def clear_history(self) -> None:
        """Clear all history records from the DataFrame."""
        record_count = len(self.df)
        self.df = pd.DataFrame(columns=['timestamp', 'value1', 'value2', 'operation', 'result'])
        self.logger.info("Cleared %d history records", record_count)

    def delete_record(self, index: int) -> bool:
        """Delete a specific record by index."""
        try:
            if 0 <= index < len(self.df):
                self.df = self.df.drop(index).reset_index(drop=True)
                self.logger.info("Deleted record at index %d", index)
                return True
            self.logger.warning("Invalid index %d for deletion", index)
            return False
        except KeyError as e:
            self.logger.error("Failed to delete record: %s", e)
            return False

    def get_history(self) -> pd.DataFrame:
        """Get the entire history DataFrame."""
        return self.df

    def filter_by_operation(self, operation: str) -> pd.DataFrame:
        """Filter history by operation type."""
        try:
            filtered = self.df[self.df['operation'] == operation]
            self.logger.info("Filtered %d records with operation '%s'", len(filtered), operation)
            return filtered
        except KeyError as e:
            self.logger.error("Failed to filter by operation: %s", e)
            return pd.DataFrame()

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from the history."""
        if len(self.df) == 0:
            return {"status": "empty", "message": "No history data available"}

        stats = {
            "total_calculations": len(self.df),
            "operations_count": self.df['operation'].value_counts().to_dict(),
            "first_calculation": self.df['timestamp'].min(),
            "last_calculation": self.df['timestamp'].max(),
            "average_results": {}
        }

        # Calculate average results with specific exception handling
        try:
            self.df['numeric_result'] = self.df['result'].apply(Decimal)
            avg_by_op = self.df.groupby('operation')['numeric_result'].mean()
            stats["average_results"] = {op: str(avg) for op, avg in avg_by_op.items()}
        except (ValueError, TypeError):
            stats["average_results"] = "Unable to calculate"

        self.logger.info("Generated history statistics")
        return stats

# Create a singleton instance for global use
history_manager = HistoryManager()
