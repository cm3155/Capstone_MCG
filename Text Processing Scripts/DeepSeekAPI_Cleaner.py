import os
import time  # Import time module for sleep
from openai import OpenAI

# Initialize OpenAI client with DeepSeek API
client = OpenAI(api_key="sk-6cdebe6c89e944278f9f58db6a0fe608", base_url="https://api.deepseek.com")

def clean_text_with_deepseek(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": 
                    "Read this text file and remove all title content, headers, table of contents, and footers"
                    },
                {"role": "user", "content": text},
            ],
            stream=False
        )
        
        cleaned_text = response.choices[0].message.content
        return cleaned_text
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        return None

def process_directory(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")
    else:
        print(f"Output directory already exists: {output_directory}")

    if not os.path.exists(input_directory):
        print(f"Error: Input directory does not exist: {input_directory}")
        return

    file_count = 0  # Track number of processed files

    for root, _, files in os.walk(input_directory):
        relative_path = os.path.relpath(root, input_directory)
        output_subfolder = os.path.join(output_directory, relative_path)

        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)
            print(f"Created subfolder: {output_subfolder}")

        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                cleaned_text = clean_text_with_deepseek(text)

                if cleaned_text:
                    cleaned_file_path = os.path.join(output_subfolder, f'clean_{filename}')
                    with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
                        cleaned_file.write(cleaned_text)
                    print(f"Processed and saved: {cleaned_file_path}")
                else:
                    print(f"Failed to process: {filename}")

                file_count += 1  # Increment file counter

                # Introduce a delay every 10 iterations
                if file_count % 10 == 0:
                    print("Waiting for 5 seconds to prevent API overload...")
                    time.sleep(5)

            else:
                print(f"Skipping non-text file: {filename}")

if __name__ == "__main__":
    input_directory = 'C:/Users/cassi/Capstone_MCG/News_Sources'
    output_directory = 'C:/Users/cassi/Capstone_MCG/News_Sources_Clean'
    process_directory(input_directory, output_directory)