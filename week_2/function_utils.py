from typing import List
from pydantic import BaseModel, ValidationError


# Defining Functions
def greet():
    """
    Prints a simple greeting message.
    """
    print("Hello!")


# Calling Functions
greet()  # Output: Hello!


# Parameters and Arguments
def greet(name: str):
    """
    Greets the user by name.

    Args:
        name (str): The name of the user.
    """
    print(f"Hello, {name}!")


greet("Alice")


# Returning Values
def square(num: float) -> float:
    """
    Returns the square of a given number.

    Args:
        num (int or float): The number to be squared.

    Returns:
        int or float: The squared value.
    """
    return num * num


result = square(5)
print(result)  # 25


# Prime Number Checker Components
class PrimeInput(BaseModel):
    """
    Pydantic model for validating prime number input.
    """
    num: int

    @classmethod
    def validate(cls, value: int) -> 'PrimeInput':
        if value < 0:
            raise ValueError("Number cannot be negative")
        return cls(num=value)


def get_input():
    """
    Prompts the user to enter a number and returns it as an integer.

    Returns:
        int: The user input converted to an integer.
    """
    try:
        num = int(input("Enter a number: "))
        PrimeInput.validate(num)  # Pydantic validation
        return num
    except ValueError as e:
        print(f"Invalid input: {e}")
        return get_input()  # Retry until valid input


def is_prime(n: int) -> bool:
    """
    Checks whether a number is a prime number.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):  # Improved prime check (only up to sqrt(n))
        if n % i == 0:
            return False
    return True


def main():
    """
    Coordinates getting input, checking for prime, and displaying the result.
    """
    num = get_input()

    if is_prime(num):
        print(f"{num} is a Prime number.")
    else:
        print(f"{num} is not a Prime number.")


main()


# List Summary Statistics Script

class ListInput(BaseModel):
    """
    Pydantic model to validate list of numbers input.
    """
    numbers: List[int]


def get_inputs():
    """
    Prompts the user to enter a comma-separated list of numbers.

    Returns:
        list of str: A list of numbers in string format.
    """
    try:
        numbers = input("Enter a list of numbers separated by comma(,) : ").split(",")
        # Convert to integers and validate using Pydantic
        numbers_int = [int(i) for i in numbers]
        ListInput(numbers=numbers_int)  # Pydantic validation
        return numbers_int
    except ValueError:
        print("Invalid input. Please enter a valid list of numbers.")
        return get_inputs()


def total(lst: List[int]):
    """
    Prints the sum of the numbers in the list.

    Args:
        lst (list of int): The list of numbers.
    """
    print("Sum:", sum(lst))


def avg(lst: List[int]):
    """
    Prints the average of the numbers in the list.

    Args:
        lst (list of int): The list of numbers.
    """
    print("Average:", sum(lst) / len(lst) if lst else 0)


def max_num(lst: List[int]):
    """
    Prints the maximum number from the list.

    Args:
        lst (list of int): The list of numbers.
    """
    print("Maximum:", max(lst) if lst else None)


def main():
    """
    Main function to gather input and print summary statistics.
    """
    numbers = get_inputs()

    total(numbers)
    avg(numbers)
    max_num(numbers)


main()
