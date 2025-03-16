"""
History Command Module

This module implements commands for managing calculation history using Pandas.
"""
# pylint: disable=too-few-public-methods
import pandas as pd
from tabulate import tabulate
from calculator.commands.command import Command
from calculator.history_manager import history_manager

class HistoryCommand(Command):
    """Handles history-related commands with CSV integration."""
    
    def execute(self, *args):
        """Handle different history commands including CSV operations."""
        if not args:
            self._show_history()
            return

        subcommand = args[0].lower()
        if subcommand == 'save':
            history_manager.save_history()
            print("History saved to CSV.")
        elif subcommand == 'load':
            history_manager.load_history()
            print("History loaded from CSV.")
        elif subcommand == 'show':
            history_manager.display_history()
        else:
            print("Unknown history command. Use 'history help' for available options.")


    def _show_history(self):
        """Display the calculation history in a tabular format."""
        df = history_manager.get_history()
        if len(df) == 0:
            print("No calculation history available.")
            return
        # Format the DataFrame for display
        display_df = df.copy()
        if len(display_df) > 10:
            print(f"Showing the most recent 10 of {len(display_df)} records:")
            display_df = display_df.tail(10)
        # Add an index column for reference
        display_df = display_df.reset_index()
        display_df.rename(columns={'index': 'id'}, inplace=True)
        # Print using tabulate for nice formatting
        print(tabulate(display_df, headers='keys', tablefmt='simple', showindex=False))

    def _save_history(self):
        """Save the calculation history to a file."""
        if history_manager.save_history():
            print("History saved successfully.")
        else:
            print("Failed to save history.")

    def _load_history(self):
        """Load the calculation history from a file."""
        if history_manager.load_history():
            print("History loaded successfully.")
        else:
            print("No history file found or error loading history.")

    def _clear_history(self):
        """Clear all calculation history."""
        confirm = input("Are you sure you want to clear all history? (y/n): ")
        if confirm.lower() == 'y':
            history_manager.clear_history()
            print("History cleared.")
        else:
            print("Operation cancelled.")

    def _delete_record(self, index_str):
        """Delete a specific record by index."""
        try:
            index = int(index_str)
            if history_manager.delete_record(index):
                print(f"Record {index} deleted.")
            else:
                print(f"Failed to delete record {index}.")
        except ValueError:
            print("Invalid index. Please provide a valid number.")

    def _filter_history(self, operation):
        """Filter history by operation type."""
        filtered_df = history_manager.filter_by_operation(operation)
        if len(filtered_df) == 0:
            print(f"No records found for operation '{operation}'.")
            return
        print(f"Found {len(filtered_df)} records for operation '{operation}':")
        # Add an index column for reference
        display_df = filtered_df.reset_index()
        display_df.rename(columns={'index': 'id'}, inplace=True)
        # Print using tabulate for nice formatting
        print(tabulate(display_df, headers='keys', tablefmt='simple', showindex=False))

    def _show_statistics(self):
        """Show statistics about the calculation history."""
        stats = history_manager.get_statistics()
        if stats.get("status") == "empty":
            print("No history data available for statistics.")
            return
        print("\nCalculation History Statistics:")
        print(f"Total calculations: {stats['total_calculations']}")
        print("\nOperations breakdown:")
        for op, count in stats['operations_count'].items():
            print(f"  {op}: {count}")
        print(f"\nFirst calculation: {stats['first_calculation']}")
        print(f"Last calculation: {stats['last_calculation']}")
        if isinstance(stats.get("average_results"), dict):
            print("\nAverage results by operation:")
            for op, avg in stats['average_results'].items():
                print(f"  {op}: {avg}")

    def _show_help(self):
        """Show help information for history commands."""
        print("\nHistory Command Help:")
        print("  history               - Show the most recent calculation history")
        print("  history save          - Save history to a file")
        print("  history load          - Load history from a file")
        print("  history clear         - Clear all history records")
        print("  history delete <id>   - Delete a specific record by ID")
        print("  history filter <op>   - Filter history by operation type")
        print("  history stats         - Show statistics about the calculation history")
        print("  history help          - Show this help information\n")
