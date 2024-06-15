import nltk
from nltk.tokenize import word_tokenize

# You may need to download the tokenizer data if you haven't done so
nltk.download('punkt')

# Open and read the file
with open('2.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize the text into words
tokens = word_tokenize(text)

# Count the tokens
token_count = len(tokens)

# Print the result
print(f"The number of tokens in 2.txt is: {token_count}")
