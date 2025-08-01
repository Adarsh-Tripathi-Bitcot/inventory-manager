# if / elif / else Statements
age = 20

if age < 18:
    print("Minor")
elif age < 60:
    print("Adult")
else:
    print("Senior")


# for Loops
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# Use range() for numeric loops:
for i in range(5):  # 0 to 4
    print(i)


# while Loops
i = 0
while i < 5:
    print(i)
    i += 1


num = int(input("Enter a number : "))
if num % 2 == 0:
    print("Even")
else:
    print("Odd")

for i in range(1, 11):
    print(f"{num} * {i} = {num * i}")
