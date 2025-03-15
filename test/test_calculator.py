"""My First calculator"""
from calculator import add, substract, division, multiplication

def test_addition():
    """this is addition """
    assert add(2,2) ==4

def test_substraction():
    """this is substactiontion """
    assert substract(2,2) ==0

def test_division():
    """this is division"""
    assert division(15,3) ==5

def test_multiplication():
    """this is multiplication"""
    assert multiplication(4,5) ==20
