def replace_next_line(input_file, custom_line, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "### command below":
            lines[i+1] = custom_line + '\n'
            break

    with open(output_file, 'w') as f:
        f.writelines(lines)

