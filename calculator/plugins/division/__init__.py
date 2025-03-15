# calculator/commands/division_command.py

"""
DivisionCommand Module

This module implements the division operation command for the calculator application.
"""

# pylint: disable=too-few-public-methods
from decimal import Decimal, InvalidOperation
from calculator.commands.command import Command
from calculator import Calculator
from calculator.utils import handle_result

class DivisionCommand(Command):
    """Handles user input for division and performs the operation."""

    @handle_result
    def execute(self):
        value1 = Decimal(input("Enter first number: "))
        value2 = Decimal(input("Enter second number: "))
        if value2 == 0:
            raise ValueError("Error: Division by zero is not allowed.")
        return Calculator.divide_numbers(value1, value2)  # Return result for the decorator
