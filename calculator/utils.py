
# pylint: disable=broad-exception-caught
"""
Utility functions for the calculator application.
"""

from decimal import InvalidOperation  # Make sure to import InvalidOperation

def handle_result(func):
    """Decorator to handle results and exceptions for calculator operations."""

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            print(f"Result: {result}")
        except InvalidOperation:  # Catches Decimal conversion errors
            print("Invalid input! Please enter valid numbers.")
        except ZeroDivisionError:  # Specific catch for division by zero
            print("Error: Division by zero is not allowed.")
        except Exception as e:  # Catch other exceptions
            print(f"Unexpected error: {e}")

    return wrapper
