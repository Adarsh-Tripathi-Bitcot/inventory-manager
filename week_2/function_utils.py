# Defining Functions
def greet():
    """
    Prints a simple greeting message.
    """
    print("Hello!")


# Calling Functions
greet()  # Output: Hello!


# Parameters and Arguments
def greet(name):
    """
    Greets the user by name.

    Args:
        name (str): The name of the user.
    """
    print(f"Hello, {name}!")


greet("Alice")


# Returning Values
def square(num):
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


def get_input():
    """
    Prompts the user to enter a number and returns it as an integer.

    Returns:
        int: The user input converted to an integer.
    """
    num = int(input("Enter a number: "))
    return num


def is_prime(n):
    """
    Checks whether a number is a prime number.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, n):
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


def get_inputs():
    """
    Prompts the user to enter a comma-separated list of numbers.

    Returns:
        list of str: A list of numbers in string format.
    """
    numbers = input("Enter a list of numbers separated by comma(,) : ").split(",")
    return numbers


def str_to_int(numbers):
    """
    Converts a list of number strings to integers.

    Args:
        numbers (list of str): The list of number strings.

    Returns:
        list of int: The converted list of integers.
    """
    lst = []
    for i in numbers:
        lst.append(int(i))
    return lst


def total(lst):
    """
    Prints the sum of the numbers in the list.

    Args:
        lst (list of int): The list of numbers.
    """
    print("Sum:", sum(lst))


def avg(lst):
    """
    Prints the average of the numbers in the list.

    Args:
        lst (list of int): The list of numbers.
    """
    print("Average:", sum(lst) / len(lst))


def max_num(lst):
    """
    Prints the maximum number from the list.

    Args:
        lst (list of int): The list of numbers.
    """
    print("Maximum:", max(lst))


def main():
    """
    Main function to gather input and print summary statistics.
    """
    numbers = get_inputs()
    lst = str_to_int(numbers)

    total(lst)
    avg(lst)
    max_num(lst)


main()
