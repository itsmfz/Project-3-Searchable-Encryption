# Import necessary modules
import os            # Operating system-related functions
import secrets       # Cryptographically strong random number generation
from hashlib import sha256  # Hash function for secure hashing
from base64 import b64encode, b64decode  # Encoding/decoding data in base64 format

# ----------------------------------------------------------------------------
# Generate Key Function: This function is to generate a random 256 bit encryptioon key
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
    #Writes an encryption key to a text file in hexadecimal format.
    #key (bytes): The encryption key to be written.
    #filename : The name of the file to write the key to. Default is 'data/key.txt'.
    hex_key = key.hex()
    with open(filename, 'w') as file:
        file.write(hex_key)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# genKeys: This function is aimed to generate the keys using the generate_key fuction after which we utilize the print_key and write_key_to_file function to print and write the key to the file respectively
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def genKeys():
    sk = generate_keys(256, 2)
    print_key(sk[0])
    write_key_to_file(sk[0], 'data/skaes.txt')
    print_key(sk[1])
    write_key_to_file(sk[1], 'data/skprf.txt')

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Open the text file to see the locations
# --------------------------------------------------------------------------------------------------------------------------------------------------------

word_locations = {}

# List of text files you want to process
file_paths = ["data/f1.txt", "data/f2.txt", "data/f3.txt", "data/f4.txt", "data/f5.txt", "data/f6.txt"]

# Iterate through each text file
for file_path in file_paths:
    with open(file_path, 'r') as file:
        # Read the contents of the file and split into words
        file_contents = file.read()
        words = file_contents.split()

        # Store the words and their file location (text file name)
        for word in words:
            # Convert the word to lowercase to avoid case sensitivity
            word = word.lower()
            if word not in word_locations:
                word_locations[word] = [file_path]
            else:
                if file_path not in word_locations[word]:
                    word_locations[word].append(file_path)

# Extract the unique words and store them in an array
unique_words = list(word_locations.keys())

# Now you have the unique words in the 'unique_words' list, and for each word, you have the locations where it appears
for word in unique_words:
    print(f"{word} {', '.join(word_locations[word])}")

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Token Generation Function
# --------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Main function, in this function you will see the call of the 'Key-Generation' function, the Encoding function and the Decoding function
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    genKeys()

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# This calls the main function in order to run the code
# --------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()    