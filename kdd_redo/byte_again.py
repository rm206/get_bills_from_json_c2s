# Path to your file
file_path = "kdd.csv"

# Position of the problematic byte
position = 11310

with open(file_path, "rb") as f:
    # Seek to the problematic position
    f.seek(position)

    # Read the byte at the problematic position
    problematic_byte = f.read(100)

    # Print the problematic byte
    print(f"Problematic byte at position {position}: {problematic_byte}")
