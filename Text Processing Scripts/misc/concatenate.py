def concatenate_files(file1, file2, output_file):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2, open(output_file, 'w', encoding='utf-8') as out:
        out.write(f1.read() + '\n')  # Ensure separation
        out.write(f2.read())

# Example usage
concatenate_files('stopwords-en.txt', 'StopWords_Names.txt', 'stopwords.txt')