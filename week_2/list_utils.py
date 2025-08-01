# Creating a List
empty_list = []
numbers = [1, 2, 3, 4, 5]

# Indexing and Slicing
print(numbers[0])  # 1
print(numbers[-1])  # 5
print(numbers[1:4])  # [2, 3, 4]

# Modifying a List
numbers[0] = 10
print(numbers)  # [10, 2, 3, 4, 5]


#  List Methods
# .append()
numbers.append(6)
print(numbers)

# .extend()
numbers.extend([7, 8])
print(numbers)

# .pop()
print(numbers.pop())  # removes 8
print(numbers)
print(numbers.pop(0))  # removes 10
print(numbers)

# .remove()
numbers.remove(3)  # removes value 3
print(numbers)

# .sort()
numbers.sort()  # ascending order
print(numbers)


# Create a list of 5 names
names = ["Adarsh", "Vansh", "Mayank Sir", "Sumer Sir"]

# Add two more names
names.extend(["Ayush Sir", "Sanidhya Sir"])

# Remove one name
names.remove("Adarsh")

# Sort the list
names.sort()

# Print the final result
print(names)
