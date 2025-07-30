#  Creating Tuples
point = (1, 2)
singleton = (3,)  # Must include comma!


# Accessing Tuple Elements
print(point[0])  # 1


# Unpacking Tuples
x, y = point
print(x, y)  # 1 2



# Write a function that: Takes two numbers Returns both the sum and the product as a tuple
# Call the function and print the results

def calculate(a,b):
    return(a+b, a*b)


num1 = int(input("Enter 1st number : "))
num2 = int(input("Enter 2nd number : "))
result = calculate(num1, num2)
print(f"Sum: {result[0]}, Product : {result[1]}")