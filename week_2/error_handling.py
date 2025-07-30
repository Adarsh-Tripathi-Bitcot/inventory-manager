# Basic try...except Syntax
try:
    x = int(input("Enter a number: "))
    print(10 / x)
except ZeroDivisionError:
    print("Cannot divide by zero.")
except ValueError:
    print("That's not a valid number.")


# Catching Multiple Exceptions
try:
    f = open("data.txt")
    number = int(f.readline())
except FileNotFoundError:
    print("File not found.")
except ValueError:
    print("Invalid number in file.")
finally:
    print("This always runs (like closing a file).")


# Custom Error Messages
try:
    marks = int(input("Enter marks: "))
    if marks < 0:
        raise ValueError("Marks can't be negative.")
except ValueError as e:
    print("Error:", e)
