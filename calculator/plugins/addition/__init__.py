# calculator/commands/addition_command.py

"""
AdditionCommand Module

This module implements the addition operation command for the calculator application.
"""

# pylint: disable=too-few-public-methods
from decimal import Decimal, InvalidOperation
from calculator.commands.command import Command
from calculator import Calculator
from calculator.utils import handle_result

class AdditionCommand(Command):
    """Handles user input for addition and performs the operation."""

    @handle_result
    def execute(self):
        """Executes the addition command by taking user input and performing the operation."""
        value1 = Decimal(input("Enter first number: "))
        value2 = Decimal(input("Enter second number: "))
        return Calculator.add_numbers(value1, value2)  # Return result for the decorator
