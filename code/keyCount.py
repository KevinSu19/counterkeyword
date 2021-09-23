import re
import sys

# Keyword List
key_list = ["auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed", "sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
            ]


# Read file
def read_file(file_path):
    # You can write the file name of the read file in the same directory
    with open(file_path, 'r', encoding='UTF-8') as f:
        text = f.read()
    return text


# Remove text interference (comments, strings)
def clean_data(text):
    # Match all comments
    pattern_notes = r'(//.*)|(/\*[\s\S]*?\*/)|(/\*[\s\S]*)'
    # Matches a single quoted string
    pattern_str1 = r'(\'[\s\S]*?\')|(\'[\s\S]*)'
    # Matches the double quoted string
    pattern_str2 = r'(\"[\s\S]*?\")|(\"[\s\S]*)'
    text = re.sub(pattern_notes, lambda x: generate_str(x.group()), text, flags=re.MULTILINE)
    text = re.sub(pattern_str1, lambda x: generate_str(x.group()), text, flags=re.MULTILINE)
    text = re.sub(pattern_str2, lambda x: generate_str(x.group()), text, flags=re.MULTILINE)
    return text


# Generates an isometric string when substituted with and
def generate_str(str):
    temp = ""
    for i in range(len(str)):
        temp += " "
    return temp


# Figure out the key word count
def key_count(text):
    pattern_num = r'[a-zA-Z]{2,}'
    key_data = re.findall(pattern_num, text)
    num = 0
    for key in key_list:
        num += key_data.count(key)
    return key_data, num


# Get the number of switch case structures
def switch_case_count(key_data):
    case_num = []
    switch_num = 0
    temp_case = 0
    for value in key_data:
        if value == "switch":
            if switch_num > 0:
                case_num.append(temp_case)
                temp_case = 0
            switch_num += 1

        if value == "case":
            temp_case += 1
    case_num.append(temp_case)

    # Handles switches without case
    num = case_num.count(0)
    for i in range(num):
        case_num.remove(0)
    switch_num -= num
    return switch_num, case_num


# only if_else
def if_else_count(text):
    pattern_out = r'[\w](if|else)[\w]'
    pattern_key = r'(if|else)'
    # Eliminate variable name interference
    text = re.sub(pattern_out, ' ', text, flags=re.MULTILINE)
    key_data = re.findall(pattern_key, text)
    # print(key_data)
    stack = []
    if_else_num = 0
    for index, values in enumerate(key_data):
        if values == 'if':
            stack.append(index)
        else:
            if len(stack) == 0:
                continue
            stack.pop()
            if_else_num += 1
    return if_else_num


# If-else mixed with if-elseif-else
def if_elseif_else_count(text):
    pattern_out = r'[\w](else if|if|else)[\w]'
    pattern_key = r'(else if|if|else)'
    # Eliminate variable name interference
    text = re.sub(pattern_out, ' ', text, flags=re.MULTILINE)
    key_data = re.findall(pattern_key, text)

    # Count if/else if/else forward Spaces
    pattern_front_space = r'\n( *)(?=if|else if|else)'
    space_data = re.findall(pattern_front_space, text)
    space_data = [len(i) for i in space_data]
    # 1 for if/ 2 for else if/ 3 for else/
    stack = []
    if_else_num = 0
    if_elseif_else_num = 0
    for index, values in enumerate(key_data):
        while len(stack) > 0:
            if space_data[index] < space_data[stack[len(stack) - 1]]:
                stack.pop()
            else:
                break
        if values == 'if':
            stack.append(index)
        elif values == 'else if':
            if len(stack) == 0:
                continue
            if key_data[stack[len(stack) - 1]] == 'if':
                stack.append(index)
        else:
            if len(stack) == 0:
                continue
            if key_data[stack[len(stack) - 1]] == 'if':
                if_else_num += 1
                stack.pop()
            else:
                while len(stack) > 0:
                    if key_data[stack[len(stack) - 1]] == 'else if':
                        stack.pop()
                    else:
                        break
                stack.pop()
                if_elseif_else_num += 1
    return if_else_num, if_elseif_else_num


def level1(filepath):
    temp_raw_text = read_file(filepath)
    temp_text = clean_data(temp_raw_text)
    temp_key, temp_num = key_count(temp_text)
    print("total num:", temp_num)
    return temp_text, temp_key, temp_num


def level2(filepath):
    temp_text, temp_key, temp_num = level1(filepath)
    temp_switch_num, temp_case_num = switch_case_count(temp_key)
    print("switch num:", temp_switch_num)
    print("case num: ", end='')
    for index, temp_value in enumerate(temp_case_num):
        if index + 1 == len(temp_case_num):
            print(temp_value)
        else:
            print(temp_value, end=' ')
    return temp_text, temp_key, temp_num


def level3(filepath):
    temp_text, temp_key, temp_num = level2(filepath)
    temp_if_else_num = if_else_count(temp_text)
    print("if-else num:", temp_if_else_num)
    return temp_text, temp_key, temp_num


def level4(filepath):
    temp_text, temp_key, temp_num = level2(filepath)
    temp_if_else_num, temp_if_elseif_else_num = if_elseif_else_count(temp_text)
    print("if-else num:", temp_if_else_num)
    print("if-elseif-else num:", temp_if_elseif_else_num)


# 选择模式
def start(filepath, level_type):
    if level_type == '1':
        level1(filepath)
    elif level_type == '2':
        level2(filepath)
    elif level_type == '3':
        level3(filepath)
    else:
        level4(filepath)


if __name__ == "__main__":
    try:
        path, level = sys.argv[1:3]
        print(path, level)
        start(filepath='../data/key.c', level_type=level)
    except Exception as e:
        print(e)
