# ZEN of Python
import this

print(this)


# Pythonic Constructs

# List comprehension
squares = [x*x for x in range(10)]
print(squares)

# vs. traditional loop
squares_alt = []
for x in range(10):
    squares_alt.append(x*x)

print(squares_alt)

# == vs is
a = [1, 2]
b = [1, 2]
print(a == b)  # True
print(a is b)  # False
