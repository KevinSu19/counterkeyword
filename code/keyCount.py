import re
import sys

# 关键字列表
key_list = ["auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed", "sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
            ]


# 读入文件
def read_file(file_path):
    # 读入文件在同一目录下可以直接写文件名
    with open(file_path, 'r', encoding='UTF-8') as f:
        text = f.read()
    return text


# 去除文本干扰成分（注释、字符串）
def clean_data(text):
    # 匹配所有注释
    pattern_notes = r'(//.*)|(/\*[\s\S]*?\*/)|(/\*[\s\S]*)'
    # 匹配单引号字符串
    pattern_str1 = r'(\'[\s\S]*?\')|(\'[\s\S]*)'
    # 匹配双引号字符串
    pattern_str2 = r'(\"[\s\S]*?\")|(\"[\s\S]*)'
    text = re.sub(pattern_notes, lambda x: generate_str(x.group()), text, flags=re.MULTILINE)
    text = re.sub(pattern_str1, lambda x: generate_str(x.group()), text, flags=re.MULTILINE)
    text = re.sub(pattern_str2, lambda x: generate_str(x.group()), text, flags=re.MULTILINE)
    return text


# 用与替换时生成等长空字符串
def generate_str(str):
    temp = ""
    for i in range(len(str)):
        temp += " "
    return temp


# 得出关键字数
def key_count(text):
    pattern_num = r'[a-zA-Z]{2,}'
    key_data = re.findall(pattern_num, text)
    num = 0
    for key in key_list:
        num += key_data.count(key)
    return key_data, num


# 得出switch_case结构数
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

    # 处理不带有case的switch
    num = case_num.count(0)
    for i in range(num):
        case_num.remove(0)
    switch_num -= num
    return switch_num, case_num


# 单纯只有if_else
def if_else_count(text):
    pattern_out = r'[\w](if|else)[\w]'
    pattern_key = r'(if|else)'
    # 排除变量名干扰
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


# if-else 与 if—elseif-else混合
def if_elseif_else_count(text):
    pattern_out = r'[\w](else if|if|else)[\w]'
    pattern_key = r'(else if|if|else)'
    # 排除变量名干扰
    text = re.sub(pattern_out, ' ', text, flags=re.MULTILINE)
    key_data = re.findall(pattern_key, text)

    # 统计if/else if/else前向空格
    pattern_front_space = r'\n( *)(?=if|else if|else)'
    space_data = re.findall(pattern_front_space, text)
    space_data = [len(i) for i in space_data]
    # 1代表if/ 2代表else if/ 3代表else/
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
