# Remove Duplicates from List
def remove_duplicates(nums):
    return list(set(nums))

print(remove_duplicates([1, 2, 2, 3, 4, 4]))


# List of Tuples → Dictionary
def map_scores(data):
    return dict(data)

print(map_scores([("Alice", 90), ("Bob", 85)]))


# Count Lines in a File
def count_lines(filename):
    try:
        with open(filename, "r") as f:
            return len(f.readlines())
    except FileNotFoundError:
        print("File not found.")
        return 0
