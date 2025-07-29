# Variables and types
name = "Adarsh"
age = 23
is_new_user = True
height = 5.8

# Operators
print(age > 18 and is_new_user)

# f-strings
print(f"{name} is {age} years old.")



# Ask the user for their name and age and print a message.

name = input("Please enter your name : ")
age = int(input("Enter your age : "))

print(f"Hi {name} Sir, your age is {age}")


# Write a function that checks if a number is odd or even.

def odd_or_even(num : int) -> str:
    if num%2==0:
        return f"{num} is even"
    else:
        return f"{num} is odd."

number = int(input("Enter a number to check whether it is even or odd : "))

print(odd_or_even(number))