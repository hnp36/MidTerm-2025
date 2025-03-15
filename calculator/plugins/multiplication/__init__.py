# calculator/commands/multiplication_command.py

"""
MultiplicationCommand Module

This module implements the multiplication operation command for the calculator application.
"""

# pylint: disable=too-few-public-methods
from decimal import Decimal, InvalidOperation
from calculator.commands.command import Command
from calculator import Calculator
from calculator.utils import handle_result

class MultiplicationCommand(Command):
    """Handles user input for multiplication and performs the operation."""

    @handle_result
    def execute(self):
        value1 = Decimal(input("Enter first number: "))
        value2 = Decimal(input("Enter second number: "))
        return Calculator.multiply_numbers(value1, value2)  # Return result for the decorator
