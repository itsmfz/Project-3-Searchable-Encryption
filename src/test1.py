import glob
import os

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
        
    return word_locations

def process_keywords(word_locations):
    # Call a function with each keyword obtained
    for index, word in enumerate(word_locations):
        # Assuming you have a function called 'process_keyword' that takes a keyword and returns a modified value
        modified_value = process_keyword(word)
        
        # Create a new file with the modified value
        output_file_name = f'c{index + 1}.txt'
        with open(output_file_name, 'w') as new_file:
            new_file.write(modified_value)
        print(f"File '{output_file_name}' created.")

# Define a function to process each keyword
def process_keyword(keyword):
    # Placeholder function - Replace this with your actual processing logic
    return f"Processed value for {keyword}"

# Call the 'location' function to get word locations
word_locations = location()

# Call a function to process each keyword and create a new file
process_keywords(word_locations) 
location()