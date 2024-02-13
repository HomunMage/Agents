import os
import re

def process_file(file_path):
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace {% raw %} and {% endraw %}
    new_content = re.sub('<div style="display: none;">', '<div>', content)

    # Check if replacements were made
    if new_content != content:
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        # Print the path of the modified file
        print(file_path)

def find_and_replace_in_md(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                process_file(full_path)

# Replace 'start_directory_path' with the path of the directory you want to start the search from
start_directory_path = './'
find_and_replace_in_md(start_directory_path)