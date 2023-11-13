# Import necessary modules
import os            # Operating system-related functions
import secrets       # Cryptographically strong random number generation
from hashlib import sha256  # Hash function for secure hashing
from base64 import b64encode, b64decode  # Encoding/decoding data in base64 format
import glob

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
    return sk

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Obtaining Index or Presense of the keywords in each individual file
# --------------------------------------------------------------------------------------------------------------------------------------------------------

def location():
    word_locations = {}
    
    directory = 'data/'

    # Define the file name pattern
    file_pattern = 'f*.txt'

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

    # Now you have the unique words in the 'unique_words' list, and for each word, you have the locations where it appears
    for word in unique_words:
        print(f"{word} {', '.join(word_locations[word])}")

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Encryption Function
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def pad_data(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def encrypt_block(block, key):
    key_hash = sha256(key).digest() #This line computes the SHA-256 hash of the encryption key (key) using Python's hashlib library. The .digest() method is called to obtain the binary representation of the hash.
    encrypted_block = bytes(x ^ y for x, y in zip(block, key_hash)) # This line performs the encryption operation. It iterates over each byte in the block and XORs it with the corresponding byte from the key_hash. This creates the encrypted block.
    return encrypted_block

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Token Generation Function
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def encryption_aes(plaintext, key, iv):
    # Define the block size (AES block size is 16 bytes)
    block_size = 16
    
    # Pad the plaintext to match the block size
    plaintext = pad_data(plaintext.encode('utf-8'), block_size)
    
    # Initialize an empty ciphertext
    ciphertext = b''
    
    # Initialize the previous block with the IV (Initialization Vector)
    prev_block = iv

    # Iterate over the plaintext in blocks
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]  # Get the current block
        
        # XOR the current block with the previous ciphertext block or IV
        xor_block = bytes(x ^ y for x, y in zip(block, prev_block))
        
        # Encrypt the XORed block using the encryption key
        encrypted_block = encrypt_block(xor_block, key)
        
        # Append the encrypted block to the ciphertext
        ciphertext += encrypted_block
        
        # Update the previous block with the current encrypted block
        prev_block = encrypted_block

    # Return the final ciphertext
    return ciphertext
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Replacement Function
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def read_key_from_file(filename='data/skaes.txt'):
    #Reads an encryption key from a text file in hexadecimal format

    try:
        with open(filename, 'r') as file:
            hex_key = file.read().strip()
            key = bytes.fromhex(hex_key)
        return key
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
# --------------------------------------------------------------------------------------------------------------------------------------------------------
# Main function, in this function you will see the call of the 'Key-Generation' function, the Encoding function and the Decoding function
# --------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    genKeys()
    location()
    gg = read_key_from_file()
    cc= encryption_aes("dswds", gg, "hNot5o0SkGzXmHqRC5a0qQ==")

# --------------------------------------------------------------------------------------------------------------------------------------------------------
# This calls the main function in order to run the code
# --------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()    