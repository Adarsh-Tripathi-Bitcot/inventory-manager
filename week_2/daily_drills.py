from typing import List, Tuple, Dict


# Remove Duplicates from List
def remove_duplicates(nums: List[int]) -> List[int]:
    """
    Remove duplicate integers from the input list.

    Args:
        nums (List[int]): A list of integers which may contain duplicates.

    Returns:
        List[int]: A new list containing only unique integers from the input.
    """
    return list(set(nums))


print(remove_duplicates([1, 2, 2, 3, 4, 4]))


# List of Tuples → Dictionary
def map_scores(data: List[Tuple[str, int]]) -> Dict[str, int]:
    """
    Convert a list of (name, score) tuples into a dictionary.

    Args:
        data (List[Tuple[str, int]]): List of (name, score) pairs.

    Returns:
        Dict[str, int]: A dictionary mapping names to their corresponding scores.
    """
    return dict(data)


print(map_scores([("Alice", 90), ("Bob", 85)]))


# Count Lines in a File
def count_lines(filename: str) -> int:
    """
    Count the number of lines in a text file.

    Args:
        filename (str): The path to the file.

    Returns:
        int: The number of lines in the file. Returns 0 if the file does not exist.
    """
    try:
        with open(filename, "r") as f:
            return len(f.readlines())
    except FileNotFoundError:
        print("File not found.")
        return 0
