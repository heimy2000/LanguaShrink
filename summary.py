import os
import pandas as pd
import openai
import logging
import time
import tiktoken


openai.api_key = "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"

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turboc.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def generate_chat_completion(content):
    prompt = f'''Summarise the above \n\n---\n{content}'''
    
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-0125-preview',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0,
            top_p=1
        )
        print(response.choices[0].message['content'])
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

def process_content(content):
    prompt = f'''Summarise the above \n\n---\n{content}'''
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-32k-0314',
            messages=[
                {'role': 'user', 'content': prompt}],
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger with the specified name and log file."""
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def txt_to_txt(input_folder, output_folder):
    log_directory = 'summary_logs'
    os.makedirs(log_directory, exist_ok=True)  # Ensure the log directory exists
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    total_tokens = 0
    total_time = 0
    num_files = 0

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            num_files += 1
            file_path = os.path.join(input_folder, filename)
            log_path = os.path.join(log_directory, f"{os.path.splitext(filename)[0]}_log.log")
            logger = setup_logger(name=filename, log_file=log_path)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            model = 'gpt-4-32k-0314'
            start_time = time.time()
            print("ok-------")
            result = generate_chat_completion(content)  # Make sure process_content is defined elsewhere
            end_time = time.time()

            processing_time = end_time - start_time
            total_time += processing_time
            logger.info(f"Total processing time: {processing_time} seconds")

            example_messages = [
                {
                    "role": "user",
                    "content": result,
                },
            ]
            tokens = num_tokens_from_messages(example_messages, model)  # Ensure num_tokens_from_messages is defined
            total_tokens += tokens
            logger.info(f"{tokens} compress_prompt tokens counted by num_tokens_from_messages().")

            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(result)

    # Log average values
    if num_files > 0:
        average_tokens = total_tokens / num_files
        average_time = total_time / num_files
        with open(os.path.join(log_directory, 'average_metrics.log'), 'w') as log_file:
            log_file.write(f"Average number of tokens: {average_tokens}\n")
            log_file.write(f"Average processing time: {average_time} seconds\n")

# Usage
txt_to_txt('split', 'summary_original')
