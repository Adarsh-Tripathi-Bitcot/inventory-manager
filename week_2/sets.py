# Creating a Set
# From list
numbers = set([1, 2, 3, 3, 2, 4])  # {1, 2, 3, 4}

# Directly
vowels = {"a", "e", "i", "o", "u"}

# Empty set
empty_set = set()  # NOT {}


# Adding and Removing Elements
colors = {'red', 'blue'}
colors.add("yellow")
colors.discard("blue")  # No error if not found
print(colors)


# Set Operations
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)   # Union: {1, 2, 3, 4, 5}
print(a & b)   # Intersection: {3}
print(a - b)   # Difference: {1, 2}


# Use Case: Remove Duplicates
numbers = [1, 2, 2, 3, 4, 4, 5]
unique_numbers = list(set(numbers))  # [1, 2, 3, 4, 5]


# Membership Test Efficiency
# For large collections
big_list = list(range(1000000))
big_set = set(big_list)

# Time to check if 999999 exists
999999 in big_set  # Very fast (O(1))
999999 in big_list  # Slower (O(n))



# Create a program that: Asks the user for student names and marks (until they type 'done'). Stores data in a dictionary.
# Uses a set to keep track of all unique marks. Prints the full dictionary and the set of unique marks.

dict = {}
unique_marks = set()
while True:
    name = input("Enter your name : ")
    if name == 'done':
        break
    marks = int(input("Enter your age : "))
    dict[name] = marks
    unique_marks.add(marks)

print(dict)
print(unique_marks)