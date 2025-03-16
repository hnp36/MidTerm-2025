""" MenuCommand Module
This module implements the menu display functionality for the calculator application."""
# pylint: disable=too-few-public-methods
from calculator.commands.command import Command
from calculator.logger import get_logger

logger = get_logger(__name__)

class MenuCommand(Command):
    """Displays the calculator menu."""

    def execute(self, *args):
        """Display the calculator menu"""
        logger.debug("Displaying menu")
        print("\nCalculator Menu:")
        print("1. Add (add)")
        print("2. Subtract (subtract)")
        print("3. Multiply (multiply)")
        print("4. Divide (divide)")
        print("5. History (history)")
        print("6. Help (help)")
        print("7. Exit (exit)\n")

        # Additional info for history command if args contain 'history'
        if args and args[0] == 'history':
            print("\nHistory Commands:")
            print("  history               - Show recent calculations")
            print("  history save          - Save history to file")
            print("  history load          - Load history from file")
            print("  history clear         - Clear all history")
            print("  history delete <id>   - Delete specific record")
            print("  history filter <op>   - Filter by operation type")
            print("  history stats         - Show history statistics")
            print("  history help          - Show history help\n")
            logger.debug("Displayed history submenu")
