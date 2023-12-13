import re
import numpy as np


def extract_content_between_dash_lines(log_file_path, output_file_path):
    with open(log_file_path, "r") as file:
        lines = file.readlines()

    dash_line = "--------------------------------------------------------------------------------"
    start_line_found = False
    extracting = False
    extracted_content = []
    current_section = []

    for line in lines:
        if "--- HUMAN READABLE ANSWER ---" in line:
            start_line_found = True
            continue

        if start_line_found and line.strip() == dash_line:
            if extracting:
                # End of the current section
                extracted_content.append("".join(current_section))
                current_section = []
                extracting = False
                start_line_found = False  # Reset for the next section
            else:
                extracting = True  # Start of a new section
            continue

        if extracting:
            current_section.append(line)

    rets = []
    for section in extracted_content:
        pattern = r"\d{1,3}(?:,\d{3})*|\d+"
        matches = re.findall(pattern, section)
        numbers = [int(match.replace(",", "")) for match in matches]
        rets.append(numbers)

    # Write the extracted content to a new file
    with open(output_file_path, "w") as file:
        for section in extracted_content:
            file.write(section + "\n\n")  # Separate sections by two newlines

    return rets


# Example usage
log_file_path = "log_supply_net.txt"  # Replace with your log file path
output_file_path = "extracted_content.txt"  # Replace with your desired output file path
res = extract_content_between_dash_lines(log_file_path, output_file_path)
correct_cnt = 0
for sec_res in res:
    correct_ans = 197000
    if correct_ans in sec_res:
        correct_cnt += 1
print(correct_cnt, "/", len(res))
