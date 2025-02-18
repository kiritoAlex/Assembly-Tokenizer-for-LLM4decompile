import json

def clean_jsonl_file(input_file, output_file):
    """
    检查 JSONL 文件中的每一行是否符合 JSON 格式，删除不符合的行。
    :param input_file: 输入的 JSONL 文件路径
    :param output_file: 输出的清理后的 txt 文件路径
    """

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line_number, line in enumerate(infile, start=1):
            line = line.strip()  # 去除两端的空白符
            if not line:  # 跳过空行
                continue
            try:
                json.loads(line)  # 尝试解析 JSON
                data = json.loads(line.strip()) #解析成功，提取汇编指令写入txt文本
                asm = data.get('output')
                o0 = asm.get('opt-state-O0')
                o1 = asm.get('opt-state-O1')
                o2 = asm.get('opt-state-O2')
                o3 = asm.get('opt-state-O3')
                outfile.write(o0 + '\n')
                outfile.write(o1 + '\n')
                outfile.write(o2 + '\n')
                outfile.write(o3 + '\n')
            except json.JSONDecodeError:
                print("error")

if __name__ == "__main__":

    input_path = "../assembly_instruction.jsonl"
    output_path = '../assembly_instruction.txt'
    
    clean_jsonl_file(input_path, output_path)
