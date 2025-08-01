# Opening Files with with open(...) as f
with open("sample.txt", "r") as f:
    content = f.read()
    print(content)


# Writing to Files
# Overwrites the file
with open("sample.txt", "w") as f:
    f.write("Hello, file!\n")
    f.write("Another line.\n")


# Append Mode
with open("sample.txt", "a") as f:
    f.write("This will be added at the end.\n")


# Reading Line-by-Line
with open("sample.txt", "r") as f:
    for line in f:
        print(line.strip())  # .strip() removes newline characters
