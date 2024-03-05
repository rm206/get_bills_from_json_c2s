with open("entered_claims.csv", "rb") as file:  # Note the 'b' in 'rb' for binary mode
    file.seek(26189 - 1)  # Go a bit before the problematic position
    print(file.read(150))  # Read bytes around the problematic position
