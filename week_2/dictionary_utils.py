# Creating a Dictionary
# Empty dictionary
empty = {}

# With data
student = {"name": "John", "marks": 85}

# Accessing Values
print(student["name"])     # John
print(student.get("marks"))  # 85
print(student.get("grade", "Not available"))  # Safe access


# Updating Values
student["marks"] = 90
student["grade"] = "A"  # Adds new key-value


# Iterating a Dictionary
# Keys
for key in student:
    print(key)

# Values
for value in student.values():
    print(value)

# Key-Value Pairs
for key, value in student.items():
    print(f"{key}: {value}")
