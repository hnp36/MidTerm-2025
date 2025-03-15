# calculator/commands/subtraction_command.py

"""
SubtractionCommand Module

This module implements the subtraction operation command for the calculator application.
"""

# pylint: disable=too-few-public-methods
from decimal import Decimal, InvalidOperation
from calculator.commands.command import Command
from calculator import Calculator
from calculator.utils import handle_result

class SubtractionCommand(Command):
    """Handles user input for subtraction and performs the operation."""

    @handle_result
    def execute(self):
        """Executes the subtraction command by taking user input and performing the operation."""
        value1 = Decimal(input("Enter first number: "))
        value2 = Decimal(input("Enter second number: "))
        return Calculator.subtract_numbers(value1, value2)  # Return result for the decorator
