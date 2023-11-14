import os
import glob
import secrets
from base64 import b64encode, b64decode

# ----------------------------------------------------------------------------
# Generate Key Function: This function is to generate a random 256-bit encryption key
# ----------------------------------------------------------------------------

def generate_keys(bit_val, num_keys):
    # Generate a specified number of random encryption keys, each with 'bit_val' bits
    keys = []
    for _ in range(num_keys):
        encryption_key = secrets.token_bytes(bit_val // 8)  # Convert bits to bytes
        keys.append(encryption_key)
    return keys

# ----------------------------------------------------------------------------
# Print Key - This function is built to print the key 
# ----------------------------------------------------------------------------

def print_key(sk):
    if sk:
        print(f'Encryption Key:')
        hex_values = ' '.join([format(byte, '02X') for byte in sk])
        print(hex_values)

# ----------------------------------------------------------------------------
# Write key to file: This writes to the desired file
# ----------------------------------------------------------------------------
def write_key_to_file(key, filename):
    # Writes an encryption key to a text file in hexadecimal format.
    # key (bytes): The encryption key to be written.
    # filename: The name of the file to write the key to. Default is 'data/key.txt'.
    hex_key = key.hex()
    with open(filename, 'w') as file:
        file.write(hex_key)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# genKeys: This function is aimed to generate the keys using the generate_key function after which we utilize the print_key and write_key_to_file functions to print and write the key to the file, respectively
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def genKeys():
    sk = generate_keys(256, 2)
    print("\n")
    print("AES")
    print_key(sk[0])
    write_key_to_file(sk[0], 'data/skaes.txt')
    print("\n")
    print("PRF")
    print_key(sk[1])
    write_key_to_file(sk[1], 'data/skprf.txt')
    return sk

def hex_to_int(hex_string):
    # Convert a hexadecimal string to an integer
    return int(hex_string, 16)

def encrypt_word(word, key):
    encrypted_word = ""
    for char in word:
        if char.isalpha():
            encrypted_char = chr((ord(char) - ord('a' if char.islower() else 'A') + key) % 26 + ord('a' if char.islower() else 'A'))
            encrypted_word += encrypted_char
        else:
            encrypted_word += char
    return encrypted_word

def encrypt_and_store_files(pattern, key_hex):
    key_int = int(key_hex, 16)
    
    file_names = glob.glob(pattern)

    keyword_mapping = {}  # Dictionary to store original and encrypted keywords

    # Create a folder for ciphertext if it doesn't exist
    ciphertext_folder = os.path.join('data', 'ciphertext')
    os.makedirs(ciphertext_folder, exist_ok=True)

    for i, file_name in enumerate(file_names, start=1):
        with open(file_name, 'r') as file:
            file_contents = file.read()
            words = file_contents.split()

            encrypted_words = []
            for word in words:
                encrypted_word = encrypt_word(word, key_int)
                encrypted_words.append(encrypted_word)

                # Store the original and encrypted keywords in the dictionary
                keyword_mapping[word] = encrypted_word

            # Store the encrypted words in a new file (c1.txt, c2.txt, etc.) in the 'ciphertext' folder
            encrypted_file_name = f"c{i}.txt"
            encrypted_file_path = os.path.join(ciphertext_folder, encrypted_file_name)
            with open(encrypted_file_path, 'w') as encrypted_file:
                encrypted_file.write(' '.join(encrypted_words))

            print(f"Encrypted and stored {file_name} to {encrypted_file_path}")

    # Write encrypted keywords to data/token.txt
    with open('data/token.txt', 'w') as token_file:
        for original, encrypted in keyword_mapping.items():
            token_file.write(f"{original} {encrypted}\n")

    return keyword_mapping

def generate_location_matrix(unique_words, directory='data/', file_pattern='f*.txt'):
    file_names = glob.glob(os.path.join(directory, file_pattern))

    # Initialize an empty matrix
    matrix = []

    # Iterate through each text file
    for file_name in file_names:
        with open(file_name, 'r') as file:
            # Read the contents of the file and split into words
            file_contents = file.read()
            words = file_contents.split()

            # Initialize a list to represent the presence of words in the current file
            word_presence = [0] * len(unique_words)

            # Update the word_presence list based on the unique words found in the file
            for i, word in enumerate(unique_words):
                if word in words:
                    word_presence[i] = 1

            # Append the word_presence list to the matrix
            matrix.append(word_presence)

    return matrix

def transpose_keyword_matrix(matrix, unique_words):
    # Use nested list comprehensions to transpose the matrix
    transposed_matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    # Display the transposed matrix with corresponding keywords
    print("\nMatrix:")
    print("Keywords:", unique_words)
    for i, row in enumerate(transposed_matrix):
        print(f"{unique_words[i]}:", row)

    return transposed_matrix

def location():
    word_locations = {}
    
    directory = ''

    # Define the file name pattern
    file_pattern = 'c*.txt'

    # Get a list of file names that match the pattern in the specified directory
    file_names = glob.glob(os.path.join(directory, file_pattern))

    # Iterate through each text file
    for file_name in file_names:
        with open(file_name, 'r') as file:
            # Read the contents of the file and split into words
            file_contents = file.read()
            words = file_contents.split()
            # Store the words and their file location (text file name)
            for word in words:
                # Convert the word to lowercase to avoid case sensitivity
                word = word.lower()
                if word not in word_locations:
                    word_locations[word] = [file_name]
                else:
                    if file_name not in word_locations[word]:
                        word_locations[word].append(file_name)

    # Extract the unique words and store them in an array
    unique_words = list(word_locations.keys())

    print("\n")
    # Now you have the unique words in the 'unique_words' list, and for each word, you have the locations where it appears
    for word in unique_words:
        print(f"{word} {', '.join(word_locations[word])}")
        
    return word_locations

def main():
    keys = genKeys()
    location_mapping = location()

    # Encrypt and store files in the specified directory and pattern
    directory = 'data/'
    file_pattern = 'f*.txt'
    keyword_mapping = encrypt_and_store_files(os.path.join(directory, file_pattern), keys[1].hex())

    # Generate the location matrix
    location_matrix = generate_location_matrix(list(keyword_mapping.keys()))

    # Transpose and display the keyword matrix
    transpose_keyword_matrix(location_matrix, list(keyword_mapping.keys()))

    print("\nKeyword Mapping:")
    for original, encrypted in keyword_mapping.items():
        print(f"{original} -> {encrypted}")

    print("\nLocation Mapping:")
    for word, locations in location_mapping.items():
        print(f"{word}: {', '.join(locations)}")

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# This calls the main function in order to run the code
# --------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
