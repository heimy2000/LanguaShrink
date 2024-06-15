import json
import openai
import re

openai.api_base = 'https://one-api.bltcy.top/v1'
openai.api_key = "sk-aN0YpOEDiDywKJhp0bDc328dC829414297D28f6e0aEe5354"


def generate_summary(messages, iteration_count=2):
    content = " ".join(messages)
    prompt_template = """Article:

{content}

----

You will generate increasingly concise, entity-dense summaries of the above interaction trajectory.

Repeat the following 2 steps {iteration_count} times.

- Step 1: Identify 1-3 informative Entities from the interaction trajectory which are missing from the previously generated summary and are the most relevant.

- Step 2: Write a new, denser summary of identical length which covers every entity and detail from the previous summary plus the missing entities

A Missing Entity is:

- Relevant: to the main interaction trajectory
- Specific: descriptive yet concise (5 words or fewer)
- Novel: not in the previous summary
- Faithful: present in the interaction trajectory
- Anywhere: located anywhere in the interaction trajectory

Guidelines:
- The first summary should be long (4-5 sentences, approx. 80 words) yet highly non-specific, containing little information beyond the entities marked as missing.

- Use overly verbose language and fillers (e.g. "The previous interaction trajectory discusses") to reach approx. 80 words.

- Make every word count: re-write the previous summary to improve flow and make space for additional entities.

- Make space with fusion, compression, and removal of uninformative phrases like "The previous interaction trajectory discusses"

- The summaries should become highly dense and concise yet self-contained, e.g., easily understood without the previous interaction trajectory.

- Missing entities can appear anywhere in the new summary.

- Never drop entities from the previous summary. If space cannot be made, add fewer new entities.

> Remember to use the exact same number of words for each summary.
Answer in JSON.

> The JSON in `summaries_per_step` should be a list (length {iteration_count}) of dictionaries whose keys are "missing_entities" and "denser_summary".

> Use chinese to response
"""
    prompt = prompt_template.format(content=content, iteration_count=iteration_count)

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message.content
    except openai.error.RateLimitError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return generate_chat_completion(prompt)

    except openai.error.ServiceUnavailableError as e:
        retry_time = 10  # Adjust the retry time as needed
        print(f"Service is unavailable. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return generate_chat_completion(prompt)

    except openai.error.APIError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"API error occurred. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return generate_chat_completion(prompt)

    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        return generate_chat_completion(prompt)


# def transform_data_and_generate_summary(input_data):
#     transformed_datas = []
#     flag = 0
#     for record in input_data:
#         transformed_data = {"items": [], "condition": "GPT4",
#                         "system": "",
#                         "history": ""}
#         messages = json.loads(record['message_list'])
#         message_contents = []  # List to accumulate message contents for the summary generation

#         for message in messages:
#             role = 'user' if message['name'] == 'human' else 'assistant'
#             content = message['text']
#             weight = 0.0 if role == 'user' else 1

#             message_contents.append(content)  # Accumulate message content

#             transformed_data["items"].append({"role": role, "content": content, "weight": weight})
#                     # Generate a summary using the accumulated message contents
#         summary = generate_summary(message_contents, iteration_count=1)
#         print(summary)
#         if summary:
#             summary_data = json.loads(summary)
#             print(summary)
#             words = re.findall(r'"(.*?)"', summary)

#             if words:
#                 summary= words[-1]
#             else:
#                 summary =  ""
#             # summary = summary_data["missing_entities_per_step"][-1]["denser_summary"] # Extract the last denser summary
#             print(summary)
#             if flag == 0:
#                 transformed_data['history'] = ""
#             else:
#                 transformed_data['history'] = summary
#             flag = 1
#             transformed_datas.append(transformed_data)

#     return transformed_datas


# def process_json_file(input_file_path, output_file_path):
#     with open(input_file_path, 'r', encoding='utf-8') as file:
#         input_data = json.load(file)

#     transformed_datas = transform_data_and_generate_summary(input_data)


#     with open(output_file_path, 'w', encoding='utf-8') as file:
#         for transformed_data in transformed_datas:
#             json_record = json.dumps(transformed_data, ensure_ascii=False)
#             file.write(json_record + '\n')

def transform_data_and_generate_summary(input_data):
    transformed_datas = []
    flag = 0
    for record in input_data:
        transformed_data = {
            "items": [],
            "condition": "GPT4",
            "system": "",
            "history": ""
        }
        # 直接访问conversations
        conversations = record['conversations']
        message_contents = []

        for conv in conversations:
            role = 'assistant' if conv['from'] == 'gpt' else 'user'
            content = conv['value']
            weight = 0.0 if role == 'user' else 0.2

            message_contents.append(content)

            transformed_data["items"].append({
                "role": role,
                "content": content,
                "weight": weight
            })

        summary = generate_summary(message_contents, iteration_count=1)
        print(summary)
        if summary:
            summary_data = json.loads(summary)
            print(summary)
            words = re.findall(r'"(.*?)"', summary)

            if words:
                summary = words[-1]
            else:
                summary = ""
            # summary = summary_data["missing_entities_per_step"][-1]["denser_summary"] # Extract the last denser summary
            print(summary)
            if flag == 0:
                transformed_data['history'] = ""
            else:
                transformed_data['history'] = summary
            flag = 1
            transformed_datas.append(transformed_data)

    return transformed_datas


def process_json_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        input_data = json.load(file)

    transformed_datas = transform_data_and_generate_summary(input_data)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for data in transformed_datas:
            json_record = json.dumps(data, ensure_ascii=False)
            file.write(json_record + '\n')


# Define your input and output file paths
input_file_path = 'merged_data.json'  # Input file path
output_file_path = 'all.json'  # Output file path

# Process the file
process_json_file(input_file_path, output_file_path)




