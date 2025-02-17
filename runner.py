from ModelSECPreprocessor import ModelSECPreprocessor
preprocessor = ModelSECPreprocessor()

file_path = "southstate_corporation/2020/10-K_2020-02-21_Business_Overview.txt" 
result = preprocessor.process_file(file_path)

if result:
    print("Processed Text:", result['processed_text'])
    print("\nChunks:", result['chunks'])
