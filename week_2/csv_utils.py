import csv

with open("sample.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)


# Reading with csv.DictReader
with open("sample.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
        print(f"{row['name']} is {row['age']} years old from {row['city']}.")


# Writing CSV Files with csv.writer
with open("sample.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Adarsh", 23, "Bhopal"])


# Writing with csv.DictWriter
data = [
    {"name": "Alice", "age": 30, "city": "NY"},
    {"name": "Bob", "age": 25, "city": "Delhi"},
]

with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(data)
