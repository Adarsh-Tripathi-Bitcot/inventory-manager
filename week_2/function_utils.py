# Defining Functions
def greet():
    print("Hello!")


# Calling Functions
greet()  # Output: Hello!


# Parameters and Arguments
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")


# Returning Values
def square(num):
    return num * num

result = square(5)
print(result)  # 25


# A function get_input() that asks the user for a number.
# A function is_prime(n) that checks if it's a prime number and returns True or False.
# A function main() that coordinates the process: Gets input Calls is_prime(). Prints the result

def get_input():
    num = int(input("Enter a number : "))
    return num

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def main():
    num = get_input()

    if is_prime(num):
        print(f"{num} is a Prime number.")
    else:
        print(f"{num} is not a Prime number.")


main()

# Write a script that: Asks for a list of numbers (comma-separated) Converts them to integers
# Uses a function to return: The sum, The average, The maximum number, 
# Use SRP by creating separate functions for each task.


def get_inputs():
    numbers = input("Enter a list of numbers separated by comma(,) : ").split(",")
    return numbers

def str_to_int(numbers):
    lst = []
    for i in numbers:
        lst.append(int(i))

    return lst

def total(lst):
    print(sum(lst))

def avg(lst):
    print(sum(lst)/len(lst))

def max_num(lst):
    print(max(lst))

def main():
    numbers = get_inputs()

    lst = str_to_int(numbers)

    total(lst)
    avg(lst)
    max_num(lst)


main()